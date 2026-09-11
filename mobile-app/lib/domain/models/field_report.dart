enum ReportSeverity { low, medium, high, critical }
enum RoadStatus { passable, singleLane, blocked, collapsed }
enum SyncStatus { pendingSync, synced, failed }

class FieldReport {
  final String clientId; // UUIDv4
  final String reporterName;
  final String reporterRole;
  final String reporterPhone;
  final String hazardType;
  final ReportSeverity severity;
  final String state;
  final String district;
  final double latitude;
  final double longitude;
  final String locationDescription;
  final double tensionCrackWidthCm;
  final RoadStatus roadStatus;
  final String? imageBase64;
  final String notes;
  final String language;
  final DateTime localCreatedAt;
  final DateTime? syncedAt;
  final SyncStatus syncStatus;

  const FieldReport({
    required this.clientId,
    required this.reporterName,
    this.reporterRole = 'Ground Scout',
    this.reporterPhone = '',
    required this.hazardType,
    required this.severity,
    required this.state,
    required this.district,
    required this.latitude,
    required this.longitude,
    required this.locationDescription,
    this.tensionCrackWidthCm = 0.0,
    this.roadStatus = RoadStatus.passable,
    this.imageBase64,
    this.notes = '',
    this.language = 'en',
    required this.localCreatedAt,
    this.syncedAt,
    this.syncStatus = SyncStatus.pendingSync,
  });

  FieldReport copyWith({
    String? clientId,
    String? reporterName,
    String? reporterRole,
    String? reporterPhone,
    String? hazardType,
    ReportSeverity? severity,
    String? state,
    String? district,
    double? latitude,
    double? longitude,
    String? locationDescription,
    double? tensionCrackWidthCm,
    RoadStatus? roadStatus,
    String? imageBase64,
    String? notes,
    String? language,
    DateTime? localCreatedAt,
    DateTime? syncedAt,
    SyncStatus? syncStatus,
  }) {
    return FieldReport(
      clientId: clientId ?? this.clientId,
      reporterName: reporterName ?? this.reporterName,
      reporterRole: reporterRole ?? this.reporterRole,
      reporterPhone: reporterPhone ?? this.reporterPhone,
      hazardType: hazardType ?? this.hazardType,
      severity: severity ?? this.severity,
      state: state ?? this.state,
      district: district ?? this.district,
      latitude: latitude ?? this.latitude,
      longitude: longitude ?? this.longitude,
      locationDescription: locationDescription ?? this.locationDescription,
      tensionCrackWidthCm: tensionCrackWidthCm ?? this.tensionCrackWidthCm,
      roadStatus: roadStatus ?? this.roadStatus,
      imageBase64: imageBase64 ?? this.imageBase64,
      notes: notes ?? this.notes,
      language: language ?? this.language,
      localCreatedAt: localCreatedAt ?? this.localCreatedAt,
      syncedAt: syncedAt ?? this.syncedAt,
      syncStatus: syncStatus ?? this.syncStatus,
    );
  }
}
