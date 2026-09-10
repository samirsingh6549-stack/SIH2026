# Module 2: Meteorological & Geotechnical Sensor Ingestion Engine

Real-time meteorological and geotechnical sensor data ingestion pipeline covering all **8 North Eastern Region (NER) states**: Sikkim, Assam, Meghalaya, Arunachal Pradesh, Nagaland, Manipur, Mizoram, and Tripura.

---

## 1. System Architecture

```
Open-Meteo Global High-Res Forecast
    │
    ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│   open_meteo_client.py  │     │   geotech_sensors.py    │
│ • 24h Real Precipitation│     │ • Vibrating Wire Piezometer│
│ • 72h Antecedent Rain   │     │ • Digital MEMS Tiltmeter │
│ • Volumetric Moisture   │     │ • Wire Extensometer     │
└───────────┬─────────────┘     └───────────┬─────────────┘
            │                               │
            └───────────────┬───────────────┘
                            ▼
                ┌───────────────────────┐     ┌─────────────────────────┐
                │      pipeline.py      │ ◄── │    gsi_inventory.py     │
                │ (Normalizes Telemetry)│     │ (GSI Bhukosh Records)   │
                └───────────┬───────────┘     └─────────────────────────┘
                            │
                            ▼
                ┌───────────────────────┐
                │  ml-engine/predictor  │ ── Generates Real-time LSI Scores & GIS Heatmap
                └───────────────────────┘
```

---

## 2. Ingested Data Streams

### A. Meteorological Feed (Live Open-Meteo API)
- **Cumulative 24h Precipitation**: Active surface rain runoff in $\text{mm}$.
- **72h Antecedent Precipitation Index (API)**: Rolling historical rain accumulation crucial for deep regolith failure.
- **Volumetric Soil Water Content**: Real-time soil moisture percentage ($0 - 100\%$).
- **Atmospheric Parameters**: 2m Temperature ($^\circ\text{C}$), Relative Humidity ($\%$), 10m Wind Speed ($\text{km/h}$).
- **Resilient Fallback**: If network is severed in mountain dead-zones, an autonomous cached regolith model provides deterministic local fallback telemetry so systems never crash.

### B. Geotechnical In-Situ Instrumentation
Simulates physical sensors deployed by Geological Survey of India (GSI) and CSIR-CRRI:
- **Piezometer (Vibrating Wire)**: Subsurface pore water pressure $u$ in $\text{kPa}$.
- **Inclinometer / Tiltmeter (MEMS Digital Biaxial)**: Slope displacement vector in degrees ($^\circ$).
- **Surface Extensometer**: Tension crack displacement in $\text{mm}$.
- **Acoustic Emission**: Micro-fracturing waveguide hits/minute.

### C. Geological Survey of India (GSI) Bhukosh Historical Records
- Includes curated fatal and major disaster records across all 8 states (e.g. Tupul Manipur 2022, Haflong Assam 2022, Teesta Sikkim 2023, Aizawl Mizoram 2024).
- Automatic nearest historical event distance calculation using the Haversine equation.

---

## 3. Station Coverage (All 8 NER States)

| State | Station Name | Lifeline Highway Corridor | Elevation | Slope |
| :--- | :--- | :--- | :--- | :--- |
| **Sikkim** | Gangtok - 9th Mile | NH-10 (Siliguri - Gangtok) | 1650 m | 41.5° |
| **Sikkim** | Mangan - Dikchu Sector | North Sikkim Highway | 1280 m | 44.0° |
| **Assam** | Haflong - Jatinga Valley | NH-27 / Lumding-Badarpur Rail | 680 m | 34.0° |
| **Assam** | Guwahati - Khanapara | Guwahati Bypass / GS Road | 180 m | 26.5° |
| **Meghalaya** | Cherrapunji - Sohra | SH-5 (Sohra-Shella Corridor) | 1430 m | 43.5° |
| **Meghalaya** | Shillong - Umiam Bypass | NH-6 (Guwahati-Shillong-Silchar) | 1020 m | 31.0° |
| **Arunachal**| Tawang - Sela Passway | NH-13 (Trans-Arunachal Highway)| 2980 m | 45.0° |
| **Arunachal**| Itanagar - Banderdewa | NH-415 (Capital Complex) | 530 m | 33.5° |
| **Nagaland** | Kohima - Dzüdza River | NH-29 (Dimapur - Kohima) | 1440 m | 39.0° |
| **Manipur**  | Noney - Tupul Yard | NH-37 (Jiribam - Imphal Highway)| 720 m | 42.0° |
| **Mizoram**  | Aizawl - Hunthar Zone | NH-54 (Silchar - Aizawl Road) | 1130 m | 38.5° |
| **Tripura**  | Jampui Hills - Vanghmun | Dharmanagar - Kanchanpur Road | 880 m | 29.5° |

---

## 4. Execution & Usage

### Step 1: Run Ingestion Pipeline (All 8 States)
```bash
python ingestion/pipeline.py
```

### Step 2: Filter Ingestion by State
```bash
python ingestion/pipeline.py --state Sikkim
python ingestion/pipeline.py --state Assam
```

### Step 3: Export Ingested Telemetry Snapshot to JSON
```bash
python ingestion/pipeline.py --export telemetry_snapshot.json
```

### Step 4: Run Automated Unit Tests
```bash
python ingestion/test_ingestion.py
```
Verifies live weather fetching, sensor physics, GSI inventory lookups, and ML scoring integration (8/8 tests passing).
