import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Dict, Any

# Ensure parent directory is in Python path so ml-engine can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
ML_ENGINE_DIR = PROJECT_ROOT / "ml-engine"
if str(ML_ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ML_ENGINE_DIR))

from ner_stations import NER_STATIONS, get_stations_by_state, get_station_by_id
from open_meteo_client import fetch_live_weather
from geotech_sensors import GeotechSensorSimulator
from gsi_inventory import find_nearest_historical_landslide

try:
    from predictor import predict_detailed_risk, generate_heatmap_probabilities
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

def ingest_station_telemetry(station: Dict[str, Any], live_network: bool = True) -> Dict[str, Any]:
    """
    Ingests live meteorological feeds, geotechnical sensor arrays,
    and historical hazard records for a single monitoring station.
    """
    lat = station["latitude"]
    lon = station["longitude"]

    # 1. Fetch live Open-Meteo weather
    weather = fetch_live_weather(lat, lon, timeout_seconds=4)

    rainfall_24h = weather["rainfall_24h_mm"]
    antecedent_72h = weather["antecedent_rainfall_72h_mm"]
    soil_moisture = weather["soil_moisture_percent"]

    # 2. Geotechnical IoT telemetry
    geotech = GeotechSensorSimulator.read_telemetry(
        station=station,
        rainfall_24h_mm=rainfall_24h,
        antecedent_72h_mm=antecedent_72h,
        soil_moisture_pct=soil_moisture
    )

    # 3. GSI Bhukosh historical context
    nearby_hist = find_nearest_historical_landslide(lat, lon)

    # 4. Map to Module 1 ML feature vector
    river_water_level = round(3.5 + (rainfall_24h / 25.0), 2)
    ml_input_payload = {
        'rainfall_mm': rainfall_24h,
        'river_water_level': river_water_level,
        'soil_moisture_percent': soil_moisture,
        'slope_angle_degrees': station["slope_angle_degrees"],
        'wind_speed_kmh': weather["wind_speed_kmh"],
        'vegetation_density_ndvi': station["vegetation_density_ndvi"],
        'antecedent_rainfall_72h_mm': antecedent_72h,
        'pore_water_pressure_kpa': geotech["piezometer"]["pore_water_pressure_kpa"],
        'elevation_m': station["elevation_m"],
        'soil_type': station["soil_type"],
        'soil_texture': station["soil_texture"],
        'lithology': station["lithology"]
    }

    # 5. Evaluate risk via Module 1 (AI/ML Engine)
    risk_assessment = {}
    if ML_AVAILABLE:
        risk_assessment = predict_detailed_risk(ml_input_payload)

    return {
        "station_id": station["station_id"],
        "station_name": station["station_name"],
        "state": station["state"],
        "district": station["district"],
        "coordinates": {
            "latitude": lat,
            "longitude": lon,
            "elevation_m": station["elevation_m"]
        },
        "lifeline_corridor": station.get("lifeline_corridor"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "meteorological_telemetry": weather,
        "geotechnical_sensors": geotech,
        "historical_hazard_proximity": nearby_hist,
        "ml_risk_assessment": risk_assessment
    }

def run_regional_ingestion_pipeline(state_filter: str = None) -> Dict[str, Any]:
    """
    Executes the ingestion pipeline across all 8 NER states or a selected state.
    """
    stations_to_process = (
        get_stations_by_state(state_filter) if state_filter
        else NER_STATIONS
    )

    records = []
    grid_for_ml = []

    for station in stations_to_process:
        telemetry = ingest_station_telemetry(station)
        records.append(telemetry)

        # Prepare grid entry for vectorized GIS heatmap
        rf = telemetry["meteorological_telemetry"]["rainfall_24h_mm"]
        sm = telemetry["meteorological_telemetry"]["soil_moisture_percent"]
        grid_for_ml.append({
            'location_id': station["station_id"],
            'station_name': station["station_name"],
            'latitude': station["latitude"],
            'longitude': station["longitude"],
            'state': station["state"],
            'rainfall_mm': rf,
            'river_water_level': 3.5 + (rf / 25.0),
            'soil_moisture_percent': sm,
            'slope_angle_degrees': station["slope_angle_degrees"],
            'wind_speed_kmh': telemetry["meteorological_telemetry"]["wind_speed_kmh"],
            'vegetation_density_ndvi': station["vegetation_density_ndvi"],
            'antecedent_rainfall_72h_mm': telemetry["meteorological_telemetry"]["antecedent_rainfall_72h_mm"],
            'pore_water_pressure_kpa': telemetry["geotechnical_sensors"]["piezometer"]["pore_water_pressure_kpa"],
            'elevation_m': station["elevation_m"],
            'soil_type': station["soil_type"],
            'soil_texture': station["soil_texture"],
            'lithology': station["lithology"]
        })

    # High-throughput batch heatmap scoring from Module 1
    heatmap_data = {}
    if ML_AVAILABLE and grid_for_ml:
        heatmap_data = generate_heatmap_probabilities(grid_for_ml)

    return {
        "pipeline": "NER_Realtime_Sensor_Ingestion_Engine",
        "processed_at": datetime.now(timezone.utc).isoformat(),
        "total_stations_monitored": len(records),
        "target_region": state_filter or "North Eastern Region (All 8 States)",
        "stations": records,
        "regional_heatmap_layer": heatmap_data
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NER Real-Time Ingestion Engine")
    parser.add_argument("--state", type=str, default=None, help="Filter by NER state (e.g. Sikkim, Assam)")
    parser.add_argument("--export", type=str, default=None, help="Filepath to export JSON telemetry snapshot")
    args = parser.parse_args()

    print("=" * 65)
    print("  SIH 2026: METEOROLOGICAL & GEOTECHNICAL SENSOR INGESTION")
    print(f"  Target: {args.state or 'All 8 North Eastern Region (NER) States'}")
    print("=" * 65)

    results = run_regional_ingestion_pipeline(state_filter=args.state)

    print(f"\nSuccessfully ingested {results['total_stations_monitored']} regional stations.")
    print("\nSample Ingested Stations:")
    for st in results["stations"][:3]:
        rf = st["meteorological_telemetry"]["rainfall_24h_mm"]
        u = st["geotechnical_sensors"]["piezometer"]["pore_water_pressure_kpa"]
        tilt = st["geotechnical_sensors"]["tiltmeter"]["vector_displacement_deg"]
        lsi = st.get("ml_risk_assessment", {}).get("lsi_score", "N/A")
        tier = st.get("ml_risk_assessment", {}).get("risk_level", "N/A")
        print(f"  • {st['station_name']} ({st['state']}): Rain={rf}mm, PorePressure={u}kPa, Tilt={tilt}°, LSI={lsi} [{tier}]")

    if args.export:
        with open(args.export, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"\nTelemetry snapshot exported to {args.export}")
    print("\n>>> Ingestion cycle completed successfully!\n")
