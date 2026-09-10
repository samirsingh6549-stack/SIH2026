"""
Multi-Channel Disaster Alert Dissemination Pipeline.
Simulates mission-critical broadcast across 4 redundant channels:
1. Telecom Cell Broadcast (CB) / High-Priority Emergency SMS
2. Automated Interactive Voice Response System (IVRS) in Native Dialects
3. Physical IoT Siren & Highway Strobe Relay Controller
4. State Emergency Operations Centre (SEOC) & 112 Dispatch Webhook
"""

import time
from typing import Dict, List, Any

class CellBroadcastDispatcher:
    """Dispatches telecom Cell Broadcast (CB) packets to cellular towers within threat polygon."""

    @staticmethod
    def dispatch(info_block: Dict[str, Any], threat_radius_km: float) -> Dict[str, Any]:
        text = info_block.get('cell_broadcast', '')
        # Cell broadcast standard chunks are 93 chars; standard SMS is 160 chars
        char_count = len(text)
        
        # Estimate number of cellular tower BTS sectors within radius (avg 1 tower per 2.5 km2 in hills)
        area_km2 = 3.14159 * (threat_radius_km ** 2)
        active_towers = max(2, int(area_km2 / 2.5))
        pop_at_risk = info_block.get('parameters', {}).get('Population_At_Risk', 1500)
        estimated_subscribers = int(pop_at_risk * 0.72)  # ~72% mobile penetration

        return {
            'channel': 'CELL_BROADCAST_SMS',
            'status': 'TRANSMITTED',
            'timestamp': time.strftime('%H:%M:%S IST'),
            'payload': text,
            'character_count': char_count,
            'bts_towers_activated': active_towers,
            'estimated_handsets_reached': estimated_subscribers,
            'priority_class': 'CLASS_0_FLASH_MESSAGE'
        }

class IvrsVoiceDispatcher:
    """Generates and dispatches automated voice evacuation calls to registered community leaders."""

    @staticmethod
    def dispatch(info_block: Dict[str, Any], district: str) -> Dict[str, Any]:
        voice_script = info_block.get('ivrs_voice', '')
        lang_name = info_block.get('language_name', 'English')
        
        # Target village headmen (Gaon Burhas), panchayat pradhans, school principals, and ASHA workers
        target_stakeholders = [
            f"Gaon Burha (Village Council Chief) - {district}",
            f"Panchayat Disaster Representative - {district}",
            f"ASHA Healthcare Coordinator - {district}",
            f"Primary School Headmaster - {district}",
            f"Local Police Station Officer-in-Charge"
        ]

        return {
            'channel': 'IVRS_AUTOMATED_VOICE',
            'status': 'DIALING_ACTIVE',
            'timestamp': time.strftime('%H:%M:%S IST'),
            'dialect_selected': lang_name,
            'voice_script': voice_script,
            'call_duration_est_sec': 38,
            'priority_cadence': 'URGENT_REPEAT_3X',
            'stakeholders_queued': len(target_stakeholders),
            'target_list': target_stakeholders
        }

class IoTSirenController:
    """Triggers solar-powered 110dB hooters, visual strobes, and automated highway barrier gates."""

    @staticmethod
    def dispatch(corridor: str, severity: str) -> Dict[str, Any]:
        is_critical = (severity == "Extreme")

        relay_commands = [
            {'relay_id': 'RLY_SIREN_110DB', 'state': 'ACTIVE' if is_critical else 'STANDBY_CHIRP', 'duration_sec': 180 if is_critical else 15},
            {'relay_id': 'RLY_STROBE_RED', 'state': 'FLASHING_RAPID', 'frequency_hz': 2.5},
            {'relay_id': 'RLY_BARRIER_GATE', 'state': 'LOWER_AND_LOCK' if is_critical else 'MAINTAIN_OPEN', 'road_section': corridor}
        ]

        return {
            'channel': 'IOT_PHYSICAL_SIREN_AND_BARRIER',
            'status': 'RELAY_TRIGGERED',
            'timestamp': time.strftime('%H:%M:%S IST'),
            'sound_pressure_level_db': 110,
            'highway_barrier_status': 'CLOSED_INTERDICTED' if is_critical else 'OPEN_WARNING',
            'relay_control_packets': relay_commands
        }

class SeocWebhookDispatcher:
    """Pushes standard CAP JSON alerts to District/State Emergency Operations Centres and 112 ERSS."""

    @staticmethod
    def dispatch(alert_data: Dict[str, Any]) -> Dict[str, Any]:
        endpoints = [
            'https://seoc.sdrf.gov.in/api/v1/cap_ingest',
            'https://erss112.mha.gov.in/api/v2/disaster_escalation',
            'https://bro.gov.in/telemetry/highway_blockage'
        ]

        return {
            'channel': 'SEOC_AND_112_WEBHOOK',
            'status': 'DISPATCHED_HTTP_200',
            'timestamp': time.strftime('%H:%M:%S IST'),
            'alert_identifier': alert_data['identifier'],
            'dispatched_endpoints': endpoints,
            'acknowledgments_received': len(endpoints)
        }

class MultiChannelDispatcher:
    """Unified coordinator that triggers all 4 dissemination channels in parallel."""

    @classmethod
    def broadcast_alert(cls, alert_data: Dict[str, Any], primary_lang: str = 'en') -> Dict[str, Any]:
        # Find matching language info block
        info_blocks = alert_data.get('info_blocks', [])
        selected_info = next((b for b in info_blocks if b['language'].startswith(primary_lang)), info_blocks[0] if info_blocks else {})

        threat_radius = selected_info.get('parameters', {}).get('Threat_Radius_km', 2.0)
        corridor = alert_data.get('station_name', 'Lifeline Corridor')
        district = alert_data.get('district', 'NER District')
        severity = alert_data.get('severity_level', 'Extreme')

        t0 = time.perf_counter()

        cb_res = CellBroadcastDispatcher.dispatch(selected_info, threat_radius)
        ivrs_res = IvrsVoiceDispatcher.dispatch(selected_info, district)
        siren_res = IoTSirenController.dispatch(corridor, severity)
        seoc_res = SeocWebhookDispatcher.dispatch(alert_data)

        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

        return {
            'status': 'BROADCAST_COMPLETED',
            'alert_identifier': alert_data['identifier'],
            'severity': severity,
            'total_channels_fired': 4,
            'dispatch_latency_ms': elapsed_ms,
            'channels': {
                'cell_broadcast': cb_res,
                'ivrs_voice': ivrs_res,
                'iot_siren_and_barrier': siren_res,
                'seoc_emergency_webhook': seoc_res
            },
            'summary_receipt': {
                'estimated_citizens_reached': cb_res['estimated_handsets_reached'],
                'community_leaders_called': ivrs_res['stakeholders_queued'],
                'physical_sirens_activated': 1,
                'highway_interdicted': siren_res['highway_barrier_status']
            }
        }
