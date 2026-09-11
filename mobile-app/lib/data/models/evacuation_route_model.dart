import '../../domain/models/evacuation_path.dart';

class EvacuationRouteModel {
  static EvacuationPath fromJson(Map<String, dynamic> json) {
    final routeData = json['route'] as Map<String, dynamic>? ?? json;

    final waypointsRaw = routeData['waypoints'] as List<dynamic>? ?? [];
    final waypoints = waypointsRaw.map((w) {
      final wm = w as Map<String, dynamic>;
      return Waypoint(
        id: wm['id'] as String? ?? '',
        name: wm['name'] as String? ?? 'Waypoint',
        latitude: (wm['latitude'] as num? ?? wm['lat'] as num? ?? 0.0).toDouble(),
        longitude: (wm['longitude'] as num? ?? wm['lon'] as num? ?? 0.0).toDouble(),
        elevationM: (wm['elevation_m'] as num? ?? 0.0).toDouble(),
      );
    }).toList();

    final shelterRaw = routeData['target_shelter'] as Map<String, dynamic>? ?? {};
    final shelter = EvacuationShelter(
      shelterId: shelterRaw['shelter_id'] as String? ?? 'SHELTER_DEFAULT',
      name: shelterRaw['name'] as String? ?? 'District Relief Camp',
      location: shelterRaw['location'] as String? ?? 'Highland Ridge Ground',
      latitude: (shelterRaw['latitude'] as num? ?? 27.32).toDouble(),
      longitude: (shelterRaw['longitude'] as num? ?? 88.61).toDouble(),
      capacity: (shelterRaw['capacity'] as num? ?? 500).toInt(),
      elevationM: (shelterRaw['elevation_m'] as num? ?? 1450.0).toDouble(),
      distanceKm: (shelterRaw['distance_km'] as num? ?? 4.2).toDouble(),
    );

    return EvacuationPath(
      routeId: routeData['route_id'] as String? ?? 'EVAC_${DateTime.now().millisecondsSinceEpoch}',
      origin: routeData['origin'] as String? ?? 'Current Location',
      destination: routeData['destination'] as String? ?? shelter.name,
      totalDistanceKm: (routeData['total_distance_km'] as num? ?? 5.5).toDouble(),
      estimatedTravelMinutes: (routeData['estimated_travel_minutes'] as num? ?? 18).toInt(),
      isSafeBypass: routeData['is_safe_bypass'] as bool? ?? true,
      avoidedHazardZone: routeData['avoided_hazard_zone'] as String? ?? 'None',
      waypoints: waypoints,
      targetShelter: shelter,
    );
  }
}
