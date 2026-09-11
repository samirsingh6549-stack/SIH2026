import 'package:flutter_test/flutter_test.dart';
import '../lib/core/i18n/dialect_translations.dart';
import '../lib/domain/models/field_report.dart';
import '../lib/domain/models/emergency_alert.dart';
import '../lib/data/models/field_report_model.dart';
import '../lib/data/models/alert_model.dart';
import '../lib/data/models/evacuation_route_model.dart';

void main() {
  group('Suite 1: FieldReport Serialization & Offline Outbox Mapping', () {
    test('should serialize FieldReport to JSON conforming to Module 0 Cloud Gateway schema', () {
      final now = DateTime.now();
      final report = FieldReport(
        clientId: 'test-uuid-1234',
        reporterName: 'Tashi Dorjee',
        reporterRole: 'Ground Scout',
        hazardType: 'Tension Crack',
        severity: ReportSeverity.high,
        state: 'Sikkim',
        district: 'East Sikkim',
        latitude: 27.3250,
        longitude: 88.6120,
        locationDescription: 'NH-10 km 22 Ranipool',
        tensionCrackWidthCm: 14.5,
        roadStatus: RoadStatus.blocked,
        notes: 'Accelerating slope deformation',
        localCreatedAt: now,
      );

      final json = FieldReportModel.toJson(report);

      expect(json['client_id'], equals('test-uuid-1234'));
      expect(json['reporter_name'], equals('Tashi Dorjee'));
      expect(json['severity'], equals('HIGH'));
      expect(json['road_status'], equals('BLOCKED'));
      expect(json['tension_crack_width_cm'], equals(14.5));
      expect(json['latitude'], equals(27.3250));
      expect(json['longitude'], equals(88.6120));
      expect(json['local_created_at'], equals(now.toIso8601String()));
    });

    test('should serialize and deserialize to SQLite database map without data loss', () {
      final now = DateTime.now();
      final original = FieldReport(
        clientId: 'db-uuid-5678',
        reporterName: 'Lian Mizo',
        reporterRole: 'Field Scout',
        hazardType: 'Debris Flow',
        severity: ReportSeverity.critical,
        state: 'Mizoram',
        district: 'Aizawl',
        latitude: 23.7307,
        longitude: 92.7173,
        locationDescription: 'Melthum Sinking Zone',
        tensionCrackWidthCm: 28.0,
        roadStatus: RoadStatus.collapsed,
        notes: 'Water main burst on cut slope',
        localCreatedAt: now,
        syncStatus: SyncStatus.pendingSync,
      );

      final dbMap = FieldReportModel.toDatabaseMap(original);
      expect(dbMap['sync_status'], equals('PENDINGSYNC')); // Or enum name

      final restored = FieldReportModel.fromDatabaseMap(dbMap);
      expect(restored.clientId, equals(original.clientId));
      expect(restored.state, equals('Mizoram'));
      expect(restored.district, equals('Aizawl'));
      expect(restored.severity, equals(ReportSeverity.critical));
      expect(restored.roadStatus, equals(RoadStatus.collapsed));
    });
  });

  group('Suite 2: OASIS CAP Alert Model Parsing', () {
    test('should parse CAP v1.2 JSON alert payload', () {
      final json = {
        'alert_id': 'CAP_SKM_2026_01',
        'headline': 'Flash Flood & Landslide Warning: Teesta River Basin',
        'description': 'High discharge and debris movement detected at Dikchu.',
        'instruction': 'Evacuate riverbank settlements immediately.',
        'severity': 'EVACUATION',
        'urgency': 'Immediate',
        'area_desc': 'East & North Sikkim',
        'language': 'en',
        'sent_at': '2026-09-11T05:00:00Z',
      };

      final alert = AlertModel.fromJson(json);

      expect(alert.alertId, equals('CAP_SKM_2026_01'));
      expect(alert.severity, equals('EVACUATION'));
      expect(alert.isEvacuation, isTrue);
      expect(alert.urgency, equals('Immediate'));
    });
  });

  group('Suite 3: Module 4 Evacuation Path & Safe Bypass Model', () {
    test('should parse dynamic evacuation route with safe bypass verification', () {
      final json = {
        'route_id': 'BYPASS_MARTAM_01',
        'origin': 'Ranipool Junction',
        'destination': 'Singtam High Ridge Stadium',
        'total_distance_km': 18.4,
        'estimated_travel_minutes': 38,
        'is_safe_bypass': true,
        'avoided_hazard_zone': 'Ranipool Debris Zone',
        'waypoints': [
          {'id': 'WP1', 'name': 'Ranipool North', 'latitude': 27.295, 'longitude': 88.585, 'elevation_m': 920.0},
          {'id': 'WP2', 'name': 'Upper Martam Crest', 'latitude': 27.325, 'longitude': 88.545, 'elevation_m': 1520.0},
        ],
        'target_shelter': {
          'shelter_id': 'SH_SINGTAM',
          'name': 'Singtam Civil Defense Camp',
          'location': 'Singtam Stadium',
          'latitude': 27.235,
          'longitude': 88.498,
          'capacity': 1200,
          'elevation_m': 820.0,
          'distance_km': 18.4,
        }
      };

      final route = EvacuationRouteModel.fromJson(json);

      expect(route.routeId, equals('BYPASS_MARTAM_01'));
      expect(route.isSafeBypass, isTrue);
      expect(route.waypoints.length, equals(2));
      expect(route.targetShelter.capacity, equals(1200));
      expect(route.avoidedHazardZone, contains('Ranipool'));
    });
  });

  group('Suite 4: 8-Dialect Multilingual String Resolution', () {
    test('should resolve urgent siren warnings across all 8 NER languages', () {
      final languages = ['en', 'hi', 'as', 'bn', 'ne', 'mz', 'mn', 'kha'];

      for (final code in languages) {
        final title = DialectTranslations.get('app_title', langCode: code);
        final siren = DialectTranslations.get('siren_warning', langCode: code);
        final offline = DialectTranslations.get('offline_mode', langCode: code);

        expect(title.isNotEmpty, isTrue, reason: 'Missing title for $code');
        expect(siren.isNotEmpty, isTrue, reason: 'Missing siren for $code');
        expect(offline.isNotEmpty, isTrue, reason: 'Missing offline status for $code');
      }
    });
  });
}
