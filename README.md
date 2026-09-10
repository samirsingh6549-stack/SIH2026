# NER Landslide Risk Monitor & Offline Sync Platform
### Smart India Hackathon (SIH 2026)
**Module 6: Cloud-Based Architecture with Offline Sync Support for Remote Regions**

---

## Overview
During severe monsoons in the **North Eastern Region (NER)** of India (Meghalaya, Sikkim, Mizoram, Arunachal Pradesh, Assam, Nagaland, Manipur, Tripura), landslides frequently snap power lines and knock out cellular towers. Disaster response teams, civil defense scouts, and citizens are often trapped in zero-connectivity dead zones.

This platform provides the **Cloud Architecture & Offline-First Sync Backbone** that connects all system components:
1. **Cloud Geospatial Database (PostgreSQL + PostGIS)**: Ready for free deployment on Supabase.
2. **Offline-First Client Sync Engine**: Local IndexedDB queuing with background auto-sync and conflict resolution.
3. **PWA Service Worker**: Instant app loading and offline caching even with no cellular reception.
4. **Zero-Hardware Telemetry Simulator**: Ingests live weather from Open-Meteo's free API and simulates slope stability sensors (tiltmeter, pore water pressure).
5. **Team Integration Contracts**: Clean REST/JSON specifications for GIS, ML, and Alert teammates.

---

## Directory Structure
```
ner-landslide-cloud-sync/
├── database/
│   └── schema.sql                # PostgreSQL + PostGIS schema with seed data
├── server/
│   └── mock_backend.js           # Zero-dependency cloud sync gateway & static server
├── client/
│   ├── public/
│   │   ├── index.html            # Interactive disaster management dashboard & field report UI
│   │   ├── app.css               # Modern dark-theme responsive styling
│   │   ├── sw.js                 # PWA Service Worker (Cache-first + Background Sync)
│   │   └── manifest.json         # PWA installation manifest
│   └── src/
│       ├── db.js                 # Client-side IndexedDB persistence layer
│       ├── syncManager.js        # Two-way sync engine, retry logic, network monitor
│       └── app.js                # UI controller & network simulation switcher
├── simulator/
│   └── telemetry_simulator.py    # Zero-hardware live weather & slope sensor simulator
├── docs/
│   └── INTEGRATION_CONTRACTS.md  # Detailed API contracts for the other 5 modules
├── tests/
│   └── test_sync.js              # Automated verification & idempotency test suite
└── package.json
```

---

## Quick Start (Zero External Dependencies)

### 1. Launch the Cloud Gateway & Web App
```bash
node server/mock_backend.js
```
Open your browser at: **`http://localhost:3000`**

### 2. Run the Automated Verification Test Suite
In another terminal:
```bash
node tests/test_sync.js
```

### 3. Run the Zero-Hardware Weather & Sensor Simulator
In another terminal:
```bash
python simulator/telemetry_simulator.py
```
*(Optionally add `--once` for a single transmission cycle)*

---

## How to Demonstrate to SIH Judges (Live Presentation Flow)

1. **Open the Web Application** at `http://localhost:3000`.
2. **Simulate a Mountain Dead Zone**:
   * Turn ON the **"Dead Zone Sim"** toggle at the top right.
   * Notice the status switches to **`OFFLINE (Mountain Dead Zone)`**.
3. **Submit an Incident Report Offline**:
   * Select a hazard (e.g. *Tension Cracks on Upper Slope* or *Rockfall on NH-10 Ranipool*).
   * Click **Save & Queue Report**.
   * Notice the report is immediately committed to the **Local Outbox** with status **`PENDING SYNC`**.
   * Emphasize to the judges: **No data is lost**, and ground teams can continue logging incidents without cell signal.
4. **Demonstrate Downstream Offline Access**:
   * Show that previously cached risk zones and emergency evacuation orders are still readable in offline mode.
5. **Simulate Regaining Connectivity**:
   * Turn OFF the **"Dead Zone Sim"** toggle (switching back to Online).
   * Watch the sync engine automatically trigger in the background!
   * The pending report immediately transitions to **`SYNCED TO CLOUD`** with green status badges!
