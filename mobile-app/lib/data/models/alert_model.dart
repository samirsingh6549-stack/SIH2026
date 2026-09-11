import '../../domain/models/emergency_alert.dart';

class AlertModel {
  static EmergencyAlert fromJson(Map<String, dynamic> json) {
    return EmergencyAlert(
      alertId: json['alert_id'] as String? ?? json['identifier'] as String? ?? 'ALERT_${DateTime.now().millisecondsSinceEpoch}',
      headline: json['headline'] as String? ?? json['headline_en'] as String? ?? 'Landslide Alert',
      description: json['description'] as String? ?? 'Elevated landslide risk detected.',
      instruction: json['instruction'] as String? ?? 'Move to higher ground and follow designated bypasses.',
      severity: json['severity'] as String? ?? 'WARNING',
      urgency: json['urgency'] as String? ?? 'Immediate',
      areaDesc: json['area_desc'] as String? ?? 'North Eastern Lifeline Corridor',
      language: json['language'] as String? ?? 'en',
      sentAt: DateTime.tryParse(json['sent_at'] as String? ?? '') ?? DateTime.now(),
      targetLatitude: (json['target_lat'] as num?)?.toDouble(),
      targetLongitude: (json['target_lon'] as num?)?.toDouble(),
    );
  }

  static Map<String, dynamic> toJson(EmergencyAlert alert) {
    return {
      'alert_id': alert.alertId,
      'headline': alert.headline,
      'description': alert.description,
      'instruction': alert.instruction,
      'severity': alert.severity,
      'urgency': alert.urgency,
      'area_desc': alert.areaDesc,
      'language': alert.language,
      'sent_at': alert.sentAt.toIso8601String(),
      'target_lat': alert.targetLatitude,
      'target_lon': alert.targetLongitude,
    };
  }
}
