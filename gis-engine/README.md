# Module 4: Central GIS Command Center & Dynamic Evacuation Router
### Smart India Hackathon (SIH 2026)
**Dynamic A\* / Dijkstra Spatial Pathfinding & Official SITREP Reporting**

---

## 1. Overview
During severe monsoons, landslides do not just threaten homes—they **sever strategic national lifelines** (such as NH-10 in Sikkim, NH-27 in Dima Hasao Assam, and NH-29 in Nagaland), cutting off entire districts, trapping ambulances, and trapping evacuating citizens in hazardous valley bottoms.

**Module 4** provides the geospatial command brain of the system:
1. **8-State Topological Road Graph**: Models critical mountain highway segments, bridges, valley bottoms, and high-altitude ridge bypasses.
2. **Hazard-Aware Evacuation Router**: Uses Dijkstra / A* pathfinding to calculate the shortest safe egress route to designated relief shelters while dynamically detouring around active landslide hazard buffers.
3. **Administrative SITREP Generator**: Automatically produces formal Disaster Situation Reports (SITREP) for District Magistrates, State Disaster Management Authorities (SDMA), and NDRF Battalion Commanders.
4. **GeoJSON Visualization Layer**: Outputs standardized RFC 7946 GeoJSON FeatureCollections for Leaflet, Mapbox, and OpenStreetMap rendering.

---

## 2. Dynamic Safe Evacuation Pathfinding Workflow

```
                        ┌──────────────────────────────┐
                        │   Module 1 LSI / Physics &   │
                        │     Module 3 CAP Trigger     │
                        └──────────────┬───────────────┘
                                       │
                                       ▼
                        ┌──────────────────────────────┐
                        │ Dynamic Hazard Interdiction  │
                        │ (Point-to-Segment Projection)│
                        └──────────────┬───────────────┘
                                       │ Compares road segment distance
                                       │ against hazard threat radius (R)
                                       ▼
                 ┌───────────────────────────────────────────┐
                 │ Compromised Roads Marked BLOCKED_LANDSLIDE│
                 │     (Traversal cost set to INFINITE)      │
                 └─────────────────────┬─────────────────────┘
                                       │
                                       ▼
                 ┌───────────────────────────────────────────┐
                 │ Dijkstra Priority-Queue Pathfinding Engine│
                 │   (Explores safe mountain ridge bypasses) │
                 └─────────────────────┬─────────────────────┘
                                       │
                                       ▼
        ┌─────────────────────────────────────────────────────────────┐
        │                 Safe Evacuation Polyline                    │
        │  • Total Safe Distance (km) & Traversal Time (minutes)      │
        │  • Turn-by-Turn Navigation (avoiding active debris flows)   │
        │  • Destination Relief Shelter & Matched Safe Route GeoJSON  │
        └─────────────────────────────────────────────────────────────┘
```

---

## 3. 8-State Lifeline Highway Coverage

* **Sikkim**: NH-10 (Singtam $\to$ 32nd Mile $\to$ Ranipool $\to$ Gangtok) and the **Upper Martam Ridge Bypass** (safe high-crest bypass).
* **Assam**: NH-27 (Mahur $\to$ Jatinga Valley cutting $\to$ Haflong Town Stadium) and the **Circuit House Ridge Bypass**.
* **Manipur**: NH-37 (Jiribam $\to$ Tupul Railway yard $\to$ Noney District Headquarters) and the **Longmai Mountain Spur**.
* **Meghalaya**: SH-5 (Shillong $\to$ Mawkdok Bridge $\to$ Dympep Canyon $\to$ Sohra Relief Shelter) and the **Laitryngew Plateau Bypass**.
* **Nagaland**: NH-29 (Dimapur $\to$ Sechu Zubza $\to$ Dzüdza River Bridge $\to$ Kohima South Stadium) and the **Khonoma Heritage Bypass**.
* **Arunachal Pradesh**: NH-13 (Bhalukpong $\to$ Dirang Civil Defense Base $\to$ Sela Alpine Pass $\to$ Tawang Monastery).
* **Mizoram**: Aizawl Ridge Spine (Chite Veng $\to$ Hunthar Sinking Zone $\to$ Vanapa Hall Disaster Sanctuary) and the **Durtlang Ridge Bypass**.
* **Tripura**: NH-8 Jampui Hills (Kanchanpur Degree College Shelter $\to$ Vanghmun YMA Relief Hub $\to$ Phuldungsei Crest).

