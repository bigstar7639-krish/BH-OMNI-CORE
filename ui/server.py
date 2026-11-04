
"""
Phase 6 Step 2 - Interactive Dashboard Server
- Serves ui/dashboard.html + LIVE API:
  GET /api/health -> real health_check() JSON
  GET /api/regression -> real run_regression() JSON
- Localhost only, NO internet, NO APK
- Run: python ui/server.py
"""
from pathlib import Path
import json, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))

def get_health():
    try:
        from release.health_check import health_check
        return health_check()
    except Exception as e:
        return {"overall": "FAIL", "error": str(e)}

def get_regression():
    try:
        from integration.full_regression import run_regression
        return run_regression()
    except Exception as e:
        return {"overall": "FAIL", "error": str(e)}

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(Path(__file__).parent), **kw)
    def log_message(self, *a):
        pass
    def do_GET(self):
        if self.path == "/api/health":
            data = json.dumps(get_health()).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        if self.path == "/api/regression":
            data = json.dumps(get_regression()).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(data))); self.end_headers(); self.wfile.write(data); return
        return super().do_GET()

def start_server(port: int = 8000):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"BH-OMNI Dashboard V2: http://127.0.0.1:{port}/dashboard.html")
    print("API: /api/health + /api/regression")
    print("Press Ctrl+C to stop")
    srv.serve_forever()

if __name__ == "__main__":
    start_server()
