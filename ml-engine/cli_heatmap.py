import sys
import json
import argparse
from pathlib import Path

# Add ml-engine to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "ml-engine"))

from predictor import generate_heatmap_probabilities

BASE_GRID = [
    {
        'location_id': 'SKM_01', 'station_name': 'Gangtok NH-10 (9th Mile)', 'state': 'Sikkim',
        'latitude': 27.3314, 'longitude': 88.6138, 'rainfall_mm': 180.0, 'river_water_level': 24.0,
        'soil_moisture_percent': 88.0, 'slope_angle_degrees': 42.0, 'wind_speed_kmh': 35.0,
        'vegetation_density_ndvi': 0.20, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'SKM_02', 'station_name': 'Mangan Dikchu Sector', 'state': 'Sikkim',
        'latitude': 27.5082, 'longitude': 88.5327, 'rainfall_mm': 145.0, 'river_water_level': 20.0,
        'soil_moisture_percent': 82.0, 'slope_angle_degrees': 44.0, 'wind_speed_kmh': 28.0,
        'vegetation_density_ndvi': 0.25, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'metamorphic'
    },
    {
        'location_id': 'ASM_01', 'station_name': 'Haflong Jatinga Valley', 'state': 'Assam',
        'latitude': 25.1833, 'longitude': 93.0167, 'rainfall_mm': 160.0, 'river_water_level': 22.0,
        'soil_moisture_percent': 85.0, 'slope_angle_degrees': 36.0, 'wind_speed_kmh': 24.0,
        'vegetation_density_ndvi': 0.35, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'ASM_02', 'station_name': 'Guwahati Khanapara Foothills', 'state': 'Assam',
        'latitude': 26.1158, 'longitude': 91.8150, 'rainfall_mm': 12.0, 'river_water_level': 4.5,
        'soil_moisture_percent': 35.0, 'slope_angle_degrees': 18.0, 'wind_speed_kmh': 10.0,
        'vegetation_density_ndvi': 0.70, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'igneous'
    },
    {
        'location_id': 'MEG_01', 'station_name': 'Cherrapunji Sohra Escarpment', 'state': 'Meghalaya',
        'latitude': 25.2702, 'longitude': 91.7323, 'rainfall_mm': 210.0, 'river_water_level': 28.0,
        'soil_moisture_percent': 94.0, 'slope_angle_degrees': 45.0, 'wind_speed_kmh': 42.0,
        'vegetation_density_ndvi': 0.22, 'soil_type': 'silt', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MEG_02', 'station_name': 'Shillong Umiam Bypass', 'state': 'Meghalaya',
        'latitude': 25.6580, 'longitude': 91.9050, 'rainfall_mm': 65.0, 'river_water_level': 10.0,
        'soil_moisture_percent': 60.0, 'slope_angle_degrees': 28.0, 'wind_speed_kmh': 18.0,
        'vegetation_density_ndvi': 0.60, 'soil_type': 'clay', 'soil_texture': 'medium', 'lithology': 'metamorphic'
    },
    {
        'location_id': 'ARN_01', 'station_name': 'Tawang Sela Passway', 'state': 'Arunachal Pradesh',
        'latitude': 27.5861, 'longitude': 91.8653, 'rainfall_mm': 95.0, 'river_water_level': 14.0,
        'soil_moisture_percent': 70.0, 'slope_angle_degrees': 41.0, 'wind_speed_kmh': 30.0,
        'vegetation_density_ndvi': 0.30, 'soil_type': 'gravel', 'soil_texture': 'coarse', 'lithology': 'igneous'
    },
    {
        'location_id': 'ARN_02', 'station_name': 'Itanagar Banderdewa Pass', 'state': 'Arunachal Pradesh',
        'latitude': 27.0844, 'longitude': 93.6053, 'rainfall_mm': 40.0, 'river_water_level': 8.0,
        'soil_moisture_percent': 50.0, 'slope_angle_degrees': 22.0, 'wind_speed_kmh': 14.0,
        'vegetation_density_ndvi': 0.65, 'soil_type': 'sand', 'soil_texture': 'coarse', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'NAG_01', 'station_name': 'Kohima Dzüdza River (NH-29)', 'state': 'Nagaland',
        'latitude': 25.6751, 'longitude': 94.1086, 'rainfall_mm': 175.0, 'river_water_level': 25.0,
        'soil_moisture_percent': 89.0, 'slope_angle_degrees': 39.0, 'wind_speed_kmh': 32.0,
        'vegetation_density_ndvi': 0.28, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MAN_01', 'station_name': 'Noney Tupul Yard (NH-37)', 'state': 'Manipur',
        'latitude': 24.8217, 'longitude': 93.6389, 'rainfall_mm': 190.0, 'river_water_level': 26.0,
        'soil_moisture_percent': 91.0, 'slope_angle_degrees': 43.0, 'wind_speed_kmh': 36.0,
        'vegetation_density_ndvi': 0.18, 'soil_type': 'clay', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'MIZ_01', 'station_name': 'Aizawl Hunthar Sinking Zone', 'state': 'Mizoram',
        'latitude': 23.7307, 'longitude': 92.7173, 'rainfall_mm': 130.0, 'river_water_level': 18.0,
        'soil_moisture_percent': 78.0, 'slope_angle_degrees': 38.0, 'wind_speed_kmh': 26.0,
        'vegetation_density_ndvi': 0.40, 'soil_type': 'silt', 'soil_texture': 'fine', 'lithology': 'sedimentary'
    },
    {
        'location_id': 'TRP_01', 'station_name': 'Jampui Hills Vanghmun Ridge', 'state': 'Tripura',
        'latitude': 23.9500, 'longitude': 92.2833, 'rainfall_mm': 25.0, 'river_water_level': 6.0,
        'soil_moisture_percent': 42.0, 'slope_angle_degrees': 18.0, 'wind_speed_kmh': 12.0,
        'vegetation_density_ndvi': 0.72, 'soil_type': 'loam', 'soil_texture': 'medium', 'lithology': 'sedimentary'
    }
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rainfall', type=float, default=None, help='Simulated rainfall surge intensity in mm/h')
    parser.add_argument('--boost_hotspots', action='store_true', help='Boost critical stations during cloudburst')
    args = parser.parse_args()

    grid = []
    for pt in BASE_GRID:
        item = pt.copy()
        if args.rainfall is not None:
            # Scale rainfall across all stations based on the simulator slider
            factor = args.rainfall / 50.0  # 50 mm/h is baseline
            item['rainfall_mm'] = round(pt['rainfall_mm'] * factor, 1)
            item['soil_moisture_percent'] = min(99.0, round(pt['soil_moisture_percent'] * (0.6 + factor * 0.4), 1))
            item['river_water_level'] = round(pt['river_water_level'] * (0.7 + factor * 0.3), 1)

        grid.append(item)

    res = generate_heatmap_probabilities(grid)
    print(json.dumps(res))

if __name__ == '__main__':
    main()
