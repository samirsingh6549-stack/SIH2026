import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from predictor import (
    predict_detailed_risk,
    predict_disaster_risk,
    predict_batch,
    generate_heatmap_probabilities,
    _get_metadata
)

HOST = os.environ.get('ML_SERVER_HOST', '0.0.0.0')
PORT = int(os.environ.get('ML_SERVER_PORT', 5001))

class MLInferenceHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers(204)

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/health' or path == '/':
            response = {
                'status': 'healthy',
                'service': 'SIH-2026 NER Landslide AI/ML Inference Engine',
                'version': '1.0.0',
                'port': PORT
            }
            self._set_cors_headers(200)
            self.wfile.write(json.dumps(response, indent=2).encode('utf-8'))

        elif path == '/api/model-info':
            metadata = _get_metadata()
            self._set_cors_headers(200)
            self.wfile.write(json.dumps(metadata, indent=2).encode('utf-8'))

        else:
            self._set_cors_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            payload = json.loads(post_data.decode('utf-8')) if post_data else {}
        except json.JSONDecodeError:
            self._set_cors_headers(400)
            self.wfile.write(json.dumps({'status': 'error', 'message': 'Invalid JSON body'}).encode('utf-8'))
            return

        if path == '/api/predict':
            result = predict_detailed_risk(payload)
            status_code = 200 if result.get('status') == 'success' else 400
            self._set_cors_headers(status_code)
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))

        elif path == '/api/predict/batch':
            points = payload.get('points', payload) if isinstance(payload, dict) else payload
            result = predict_batch(points)
            status_code = 200 if result.get('status') == 'success' else 400
            self._set_cors_headers(status_code)
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))

        elif path == '/api/predict/heatmap':
            points = payload.get('points', payload) if isinstance(payload, dict) else payload
            result = generate_heatmap_probabilities(points)
            status_code = 200 if result.get('status') == 'success' else 400
            self._set_cors_headers(status_code)
            self.wfile.write(json.dumps(result, indent=2).encode('utf-8'))

        elif path == '/api/predict/simple':
            simple_text = predict_disaster_risk(payload)
            self._set_cors_headers(200)
            self.wfile.write(json.dumps({'result': simple_text}).encode('utf-8'))

        else:
            self._set_cors_headers(404)
            self.wfile.write(json.dumps({'error': 'Endpoint not found'}).encode('utf-8'))

    def log_message(self, format, *args):
        # Clean logging format
        print(f"[ML-API] {self.address_string()} - {args[0]} {args[1]}")

def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, MLInferenceHandler)
    print("=" * 60)
    print(f"  SIH 2026: ML PREDICTIVE ANALYTICS REST API")
    print(f"  Server listening on http://localhost:{PORT}")
    print(f"  Endpoints:")
    print(f"    - GET  /health")
    print(f"    - GET  /api/model-info")
    print(f"    - POST /api/predict        (Full LSI & Geotechnical Physics)")
    print(f"    - POST /api/predict/batch  (Vectorized High-Throughput Matrix Inference)")
    print(f"    - POST /api/predict/heatmap (Leaflet-Ready [lat, lon, intensity] Grid)")
    print(f"    - POST /api/predict/simple (Legacy string response)")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down ML server.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
