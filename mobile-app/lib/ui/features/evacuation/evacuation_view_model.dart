import 'package:flutter/foundation.dart';
import '../../../data/repositories/evacuation_repository.dart';
import '../../../data/services/gps_service.dart';
import '../../../domain/models/evacuation_path.dart';

class EvacuationViewModel extends ChangeNotifier {
  final EvacuationRepository _evacRepo;
  final GpsService _gpsService;

  EvacuationViewModel({
    EvacuationRepository? evacRepo,
    GpsService? gpsService,
  })  : _evacRepo = evacRepo ?? EvacuationRepository(),
        _gpsService = gpsService ?? GpsService();

  bool _isLoading = false;
  bool get isLoading => _isLoading;

  EvacuationPath? _evacuationPath;
  EvacuationPath? get evacuationPath => _evacuationPath;

  GpsCoordinates? _currentGps;
  GpsCoordinates? get currentGps => _currentGps;

  Future<void> loadSafeRoute() async {
    _isLoading = true;
    notifyListeners();

    try {
      _currentGps = await _gpsService.getCurrentLocation();
      final gps = _currentGps ?? GpsService.defaultNerCoordinates;

      _evacuationPath = await _evacRepo.getEvacuationRoute(
        userLat: gps.latitude,
        userLon: gps.longitude,
        blockedHazardId: 'HAZARD_RANIPOOL_01',
      );
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
