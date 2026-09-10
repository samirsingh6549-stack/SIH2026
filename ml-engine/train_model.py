import os
import json
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, accuracy_score, roc_auc_score, f1_score

from data_cleaner import FEATURE_COLUMNS, SOIL_TYPE_MAP, SOIL_TEXTURE_MAP, LITHOLOGY_MAP
from physics_engine import calculate_factor_of_safety

def generate_synthetic_ner_dataset(n_samples: int = 5000, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates a scientifically calibrated synthetic dataset modeling geotechnical
    and hydro-meteorological dynamics across the 8 North Eastern Region (NER) states.
    """
    np.random.seed(random_seed)

    # 1. Slope angles (NER mountainous terrain: 5° to 65°, skewed towards 25°-45°)
    slope = np.clip(np.random.normal(loc=32.0, scale=12.0, size=n_samples), 5.0, 65.0)

    # 2. Daily Rainfall (mm) - monsoon patterns with occasional cloudburst extremes
    # Mixture: 70% normal monsoon (10-80mm), 30% heavy/extreme monsoon (80-260mm)
    is_heavy = np.random.binomial(1, 0.30, size=n_samples)
    rainfall = np.where(
        is_heavy == 1,
        np.random.uniform(70.0, 240.0, size=n_samples),
        np.random.exponential(scale=25.0, size=n_samples)
    )
    rainfall = np.clip(rainfall, 0.0, 300.0)

    # 3. 72-hour Antecedent Precipitation (mm)
    antecedent_72h = rainfall * np.random.uniform(1.6, 2.8, size=n_samples) + np.random.uniform(0.0, 40.0, size=n_samples)
    antecedent_72h = np.clip(antecedent_72h, 0.0, 600.0)

    # 4. Soil moisture percent (strongly correlated with antecedent rainfall and clay content)
    soil_moisture = np.clip(30.0 + (antecedent_72h / 600.0) * 65.0 + np.random.normal(0, 5, size=n_samples), 10.0, 99.0)

    # 5. Pore water pressure (kPa)
    pore_pressure = np.clip(
        ((soil_moisture - 40.0) / 60.0) * 16.0 * np.cos(np.radians(slope)) + np.random.normal(0, 1.0, size=n_samples),
        0.0, 25.0
    )

    # 6. River water level (m) - toe erosion proxy for highway and river valley corridors
    river_water_level = np.clip(np.random.gamma(shape=5.0, scale=2.5, size=n_samples) + (rainfall / 30.0), 1.0, 35.0)

    # 7. Vegetation density (NDVI) - Himalayan hills range from degraded (-0.05 to 0.25) to dense forest (0.65 to 0.85)
    vegetation_ndvi = np.clip(np.random.beta(a=4.0, b=2.5, size=n_samples), 0.05, 0.90)

    # 8. Wind speed (km/h)
    wind_speed = np.clip(np.random.weibull(a=1.8, size=n_samples) * 14.0, 2.0, 85.0)

    # 9. Elevation (m) - NER valleys to high ridges (300m to 3500m)
    elevation = np.random.uniform(350.0, 3200.0, size=n_samples)

    # 10. Categorical indices
    soil_type_idx = np.random.choice([1, 2, 3, 4, 5], size=n_samples, p=[0.15, 0.30, 0.35, 0.15, 0.05])
    soil_texture_idx = np.random.choice([1, 2, 3], size=n_samples, p=[0.25, 0.45, 0.30])
    lithology_idx = np.random.choice([1, 2, 3, 4], size=n_samples, p=[0.15, 0.35, 0.40, 0.10])

    # Geotechnical Ground-Truth labeling:
    # A slope fails if Factor of Safety < 1.05 OR empirical hazard score crosses failure trigger
    # Combining Coulomb shear equilibrium + empirical rainfall saturation threshold
    soil_type_names = {1: 'sand', 2: 'loam', 3: 'clay', 4: 'silt', 5: 'gravel'}
    landslide_labels = []

    for i in range(n_samples):
        st_name = soil_type_names[soil_type_idx[i]]
        fos_calc = calculate_factor_of_safety(
            slope_angle_deg=slope[i],
            pore_pressure_kpa=pore_pressure[i],
            soil_type=st_name,
            soil_depth_m=1.8
        )
        fos = fos_calc['factor_of_safety']

        # Empirical triggering components
        rainfall_trigger = (rainfall[i] > 110.0 and antecedent_72h[i] > 180.0 and slope[i] > 28.0)
        saturation_trigger = (soil_moisture[i] > 84.0 and slope[i] > 32.0 and pore_pressure[i] > 7.0)
        degraded_slope_trigger = (vegetation_ndvi[i] < 0.25 and slope[i] > 35.0 and rainfall[i] > 75.0)

        if fos < 1.0 or rainfall_trigger or saturation_trigger or degraded_slope_trigger:
            # High / Severe Risk (Positive class 1)
            landslide_labels.append(1)
        else:
            # Low / Stable Risk (Negative class 0)
            landslide_labels.append(0)

    df = pd.DataFrame({
        'rainfall_mm': np.round(rainfall, 2),
        'river_water_level': np.round(river_water_level, 2),
        'soil_moisture_percent': np.round(soil_moisture, 2),
        'slope_angle_degrees': np.round(slope, 2),
        'wind_speed_kmh': np.round(wind_speed, 2),
        'vegetation_density_ndvi': np.round(vegetation_ndvi, 3),
        'antecedent_rainfall_72h_mm': np.round(antecedent_72h, 2),
        'pore_water_pressure_kpa': np.round(pore_pressure, 2),
        'elevation_m': np.round(elevation, 1),
        'soil_type_idx': soil_type_idx,
        'soil_texture_idx': soil_texture_idx,
        'lithology_idx': lithology_idx,
        'target': np.array(landslide_labels, dtype=int)
    })

    return df

def train_and_export():
    """
    Trains the Random Forest model on the NER dataset, prints metrics,
    and exports model.pkl alongside model_metadata.json.
    """
    print("=" * 65)
    print("  SIH 2026: AI/ML SLOPE STABILITY PREDICTIVE MODEL TRAINING")
    print("  Region: North Eastern Region (NER) Geotechnical Framework")
    print("=" * 65)

    print("\n[1/5] Synthesizing calibrated NER geotechnical training dataset...")
    df = generate_synthetic_ner_dataset(n_samples=6000, random_seed=42)
    print(f"      Total samples generated: {len(df)}")
    pos_count = df['target'].sum()
    print(f"      Hazardous events: {pos_count} ({pos_count / len(df) * 100:.1f}%) | Baseline stable: {len(df) - pos_count}")

    X = df[FEATURE_COLUMNS]
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
    print(f"\n[2/5] Partitioned data: {len(X_train)} train samples, {len(X_test)} test samples.")

    print("\n[3/5] Fitting ensemble Random Forest Classifier (120 estimators, depth=14)...")
    rf_model = RandomForestClassifier(
        n_estimators=120,
        max_depth=14,
        min_samples_split=4,
        min_samples_leaf=2,
        class_weight='balanced',
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)

    # Predictions & evaluation
    y_pred = rf_model.predict(X_test)
    y_prob = rf_model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)

    print(f"\n[4/5] Model Performance Evaluation:")
    print(f"      Accuracy:  {acc * 100:.2f}%")
    print(f"      F1-Score:  {f1:.4f}")
    print(f"      ROC-AUC:   {roc_auc:.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=['Stable', 'Landslide Hazard']))

    # Feature Importance ranking
    feature_importances = dict(zip(FEATURE_COLUMNS, [round(float(v), 4) for v in rf_model.feature_importances_]))
    sorted_importances = sorted(feature_importances.items(), key=lambda item: item[1], reverse=True)
    print("Top Predictive Feature Drivers:")
    for rank, (feat, imp) in enumerate(sorted_importances[:6], start=1):
        print(f"      {rank}. {feat: <26}: {imp * 100:.1f}% contribution")

    # Serialize artifacts
    current_folder = Path(__file__).parent
    model_path = current_folder / "model.pkl"
    metadata_path = current_folder / "model_metadata.json"

    print(f"\n[5/5] Exporting model artifact to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(rf_model, f, protocol=pickle.HIGHEST_PROTOCOL)

    metadata = {
        'model_name': 'RandomForest_NER_Landslide_Susceptibility',
        'algorithm': 'RandomForestClassifier',
        'n_estimators': 120,
        'features': FEATURE_COLUMNS,
        'accuracy': round(float(acc), 4),
        'f1_score': round(float(f1), 4),
        'roc_auc': round(float(roc_auc), 4),
        'feature_importances': feature_importances,
        'classes': [0, 1],
        'class_labels': ['Stable / Low Risk', 'Landslide Hazard Detected'],
        'target_region': 'North Eastern Region (NER) - 8 States'
    }

    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)

    print(f"      Metadata saved to {metadata_path}")
    print("\n>>> Model training pipeline completed successfully!\n")

if __name__ == '__main__':
    train_and_export()