---

## 4. Administrative Situation Report (SITREP)

Module 4 compiles active alerts and road closures into an official **Daily Situation Report (SITREP)** for disaster administration:

### Sample SITREP Summary:
```
========================================================================
  SITUATION REPORT (SITREP): SITREP-NER-20260910-1456
  NER-LEWS Central Command Centre (Ministry of Earth Sciences / NDMA)
  Issued: 10-Sep-2026 14:56:00 IST | Status: CRITICAL / CODE_RED
========================================================================

1. EXECUTIVE OVERVIEW:
   • Active Landslide Hazard Points:   1
   • Closed Highway Corridors:          1 (3.4 km blocked)
   • Active Relief Shelters:            8 (Total Capacity: 8800 evacuees)

2. INTERDICTED HIGHWAY CORRIDORS (BLOCKED):
   [!] NH-10 Ranipool Sector (3.4 km)
       Reason: Mudslide 2m deep over Ranipool roadway
       Action: Border Roads Organisation (BRO) / NHIDCL deploying Excavator (20T) + Wheel Loader

3. ACTIONABLE DIRECTIVES FOR DISTRICT MAGISTRATES & NDRF:
   1. BRO Project Swastik: Deploy earthmovers immediately to clear primary lifeline bypasses.
   2. SDRF / NDRF 1st Battalion (Guwahati): Position swift water rescue teams.
   3. District Transport Authorities: Impose strict traffic stoppage at Singtam checkpoint.
   4. District Medical Officers: Activate mobile health units at Upper Martam School.
========================================================================
```

---

## 5. REST API Endpoints (Port 5003)

Launch the GIS command server:
```bash
python gis-engine/server.py
```

### Endpoints:
* **`GET /api/health`**: Health status, nodes/edges count, and active hazard count.
* **`GET /api/network/corridors`**: Returns full 8-state road network as GeoJSON FeatureCollection.
* **`GET /api/sitrep?format=json|text`**: Returns live SITREP briefing document.
* **`POST /api/routes/evacuate`**: Computes shortest safe route from start GPS coordinate to shelter avoiding active hazards.
* **`POST /api/network/block_segment`**: Interdicts a specific road segment.
* **`POST /api/network/reset`**: Resets all roads back to open status.

#### Example Evacuation Route Request:
```json
POST /api/routes/evacuate
{
  "start_node_id": "SKM_32MILE",
  "target_shelter_id": "SKM_UPPER_MARTAM_SHELTER",
  "hazards": [
    {
      "lat": 27.3050,
      "lng": 88.5880,
      "threat_radius_km": 1.8,
      "label": "Ranipool Active Mudslide"
    }
  ]
}
```

---

## 6. Verification & Automated Tests

Run the complete test suite (11/11 tests):
```bash
python gis-engine/test_gis_engine.py
```

Output:
```
Ran 11 tests in 0.005s
OK
```

Tests verify:
1. Complete 8-state road network topology and shelter capacity validation.
2. Point-to-segment perpendicular distance algorithm.
3. Baseline shortest path routing under clear conditions.
4. Dynamic hazard avoidance rerouting: Algorithm cleanly avoids Ranipool debris flow and discovers the Upper Martam Western Crest bypass.
5. Turn-by-turn evacuation navigation cues.
6. GeoJSON compliance for Leaflet rendering.
7. SITREP compilation and directive generation.
