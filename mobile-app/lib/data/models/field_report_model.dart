import '../../domain/models/field_report.dart';

class FieldReportModel {
  static Map<String, dynamic> toJson(FieldReport report) {
    return {
      'client_id': report.clientId,
      'reporter_name': report.reporterName,
      'reporter_role': report.reporterRole,
      'reporter_phone': report.reporterPhone,
      'hazard_type': report.hazardType,
      'severity': report.severity.name.toUpperCase(),
      'state': report.state,
      'district': report.district,
      'latitude': report.latitude,
      'longitude': report.longitude,
      'location_description': report.locationDescription,
      'tension_crack_width_cm': report.tensionCrackWidthCm,
      'road_status': _formatRoadStatus(report.roadStatus),
      'image_url': report.imageBase64 != null ? 'data:image/jpeg;base64,${report.imageBase64}' : null,
      'notes': report.notes,
      'language': report.language,
      'local_created_at': report.localCreatedAt.toIso8601String(),
    };
  }

  static FieldReport fromJson(Map<String, dynamic> json) {
    return FieldReport(
      clientId: json['client_id'] as String,
      reporterName: json['reporter_name'] as String? ?? 'Ground Scout',
      reporterRole: json['reporter_role'] as String? ?? 'Ground Scout',
      reporterPhone: json['reporter_phone'] as String? ?? '',
      hazardType: json['hazard_type'] as String? ?? 'Tension Crack',
      severity: _parseSeverity(json['severity'] as String?),
      state: json['state'] as String? ?? 'Sikkim',
      district: json['district'] as String? ?? 'East Sikkim',
      latitude: (json['latitude'] as num).toDouble(),
      longitude: (json['longitude'] as num).toDouble(),
      locationDescription: json['location_description'] as String? ?? '',
      tensionCrackWidthCm: (json['tension_crack_width_cm'] as num?)?.toDouble() ?? 0.0,
      roadStatus: _parseRoadStatus(json['road_status'] as String?),
      imageBase64: json['image_url'] as String?,
      notes: json['notes'] as String? ?? '',
      language: json['language'] as String? ?? 'en',
      localCreatedAt: DateTime.tryParse(json['local_created_at'] as String? ?? '') ?? DateTime.now(),
      syncedAt: json['synced_at'] != null ? DateTime.tryParse(json['synced_at'] as String) : null,
      syncStatus: _parseSyncStatus(json['sync_status'] as String?),
    );
  }

  static Map<String, dynamic> toDatabaseMap(FieldReport report) {
    return {
      'client_id': report.clientId,
      'reporter_name': report.reporterName,
      'reporter_role': report.reporterRole,
      'reporter_phone': report.reporterPhone,
      'hazard_type': report.hazardType,
      'severity': report.severity.name.toUpperCase(),
      'state': report.state,
      'district': report.district,
      'latitude': report.latitude,
      'longitude': report.longitude,
      'location_description': report.locationDescription,
      'tension_crack_width_cm': report.tensionCrackWidthCm,
      'road_status': _formatRoadStatus(report.roadStatus),
      'image_base64': report.imageBase64,
      'notes': report.notes,
      'language': report.language,
      'local_created_at': report.localCreatedAt.millisecondsSinceEpoch,
      'synced_at': report.syncedAt?.millisecondsSinceEpoch,
      'sync_status': report.syncStatus.name.toUpperCase(),
    };
  }

  static FieldReport fromDatabaseMap(Map<String, dynamic> map) {
    return FieldReport(
      clientId: map['client_id'] as String,
      reporterName: map['reporter_name'] as String? ?? 'Ground Scout',
      reporterRole: map['reporter_role'] as String? ?? 'Ground Scout',
      reporterPhone: map['reporter_phone'] as String? ?? '',
      hazardType: map['hazard_type'] as String? ?? 'Tension Crack',
      severity: _parseSeverity(map['severity'] as String?),
      state: map['state'] as String? ?? 'Sikkim',
      district: map['district'] as String? ?? 'East Sikkim',
      latitude: (map['latitude'] as num).toDouble(),
      longitude: (map['longitude'] as num).toDouble(),
      locationDescription: map['location_description'] as String? ?? '',
      tensionCrackWidthCm: (map['tension_crack_width_cm'] as num?)?.toDouble() ?? 0.0,
      roadStatus: _parseRoadStatus(map['road_status'] as String?),
      imageBase64: map['image_base64'] as String?,
      notes: map['notes'] as String? ?? '',
      language: map['language'] as String? ?? 'en',
      localCreatedAt: DateTime.fromMillisecondsSinceEpoch(map['local_created_at'] as int),
      syncedAt: map['synced_at'] != null ? DateTime.fromMillisecondsSinceEpoch(map['synced_at'] as int) : null,
      syncStatus: _parseSyncStatus(map['sync_status'] as String?),
    );
  }

  static ReportSeverity _parseSeverity(String? val) {
    switch (val?.toUpperCase()) {
      case 'CRITICAL':
        return ReportSeverity.critical;
      case 'HIGH':
        return ReportSeverity.high;
      case 'MEDIUM':
        return ReportSeverity.medium;
      default:
        return ReportSeverity.low;
    }
  }

  static RoadStatus _parseRoadStatus(String? val) {
    switch (val?.toUpperCase()) {
      case 'COLLAPSED':
        return RoadStatus.collapsed;
      case 'BLOCKED':
        return RoadStatus.blocked;
      case 'SINGLE_LANE':
        return RoadStatus.singleLane;
      default:
        return RoadStatus.passable;
    }
  }

  static String _formatRoadStatus(RoadStatus status) {
    switch (status) {
      case RoadStatus.collapsed:
        return 'COLLAPSED';
      case RoadStatus.blocked:
        return 'BLOCKED';
      case RoadStatus.singleLane:
        return 'SINGLE_LANE';
      case RoadStatus.passable:
        return 'PASSABLE';
    }
  }

  static SyncStatus _parseSyncStatus(String? val) {
    switch (val?.toUpperCase()) {
      case 'SYNCED':
        return SyncStatus.synced;
      case 'FAILED':
        return SyncStatus.failed;
      default:
        return SyncStatus.pendingSync;
    }
  }
}
