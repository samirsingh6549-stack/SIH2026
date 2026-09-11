import 'package:geolocator/geolocator.dart';

class GpsCoordinates {
  final double latitude;
  final double longitude;
  final double altitude;
  final double accuracy;
  final bool isMockOrCached;

  const GpsCoordinates({
    required this.latitude,
    required this.longitude,
    this.altitude = 1450.0,
    this.accuracy = 5.0,
    this.isMockOrCached = false,
  });
}

class GpsService {
  // Default NER fallback: Gangtok NH-10 corridor
  static const GpsCoordinates defaultNerCoordinates = GpsCoordinates(
    latitude: 27.3250,
    longitude: 88.6120,
    altitude: 1650.0,
    accuracy: 10.0,
    isMockOrCached: true,
  );

  static GpsCoordinates? _cachedLastKnown;

  Future<GpsCoordinates> getCurrentLocation() async {
    try {
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        return _cachedLastKnown ?? defaultNerCoordinates;
      }

      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          return _cachedLastKnown ?? defaultNerCoordinates;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        return _cachedLastKnown ?? defaultNerCoordinates;
      }

      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 4),
      );

      final coords = GpsCoordinates(
        latitude: position.latitude,
        longitude: position.longitude,
        altitude: position.altitude,
        accuracy: position.accuracy,
        isMockOrCached: false,
      );

      _cachedLastKnown = coords;
      return coords;
    } catch (_) {
      return _cachedLastKnown ?? defaultNerCoordinates;
    }
  }
}
