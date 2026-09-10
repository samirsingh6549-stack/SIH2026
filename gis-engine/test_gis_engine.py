"""
Comprehensive Automated Test Suite for Module 4:
Central GIS Command Center & Dynamic Evacuation Router.
Verifies topological graph building, A*/Dijkstra pathfinding,
active hazard avoidance rerouting, and SITREP generation.
"""

import unittest
from road_network import RoadNetworkGraph, RoadNode, RoadEdge
from evacuation_router import (
    EvacuationRouter,
    haversine_km,
    point_to_segment_distance_km
)
from geojson_exporter import GeoJsonExporter
from sitrep_generator import SitrepGenerator

class TestRoadNetwork(unittest.TestCase):
    """Verifies 8-state highway topology and graph integrity."""

    def setUp(self):
        self.network = RoadNetworkGraph()

    def test_eight_states_coverage(self):
        states_found = set(n.state for n in self.network.nodes.values())
        expected = {'Sikkim', 'Assam', 'Manipur', 'Meghalaya', 'Nagaland', 'Arunachal Pradesh', 'Mizoram', 'Tripura'}
        self.assertTrue(expected.issubset(states_found), f"Missing states in road network: {expected - states_found}")

    def test_shelters_presence_and_capacity(self):
        shelters = [n for n in self.network.nodes.values() if n.is_shelter]
        self.assertGreaterEqual(len(shelters), 8)
        for s in shelters:
            self.assertGreater(s.shelter_capacity, 0, f"Shelter {s.name} has 0 capacity")

    def test_bidirectional_connectivity(self):
        # Edges should have corresponding reverse edges
        singtam_neighbors = [nid for nid, _ in self.network.get_neighbors("SKM_SINGTAM")]
        self.assertIn("SKM_32MILE", singtam_neighbors)
        mile32_neighbors = [nid for nid, _ in self.network.get_neighbors("SKM_32MILE")]
        self.assertIn("SKM_SINGTAM", mile32_neighbors)

class TestEvacuationRouter(unittest.TestCase):
    """Verifies shortest path finding and dynamic hazard avoidance rerouting."""

    def setUp(self):
        self.network = RoadNetworkGraph()
        self.router = EvacuationRouter(self.network)

    def test_point_to_segment_distance(self):
        # Segment from (0, 0) to (0, 10), point at (0, 5) should be distance 0
        d_on = point_to_segment_distance_km(0.0, 5.0, 0.0, 0.0, 0.0, 10.0)
        self.assertAlmostEqual(d_on, 0.0, delta=0.1)

        # Point at (1, 5) is ~110 km away (1 degree lat)
        d_off = point_to_segment_distance_km(1.0, 5.0, 0.0, 0.0, 0.0, 10.0)
        self.assertTrue(105.0 <= d_off <= 115.0)

    def test_clear_conditions_direct_route(self):
        # Singtam to Gangtok with all roads open should use direct valley route (NH-10)
        res = self.router.compute_safe_route("SKM_SINGTAM", "SKM_GANGTOK")
        self.assertTrue(res['success'])
        self.assertEqual(res['status'], 'CLEAR_DIRECT_CORRIDOR')
        # Direct route goes through Ranipool
        self.assertIn("SKM_RANIPOOL", res['node_sequence'])
        self.assertIn("SKM_9TH_MILE", res['node_sequence'])
        self.assertTrue(15.0 <= res['total_distance_km'] <= 22.0)

    def test_dynamic_rerouting_around_landslide(self):
        # Landslide occurs at Ranipool Bridge (27.3050, 88.5880) with 1.8km debris runout
        hazards = [{
            'lat': 27.3050, 'lng': 88.5880,
            'threat_radius_km': 1.8,
            'label': 'Ranipool Active Debris Flow'
        }]

        res = self.router.compute_safe_route("SKM_32MILE", "SKM_GANGTOK", hazards=hazards)
        self.assertTrue(res['success'])
        self.assertEqual(res['status'], 'SAFE_BYPASS_VERIFIED')

        # Ranipool MUST be avoided!
        self.assertNotIn("SKM_RANIPOOL", res['node_sequence'], "Router failed to avoid Ranipool hazard zone!")
        self.assertNotIn("SKM_9TH_MILE", res['node_sequence'], "Router routed through compromised 9th Mile!")

        # Instead, it must detour through Upper Martam Shelter Ridge Bypass
        self.assertIn("SKM_UPPER_MARTAM_SHELTER", res['node_sequence'])
        self.assertGreater(res['avoided_hazards_count'], 0)
        self.assertGreater(len(res['turn_by_turn_instructions']), 0)

    def test_nearest_node_snapping(self):
        # Coordinates near Singtam
        node = self.router.find_nearest_node(27.2340, 88.4975)
        self.assertEqual(node.node_id, "SKM_SINGTAM")

    def test_trapped_scenario_handling(self):
        # Artificially block all outgoing edges from Mahur
        for edge_id, edge in self.network.edges.items():
            if edge.u == "ASM_MAHUR" or edge.v == "ASM_MAHUR":
                edge.status = "BLOCKED_LANDSLIDE"

        res = self.router.compute_safe_route("ASM_MAHUR", "ASM_HAFLONG_SHELTER")
        self.assertFalse(res['success'])
        self.assertEqual(res['status'], 'TRAPPED_ALL_ROADS_BLOCKED')
        self.assertIn('recommendation', res)

class TestGeoJsonExporter(unittest.TestCase):
    """Verifies GeoJSON output conforms to RFC 7946 specifications."""

    def setUp(self):
        self.network = RoadNetworkGraph()
        self.router = EvacuationRouter(self.network)

    def test_road_network_geojson(self):
        geojson = GeoJsonExporter.export_road_network(self.network)
        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertGreater(len(geojson['features']), 20)

        # Check line features have stroke colors
        line_features = [f for f in geojson['features'] if f['geometry']['type'] == 'LineString']
        self.assertGreater(len(line_features), 10)
        self.assertIn('stroke', line_features[0]['properties'])

    def test_evacuation_route_geojson(self):
        route_res = self.router.compute_safe_route("SKM_SINGTAM", "SKM_UPPER_MARTAM_SHELTER")
        geojson = GeoJsonExporter.export_evacuation_route(route_res)
        self.assertEqual(geojson['type'], 'FeatureCollection')
        self.assertEqual(len(geojson['features']), 3)  # Route LineString + Start Point + End Point

class TestSitrepGenerator(unittest.TestCase):
    """Verifies SITREP briefing document compilation."""

    def setUp(self):
        self.network = RoadNetworkGraph()

    def test_sitrep_structure(self):
        # Interdict a corridor
        self.network.set_edge_status("E_SKM_03", "BLOCKED_LANDSLIDE", "Mudslide 2m deep over Ranipool roadway")
        hazards = [{'state': 'Sikkim', 'label': 'Ranipool Debris Flow'}]

        sitrep = SitrepGenerator.generate_sitrep(self.network, hazards)
        self.assertIn('metadata', sitrep)
        self.assertIn('executive_summary', sitrep)
        self.assertEqual(sitrep['executive_summary']['threat_level'], 'CRITICAL / CODE_RED')
        self.assertEqual(sitrep['executive_summary']['closed_highway_sections'], 1)

        # Verify text format
        text_report = SitrepGenerator.format_sitrep_text(sitrep)
        self.assertIn("SITUATION REPORT", text_report)
        self.assertIn("Ranipool", text_report)
        self.assertIn("ACTIONABLE DIRECTIVES", text_report)

if __name__ == '__main__':
    unittest.main()
