import '../../domain/models/emergency_alert.dart';
import '../services/api_client.dart';

class AlertRepository {
  final ApiClient _apiClient;
  List<EmergencyAlert> _cachedAlerts = [];

  AlertRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  // Returns live alerts if online, or cached/pre-loaded alerts if offline
  Future<List<EmergencyAlert>> getAlerts({String language = 'en'}) async {
    final live = await _apiClient.fetchActiveAlerts(language: language);
    if (live.isNotEmpty) {
      _cachedAlerts = live;
      return live;
    }

    if (_cachedAlerts.isNotEmpty) {
      return _cachedAlerts;
    }

    // Default pre-cached emergency advisory for NER mountainous highways
    return [
      EmergencyAlert(
        alertId: 'NER_OFFLINE_ADVISORY_01',
        headline: 'Monsoon Saturation Advisory: NH-10 & NH-29',
        description: 'Continuous 72h antecedent rainfall exceeding 140mm across Sikkim and Assam foothills.',
        instruction: 'Commercial heavy vehicles restricted on cut-slopes. Monitor tension cracks along road shoulders.',
        severity: 'WARNING',
        urgency: 'Expected',
        areaDesc: 'East Sikkim, Dima Hasao, Noney sectors',
        language: language,
        sentAt: DateTime.now().subtract(const Duration(hours: 2)),
      ),
    ];
  }
}
