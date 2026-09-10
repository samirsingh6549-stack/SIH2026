"""
Comprehensive Automated Test Suite for Module 3:
Common Alerting Protocol (CAP v1.2) & Multi-Channel Dissemination Engine.
Runs under standard Python unittest runner with 0 external dependencies.
"""

import unittest
import xml.etree.ElementTree as ET
from i18n_templates import I18N_TEMPLATES, render_alert_message
from evacuation_matcher import (
    calculate_threat_radius_km,
    haversine_distance_km,
    match_evacuation_targets,
    NER_SHELTER_INVENTORY
)
from cap_generator import (
    build_cap_alert_payload,
    generate_cap_xml,
    generate_cap_json,
    CAP_NAMESPACE
)
from dissemination_channels import MultiChannelDispatcher
from alert_orchestrator import AlertOrchestrator

class TestI18nTemplates(unittest.TestCase):
    """Verifies multilingual alert template generation across 8 NER languages."""

    def test_all_eight_languages_present(self):
        expected_langs = {'en', 'hi', 'as', 'bn', 'ne', 'mz', 'mn', 'kha'}
        self.assertTrue(expected_langs.issubset(set(I18N_TEMPLATES.keys())),
                        f"Missing languages in templates: {expected_langs - set(I18N_TEMPLATES.keys())}")

    def test_template_rendering_no_unbound_placeholders(self):
        context = {
            'corridor': 'NH-10 Ranipool',
            'district': 'East Sikkim',
            'state': 'Sikkim',
            'lsi_score': 0.945,
            'factor_of_safety': 0.78,
            'evacuation_shelter': 'Upper Martam School',
            'evacuation_route': 'Upper Ridge Trail'
        }

        for lang in I18N_TEMPLATES.keys():
            rendered = render_alert_message(lang, 'EVACUATION', context)
            self.assertEqual(rendered['language'], lang)
            self.assertIn('Upper Martam School', rendered['instruction'])
            self.assertNotIn('{', rendered['headline'], f"Unrendered placeholder in {lang} headline")
            self.assertNotIn('{', rendered['cell_broadcast'], f"Unrendered placeholder in {lang} cell broadcast")
            self.assertLessEqual(len(rendered['cell_broadcast']), 160, f"Cell broadcast text in {lang} exceeds SMS limit")

class TestEvacuationMatcher(unittest.TestCase):
    """Verifies threat radius calculation and spatial habitation/shelter matching."""

    def test_haversine_distance_accuracy(self):
        # Distance between Gangtok (27.33, 88.61) and Mangan (27.51, 88.53) is ~21 km
        dist = haversine_distance_km(27.33, 88.61, 27.51, 88.53)
        self.assertTrue(18.0 <= dist <= 24.0, f"Unexpected Haversine distance: {dist} km")

    def test_dynamic_threat_radius(self):
        # Steep slope + high pore pressure + torrential rain should yield larger runout
        r_severe = calculate_threat_radius_km(slope_deg=45.0, pore_pressure_kpa=55.0, rainfall_mm=120.0)
        r_mild = calculate_threat_radius_km(slope_deg=25.0, pore_pressure_kpa=25.0, rainfall_mm=20.0)
        self.assertGreater(r_severe, r_mild)
        self.assertTrue(1.0 <= r_severe <= 5.0)

    def test_match_evacuation_targets_sikkim(self):
        result = match_evacuation_targets(
            latitude=27.3389, longitude=88.6065,
            risk_tier='EVACUATION',
            slope_deg=42.0, pore_pressure_kpa=48.0, rainfall_mm=90.0
        )
        self.assertEqual(result['state'], 'Sikkim')
        self.assertEqual(result['district'], 'East Sikkim')
        self.assertIn('Ranipool Bazaar', result['threatened_villages'])
        self.assertGreater(result['total_population_at_risk'], 1000)
        self.assertIn('Upper Martam', result['primary_shelter']['name'])

    def test_match_evacuation_targets_assam_haflong(self):
        result = match_evacuation_targets(
            latitude=25.1837, longitude=93.0298,
            risk_tier='EVACUATION'
        )
        self.assertEqual(result['state'], 'Assam')
        self.assertEqual(result['district'], 'Dima Hasao')
        self.assertIn('Haflong', result['primary_shelter']['name'])

