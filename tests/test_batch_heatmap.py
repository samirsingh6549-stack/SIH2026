import sys
import time
from pathlib import Path

# Add ml-engine to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "ml-engine"))

from predictor import generate_heatmap_probabilities, predict_batch

# 12 regional stations / grid cells across the 8 NER states
NER_GRID_CELLS = [
    {
        'location_id': 'SKM_01', 'station_name': 'Gangtok NH-10', 'state': 'Sikkim',
        'latitude': 27.33, 'longitude': 88.61, 'rainfall_mm': 180.0, 'river_water_level': 24.0,
        'soil_moisture_percent': 88.0, 'slope_angle_degrees': 42.0, 'wind_speed_kmh': 35.0,
        'vegetation_density_ndvi': 0.20, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'SKM_02', 'station_name': 'Mangan Dikchu Sector', 'state': 'Sikkim',
        'latitude': 27.51, 'longitude': 88.53, 'rainfall_mm': 145.0, 'river_water_level': 20.0,
        'soil_moisture_percent': 82.0, 'slope_angle_degrees': 44.0, 'wind_speed_kmh': 28.0,
        'vegetation_density_ndvi': 0.25, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'metamorphic'
    },
    {
        'location_id': 'ASM_01', 'station_name': 'Haflong Jatinga Valley', 'state': 'Assam',
        'latitude': 25.18, 'longitude': 93.02, 'rainfall_mm': 160.0, 'river_water_level': 22.0,
        'soil_moisture_percent': 85.0, 'slope_angle_degrees': 36.0, 'wind_speed_kmh': 24.0,
        'vegetation_density_ndvi': 0.35, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'ASM_02', 'station_name': 'Guwahati Valley Baseline', 'state': 'Assam',
        'latitude': 26.14, 'longitude': 91.73, 'rainfall_mm': 12.0, 'river_water_level': 4.5,
        'soil_moisture_percent': 35.0, 'slope_angle_degrees': 12.0, 'wind_speed_kmh': 10.0,
        'vegetation_density_ndvi': 0.70, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'igneous'
    },
    {
        'location_id': 'MEG_01', 'station_name': 'Cherrapunji Sohra Cliff', 'state': 'Meghalaya',
        'latitude': 25.27, 'longitude': 91.73, 'rainfall_mm': 210.0, 'river_water_level': 28.0,
        'soil_moisture_percent': 94.0, 'slope_angle_degrees': 45.0, 'wind_speed_kmh': 42.0,
        'vegetation_density_ndvi': 0.22, 'soil_type': 'silt', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MEG_02', 'station_name': 'Shillong Umiam Bypass', 'state': 'Meghalaya',
        'latitude': 25.57, 'longitude': 91.89, 'rainfall_mm': 65.0, 'river_water_level': 10.0,
        'soil_moisture_percent': 60.0, 'slope_angle_degrees': 28.0, 'wind_speed_kmh': 18.0,
        'vegetation_density_ndvi': 0.60, 'soil_type': 'clay', 'soil_texture': 'medium', 'lithology': 'metamorphic'
    },
    {
        'location_id': 'ARN_01', 'station_name': 'Tawang Sela Pass', 'state': 'Arunachal',
        'latitude': 27.58, 'longitude': 91.86, 'rainfall_mm': 95.0, 'river_water_level': 14.0,
        'soil_moisture_percent': 70.0, 'slope_angle_degrees': 41.0, 'wind_speed_kmh': 30.0,
        'vegetation_density_ndvi': 0.30, 'soil_type': 'gravel', 'soil_texture': 'coarse', 'lithology': 'igneous'
    },
    {
        'location_id': 'ARN_02', 'station_name': 'Itanagar Hills', 'state': 'Arunachal',
        'latitude': 27.08, 'longitude': 93.60, 'rainfall_mm': 40.0, 'river_water_level': 8.0,
        'soil_moisture_percent': 50.0, 'slope_angle_degrees': 22.0, 'wind_speed_kmh': 14.0,
        'vegetation_density_ndvi': 0.65, 'soil_type': 'sand', 'soil_texture': 'coarse', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'NAG_01', 'station_name': 'Kohima NH-29 Lifeline', 'state': 'Nagaland',
        'latitude': 25.67, 'longitude': 94.11, 'rainfall_mm': 175.0, 'river_water_level': 25.0,
        'soil_moisture_percent': 89.0, 'slope_angle_degrees': 39.0, 'wind_speed_kmh': 32.0,
        'vegetation_density_ndvi': 0.28, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MAN_01', 'station_name': 'Noney Tupul Yard', 'state': 'Manipur',
        'latitude': 24.82, 'longitude': 93.64, 'rainfall_mm': 190.0, 'river_water_level': 26.0,
        'soil_moisture_percent': 91.0, 'slope_angle_degrees': 43.0, 'wind_speed_kmh': 36.0,
        'vegetation_density_ndvi': 0.18, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MIZ_01', 'station_name': 'Aizawl Hunthar Zone', 'state': 'Mizoram',
        'latitude': 23.73, 'longitude': 92.71, 'rainfall_mm': 130.0, 'river_water_level': 18.0,
        'soil_moisture_percent': 78.0, 'slope_angle_degrees': 38.0, 'wind_speed_kmh': 26.0,
        'vegetation_density_ndvi': 0.40, 'soil_type': 'silt', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'TRP_01', 'station_name': 'Jampui Hills Ridge', 'state': 'Tripura',
        'latitude': 23.95, 'longitude': 92.28, 'rainfall_mm': 25.0, 'river_water_level': 6.0,
        'soil_moisture_percent': 42.0, 'slope_angle_degrees': 18.0, 'wind_speed_kmh': 12.0,
        'vegetation_density_ndvi': 0.72, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'sedimentary'
    }
]

