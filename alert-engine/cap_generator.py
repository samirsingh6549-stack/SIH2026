"""
OASIS Common Alerting Protocol (CAP) v1.2 / ITU-T X.1303 Serializer.
Compliant with India National Disaster Management Authority (NDMA) SACHET specifications.
Generates validated CAP v1.2 XML and companion JSON structures for multi-hazard alerting.
"""

import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional

from i18n_templates import render_alert_message
from evacuation_matcher import match_evacuation_targets

CAP_NAMESPACE = "urn:oasis:names:tc:emergency:cap:1.2"

def _iso_now(offset_hours: int = 0) -> str:
    """Returns ISO 8601 string with Indian Standard Time (+05:30) offset."""
    ist = timezone(timedelta(hours=5, minutes=30))
    dt = datetime.now(ist) + timedelta(hours=offset_hours)
    return dt.isoformat(timespec='seconds')

def build_cap_alert_payload(
    zone_code: str,
    station_name: str,
    state: str,
    district: str,
    latitude: float,
    longitude: float,
    lsi_score: float,
    factor_of_safety: float,
    rainfall_mm: float,
    pore_pressure_kpa: float,
    slope_deg: float = 38.0,
    languages: Optional[List[str]] = None,
    status: str = "Actual",
    msg_type: str = "Alert"
) -> Dict[str, Any]:
    """
    Assembles a full CAP alert object containing metadata, multiple localized <info> blocks,
    geotechnical parameters, and downstream evacuation targets.
    """
    if languages is None:
        languages = ['en', 'hi', 'as', 'ne', 'mz', 'bn']

    # Map LSI score and Factor of Safety to standard CAP severity / urgency
    if lsi_score >= 0.82 or factor_of_safety < 1.0:
        severity = "Extreme"
        urgency = "Immediate"
        certainty = "Observed" if factor_of_safety < 0.9 else "Likely"
        response_type = "Evacuate"
        template_severity = "EVACUATION"
    elif lsi_score >= 0.60 or factor_of_safety <= 1.25:
        severity = "Severe"
        urgency = "Expected"
        certainty = "Likely"
        response_type = "Prepare"
        template_severity = "WARNING"
    else:
        severity = "Moderate"
        urgency = "Future"
        certainty = "Possible"
        response_type = "Monitor"
        template_severity = "WATCH"

    # Match endangered downstream villages and relief shelters
    evac_data = match_evacuation_targets(
        latitude=latitude,
        longitude=longitude,
        risk_tier=template_severity,
        slope_deg=slope_deg,
        pore_pressure_kpa=pore_pressure_kpa,
        rainfall_mm=rainfall_mm
    )

    alert_id = f"IN-NER-LEWS-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
    sent_time = _iso_now(0)
    expires_time = _iso_now(6)  # 6-hour alert validity window

    context = {
        'corridor': evac_data['matched_corridor'],
        'district': district,
        'state': state,
        'lsi_score': lsi_score,
        'factor_of_safety': factor_of_safety,
        'evacuation_shelter': evac_data['primary_shelter']['name'],
        'evacuation_route': evac_data['safe_evacuation_route']
    }

    # Generate info blocks for each requested regional language
    info_blocks = []
    for lang in languages:
        rendered = render_alert_message(lang, template_severity, context)
        info_blocks.append({
            'language': f"{lang}-IN",
            'language_name': rendered['language_name'],
            'category': 'Geo',
            'event': 'Landslide Early Warning',
            'responseType': response_type,
            'urgency': urgency,
            'severity': severity,
            'certainty': certainty,
            'eventCode': {'valueName': 'SAME', 'value': 'LSW'},
            'expires': expires_time,
            'senderName': f"District Disaster Management Authority ({district}, {state})",
            'headline': rendered['headline'],
            'description': rendered['description'],
            'instruction': rendered['instruction'],
            'cell_broadcast': rendered['cell_broadcast'],
            'ivrs_voice': rendered['ivrs_voice'],
            'contact': 'State Emergency Operations Centre (SEOC) Helpline: 112 / 1070',
            'parameters': {
                'LSI_Probability': round(lsi_score, 4),
                'Factor_Of_Safety': round(factor_of_safety, 2),
                'Rainfall_mm_h': round(rainfall_mm, 1),
                'Pore_Pressure_kPa': round(pore_pressure_kpa, 1),
                'Threat_Radius_km': evac_data['threat_radius_km'],
                'Population_At_Risk': evac_data['total_population_at_risk']
            },
            'area': {
                'areaDesc': f"{evac_data['matched_corridor']}, {district}, {state}",
                'circle': f"{latitude:.4f},{longitude:.4f} {evac_data['threat_radius_km']}",
                'threatened_villages': evac_data['threatened_villages'],
                'primary_shelter': evac_data['primary_shelter'],
                'secondary_shelter': evac_data['secondary_shelter'],
                'safe_evacuation_route': evac_data['safe_evacuation_route']
            }
        })

    return {
        'identifier': alert_id,
        'sender': f"ner-lews.{district.lower().replace(' ', '')}@disastermanagement.gov.in",
        'sent': sent_time,
        'status': status,
        'msgType': msg_type,
        'scope': 'Public',
        'code': ['IPAWS-CAP', 'NDMA-SACHET'],
        'zone_code': zone_code,
        'station_name': station_name,
        'state': state,
        'district': district,
        'coordinates': {'latitude': latitude, 'longitude': longitude},
        'severity_level': severity,
        'info_blocks': info_blocks
    }

