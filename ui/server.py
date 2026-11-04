
"""
Phase 6 Step 1 - Dashboard Server
- Serves ui/dashboard.html on localhost:8000
- NO internet needed, NO APK, NO fake app
- Run: python ui/server.py
"""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

def start_server(port: int = 8000):
    base = Path(__file__).parent
    class H(SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(base), **kw)
        def log_message(self, *a):
            pass
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"BH-OMNI Dashboard: http://127.0.0.1:{port}/dashboard.html")
    print("Press Ctrl+C to stop")
    srv.serve_forever()

if __name__ == "__main__":
    start_server()
