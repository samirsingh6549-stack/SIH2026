# Module 5: Ground Truth Scout & Citizen Mobile Application (Flutter)

An offline-first, physics-guided mobile application for ground scouts, disaster response teams (SDRF/NDRF), and citizens across the 8 North Eastern Region (NER) states.

---

## 📱 Core Capabilities

1. **Zero-Network Offline Outbox (Module 0 Integration)**:
   - Ground scouts in deep Himalayan gorges can measure tension cracks, soil displacement, and road blockages completely offline.
   - Observations are persisted in an on-device encrypted **SQLite database** (`sqflite`) with cryptographic **UUIDv4** idempotency keys.
   - When 2G, base-camp Wi-Fi, or mesh connectivity is detected, the outbox automatically synchronizes in an atomic batch with the Cloud Sync Gateway (`POST /api/field_reports/batch`).

2. **One-Tap Emergency Distress SOS (Module 3 Integration)**:
   - Acquires direct satellite GPS coordinates (no cellular data required).
   - Generates compact **93-character SMS beacons** formatted for India's National Emergency Response System (**ERSS 112**).
   - Sounds a loud 110 dB siren on device hardware.

3. **Safe Dynamic Evacuation Navigator (Module 4 Integration)**:
   - Displays pre-cached lifeline highway graphs (e.g. Sikkim NH-10).
   - Dynamically avoids active landslide debris runouts (e.g. Ranipool debris zone) and guides users through ridge bypasses (e.g. Upper Martam Western Crest) to designated high-ground relief shelters.

4. **Multilingual Disaster Advisories (OASIS CAP v1.2)**:
   - Real-time emergency alerts translated across **8 North Eastern languages**:
     * Assamese (`as`)
     * Bengali (`bn`)
     * Nepali (`ne`)
     * Mizo (`mz`)
     * Manipuri (`mn`)
     * Khasi (`kha`)
     * Hindi (`hi`)
     * English (`en`)

---

## 🏛️ Clean Layered Architecture (MVVM)

```
lib/
├── main.dart                       # App entrypoint and Provider registration
├── core/
│   ├── constants/                  # Colors, tactical themes, microservice endpoints
│   ├── theme/                      # Glassmorphism dark mode for tactical command
│   └── i18n/                       # 8-Dialect translation dictionaries
├── domain/
│   └── models/                     # Clean immutable entities (FieldReport, EmergencyAlert, EvacuationPath)
├── data/
│   ├── models/                     # DTOs with JSON & SQLite serializers
│   ├── services/                   # SQLite database helper, HTTP API client, GPS service, Audio siren
│   └── repositories/               # Single-source-of-truth repositories for offline outbox & routing
└── ui/
    ├── shared_widgets/             # Offline sync banner, status badges, custom buttons
    └── features/
        ├── home/                   # Main tactical HUD & GPS telemetry
        ├── report/                 # Field hazard observation form
        ├── sos/                    # Emergency panic trigger & 112 SMS beacon
        ├── evacuation/             # Safe bypass pathfinder & shelter guidance
        └── alerts/                 # OASIS CAP v1.2 alert feed with dialect switcher
```

---

## 🚀 How to Run & Build

### Prerequisites
1. Install [Flutter SDK](https://docs.flutter.dev/get-started/install) (`>= 3.0.0`).
2. Verify installation:
   ```bash
   flutter doctor
   ```

### 1. Install Dependencies
```bash
cd mobile-app
flutter pub get
```

### 2. Run in Debug Mode (Emulator or Physical Device)
```bash
flutter run
```

### 3. Build Production Android APK
```bash
flutter build apk --release
```
The compiled APK will be generated at:
`build/app/outputs/flutter-apk/app-release.apk`
