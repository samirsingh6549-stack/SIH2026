import 'package:flutter/foundation.dart';
import 'package:uuid/uuid.dart';
import '../../../data/repositories/field_report_repository.dart';
import '../../../data/services/gps_service.dart';
import '../../../domain/models/field_report.dart';

class NewReportViewModel extends ChangeNotifier {
  final FieldReportRepository _reportRepo;
  final GpsService _gpsService;

  NewReportViewModel({
    FieldReportRepository? reportRepo,
    GpsService? gpsService,
  })  : _reportRepo = reportRepo ?? FieldReportRepository(),
        _gpsService = gpsService ?? GpsService();

  bool _isSaving = false;
  bool get isSaving => _isSaving;

  GpsCoordinates? _currentGps;
  GpsCoordinates? get currentGps => _currentGps;

  ReportSeverity _severity = ReportSeverity.medium;
  ReportSeverity get severity => _severity;

  RoadStatus _roadStatus = RoadStatus.passable;
  RoadStatus get roadStatus => _roadStatus;

  double _crackWidthCm = 2.5;
  double get crackWidthCm => _crackWidthCm;

  void setSeverity(ReportSeverity val) {
    _severity = val;
    notifyListeners();
  }

  void setRoadStatus(RoadStatus val) {
    _roadStatus = val;
    notifyListeners();
  }

  void setCrackWidth(double val) {
    _crackWidthCm = val;
    notifyListeners();
  }

  Future<void> initLocation() async {
    _currentGps = await _gpsService.getCurrentLocation();
    notifyListeners();
  }

  Future<bool> submitReport({
    required String reporterName,
    required String reporterPhone,
    required String hazardType,
    required String state,
    required String district,
    required String locationDescription,
    required String notes,
    String? imageBase64,
  }) async {
    _isSaving = true;
    notifyListeners();

    try {
      final gps = _currentGps ?? GpsService.defaultNerCoordinates;
      final clientId = const Uuid().v4();

      final report = FieldReport(
        clientId: clientId,
        reporterName: reporterName.trim().isEmpty ? 'Ground Scout' : reporterName.trim(),
        reporterRole: 'Field Scout',
        reporterPhone: reporterPhone.trim(),
        hazardType: hazardType,
        severity: _severity,
        state: state,
        district: district,
        latitude: gps.latitude,
        longitude: gps.longitude,
        locationDescription: locationDescription.trim(),
        tensionCrackWidthCm: _crackWidthCm,
        roadStatus: _roadStatus,
        imageBase64: imageBase64,
        notes: notes.trim(),
        language: 'en',
        localCreatedAt: DateTime.now(),
        syncStatus: SyncStatus.pendingSync,
      );

      // Saves locally to SQLite first, then attempts background sync
      await _reportRepo.submitReport(report);
      return true;
    } catch (_) {
      return false;
    } finally {
      _isSaving = false;
      notifyListeners();
    }
  }
}
