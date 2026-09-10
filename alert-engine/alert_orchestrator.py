"""
Alert Pipeline Orchestrator.
Connects Module 1 AI risk scores (LSI & Factor of Safety) and Module 2 sensor triggers
to the Common Alerting Protocol (CAP v1.2) serialization and multi-channel broadcast engine.
"""

from typing import Dict, List, Any, Optional
from cap_generator import build_cap_alert_payload, generate_cap_xml, generate_cap_json
from dissemination_channels import MultiChannelDispatcher

class AlertOrchestrator:
    """Manages disaster alert lifecycle: evaluation, generation, broadcast, and tracking."""

    def __init__(self):
        # In-memory store for active regional alerts
        self._active_alerts: Dict[str, Dict[str, Any]] = {}
        self._dispatch_history: List[Dict[str, Any]] = []

    def evaluate_hazard(self, telemetry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Evaluates risk criteria based on geotechnical mechanics and ML probabilities:
        - RED / EVACUATION: LSI >= 0.82 or FoS < 1.0 or Pore Pressure > 42 kPa
        - ORANGE / WARNING: 0.60 <= LSI < 0.82 or FoS < 1.25
        - YELLOW / WATCH:   0.35 <= LSI < 0.60
        - GREEN / LOW:      LSI < 0.35 (No alert dispatched)
        """
        lsi = float(telemetry.get('lsi_score', 0.50))
        fos = float(telemetry.get('factor_of_safety', 1.30))
        pore_pressure = float(telemetry.get('pore_pressure_kpa', 25.0))
        rainfall_mm = float(telemetry.get('rainfall_mm', 40.0))

        # Determine threshold
        if lsi >= 0.82 or fos < 1.0 or pore_pressure >= 45.0:
            severity = "Extreme"
        elif lsi >= 0.60 or fos <= 1.25 or pore_pressure >= 35.0:
            severity = "Severe"
        elif lsi >= 0.35 or rainfall_mm >= 30.0:
            severity = "Moderate"
        else:
            return None  # Normal conditions; no broadcast required

        zone_code = telemetry.get('zone_code', telemetry.get('location_id', 'NER-GEN-01'))
        station_name = telemetry.get('station_name', telemetry.get('name', 'Lifeline Sector'))
        state = telemetry.get('state', 'Sikkim')
        district = telemetry.get('district', 'East Sikkim')
        lat = float(telemetry.get('latitude', telemetry.get('lat', 27.3389)))
        lng = float(telemetry.get('longitude', telemetry.get('lng', 88.6065)))
        slope = float(telemetry.get('slope_angle_degrees', telemetry.get('slope_deg', 40.0)))

        # Build OASIS CAP v1.2 data structure
        alert_payload = build_cap_alert_payload(
            zone_code=zone_code,
            station_name=station_name,
            state=state,
            district=district,
            latitude=lat,
            longitude=lng,
            lsi_score=lsi,
            factor_of_safety=fos,
            rainfall_mm=rainfall_mm,
            pore_pressure_kpa=pore_pressure,
            slope_deg=slope
        )

        return alert_payload

    def trigger_and_broadcast(self, telemetry: Dict[str, Any], primary_lang: str = 'en') -> Dict[str, Any]:
        """
        Evaluates incoming telemetry, builds CAP alert, and executes multi-channel dissemination.
        """
        alert_data = self.evaluate_hazard(telemetry)
        if not alert_data:
            return {
                'status': 'NO_ALERT_REQUIRED',
                'message': 'Telemetry within safe environmental thresholds (LSI < 0.35, FoS > 1.30)',
                'lsi_score': telemetry.get('lsi_score'),
                'factor_of_safety': telemetry.get('factor_of_safety')
            }

        # Store in active alerts dictionary
        alert_id = alert_data['identifier']
        self._active_alerts[alert_id] = alert_data

        # Generate standard XML and JSON
        cap_xml = generate_cap_xml(alert_data)
        cap_json = generate_cap_json(alert_data)

        # Execute 4-channel broadcast
        broadcast_receipt = MultiChannelDispatcher.broadcast_alert(alert_data, primary_lang=primary_lang)

        receipt = {
            'status': 'ALERT_DISPATCHED',
            'alert_identifier': alert_id,
            'zone_code': alert_data['zone_code'],
            'station_name': alert_data['station_name'],
            'state': alert_data['state'],
            'district': alert_data['district'],
            'severity': alert_data['severity_level'],
            'broadcast_details': broadcast_receipt,
            'cap_json': cap_json,
            'cap_xml_preview': cap_xml[:450] + '... [TRUNCATED XML]'
        }

        self._dispatch_history.append(receipt)
        return receipt

    def get_active_alerts(self) -> List[Dict[str, Any]]:
        """Returns all currently active disaster alerts."""
        return list(self._active_alerts.values())

    def get_alert_by_id(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Fetches an active alert by unique identifier."""
        return self._active_alerts.get(alert_id)

    def get_alert_xml(self, alert_id: str) -> Optional[str]:
        """Returns raw CAP v1.2 XML string for an alert."""
        alert_data = self._active_alerts.get(alert_id)
        if alert_data:
            return generate_cap_xml(alert_data)
        return None

# Global orchestrator singleton instance
orchestrator = AlertOrchestrator()
