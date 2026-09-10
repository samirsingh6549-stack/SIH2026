# Module 1: AI/ML Predictive Analytics & Slope Stability Engine

An AI/ML slope susceptibility and early warning analytics engine tailored to the terrain, geology, and hydrometeorology of the **North Eastern Region (NER)** of India.

---

## 1. System Architecture

The engine combines data-driven ensemble learning with physics-based slope equilibrium and empirical rainfall thresholds:

```
Raw Telemetry / Weather Feed
            │
            ▼
┌─────────────────────────┐
│   data_cleaner.py       │ ── Schema validation, categorical encoding, geotechnical defaults
└───────────┬─────────────┘
            │ Standardized Feature Vector
            ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│     train_model.py      │     │    physics_engine.py    │
│  (Random Forest 120 est)│     │ • Caine Rainfall Threshold│
│  Outputs: LSI (0.0-1.0) │     │ • Infinite Slope FoS    │
└───────────┬─────────────┘     └───────────┬─────────────┘
            │                               │
            └───────────────┬───────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │     predictor.py      │ ── LSI Score, 4-Tier Risk, FoS, Explainable Factors
                └───────────┬───────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
    HTTP REST API (server.py)       Python Library Import
```

---

## 2. Mathematical & Geotechnical Formulation

### A. Caine's Empirical Rainfall Intensity-Duration Threshold
Evaluates whether sustained precipitation exceeds the empirical slope initiation threshold:
$$I_c = 14.82 \times D^{-0.39}$$
- $I_c$: Critical precipitation intensity ($\text{mm/hr}$)
- $D$: Rainfall duration ($\text{hours}$, default 24h)

### B. Infinite Slope Stability Model (Factor of Safety - FoS)
Evaluates limit equilibrium of planar translational failure along weathered regolith:
$$\text{FoS} = \frac{c' + (\gamma \cdot z - u) \cos^2\beta \tan\phi'}{\gamma \cdot z \sin\beta \cos\beta}$$
- $c'$: Effective soil cohesion ($\text{kPa}$)
- $\phi'$: Internal angle of friction ($\text{degrees}$)
- $\gamma$: Total unit weight of saturated soil ($\sim 18.5\text{ kN/m}^3$)
- $z$: Regolith slip depth ($1.8\text{ m}$)
- $u$: Subsurface pore water pressure ($\text{kPa}$)
- $\beta$: Slope inclination angle ($\text{degrees}$)

**Safety Tiers:**
- $\text{FoS} > 1.30$: Stable Slope
- $1.00 \le \text{FoS} \le 1.30$: Marginally Stable / Watch State
- $\text{FoS} < 1.00$: Active Failure / Imminent Collapse

### C. Landslide Susceptibility Index (LSI) via Supervised ML
A tuned `RandomForestClassifier` (120 estimators, depth=14) trained on regional geo-environmental vectors outputs a continuous probability distribution ($0.00 \le \text{LSI} \le 1.00$):
- **LOW** ($\text{LSI} < 0.35$): Baseline green conditions.
- **MODERATE** ($0.35 \le \text{LSI} < 0.60$): Advisory watch.
- **HIGH** ($0.60 \le \text{LSI} < 0.82$): Orange alert, highway monitoring.
- **SEVERE** ($\text{LSI} \ge 0.82$): Red alert, evacuation order.

---

## 3. Input Feature Schema

| Parameter | Type | Range | Description |
| :--- | :--- | :--- | :--- |
| `rainfall_mm` | Float | $\ge 0$ | 24-hour cumulative rainfall |
| `river_water_level` | Float | $\ge 0$ | Fluvial gauge level / toe erosion indicator (m) |
| `soil_moisture_percent` | Float | $0 - 100$ | Volumetric water content (%) |
| `slope_angle_degrees` | Float | $0 - 90$ | Topographical slope inclination (deg) |
| `wind_speed_kmh` | Float | $\ge 0$ | Surface wind velocity (km/h) |
| `vegetation_density_ndvi`| Float | $-1.0 - 1.0$| Normalized Difference Vegetation Index |
| `soil_type` | String | `sand`, `loam`, `clay`, `silt`, `gravel` | Regolith grain categorization |
| `soil_texture` | String | `coarse`, `medium`, `fine` | Soil texture classification |
| `lithology` | String | `igneous`, `metamorphic`, `sedimentary`, `unconsolidated` | Bedrock geology |

---

## 4. Execution & Usage

### Step 1: Train Model & Generate Artifacts
```bash
python ml-engine/train_model.py
```
Outputs `model.pkl` and `model_metadata.json`.

### Step 2: Run Unit & Integration Tests
```bash
python ml-engine/test_ml_engine.py
```

### Step 3: Run Interactive Predictor CLI
```bash
python ml-engine/predictor.py
```

### Step 4: Launch REST API Server
```bash
python ml-engine/server.py
```
Listens on `http://localhost:5001`.

#### Sample Single-Point Request:
```bash
curl -X POST http://localhost:5001/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "rainfall_mm": 180.0,
    "river_water_level": 24.0,
    "soil_moisture_percent": 85.0,
    "slope_angle_degrees": 42.0,
    "wind_speed_kmh": 35.5,
    "vegetation_density_ndvi": 0.2,
    "soil_type": "clay",
    "soil_texture": "fine",
    "lithology": "sedimentary"
  }'
```

#### Sample Batch Inference Request:
```bash
curl -X POST http://localhost:5001/api/predict/batch \
  -H "Content-Type: application/json" \
  -d '{
    "points": [
      {
        "location_id": "gangtok_nh10_mile12",
        "station_name": "Gangtok NH-10",
        "latitude": 27.33,
        "longitude": 88.61,
        "state": "Sikkim",
        "rainfall_mm": 185.0,
        "river_water_level": 24.0,
        "soil_moisture_percent": 86.0,
        "slope_angle_degrees": 43.0,
        "wind_speed_kmh": 32.0,
        "vegetation_density_ndvi": 0.18,
        "soil_type": "clay",
        "soil_texture": "fine",
        "lithology": "sedimentary"
      }
    ]
  }'
```

#### Sample Leaflet Heatmap Grid Request:
```bash
curl -X POST http://localhost:5001/api/predict/heatmap \
  -H "Content-Type: application/json" \
  -d '{
    "points": [ ...array of grid cells... ]
  }'
```
Returns:
- `leaflet_heat_points`: Array of `[lat, lon, intensity]` ready for `L.heatLayer()`.
- `geojson_feature_collection`: Standard GeoJSON for vector marker layers with hex colors (`#22c55e`, `#eab308`, `#f97316`, `#ef4444`).
- `regional_hotspots_count`: Total high-hazard clusters identified.
