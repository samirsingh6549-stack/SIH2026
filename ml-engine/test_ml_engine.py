import unittest
import time
from pathlib import Path
from data_cleaner import validate_weather_input, clean_and_prepare
from physics_engine import evaluate_caine_threshold, calculate_factor_of_safety, extract_contributing_risk_factors
from predictor import predict_disaster_risk, predict_detailed_risk, predict_batch, generate_heatmap_probabilities

class TestMLEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid_high_risk = {
            'rainfall_mm': 180.0,
            'river_water_level': 24.0,
            'soil_moisture_percent': 85.0,
            'slope_angle_degrees': 42.0,
            'wind_speed_kmh': 35.5,
            'vegetation_density_ndvi': 0.2,
            'soil_type': 'clay',
            'soil_texture': 'fine',
            'lithology': 'sedimentary'
        }

        cls.valid_low_risk = {
            'rainfall_mm': 6.0,
            'river_water_level': 4.5,
            'soil_moisture_percent': 30.0,
            'slope_angle_degrees': 12.0,
            'wind_speed_kmh': 10.0,
            'vegetation_density_ndvi': 0.82,
            'soil_type': 'loam',
            'soil_texture': 'medium',
            'lithology': 'igneous'
        }

    def test_01_validation_success(self):
        is_valid, msg = validate_weather_input(self.valid_high_risk)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Valid")

    def test_02_validation_missing_key(self):
        broken = self.valid_high_risk.copy()
        del broken['rainfall_mm']
        is_valid, msg = validate_weather_input(broken)
        self.assertFalse(is_valid)
        self.assertIn("Missing required parameter: 'rainfall_mm'", msg)

    def test_03_validation_invalid_categorical(self):
        broken = self.valid_high_risk.copy()
        broken['lithology'] = 'unknown_rock_type'
        is_valid, msg = validate_weather_input(broken)
        self.assertFalse(is_valid)
        self.assertIn("Invalid lithology", msg)

    def test_04_validation_range_bounds(self):
        broken = self.valid_high_risk.copy()
        broken['soil_moisture_percent'] = 145.0  # Impossible percentage
        is_valid, msg = validate_weather_input(broken)
        self.assertFalse(is_valid)
        self.assertIn("Must be between 0 and 100", msg)

    def test_05_caine_threshold_physics(self):
        # 180mm over 24h = 7.5 mm/h. Caine threshold for 24h = 14.82 * (24^-0.39) ~= 4.29 mm/h.
        caine = evaluate_caine_threshold(rainfall_intensity_mmh=7.5, duration_hours=24.0)
        self.assertTrue(caine['breached'])
        self.assertGreater(caine['intensity_ratio'], 1.0)

    def test_06_factor_of_safety_physics(self):
        # 42 degree slope with high pore water pressure should result in unstable slope (FoS < 1.0)
        fos_result = calculate_factor_of_safety(slope_angle_deg=42.0, pore_pressure_kpa=12.0, soil_type='clay')
        self.assertLess(fos_result['factor_of_safety'], 1.05)
        self.assertEqual(fos_result['stability_status'], 'UNSTABLE')

    def test_07_predict_disaster_risk_high(self):
        result = predict_disaster_risk(self.valid_high_risk)
        self.assertEqual(result, "High Risk: Landslide/Flood conditions detected.")

    def test_08_predict_disaster_risk_low(self):
        result = predict_disaster_risk(self.valid_low_risk)
        self.assertEqual(result, "Low Risk: Normal conditions.")

    def test_09_predict_detailed_risk_structure(self):
        detailed = predict_detailed_risk(self.valid_high_risk)
        self.assertEqual(detailed['status'], 'success')
        self.assertIn('lsi_score', detailed)
        self.assertIn('risk_level', detailed)
        self.assertIn('physics_validation', detailed)
        self.assertIn('contributing_factors', detailed)
        self.assertGreaterEqual(detailed['lsi_score'], 0.70)
        self.assertIn(detailed['risk_level'], ['HIGH', 'SEVERE'])

    def test_10_inference_latency_benchmark(self):
        start = time.perf_counter()
        iterations = 50
        for _ in range(iterations):
            _ = predict_detailed_risk(self.valid_high_risk)
        elapsed_ms = ((time.perf_counter() - start) / iterations) * 1000
        print(f"\n[BENCHMARK] Average inference latency: {elapsed_ms:.2f} ms per request.")
        self.assertLess(elapsed_ms, 50.0)  # Sub-50ms SLA for real-time edge early warning

    def test_11_predict_batch_throughput(self):
        # Generate 100 diverse terrain grid cells
        batch = []
        for i in range(100):
            pt = self.valid_high_risk.copy() if i % 2 == 0 else self.valid_low_risk.copy()
            pt['location_id'] = f"grid_cell_{i:04d}"
            pt['latitude'] = 27.0 + (i * 0.01)
            pt['longitude'] = 88.5 + (i * 0.01)
            batch.append(pt)

        start_time = time.perf_counter()
        batch_result = predict_batch(batch)
        elapsed_total_ms = (time.perf_counter() - start_time) * 1000

        self.assertEqual(batch_result['status'], 'success')
        self.assertEqual(batch_result['total_processed'], 100)
        self.assertEqual(len(batch_result['predictions']), 100)
        print(f"\n[BATCH BENCHMARK] 100 grid cells processed in {elapsed_total_ms:.2f} ms ({elapsed_total_ms / 100:.3f} ms/point).")
        # 100 points must process in under 250ms via vectorized matrix operations (avg < 2.5ms/point)
        self.assertLess(elapsed_total_ms, 250.0)

    def test_12_generate_heatmap_probabilities(self):
        grid = [
            {**self.valid_high_risk, 'lat': 27.33, 'lon': 88.61, 'station_name': 'Gangtok NH-10'},
            {**self.valid_low_risk, 'lat': 26.14, 'lon': 91.73, 'station_name': 'Guwahati Valley'},
            {**self.valid_high_risk, 'lat': 25.57, 'lon': 91.89, 'station_name': 'Cherrapunji Ridge'}
        ]

        heatmap_res = generate_heatmap_probabilities(grid)
        self.assertEqual(heatmap_res['status'], 'success')
        self.assertEqual(heatmap_res['grid_cell_count'], 3)
        self.assertIn('leaflet_heat_points', heatmap_res)
        self.assertEqual(len(heatmap_res['leaflet_heat_points']), 3)

        # Check Leaflet [lat, lon, intensity] format
        for pt in heatmap_res['leaflet_heat_points']:
            self.assertEqual(len(pt), 3)
            self.assertTrue(20.0 <= pt[0] <= 30.0)
            self.assertTrue(85.0 <= pt[1] <= 98.0)
            self.assertTrue(0.0 <= pt[2] <= 1.0)

        # Verify GeoJSON FeatureCollection
        fc = heatmap_res['geojson_feature_collection']
        self.assertEqual(fc['type'], 'FeatureCollection')
        self.assertEqual(len(fc['features']), 3)
        self.assertIn(fc['features'][0]['properties']['color'], ['#ef4444', '#f97316', '#eab308', '#22c55e'])

if __name__ == '__main__':
    unittest.main()
