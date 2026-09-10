"""
Module 3 REST API Server: Common Alerting Protocol (CAP v1.2) Engine.
Runs on port 5002 using Python's native HTTP library (Zero external dependencies).
Provides endpoints for CAP XML generation, multi-channel dispatch, and active alert queries.
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from typing import Any, Dict, List, Optional
from alert_orchestrator import orchestrator, generate_cap_xml

PORT = 5002

class AlertEngineRequestHandler(BaseHTTPRequestHandler):

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

    def _send_xml(self, status: int, xml_content: str):
        body = xml_content.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/xml; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
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
                'module': 'Module 3: CAP Alerting & Dissemination Engine',
                'standard': 'OASIS-CAP-v1.2 / ITU-T X.1303',
                'active_alerts_count': len(orchestrator.get_active_alerts())
            })

        if path == '/api/alerts/active':
            return self._send_json(200, {
                'count': len(orchestrator.get_active_alerts()),
                'alerts': orchestrator.get_active_alerts()
            })

        if path == '/api/alerts/xml':
            query = parse_qs(parsed.query)
            alert_id = query.get('id', [None])[0]
            if not alert_id:
                active = orchestrator.get_active_alerts()
                if active:
                    xml_str = generate_cap_xml(active[0])
                    return self._send_xml(200, xml_str)
                return self._send_json(404, {'error': 'No active alert found. Provide ?id=<identifier>'})

            xml_str = orchestrator.get_alert_xml(alert_id)
            if xml_str:
                return self._send_xml(200, xml_str)
            return self._send_json(404, {'error': f'Alert {alert_id} not found'})

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

        if path == '/api/alerts/generate':
            alert_data = orchestrator.evaluate_hazard(data)
            if not alert_data:
                return self._send_json(200, {
                    'status': 'SAFE',
                    'message': 'No CAP alert triggered based on provided parameters.'
                })
            xml_preview = generate_cap_xml(alert_data)
            return self._send_json(200, {
                'status': 'CAP_GENERATED',
                'alert': alert_data,
                'xml_bytes': len(xml_preview)
            })

        if path == '/api/alerts/broadcast':
            lang = data.get('primary_language', 'en')
            telemetry = data.get('telemetry', data)
            receipt = orchestrator.trigger_and_broadcast(telemetry, primary_lang=lang)
            return self._send_json(201, receipt)

        self._send_json(404, {'error': f'Route not found: {path}'})

def run_server(port: int = PORT):
    server = HTTPServer(('0.0.0.0', port), AlertEngineRequestHandler)
    print(f"[alert-engine] OASIS CAP v1.2 Gateway listening on port {port}...")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[alert-engine] Server shut down gracefully.")
        server.server_close()

if __name__ == '__main__':
    run_server()