class TestCapGenerator(unittest.TestCase):
    """Verifies strict compliance with OASIS CAP v1.2 / ITU-T X.1303 specifications."""

    def setUp(self):
        self.alert_data = build_cap_alert_payload(
            zone_code="NER-SIKK-01",
            station_name="Ranipool NH-10 Corridor",
            state="Sikkim",
            district="East Sikkim",
            latitude=27.3389,
            longitude=88.6065,
            lsi_score=0.9572,
            factor_of_safety=0.74,
            rainfall_mm=95.0,
            pore_pressure_kpa=52.0,
            slope_deg=43.0,
            languages=['en', 'hi', 'ne']
        )

    def test_cap_payload_structure(self):
        self.assertTrue(self.alert_data['identifier'].startswith('IN-NER-LEWS-'))
        self.assertEqual(self.alert_data['status'], 'Actual')
        self.assertEqual(self.alert_data['msgType'], 'Alert')
        self.assertEqual(self.alert_data['scope'], 'Public')
        self.assertEqual(self.alert_data['severity_level'], 'Extreme')
        self.assertEqual(len(self.alert_data['info_blocks']), 3)

    def test_cap_xml_conformance(self):
        xml_string = generate_cap_xml(self.alert_data)
        self.assertIsInstance(xml_string, str)
        self.assertIn('<?xml', xml_string)

        # Parse XML tree to verify schema validity
        root = ET.fromstring(xml_string)
        # Check namespace URI
        self.assertEqual(root.tag, f"{{{CAP_NAMESPACE}}}alert")

        # Check critical child elements
        ns = {'cap': CAP_NAMESPACE}
        identifier = root.find('cap:identifier', ns)
        self.assertIsNotNone(identifier)
        self.assertEqual(identifier.text, self.alert_data['identifier'])

        info_elements = root.findall('cap:info', ns)
        self.assertEqual(len(info_elements), 3)

        # Verify first info element fields
        info0 = info_elements[0]
        self.assertEqual(info0.find('cap:language', ns).text, 'en-IN')
        self.assertEqual(info0.find('cap:severity', ns).text, 'Extreme')
        self.assertEqual(info0.find('cap:urgency', ns).text, 'Immediate')
        self.assertEqual(info0.find('cap:category', ns).text, 'Geo')

        # Verify area and circle tag
        area = info0.find('cap:area', ns)
        self.assertIsNotNone(area)
        circle = area.find('cap:circle', ns)
        self.assertIsNotNone(circle)
        self.assertIn('27.3389,88.6065', circle.text)

    def test_cap_json_conformance(self):
        cap_json = generate_cap_json(self.alert_data)
        self.assertEqual(cap_json['cap_version'], '1.2')
        self.assertIn('alert', cap_json)
        self.assertEqual(cap_json['alert']['identifier'], self.alert_data['identifier'])

class TestMultiChannelDissemination(unittest.TestCase):
    """Verifies that all 4 broadcast channels execute properly."""

    def setUp(self):
        self.alert_data = build_cap_alert_payload(
            zone_code="NER-NAGA-05",
            station_name="Kohima Dzüdza River NH-29",
            state="Nagaland",
            district="Kohima",
            latitude=25.6751,
            longitude=94.1086,
            lsi_score=0.9733,
            factor_of_safety=0.68,
            rainfall_mm=110.0,
            pore_pressure_kpa=56.0,
            languages=['en', 'hi']
        )

    def test_broadcast_execution_all_channels(self):
        receipt = MultiChannelDispatcher.broadcast_alert(self.alert_data, primary_lang='en')

        self.assertEqual(receipt['status'], 'BROADCAST_COMPLETED')
        self.assertEqual(receipt['total_channels_fired'], 4)
        self.assertLess(receipt['dispatch_latency_ms'], 100.0, "Dispatch latency exceeded 100ms")

        channels = receipt['channels']
        # 1. Cell Broadcast
        self.assertEqual(channels['cell_broadcast']['status'], 'TRANSMITTED')
        self.assertGreater(channels['cell_broadcast']['bts_towers_activated'], 0)
        self.assertGreater(channels['cell_broadcast']['estimated_handsets_reached'], 500)

        # 2. IVRS Voice
        self.assertEqual(channels['ivrs_voice']['status'], 'DIALING_ACTIVE')
        self.assertGreater(channels['ivrs_voice']['stakeholders_queued'], 3)

        # 3. IoT Sirens & Barriers
        self.assertEqual(channels['iot_siren_and_barrier']['status'], 'RELAY_TRIGGERED')
        self.assertEqual(channels['iot_siren_and_barrier']['sound_pressure_level_db'], 110)
        self.assertEqual(channels['iot_siren_and_barrier']['highway_barrier_status'], 'CLOSED_INTERDICTED')

        # 4. SEOC Webhook
        self.assertEqual(channels['seoc_emergency_webhook']['status'], 'DISPATCHED_HTTP_200')
        self.assertEqual(channels['seoc_emergency_webhook']['acknowledgments_received'], 3)

