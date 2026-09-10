import pandas as pd
from typing import Dict, Any, Tuple

SOIL_TYPE_MAP = {
    'sand': 1,
    'loam': 2,
    'clay': 3,
    'silt': 4,
    'gravel': 5
}

SOIL_TEXTURE_MAP = {
    'coarse': 1,
    'medium': 2,
    'fine': 3
}

LITHOLOGY_MAP = {
    'igneous': 1,
    'metamorphic': 2,
    'sedimentary': 3,
    'unconsolidated': 4
}

FEATURE_COLUMNS = [
    'rainfall_mm',
    'river_water_level',
    'soil_moisture_percent',
    'slope_angle_degrees',
    'wind_speed_kmh',
    'vegetation_density_ndvi',
    'antecedent_rainfall_72h_mm',
    'pore_water_pressure_kpa',
    'elevation_m',
    'soil_type_idx',
    'soil_texture_idx',
    'lithology_idx'
]

def validate_weather_input(raw_data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validates the structure and content of raw input data.
    Ensures all required numerical and categorical fields are provided with acceptable ranges.
    """
    if not isinstance(raw_data, dict):
        return False, "Input payload must be a JSON object / dictionary."

    required_numeric = [
        'rainfall_mm',
        'river_water_level',
        'soil_moisture_percent',
        'slope_angle_degrees',
        'wind_speed_kmh',
        'vegetation_density_ndvi'
    ]
    required_categorical = ['soil_type', 'soil_texture', 'lithology']

    # Validate numerical fields
    for key in required_numeric:
        if key not in raw_data:
            return False, f"Missing required parameter: '{key}'"
        try:
            val = float(raw_data[key])
            if key == 'soil_moisture_percent' and not (0.0 <= val <= 100.0):
                return False, f"Invalid 'soil_moisture_percent': {val}. Must be between 0 and 100."
            if key == 'slope_angle_degrees' and not (0.0 <= val <= 90.0):
                return False, f"Invalid 'slope_angle_degrees': {val}. Must be between 0 and 90."
            if key == 'vegetation_density_ndvi' and not (-1.0 <= val <= 1.0):
                return False, f"Invalid 'vegetation_density_ndvi': {val}. Must be between -1.0 and 1.0."
            if key in ['rainfall_mm', 'river_water_level', 'wind_speed_kmh'] and val < 0.0:
                return False, f"Parameter '{key}' cannot be negative."
        except (ValueError, TypeError):
            return False, f"Invalid value: '{key}' must be a valid numerical value."

    # Validate categorical fields
    for key in required_categorical:
        if key not in raw_data:
            return False, f"Missing required parameter: '{key}'"

    soil_type = str(raw_data['soil_type']).strip().lower()
    if soil_type not in SOIL_TYPE_MAP:
        return False, f"Invalid soil_type '{raw_data['soil_type']}'. Expected one of: {list(SOIL_TYPE_MAP.keys())}"

    soil_texture = str(raw_data['soil_texture']).strip().lower()
    if soil_texture not in SOIL_TEXTURE_MAP:
        return False, f"Invalid soil_texture '{raw_data['soil_texture']}'. Expected one of: {list(SOIL_TEXTURE_MAP.keys())}"

    lithology = str(raw_data['lithology']).strip().lower()
    if lithology not in LITHOLOGY_MAP:
        return False, f"Invalid lithology '{raw_data['lithology']}'. Expected one of: {list(LITHOLOGY_MAP.keys())}"

    return True, "Valid"

def transform_features(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Transforms validated raw input data into a standardized feature DataFrame.
    Applies geotechnical heuristics for antecedent precipitation and pore pressure
    if extended sensor feeds are absent.
    """
    rainfall_24h = float(raw_data['rainfall_mm'])
    soil_moisture = float(raw_data['soil_moisture_percent'])
    slope = float(raw_data['slope_angle_degrees'])

    # Geotechnical defaults for extended parameters if not explicitly provided
    if 'antecedent_rainfall_72h_mm' in raw_data and raw_data['antecedent_rainfall_72h_mm'] is not None:
        antecedent_72h = float(raw_data['antecedent_rainfall_72h_mm'])
    else:
        # Hydro-meteorological approximation: 72h antecedent rainfall is correlated with current 24h intensity
        antecedent_72h = round(rainfall_24h * 2.15 + (soil_moisture * 0.4), 2)

    if 'pore_water_pressure_kpa' in raw_data and raw_data['pore_water_pressure_kpa'] is not None:
        pore_pressure = float(raw_data['pore_water_pressure_kpa'])
    else:
        # Hydrostatic pore pressure approximation: u = saturation * gamma_w * depth * cos^2(slope)
        saturation_ratio = max(0.0, min(1.0, (soil_moisture - 20.0) / 80.0))
        pore_pressure = round(saturation_ratio * 9.81 * 1.5 * ((1.0 - (slope / 90.0) * 0.3) ** 2), 2)

    elevation = float(raw_data.get('elevation_m', 1250.0))

    features = {
        'rainfall_mm': [rainfall_24h],
        'river_water_level': [float(raw_data['river_water_level'])],
        'soil_moisture_percent': [soil_moisture],
        'slope_angle_degrees': [slope],
        'wind_speed_kmh': [float(raw_data['wind_speed_kmh'])],
        'vegetation_density_ndvi': [float(raw_data['vegetation_density_ndvi'])],
        'antecedent_rainfall_72h_mm': [antecedent_72h],
        'pore_water_pressure_kpa': [pore_pressure],
        'elevation_m': [elevation],
        'soil_type_idx': [SOIL_TYPE_MAP[str(raw_data['soil_type']).strip().lower()]],
        'soil_texture_idx': [SOIL_TEXTURE_MAP[str(raw_data['soil_texture']).strip().lower()]],
        'lithology_idx': [LITHOLOGY_MAP[str(raw_data['lithology']).strip().lower()]]
    }

    df = pd.DataFrame(features)
    return df[FEATURE_COLUMNS]

def clean_and_prepare(raw_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Validates and transforms raw input dictionary into an ML-ready DataFrame.
    Raises ValueError if input data fails validation.
    """
    is_valid, message = validate_weather_input(raw_data)
    if not is_valid:
        raise ValueError(message)
    return transform_features(raw_data)

def clean_and_prepare_batch(raw_points: list) -> Tuple[pd.DataFrame, list]:
    """
    Performs vectorized validation and transformation for a batch of coordinate points.
    Preserves spatial metadata (latitude, longitude, location_id, station_name) while
    generating standard ML feature matrices.

    Returns:
        Tuple[pd.DataFrame, list]: (df_features ready for model, list of metadata dicts)
    """
    if not isinstance(raw_points, list) or len(raw_points) == 0:
        raise ValueError("Batch input must be a non-empty list of data points.")

    metadata_list = []
    feature_rows = []

    for idx, point in enumerate(raw_points):
        is_valid, err_msg = validate_weather_input(point)
        if not is_valid:
            raise ValueError(f"Batch item at index {idx} failed validation: {err_msg}")

        # Preserve spatial metadata for GIS mapping
        metadata_list.append({
            'index': idx,
            'location_id': point.get('location_id', f'grid_cell_{idx:04d}'),
            'station_name': point.get('station_name', 'NER Station'),
            'latitude': float(point.get('latitude', point.get('lat', 26.5))),
            'longitude': float(point.get('longitude', point.get('lon', 92.5))),
            'state': point.get('state', 'NER Region')
        })

        df_single = transform_features(point)
        feature_rows.append(df_single)

    batch_df = pd.concat(feature_rows, ignore_index=True)
    return batch_df, metadata_list

