import '../../domain/models/evacuation_path.dart';
import '../services/api_client.dart';

class EvacuationRepository {
  final ApiClient _apiClient;

  EvacuationRepository({ApiClient? apiClient}) : _apiClient = apiClient ?? ApiClient();

  // Fetches live dynamic evacuation route from Module 4, or serves pre-cached regional lifeline detour
  Future<EvacuationPath> getEvacuationRoute({
    required double userLat,
    required double userLon,
    String? blockedHazardId,
  }) async {
    // 1. Try fetching real-time calculation from GIS Engine
    final live = await _apiClient.fetchEvacuationRoute(
      userLat: userLat,
      userLon: userLon,
      blockedHazardId: blockedHazardId,
    );

    if (live != null) return live;

    // 2. Offline Pre-Cached Safe Bypass (Mirrors Module 4 GIS Road Graph)
    // When NH-10 Ranipool sector is blocked, detours via Upper Martam Western Crest
    return const EvacuationPath(
      routeId: 'ROUTE_SKM_MARTAM_SAFE_BYPASS',
      origin: 'Gangtok NH-10 Axis (27.3314 N, 88.6138 E)',
      destination: 'Singtam Community High Ground Relief Shelter',
      totalDistanceKm: 18.4,
      estimatedTravelMinutes: 38,
      isSafeBypass: true,
      avoidedHazardZone: 'Ranipool Active Debris Runout Zone (1.8km Buffer)',
      waypoints: [
        Waypoint(id: 'SKM_GTK', name: 'Gangtok Zero Point', latitude: 27.3314, longitude: 88.6138, elevationM: 1650.0),
        Waypoint(id: 'SKM_MARTAM_CREST', name: 'Upper Martam Western Crest (Safe Ridge)', latitude: 27.3250, longitude: 88.5450, elevationM: 1520.0),
        Waypoint(id: 'SKM_SINGTAM_NORTH', name: 'Singtam High Ground Relief Camp', latitude: 27.2350, longitude: 88.4980, elevationM: 820.0),
      ],
      targetShelter: EvacuationShelter(
        shelterId: 'SHELTER_SINGTAM_01',
        name: 'Singtam Senior Secondary School & Stadium',
        location: 'Singtam High Ridge Plateau',
        latitude: 27.2350,
        longitude: 88.4980,
        capacity: 1200,
        elevationM: 820.0,
        distanceKm: 18.4,
      ),
    );
  }
}