class TestAlertOrchestrator(unittest.TestCase):
    """Tests the alert lifecycle and risk escalation thresholds."""

    def setUp(self):
        self.orchestrator = AlertOrchestrator()

    def test_critical_trigger_escalation(self):
        telemetry = {
            'location_id': 'SKM_01',
            'station_name': 'Ranipool NH-10',
            'state': 'Sikkim',
            'district': 'East Sikkim',
            'latitude': 27.3389,
            'longitude': 88.6065,
            'lsi_score': 0.94,
            'factor_of_safety': 0.72,
            'pore_pressure_kpa': 54.0,
            'rainfall_mm': 120.0
        }
        res = self.orchestrator.trigger_and_broadcast(telemetry, primary_lang='en')
        self.assertEqual(res['status'], 'ALERT_DISPATCHED')
        self.assertEqual(res['severity'], 'Extreme')
        self.assertIn('Upper Martam', str(res['cap_json']))

        # Verify active alerts registry
        active = self.orchestrator.get_active_alerts()
        self.assertEqual(len(active), 1)

    def test_normal_conditions_no_alert(self):
        safe_telemetry = {
            'location_id': 'ASM_02',
            'station_name': 'Guwahati Foothills',
            'state': 'Assam',
            'district': 'Kamrup Metro',
            'latitude': 26.14,
            'longitude': 91.73,
            'lsi_score': 0.12,
            'factor_of_safety': 2.45,
            'pore_pressure_kpa': 12.0,
            'rainfall_mm': 5.0
        }
        res = self.orchestrator.trigger_and_broadcast(safe_telemetry)
        self.assertEqual(res['status'], 'NO_ALERT_REQUIRED')

    def test_eight_states_alert_generation(self):
        states_data = [
            ('Sikkim', 'East Sikkim', 27.3389, 88.6065),
            ('Assam', 'Dima Hasao', 25.1837, 93.0298),
            ('Meghalaya', 'East Khasi Hills', 25.2702, 91.7323),
            ('Manipur', 'Noney', 24.8167, 93.6833),
            ('Nagaland', 'Kohima', 25.6751, 94.1086),
            ('Arunachal Pradesh', 'West Kameng', 27.5861, 91.8653),
            ('Mizoram', 'Aizawl', 23.7271, 92.7176),
            ('Tripura', 'North Tripura', 23.9500, 92.2667)
        ]
        for st, dist, lat, lng in states_data:
            t = {
                'location_id': f'TEST_{st[:3].upper()}',
                'station_name': f'{st} Sector',
                'state': st,
                'district': dist,
                'latitude': lat,
                'longitude': lng,
                'lsi_score': 0.88,
                'factor_of_safety': 0.82,
                'pore_pressure_kpa': 46.0,
                'rainfall_mm': 80.0
            }
            alert = self.orchestrator.evaluate_hazard(t)
            self.assertIsNotNone(alert, f"Alert evaluation failed for {st}")
            self.assertEqual(alert['state'], st)
            self.assertEqual(alert['severity_level'], 'Extreme')

if __name__ == '__main__':
    unittest.main()
