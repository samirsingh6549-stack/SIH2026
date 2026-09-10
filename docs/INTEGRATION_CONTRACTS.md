# Team Integration Contracts (SIH 2026)
## AI-Based Landslide Early Warning & Risk Monitoring System in NER
### Module 6 Backbone: Cloud Architecture & Offline Sync Engine

This document provides the exact API endpoints, database schemas, and integration code snippets for all 5 team members to connect their modules into the centralized Cloud & Offline-Sync Backbone.

---

## 1. Module 1: Real-time GIS Dashboard & Heatmaps

### Objective
Visualize risk heatmaps, monitored geotechnical stations, and field incident markers on an interactive map.

### How GIS Team Integrates
The GIS Dashboard pulls the current risk zones and field reports from the cloud API (or reads from local cache if offline).

#### Endpoint: `GET /api/risk_zones`
* **Query Parameters:** Optional `state=Sikkim` or `min_risk=0.7`
* **Response (JSON):**
```json
{
  "count": 3,
  "data": [
    {
      "id": "rz-1",
      "zone_code": "NER-MEGH-SHILLONG-01",
      "zone_name": "East Khasi Hills Slope Segment A",
      "state": "Meghalaya",
      "district": "East Khasi Hills",
      "risk_level": "HIGH",
      "risk_score": 0.81,
      "latitude": 25.5788,
      "longitude": 91.8933,
      "contributing_factors": {
        "rain_accum_mm": 142.5,
        "slope_angle_deg": 38.2
      },
      "updated_at": "2026-09-09T17:15:00.000Z"
    }
  ]
}
```

#### Endpoint: `GET /api/field_reports`
* **Purpose:** Render user-reported slope cracks, mudslides, and road blockages directly on the GIS map with pins color-coded by severity (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`).

---

## 2. Module 2: AI/ML Predictive Analytics Engine

### Objective
Ingest real-time sensor streams and weather forecasts, compute landslide probability scores, and write predictions back to the cloud database.

### How ML Team Integrates
1. **Fetch Latest Telemetry (Input):**
   * Endpoint: `GET /api/telemetry`
   * Provides time-series data: `rainfall_mm_h`, `soil_moisture_percent`, `pore_water_pressure_kpa`, `slope_tilt_degrees`.
2. **Post Risk Predictions (Output):**
   * Endpoint: `POST /api/risk_zones`
   * Request Payload:
```json
{
  "zone_code": "NER-SIKK-GANGTOK-02",
  "zone_name": "NH-10 Corridor Near Ranipool",
  "state": "Sikkim",
  "district": "East Sikkim",
  "risk_level": "CRITICAL",
  "risk_score": 0.942,
  "latitude": 27.3389,
  "longitude": 88.6065,
  "contributing_factors": {
    "rainfall_trigger_index": 0.88,
    "pore_water_pressure_kpa": 44.5,
    "tilt_velocity_deg_per_hour": 0.22
  }
}
```

---

## 3. Module 3: Mobile/Web Application for Field Reporting

### Objective
Allow ground scouts, NDRF personnel, and citizens in remote NER valleys to submit incident reports even when cellular connectivity drops completely.

### How Field App Team Integrates
Instead of making raw `fetch()` calls that fail when there is no internet, the app team simply imports the **Offline Sync Manager**:

```javascript
import { syncManager } from './src/syncManager.js';

// Inside the App Submit Button handler:
async function onReportSubmit(formData) {
  // Automatically writes to local IndexedDB, queues offline, and syncs upon reconnection!
  const queuedReport = await syncManager.submitFieldReport({
    reporter_name: "Tashi Dorjee",
    reporter_role: "NDRF / SDRF",
    hazard_type: "Debris Flow / Mudslide",
    severity: "CRITICAL",
    latitude: 27.3389,
    longitude: 88.6065,
    notes: "NH-10 Ranipool stretch covered in slurry. Traffic halted."
  });

  console.log("Report saved with ID:", queuedReport.client_id);
}
```

---

## 4. Module 4: Ingestion (IMD Weather, Satellites & Sensors)

### Objective
Feed meteorological precipitation, satellite moisture indices, and ground sensor data into the cloud platform.

### How Ingestion Team Integrates
The ingestion script makes periodic HTTP POST requests:

#### Endpoint: `POST /api/telemetry`
```json
{
  "station_id": "NER-MEGH-SHILLONG-01",
  "station_name": "East Khasi Hills Monitoring Station",
  "state": "Meghalaya",
  "latitude": 25.5788,
  "longitude": 91.8933,
  "rainfall_mm_h": 24.5,
  "temperature_c": 19.8,
  "soil_moisture_percent": 82.4,
  "pore_water_pressure_kpa": 38.6,
  "slope_tilt_degrees": 2.15,
  "recorded_at": "2026-09-09T17:30:00Z"
}
```

---

## 5. Module 5: Automated SMS / Early Warning Alert System

### Objective
Broadcast evacuation notices and SMS/Telegram alerts to vulnerable populations when risk levels breach critical thresholds.

### How Alert Team Integrates
1. **Poll for Active Alerts:**
   * Endpoint: `GET /api/alerts`
   * Returns list of alerts with instructions and targeted villages:
```json
{
  "count": 1,
  "data": [
    {
      "id": "alt-1",
      "alert_code": "ALT-2026-001",
      "zone_code": "NER-SIKK-GANGTOK-02",
      "severity": "EVACUATION",
      "headline": "Immediate Evacuation Order: Active debris flow risk along NH-10 Ranipool sector",
      "instructions": "Move immediately to assigned disaster relief shelter at Upper Martam School. Avoid valley roads.",
      "target_villages": ["Ranipool", "Martam", "Singtam"],
      "is_active": true
    }
  ]
}
```

2. **Trigger Dispatch:**
   * In production Supabase, an `AFTER INSERT OR UPDATE` trigger on `landslide_risk_zones` calls an Edge Function or Webhook to your Telegram Bot / SMS gateway whenever `risk_score > 0.85`.

---

## Summary of Shared Cloud Schema (PostgreSQL)

| Table Name | Written By | Read By | Offline Cache? |
| :--- | :--- | :--- | :--- |
| `sensor_telemetry` | Module 4 (Weather / Sensors) | Module 2 (AI/ML Engine) | No (High frequency) |
| `landslide_risk_zones` | Module 2 (AI/ML Engine) | Module 1 (GIS) & Module 3 (App) | **Yes** (Cached on client) |
| `field_reports` | Module 3 (Field App via Sync) | Module 1 (GIS Dashboard) | **Yes** (Client Outbox Queue) |
| `emergency_alerts` | Module 5 / Automated Trigger | Module 3 (Citizens / NDRF) | **Yes** (Cached on client) |
