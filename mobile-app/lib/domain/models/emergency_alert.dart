class EmergencyAlert {
  final String alertId;
  final String headline;
  final String description;
  final String instruction;
  final String severity; // ADVISORY, WARNING, EVACUATION
  final String urgency;
  final String areaDesc;
  final String language;
  final DateTime sentAt;
  final double? targetLatitude;
  final double? targetLongitude;

  const EmergencyAlert({
    required this.alertId,
    required this.headline,
    required this.description,
    required this.instruction,
    required this.severity,
    required this.urgency,
    required this.areaDesc,
    required this.language,
    required this.sentAt,
    this.targetLatitude,
    this.targetLongitude,
  });

  bool get isEvacuation => severity.toUpperCase() == 'EVACUATION' || severity.toUpperCase() == 'CRITICAL';
}
