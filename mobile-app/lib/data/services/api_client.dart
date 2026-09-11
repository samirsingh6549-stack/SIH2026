import 'dart:async';
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/constants/api_endpoints.dart';
import '../../domain/models/field_report.dart';
import '../../domain/models/emergency_alert.dart';
import '../../domain/models/evacuation_path.dart';
import '../models/field_report_model.dart';
import '../models/alert_model.dart';
import '../models/evacuation_route_model.dart';

class ApiClient {
  final http.Client _client;
  static const Duration _timeout = Duration(seconds: 5);

  ApiClient({http.Client? client}) : _client = client ?? http.Client();

  // Check if Cloud Gateway is reachable
  Future<bool> checkConnectivity() async {
    try {
      final res = await _client.get(Uri.parse(ApiEndpoints.healthCheck)).timeout(_timeout);
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  // Module 0: Push queued outbox reports to Cloud Sync Gateway in an atomic batch
  Future<List<String>> syncBatchReports(List<FieldReport> reports) async {
    if (reports.isEmpty) return [];

    final payload = {
      'batch_size': reports.length,
      'timestamp': DateTime.now().toIso8601String(),
      'reports': reports.map((r) => FieldReportModel.toJson(r)).toList(),
    };

    try {
      final res = await _client.post(
        Uri.parse(ApiEndpoints.syncBatch),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload),
      ).timeout(_timeout);

      if (res.statusCode == 200 || res.statusCode == 201) {
        final data = jsonDecode(res.body) as Map<String, dynamic>;
        final syncedIds = (data['synced_ids'] as List<dynamic>?)
            ?.map((e) => e.toString())
            .toList();
        return syncedIds ?? reports.map((r) => r.clientId).toList();
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  // Module 3: Fetch active emergency alerts
  Future<List<EmergencyAlert>> fetchActiveAlerts({String language = 'en'}) async {
    try {
      final res = await _client.get(
        Uri.parse('${ApiEndpoints.activeAlerts}?lang=$language'),
      ).timeout(_timeout);

      if (res.statusCode == 200) {
        final data = jsonDecode(res.body);
        final List<dynamic> list = data is List ? data : (data['alerts'] as List<dynamic>? ?? []);
        return list.map((item) => AlertModel.fromJson(item as Map<String, dynamic>)).toList();
      }
      return [];
    } catch (_) {
      return [];
    }
  }

  // Module 3: Dispatch Emergency SOS beacon
  Future<bool> dispatchSosBeacon({
    required double latitude,
    required double longitude,
    required String senderName,
    required String district,
    required String dialect,
  }) async {
    final payload = {
      'sos_id': 'SOS_${DateTime.now().millisecondsSinceEpoch}',
      'sender_name': senderName,
      'district': district,
      'latitude': latitude,
      'longitude': longitude,
      'language': dialect,
      'timestamp': DateTime.now().toIso8601String(),
      'emergency_type': 'LANDSLIDE_TRAPPED',
    };

    try {
      final res = await _client.post(
        Uri.parse(ApiEndpoints.triggerSos),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(payload),
      ).timeout(_timeout);
      return res.statusCode == 200 || res.statusCode == 201;
    } catch (_) {
      // Return false so UI triggers native SMS/2G fallback
      return false;
    }
  }

  // Module 4: Fetch safe dynamic evacuation route around active landslide debris
  Future<EvacuationPath?> fetchEvacuationRoute({
    required double userLat,
    required double userLon,
    String? blockedHazardId,
  }) async {
    final uri = Uri.parse(ApiEndpoints.evacuationRoute).replace(
      queryParameters: {
        'lat': userLat.toString(),
        'lon': userLon.toString(),
        if (blockedHazardId != null) 'avoid_hazard': blockedHazardId,
      },
    );

    try {
      final res = await _client.get(uri).timeout(_timeout);
      if (res.statusCode == 200) {
        final data = jsonDecode(res.body) as Map<String, dynamic>;
        return EvacuationRouteModel.fromJson(data);
      }
      return null;
    } catch (_) {
      return null;
    }
  }
}