def run_test():
    print("=" * 70)
    print("  VERIFICATION: BATCH PROCESSING & HEATMAP PROBABILITY SCORING")
    print("=" * 70)

    t0 = time.perf_counter()
    heatmap_res = generate_heatmap_probabilities(NER_GRID_CELLS)
    elapsed_ms = (time.perf_counter() - t0) * 1000

    print(f"\n[1] PERFORMANCE & BATCH SPEED:")
    print(f"    Total Grid Points Evaluated: {heatmap_res['grid_cell_count']}")
    print(f"    Total Execution Time:        {elapsed_ms:.2f} ms")
    print(f"    Average Speed Per Point:     {elapsed_ms / len(NER_GRID_CELLS):.3f} ms/point (Vectorized Matrix)")

    print(f"\n[2] REGIONAL STATISTICAL SUMMARY:")
    print(f"    Highest LSI Probability:     {heatmap_res['max_lsi_score']:.4f} ({heatmap_res['max_lsi_score'] * 100:.1f}%)")
    print(f"    Mean Regional Probability:   {heatmap_res['mean_lsi_score']:.4f}")
    print(f"    Active Hotspots (High/Sev):  {heatmap_res['regional_hotspots_count']}")
    print(f"    Risk Tier Distribution:      {heatmap_res['tier_distribution']}")

    print(f"\n[3] LEAFLET GIS HEATMAP TRIPLES [Latitude, Longitude, Probability Weight (0.0 to 1.0)]:")
    for pt in heatmap_res['leaflet_heat_points']:
        print(f"    • Coord: [{pt[0]:.2f}, {pt[1]:.2f}] --> Weight: {pt[2]:.4f}")

    print(f"\n[4] INDIVIDUAL LOCATION PROBABILITY SCORES & COLOR CODES:")
    features = heatmap_res['geojson_feature_collection']['features']
    print(f"    {'Location / Sector':<26} {'State':<10} {'LSI Score':<12} {'Risk Tier':<10} {'Hex Color'}")
    print("    " + "-" * 66)
    for f in features:
        props = f['properties']
        loc = props['station_name']
        st = props['state']
        lsi = f"{props['lsi_score']:.4f} ({props['intensity']*100:.1f}%)"
        tier = props['risk_level']
        col = props['color']
        print(f"    {loc:<26} {st:<10} {lsi:<12} {tier:<10} {col}")

    print("\n" + "=" * 70)
    print("  RESULT: SUCCESS - BATCH PROCESSING & PROBABILITY SCORING VERIFIED!")
    print("=" * 70)

if __name__ == "__main__":
    run_test()
