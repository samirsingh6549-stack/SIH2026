# Module 3: Common Alerting Protocol (CAP v1.2) & Multi-Channel Dissemination Engine
### Smart India Hackathon (SIH 2026)
**Official Standard: OASIS CAP v1.2 / ITU-T X.1303 (NDMA SACHET Compliant)**

---

## 1. Overview
When the Machine Learning Engine (**Module 1**) and Telemetry Ingestion (**Module 2**) detect that a mountain slope is approaching failure ($LSI \ge 0.82$ or $FoS < 1.0$), **Module 3** immediately formats and disseminates authoritative, life-saving warnings.

In India, disaster alerting is governed by the **National Disaster Management Authority (NDMA)** via the **SACHET** platform, which mandates the **OASIS Common Alerting Protocol (CAP v1.2)**. Module 3 serializes all alerts into this exact standard and broadcasts them across **4 redundant channels** simultaneously.

---

## 2. Multi-Channel Broadcast Pipeline

```
              ┌─────────────────────────────────────────────────┐
              │  Hazard Trigger (Module 1 LSI / Module 2 FoS)   │
              └────────────────────────┬────────────────────────┘
                                       │
                                       ▼
              ┌─────────────────────────────────────────────────┐
              │      OASIS CAP v1.2 XML & JSON Serializer       │
              └────────────────────────┬────────────────────────┘
                                       │
         ┌──────────────────┬──────────┴──────────┬──────────────────┐
         │                  │                     │                  │
         ▼                  ▼                     ▼                  ▼
┌─────────────────┐ ┌────────────────┐ ┌───────────────────┐ ┌─────────────────┐
│ Channel 1:      │ │ Channel 2:     │ │ Channel 3:        │ │ Channel 4:      │
│ Telecom Cell    │ │ Automated IVRS │ │ IoT Physical      │ │ State EOC / 112 │
│ Broadcast / SMS │ │ Voice Dialing  │ │ Sirens & Barriers │ │ ERSS Webhooks   │
│ (Class 0 Flash) │ │ (8 Dialects)   │ │ (110dB + Strobes) │ │ (NDMA Push)     │
└─────────────────┘ └────────────────┘ └───────────────────┘ └─────────────────┘
```

1. **Telecom Cell Broadcast (CB) / High-Priority SMS**:
   * Uses 93-character cell broadcast packets that override user silent settings (Class 0 Flash SMS).
   * Targets only cellular towers (BTS) physically located within the dynamic hazard runout polygon.
2. **Automated IVRS Voice Calls**:
   * Outbound auto-dialer scripts dispatched to registered village headmen (*Gaon Burhas*), local panchayat pradhans, school principals, and ASHA healthcare workers.
   * Synthesized in the dominant local dialect.
3. **IoT Physical Sirens & Highway Barriers**:
   * Sends binary relay switching packets to solar-powered roadside control boxes.
   * Activates **110 dB hooters**, red emergency strobes, and automatically lowers highway barrier gates (e.g. NH-10 Ranipool or NH-27 Haflong) to block vehicles before debris hits.
4. **State Emergency Operations Centre (SEOC) & 112 ERSS Webhooks**:
   * Pushes full CAP JSON/XML alerts to district magistrates, SDRF battalions, and Border Roads Organisation (BRO) control rooms.

---

## 3. Multilingual Support across all 8 NER States

Module 3 includes native pre-cached disaster warning templates for:
* **Assamese (`as`)**: Brahmaputra and Barak valley corridors (NH-27, NH-37).
* **Bengali (`bn`)**: Barak valley, Tripura, and border communities.
* **Hindi (`hi`)**: National highway travelers, BRO personnel, and military convoys.
* **Nepali (`ne`)**: Widely spoken across Sikkim (Ranipool, Mangan) and North Bengal.
* **Mizo (`mz`)**: Aizawl and southern hill sectors.
* **Manipuri / Meitei (`mn`)**: Noney, Tupul, and Imphal valleys.
* **Khasi (`kha`)**: Meghalaya plateau and East Khasi Hills (Sohra, Mawdok).
* **English (`en`)**: Administrative and central disaster agency feeds.

---

## 4. Downstream Habitation & Shelter Matching

Rather than issuing vague alerts, Module 3 calculates the dynamic **runout threat radius** ($1.0\text{ km} \to 5.0\text{ km}$) using slope angle, pore water pressure, and rainfall:
* Identifies threatened downstream settlements (e.g., *Ranipool Bazaar*, *Lower Jatinga Village*).
* Calculates estimated population at risk.
* Directs citizens to the **nearest designated disaster relief shelter** (e.g., *Upper Martam School*, *Haflong Town Stadium*) with safe, non-riverbank evacuation routes.

---

## 5. REST API Endpoints (Port 5002)

Start the alert server:
```bash
python alert-engine/server.py
```

### Endpoints:
* **`GET /api/health`**: Health status and active alert count.
* **`GET /api/alerts/active`**: Lists all active regional CAP alerts.
* **`GET /api/alerts/xml?id=<alert_id>`**: Returns raw `application/xml` compliant with OASIS CAP v1.2 / ITU-T X.1303 for NDMA SACHET ingestion.
* **`POST /api/alerts/generate`**: Evaluates telemetry and generates CAP XML/JSON without broadcasting.
* **`POST /api/alerts/broadcast`**: Generates CAP alert and executes simulated 4-channel broadcast.

#### Example Broadcast Request:
```json
POST /api/alerts/broadcast
{
  "primary_language": "en",
  "telemetry": {
    "location_id": "NER-SIKK-01",
    "station_name": "Ranipool NH-10 (9th Mile)",
    "state": "Sikkim",
    "district": "East Sikkim",
    "latitude": 27.3389,
    "longitude": 88.6065,
    "lsi_score": 0.957,
    "factor_of_safety": 0.74,
    "pore_pressure_kpa": 52.0,
    "rainfall_mm": 95.0,
    "slope_angle_degrees": 43.0
  }
}
```

---

## 6. Verification & Automated Tests

Run the complete test suite (13/13 tests):
```bash
python alert-engine/test_alert_engine.py
```

Output:
```
Ran 13 tests in 0.011s
OK
```

Tests verify:
1. Template rendering across all 8 NER regional languages without unbound placeholders.
2. OASIS CAP v1.2 XML schema conformance (`urn:oasis:names:tc:emergency:cap:1.2`).
3. Haversine distance and dynamic runout threat radius calculations.
4. Downstream village matching and relief shelter pairing for all 8 NER states.
5. Parallel execution of all 4 dissemination channels under 100 ms.