def generate_cap_xml(alert_data: Dict[str, Any]) -> str:
    """
    Serializes an alert dictionary into strict, standardized OASIS CAP v1.2 XML.
    """
    root = ET.Element('alert', xmlns=CAP_NAMESPACE)

    ET.SubElement(root, 'identifier').text = alert_data['identifier']
    ET.SubElement(root, 'sender').text = alert_data['sender']
    ET.SubElement(root, 'sent').text = alert_data['sent']
    ET.SubElement(root, 'status').text = alert_data['status']
    ET.SubElement(root, 'msgType').text = alert_data['msgType']
    ET.SubElement(root, 'scope').text = alert_data['scope']

    for code in alert_data.get('code', []):
        ET.SubElement(root, 'code').text = code

    # Add <info> elements for each language
    for info in alert_data.get('info_blocks', []):
        info_el = ET.SubElement(root, 'info')
        ET.SubElement(info_el, 'language').text = info['language']
        ET.SubElement(info_el, 'category').text = info['category']
        ET.SubElement(info_el, 'event').text = info['event']
        ET.SubElement(info_el, 'responseType').text = info['responseType']
        ET.SubElement(info_el, 'urgency').text = info['urgency']
        ET.SubElement(info_el, 'severity').text = info['severity']
        ET.SubElement(info_el, 'certainty').text = info['certainty']

        event_code = ET.SubElement(info_el, 'eventCode')
        ET.SubElement(event_code, 'valueName').text = info['eventCode']['valueName']
        ET.SubElement(event_code, 'value').text = info['eventCode']['value']

        ET.SubElement(info_el, 'expires').text = info['expires']
        ET.SubElement(info_el, 'senderName').text = info['senderName']
        ET.SubElement(info_el, 'headline').text = info['headline']
        ET.SubElement(info_el, 'description').text = info['description']
        ET.SubElement(info_el, 'instruction').text = info['instruction']
        ET.SubElement(info_el, 'contact').text = info['contact']

        # Parameters (Geotechnical & AI metrics)
        for key, val in info.get('parameters', {}).items():
            param_el = ET.SubElement(info_el, 'parameter')
            ET.SubElement(param_el, 'valueName').text = str(key)
            ET.SubElement(param_el, 'value').text = str(val)

        # Geographic Target Area
        area_info = info.get('area', {})
        area_el = ET.SubElement(info_el, 'area')
        ET.SubElement(area_el, 'areaDesc').text = area_info.get('areaDesc', '')
        if 'circle' in area_info:
            ET.SubElement(area_el, 'circle').text = area_info['circle']

    return ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')

def generate_cap_json(alert_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Produces clean JSON representation formatted for modern REST/WebSockets consumers.
    """
    return {
        'cap_version': '1.2',
        'standard': 'OASIS-CAP-v1.2 / ITU-T X.1303',
        'alert': alert_data
    }
