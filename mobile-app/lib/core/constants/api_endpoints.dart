class ApiEndpoints {
  // Default to localhost or LAN IP for testing against local microservices
  static const String baseHost = 'http://10.0.2.2'; // Standard Android emulator localhost alias
  static const String localHostFallback = 'http://localhost';

  // Module 0: Cloud Sync Gateway
  static const int syncPort = 3000;
  static String get syncBatch => '$baseHost:$syncPort/api/field_reports/batch';
  static String get syncSingle => '$baseHost:$syncPort/api/field_reports';
  static String get healthCheck => '$baseHost:$syncPort/api/health';
  static String get activeAlerts => '$baseHost:$syncPort/api/alerts';
  static String get riskZones => '$baseHost:$syncPort/api/risk_zones';

  // Module 1: ML Predictive Engine
  static const int mlPort = 5001;
  static String get mlPredict => '$baseHost:$mlPort/api/v1/predict';
  static String get mlBatchHeatmap => '$baseHost:$mlPort/api/v1/predict_batch';

  // Module 3: CAP Alert Engine
  static const int alertPort = 5002;
  static String get capAlertBroadcast => '$baseHost:$alertPort/api/alerts/broadcast';
  static String get triggerSos => '$baseHost:$alertPort/api/sos/dispatch';

  // Module 4: Central GIS Engine
  static const int gisPort = 5003;
  static String get evacuationRoute => '$baseHost:$gisPort/api/gis/evacuate/route';
  static String get roadNetwork => '$baseHost:$gisPort/api/gis/network';
  static String get sitrepSummary => '$baseHost:$gisPort/api/gis/sitrep';
}
