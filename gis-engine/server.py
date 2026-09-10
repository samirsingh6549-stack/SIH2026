"""
Module 4 REST API Server: GIS Command Center & Dynamic Evacuation Router.
Runs on port 5003 using Python's native HTTP library (Zero external dependencies).
Provides endpoints for safe evacuation pathfinding, GeoJSON corridors, and SITREP reports.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, List, Optional

from road_network import RoadNetworkGraph
from evacuation_router import EvacuationRouter
from geojson_exporter import GeoJsonExporter
from sitrep_generator import SitrepGenerator

PORT = 5003

# Singleton graph and router instances
network = RoadNetworkGraph()
router = EvacuationRouter(network)
active_hazards_cache: List[Dict[str, Any]] = []

class GisEngineRequestHandler(BaseHTTPRequestHandler):

    def _send_json(self, status: int, data: Any):
        body = json.dumps(data, indent=2).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == '/api/health':
            return self._send_json(200, {
                'status': 'HEALTHY',
                'module': 'Module 4: Central GIS Command Center & Evacuation Router',
                'nodes_count': len(network.nodes),
                'edges_count': len(network.edges),
                'active_hazards_count': len(active_hazards_cache)
            })

        if path == '/api/network/corridors':
            geojson = GeoJsonExporter.export_road_network(network)
            return self._send_json(200, geojson)

        if path == '/api/sitrep':
            query = parse_qs(parsed.query)
            fmt = query.get('format', ['json'])[0]
            sitrep_doc = SitrepGenerator.generate_sitrep(network, active_hazards_cache)
            if fmt == 'text':
                text_out = SitrepGenerator.format_sitrep_text(sitrep_doc)
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                return self.wfile.write(text_out.encode('utf-8'))
            return self._send_json(200, sitrep_doc)

        self._send_json(404, {'error': f'Route not found: {path}'})

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        try:
            content_length = int(self.headers.get('Content-Length', 0))
            raw_body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(raw_body) if raw_body else {}
        except Exception as e:
            return self._send_json(400, {'error': f'Malformed JSON: {str(e)}'})

        if path == '/api/routes/evacuate':
            # Resolve start location
            start_node_id = data.get('start_node_id')
            if not start_node_id and 'latitude' in data and 'longitude' in data:
                nearest = router.find_nearest_node(data['latitude'], data['longitude'])
                start_node_id = nearest.node_id if nearest else 'SKM_SINGTAM'

            target_shelter_id = data.get('target_shelter_id')
            hazards = data.get('hazards', active_hazards_cache)

            # Compute shortest safe path avoiding active hazards
            route_res = router.compute_safe_route(
                start_id=start_node_id or 'SKM_SINGTAM',
                target_shelter_id=target_shelter_id,
                hazards=hazards
            )

            # Package with Leaflet GeoJSON
            geojson_bundle = GeoJsonExporter.export_evacuation_route(route_res)
            return self._send_json(200, {
                'routing_result': route_res,
                'geojson': geojson_bundle
            })

        if path == '/api/network/block_segment':
            edge_id = data.get('edge_id')
            reason = data.get('reason', 'Active Landslide Closure')
            if not edge_id or edge_id not in network.edges:
                return self._send_json(404, {'error': f'Edge {edge_id} not found'})
            network.set_edge_status(edge_id, "BLOCKED_LANDSLIDE", reason)
            return self._send_json(200, {
                'status': 'EDGE_INTERDICTED',
                'edge_id': edge_id,
                'reason': reason
            })

        if path == '/api/network/reset':
            for edge in network.edges.values():
                edge.status = "OPEN"
                edge.hazard_reason = None
            active_hazards_cache.clear()
            return self._send_json(200, {'status': 'NETWORK_RESET_TO_OPEN'})

        self._send_json(404, {'error': f'Route not found: {path}'})

def run_server(port: int = PORT):
    server = HTTPServer(('0.0.0.0', port), GisEngineRequestHandler)
    print(f"[gis-engine] Central Command Router listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[gis-engine] Server shut down gracefully.")
        server.server_close()

if __name__ == '__main__':
    run_server()
