import pickle
import json
from pathlib import Path
from typing import Dict, Any, Union

from data_cleaner import clean_and_prepare, transform_features, clean_and_prepare_batch
from physics_engine import evaluate_caine_threshold, calculate_factor_of_safety, extract_contributing_risk_factors

_MODEL_CACHE = None
_METADATA_CACHE = None

def _get_model():
    """
    Loads and caches the model from disk to eliminate repetitive I/O latency.
    """
    global _MODEL_CACHE
    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    current_folder = Path(__file__).parent
    model_path = current_folder / "model.pkl"

    if not model_path.exists():
        raise FileNotFoundError(f"Model artifact not found at {model_path}. Run train_model.py first.")

    with open(model_path, 'rb') as f:
        _MODEL_CACHE = pickle.load(f)
    # Configure single-threaded inference for sub-millisecond edge response
    if hasattr(_MODEL_CACHE, 'n_jobs'):
        _MODEL_CACHE.n_jobs = 1

    return _MODEL_CACHE

def _get_metadata():
    """
    Loads and caches model metadata.
    """
    global _METADATA_CACHE
    if _METADATA_CACHE is not None:
        return _METADATA_CACHE

    current_folder = Path(__file__).parent
    meta_path = current_folder / "model_metadata.json"

    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            _METADATA_CACHE = json.load(f)
    else:
        _METADATA_CACHE = {}

    return _METADATA_CACHE

def predict_disaster_risk(raw_weather_data: dict) -> str:
    """
    Predicts landslide disaster risk using the trained ML model.
    Maintains 100% backward compatibility with original application specifications.

    Parameters:
        raw_weather_data (dict): Raw input payload containing sensor & weather readings.

    Returns:
        str: Human-readable risk assessment message.
    """
    try:
        # 1. Clean and prepare the data (validates schema & normalizes features)
        clean_dataframe = clean_and_prepare(raw_weather_data)

        # 2. Load the trained model (cached in memory for high-throughput inference)
        model = _get_model()

        # 3. Ask the model for a prediction
        prediction = model.predict(clean_dataframe)

        # 4. Translate the result
        if prediction[0] == 1:
            return "High Risk: Landslide/Flood conditions detected."
        else:
            return "Low Risk: Normal conditions."

    except ValueError as validation_error:
        return f"Data Error: {str(validation_error)}"
    except FileNotFoundError:
        return "System Error: model.pkl missing. Run training notebook first."
    except Exception as e:
        return f"Prediction Error: {str(e)}"

