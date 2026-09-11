import 'package:flutter/foundation.dart';
import '../../../data/repositories/field_report_repository.dart';
import '../../../data/repositories/alert_repository.dart';
import '../../../data/services/gps_service.dart';
import '../../../data/services/api_client.dart';
import '../../../domain/models/emergency_alert.dart';

class HomeViewModel extends ChangeNotifier {
  final FieldReportRepository _reportRepo;
  final AlertRepository _alertRepo;
  final GpsService _gpsService;
  final ApiClient _apiClient;

  HomeViewModel({
    FieldReportRepository? reportRepo,
    AlertRepository? alertRepo,
    GpsService? gpsService,
    ApiClient? apiClient,
  })  : _reportRepo = reportRepo ?? FieldReportRepository(),
        _alertRepo = alertRepo ?? AlertRepository(),
        _gpsService = gpsService ?? GpsService(),
        _apiClient = apiClient ?? ApiClient();

  bool _isOnline = false;
  bool get isOnline => _isOnline;

  int _pendingOutboxCount = 0;
  int get pendingOutboxCount => _pendingOutboxCount;

  bool _isSyncing = false;
  bool get isSyncing => _isSyncing;

  GpsCoordinates? _currentGps;
  GpsCoordinates? get currentGps => _currentGps;

  List<EmergencyAlert> _activeAlerts = [];
  List<EmergencyAlert> get activeAlerts => _activeAlerts;

  String _selectedLanguage = 'en';
  String get selectedLanguage => _selectedLanguage;

  void setLanguage(String langCode) {
    _selectedLanguage = langCode;
    notifyListeners();
  }

  Future<void> init() async {
    await refreshState();
  }

  Future<void> refreshState() async {
    // 1. Check network connectivity to Cloud Gateway
    _isOnline = await _apiClient.checkConnectivity();

    // 2. Query local SQLite outbox for pending report count
    _pendingOutboxCount = await _reportRepo.getPendingCount();

    // 3. Acquire satellite GPS coordinates
    _currentGps = await _gpsService.getCurrentLocation();

    // 4. Fetch alerts (live or cached fallback)
    _activeAlerts = await _alertRepo.getAlerts(language: _selectedLanguage);

    notifyListeners();
  }

  // Manually trigger outbox sync
  Future<void> triggerSync() async {
    if (_isSyncing) return;
    _isSyncing = true;
    notifyListeners();

    try {
      await _reportRepo.syncPendingReports();
      _pendingOutboxCount = await _reportRepo.getPendingCount();
      _isOnline = await _apiClient.checkConnectivity();
    } finally {
      _isSyncing = false;
      notifyListeners();
    }
  }
}
