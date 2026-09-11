import 'package:flutter/foundation.dart';
import '../../../data/repositories/alert_repository.dart';
import '../../../domain/models/emergency_alert.dart';

class AlertsViewModel extends ChangeNotifier {
  final AlertRepository _alertRepo;

  AlertsViewModel({AlertRepository? alertRepo})
      : _alertRepo = alertRepo ?? AlertRepository();

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  List<EmergencyAlert> _alerts = [];
  List<EmergencyAlert> get alerts => _alerts;

  String _currentLanguage = 'en';
  String get currentLanguage => _currentLanguage;

  Future<void> loadAlerts({String language = 'en'}) async {
    _isLoading = true;
    _currentLanguage = language;
    notifyListeners();

    try {
      _alerts = await _alertRepo.getAlerts(language: language);
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  void switchLanguage(String code) {
    loadAlerts(language: code);
  }
}