def predict_detailed_risk(raw_weather_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generates a full-spectrum analytical risk assessment including:
    - ML probability / Landslide Susceptibility Index (LSI: 0.00 to 1.00)
    - 4-Tier Risk Categorization (LOW, MODERATE, HIGH, SEVERE)
    - Geotechnical Factor of Safety (FoS) equilibrium
    - Empirical Caine Rainfall Threshold status
    - Explainable contributing drivers and SDMA recommended actions.
    """
    try:
        # 1. Validate & transform inputs
        df_features = clean_and_prepare(raw_weather_data)
        model = _get_model()

        # 2. Probability & classification
        probabilities = model.predict_proba(df_features)[0]
        lsi_score = float(probabilities[1])  # Probability of landslide hazard
        prediction_class = int(model.predict(df_features)[0])

        # 3. Dynamic 4-Tier Risk Classification
        if lsi_score >= 0.82:
            risk_tier = "SEVERE"
            action_code = "EVACUATION_WARNING"
            recommended_action = "Issue immediate evacuation order for downslope settlements. Restrict transit on vulnerable highway sectors."
        elif lsi_score >= 0.60:
            risk_tier = "HIGH"
            action_code = "ALERT_ORANGE"
            recommended_action = "Activate emergency quick-reaction teams. Pre-position earthmoving machinery along lifeline routes."
        elif lsi_score >= 0.35:
            risk_tier = "MODERATE"
            action_code = "WATCH_YELLOW"
            recommended_action = "Intensify automated geotechnical sensor polling. Issue advisory to commercial transport operators."
        else:
            risk_tier = "LOW"
            action_code = "NORMAL_GREEN"
            recommended_action = "Normal monitoring protocol. No immediate slope destabilization risk detected."

        # 4. Physics Engine Calculations
        rainfall_24h = float(raw_weather_data['rainfall_mm'])
        slope_angle = float(raw_weather_data['slope_angle_degrees'])
        soil_type = str(raw_weather_data.get('soil_type', 'clay')).lower()

        # Derive pore pressure from DataFrame
        pore_pressure = float(df_features['pore_water_pressure_kpa'].iloc[0])

        caine_eval = evaluate_caine_threshold(rainfall_intensity_mmh=rainfall_24h / 24.0, duration_hours=24.0)
        fos_eval = calculate_factor_of_safety(
            slope_angle_deg=slope_angle,
            pore_pressure_kpa=pore_pressure,
            soil_type=soil_type,
            soil_depth_m=1.8
        )

        # 5. Explainable AI risk factors
        feature_dict = df_features.to_dict(orient='records')[0]
        contributing_factors = extract_contributing_risk_factors(feature_dict)

        confidence_pct = round(max(probabilities) * 100, 1)

        return {
            'status': 'success',
            'prediction': prediction_class,
            'risk_level': risk_tier,
            'lsi_score': round(lsi_score, 4),
            'confidence_percentage': confidence_pct,
            'action_code': action_code,
            'recommended_action': recommended_action,
            'physics_validation': {
                'factor_of_safety': fos_eval['factor_of_safety'],
                'stability_state': fos_eval['stability_status'],
                'caine_threshold_breached': caine_eval['breached'],
                'caine_intensity_ratio': caine_eval['intensity_ratio']
            },
            'contributing_factors': contributing_factors,
            'input_summary': {
                'rainfall_24h_mm': rainfall_24h,
                'slope_angle_deg': slope_angle,
                'soil_moisture_pct': float(raw_weather_data['soil_moisture_percent']),
                'lithology': str(raw_weather_data.get('lithology')),
                'soil_type': soil_type
            }
        }

    except ValueError as ve:
        return {'status': 'error', 'error_type': 'ValidationError', 'message': str(ve)}
    except FileNotFoundError as fe:
        return {'status': 'error', 'error_type': 'MissingModelError', 'message': str(fe)}
    except Exception as e:
        return {'status': 'error', 'error_type': 'InferenceError', 'message': str(e)}

def predict_batch(raw_points: list) -> Dict[str, Any]:
    """
    Executes high-throughput vectorized inference across an array of coordinate/sensor points.
    Processes hundreds of points in a single matrix operation for sub-50ms regional scanning.
    """
    try:
        # 1. Clean and vectorize batch data
        batch_df, metadata_list = clean_and_prepare_batch(raw_points)
        model = _get_model()

        # 2. Vectorized matrix inference in one call
        probabilities = model.predict_proba(batch_df)[:, 1]
        class_predictions = model.predict(batch_df)

        results = []
        for i, prob in enumerate(probabilities):
            lsi = float(prob)
            cls_pred = int(class_predictions[i])
            meta = metadata_list[i]

            if lsi >= 0.82:
                tier = "SEVERE"
                color = "#ef4444"
            elif lsi >= 0.60:
                tier = "HIGH"
                color = "#f97316"
            elif lsi >= 0.35:
                tier = "MODERATE"
                color = "#eab308"
            else:
                tier = "LOW"
                color = "#22c55e"

            results.append({
                'location_id': meta['location_id'],
                'station_name': meta['station_name'],
                'latitude': meta['latitude'],
                'longitude': meta['longitude'],
                'state': meta['state'],
                'lsi_score': round(lsi, 4),
                'risk_level': tier,
                'color_code': color,
                'prediction': cls_pred
            })

        return {
            'status': 'success',
            'total_processed': len(results),
            'predictions': results
        }

    except ValueError as ve:
        return {'status': 'error', 'error_type': 'ValidationError', 'message': str(ve)}
    except Exception as e:
        return {'status': 'error', 'error_type': 'BatchInferenceError', 'message': str(e)}

def generate_heatmap_probabilities(grid_points: list) -> Dict[str, Any]:
    """
    Transforms grid telemetry into GIS-ready heatmap structures:
    1. Leaflet Heat Layer format: [ [lat, lon, intensity], ... ]
    2. Categorized GeoJSON points with dynamic hex color gradations
    3. Regional summary metrics (max LSI, mean LSI, critical cluster count).
    """
    batch_res = predict_batch(grid_points)
    if batch_res.get('status') != 'success':
        return batch_res

    predictions = batch_res['predictions']
    leaflet_heat_points = []
    geo_features = []

    tier_counts = {'LOW': 0, 'MODERATE': 0, 'HIGH': 0, 'SEVERE': 0}
    lsi_values = []

    for p in predictions:
        lat = p['latitude']
        lon = p['longitude']
        lsi = p['lsi_score']
        tier = p['risk_level']
        color = p['color_code']

        lsi_values.append(lsi)
        tier_counts[tier] += 1

        # Leaflet heat layer tuple: [lat, lon, intensity (0.0 to 1.0)]
        leaflet_heat_points.append([lat, lon, lsi])

        # Rich feature point for interactive map popups
        geo_features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'location_id': p['location_id'],
                'station_name': p['station_name'],
                'state': p['state'],
                'lsi_score': lsi,
                'intensity': round(lsi, 3),
                'risk_level': tier,
                'color': color,
                'stroke_color': '#ffffff'
            }
        })

    max_lsi = max(lsi_values) if lsi_values else 0.0
    mean_lsi = round(sum(lsi_values) / len(lsi_values), 4) if lsi_values else 0.0

    return {
        'status': 'success',
        'grid_cell_count': len(predictions),
        'max_lsi_score': max_lsi,
        'mean_lsi_score': mean_lsi,
        'regional_hotspots_count': tier_counts['HIGH'] + tier_counts['SEVERE'],
        'tier_distribution': tier_counts,
        'leaflet_heat_points': leaflet_heat_points,
        'geojson_feature_collection': {
            'type': 'FeatureCollection',
            'features': geo_features
        },
        'color_scale': {
            'low': {'min': 0.0, 'max': 0.35, 'color': '#22c55e', 'label': 'Safe / Low'},
            'moderate': {'min': 0.35, 'max': 0.60, 'color': '#eab308', 'label': 'Watch / Moderate'},
            'high': {'min': 0.60, 'max': 0.82, 'color': '#f97316', 'label': 'Warning / High'},
            'severe': {'min': 0.82, 'max': 1.00, 'color': '#ef4444', 'label': 'Evacuation / Severe'}
        }
    }


# --- Quick Test ---
if __name__ == "__main__":
    print("-" * 60)
    print("TEST 1: High-Risk Scenario (Monsoon cloudburst on steep slope)")
    test_payload_high = {
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

    simple_high = predict_disaster_risk(test_payload_high)
    print(f"Simple Output:   {simple_high}")
    detailed_high = predict_detailed_risk(test_payload_high)
    print(f"Detailed Output: LSI={detailed_high.get('lsi_score')}, Tier={detailed_high.get('risk_level')}, FoS={detailed_high.get('physics_validation', {}).get('factor_of_safety')}")
    print(f"Action:          {detailed_high.get('recommended_action')}")

    print("\n" + "-" * 60)
    print("TEST 2: Low-Risk Scenario (Dry spell, gentle slope, dense vegetation)")
    test_payload_low = {
        'rainfall_mm': 5.0,
        'river_water_level': 4.2,
        'soil_moisture_percent': 32.0,
        'slope_angle_degrees': 14.0,
        'wind_speed_kmh': 12.0,
        'vegetation_density_ndvi': 0.78,
        'soil_type': 'loam',
        'soil_texture': 'medium',
        'lithology': 'igneous'
    }

    simple_low = predict_disaster_risk(test_payload_low)
    print(f"Simple Output:   {simple_low}")
    detailed_low = predict_detailed_risk(test_payload_low)
    print(f"Detailed Output: LSI={detailed_low.get('lsi_score')}, Tier={detailed_low.get('risk_level')}, FoS={detailed_low.get('physics_validation', {}).get('factor_of_safety')}")
    print(f"Action:          {detailed_low.get('recommended_action')}")
    print("-" * 60)
