class Waypoint {
  final String id;
  final String name;
  final double latitude;
  final double longitude;
  final double elevationM;

  const Waypoint({
    required this.id,
    required this.name,
    required this.latitude,
    required this.longitude,
    required this.elevationM,
  });
}

class EvacuationShelter {
  final String shelterId;
  final String name;
  final String location;
  final double latitude;
  final double longitude;
  final int capacity;
  final double elevationM;
  final double distanceKm;

  const EvacuationShelter({
    required this.shelterId,
    required this.name,
    required this.location,
    required this.latitude,
    required this.longitude,
    required this.capacity,
    required this.elevationM,
    required this.distanceKm,
  });
}

class EvacuationPath {
  final String routeId;
  final String origin;
  final String destination;
  final double totalDistanceKm;
  final int estimatedTravelMinutes;
  final bool isSafeBypass;
  final String avoidedHazardZone;
  final List<Waypoint> waypoints;
  final EvacuationShelter targetShelter;

  const EvacuationPath({
    required this.routeId,
    required this.origin,
    required this.destination,
    required this.totalDistanceKm,
    required this.estimatedTravelMinutes,
    required this.isSafeBypass,
    required this.avoidedHazardZone,
    required this.waypoints,
    required this.targetShelter,
  });
}
