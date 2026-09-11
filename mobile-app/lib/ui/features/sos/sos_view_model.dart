import 'dart:async';
import 'package:flutter/foundation.dart';
import '../../../data/services/gps_service.dart';
import '../../../data/services/api_client.dart';
import '../../../data/services/audio_alarm_service.dart';

class SosViewModel extends ChangeNotifier {
  final GpsService _gpsService;
  final ApiClient _apiClient;
  final AudioAlarmService _audioAlarm;

  SosViewModel({
    GpsService? gpsService,
    ApiClient? apiClient,
    AudioAlarmService? audioAlarm,
  })  : _gpsService = gpsService ?? GpsService(),
        _apiClient = apiClient ?? ApiClient(),
        _audioAlarm = audioAlarm ?? AudioAlarmService();

  bool _isDispatched = false;
  bool get isDispatched => _isDispatched;

  bool _isSirenActive = false;
  bool get isSirenActive => _isSirenActive;

  GpsCoordinates? _currentGps;
  GpsCoordinates? get currentGps => _currentGps;

  String? _smsPayload;
  String? get smsPayload => _smsPayload;

  Future<void> init() async {
    _currentGps = await _gpsService.getCurrentLocation();
    _generateSmsPayload();
    notifyListeners();
  }

  void _generateSmsPayload() {
    final lat = _currentGps?.latitude.toStringAsFixed(4) ?? '27.3250';
    final lon = _currentGps?.longitude.toStringAsFixed(4) ?? '88.6120';
    // Standard compact 93-char Indian ERSS 112 SMS payload
    _smsPayload = 'EMERGENCY SOS: Landslide trapped. Loc: $lat N, $lon E. Send SDRF/NDRF team immediately.';
  }

  Future<void> triggerEmergencyBeacon() async {
    _isDispatched = true;
    _isSirenActive = true;
    notifyListeners();

    // 1. Play high-decibel local emergency siren
    await _audioAlarm.playEmergencySiren();

    // 2. Dispatch network beacon to Module 3 Alert Engine if connectivity exists
    final gps = _currentGps ?? GpsService.defaultNerCoordinates;
    await _apiClient.dispatchSosBeacon(
      latitude: gps.latitude,
      longitude: gps.longitude,
      senderName: 'Citizen SOS',
      district: 'East Sikkim',
      dialect: 'en',
    );
  }

  Future<void> stopSiren() async {
    _isSirenActive = false;
    await _audioAlarm.stopSiren();
    notifyListeners();
  }

  @override
  void dispose() {
    _audioAlarm.dispose();
    super.dispose();
  }
}
