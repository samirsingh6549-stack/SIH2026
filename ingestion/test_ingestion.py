import unittest
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
ML_ENGINE_DIR = PROJECT_ROOT / "ml-engine"
if str(ML_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ML_ENGINE_DIR))

from ner_stations import NER_STATIONS, get_stations_by_state, get_station_by_id
from open_meteo_client import fetch_live_weather, _generate_offline_fallback
from geotech_sensors import GeotechSensorSimulator
from gsi_inventory import get_all_historical_landslides, find_nearest_historical_landslide
from pipeline import ingest_station_telemetry, run_regional_ingestion_pipeline

class TestIngestionEngine(unittest.TestCase):

    def test_01_all_ner_states_covered(self):
        expected_states = {
            "Sikkim", "Assam", "Meghalaya", "Arunachal Pradesh",
            "Nagaland", "Manipur", "Mizoram", "Tripura"
        }
        present_states = {s["state"] for s in NER_STATIONS}
        self.assertEqual(expected_states, present_states)
        self.assertGreaterEqual(len(NER_STATIONS), 12)

    def test_02_station_metadata_integrity(self):
        for st in NER_STATIONS:
            self.assertIn("station_id", st)
            self.assertIn("latitude", st)
            self.assertIn("longitude", st)
            self.assertIn("slope_angle_degrees", st)
            self.assertIn("soil_type", st)
            self.assertTrue(20.0 <= st["latitude"] <= 30.0)
            self.assertTrue(85.0 <= st["longitude"] <= 98.0)

    def test_03_weather_fetching_or_fallback(self):
        gangtok = get_station_by_id("SKM_GNT_01")
        weather = fetch_live_weather(gangtok["latitude"], gangtok["longitude"], timeout_seconds=4)
        self.assertIn("rainfall_24h_mm", weather)
        self.assertIn("antecedent_rainfall_72h_mm", weather)
        self.assertIn("soil_moisture_percent", weather)
        self.assertGreaterEqual(weather["rainfall_24h_mm"], 0.0)
        self.assertGreaterEqual(weather["antecedent_rainfall_72h_mm"], 0.0)

    def test_04_offline_resilience_fallback(self):
        fallback = _generate_offline_fallback(27.33, 88.61, "Forced offline simulation")
        self.assertEqual(fallback["status"], "offline_cached_fallback")
        self.assertGreater(fallback["rainfall_24h_mm"], 0.0)
        self.assertGreater(fallback["soil_moisture_percent"], 0.0)

    def test_05_geotech_sensor_simulation(self):
        haflong = get_station_by_id("ASM_HFL_01")
        # Simulate heavy monsoon conditions
        sensor_data = GeotechSensorSimulator.read_telemetry(
            station=haflong,
            rainfall_24h_mm=120.0,
            antecedent_72h_mm=260.0,
            soil_moisture_pct=88.0
        )
        self.assertIn("piezometer", sensor_data)
        self.assertIn("tiltmeter", sensor_data)
        self.assertIn("extensometer", sensor_data)
        self.assertGreater(sensor_data["piezometer"]["pore_water_pressure_kpa"], 8.0)
        self.assertGreater(sensor_data["tiltmeter"]["vector_displacement_deg"], 0.1)

    def test_06_gsi_bhukosh_records(self):
        records = get_all_historical_landslides()
        self.assertGreaterEqual(len(records), 8)
        nearest = find_nearest_historical_landslide(lat=24.82, lon=93.63)
        self.assertIsNotNone(nearest["nearest_event"])
        self.assertLess(nearest["distance_km"], 20.0)  # Near Tupul/Noney

    def test_07_end_to_end_single_station_ingestion(self):
        gangtok = get_station_by_id("SKM_GNT_01")
        telemetry = ingest_station_telemetry(gangtok)

        self.assertEqual(telemetry["station_id"], "SKM_GNT_01")
        self.assertIn("meteorological_telemetry", telemetry)
        self.assertIn("geotechnical_sensors", telemetry)
        self.assertIn("ml_risk_assessment", telemetry)

        # Check Module 1 ML scoring is attached
        ml_eval = telemetry["ml_risk_assessment"]
        if ml_eval:
            self.assertIn("lsi_score", ml_eval)
            self.assertIn("risk_level", ml_eval)
            self.assertIn(ml_eval["risk_level"], ["LOW", "MODERATE", "HIGH", "SEVERE"])

    def test_08_regional_pipeline_with_heatmap(self):
        regional_output = run_regional_ingestion_pipeline(state_filter="Sikkim")
        self.assertEqual(regional_output["total_stations_monitored"], 2)
        self.assertIn("regional_heatmap_layer", regional_output)

        hm = regional_output["regional_heatmap_layer"]
        if hm and hm.get("status") == "success":
            self.assertIn("leaflet_heat_points", hm)
            self.assertEqual(len(hm["leaflet_heat_points"]), 2)

if __name__ == '__main__':
    unittest.main()
