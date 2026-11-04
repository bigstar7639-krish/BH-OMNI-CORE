"""
Phase 6 Step 4 - Theme + Analytics Server
- GET /api/health, /api/regression, /api/story, /api/voice, /api/market, /api/analytics
- Localhost only, NO internet, NO APK
"""
from pathlib import Path
import json, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
BASE = Path(__file__).parent.parent
sys.path.insert(0, str(BASE))
_ANALYTICS = None
def get_analytics(track=False):
    global _ANALYTICS
    try:
        from systems_fj.analytics import Analytics
        if _ANALYTICS is None:
            _ANALYTICS = Analytics()
        if track:
            _ANALYTICS.track("dashboard_user", "app_open")
        return {"total_events": _ANALYTICS.total_events(), "unique_users": _ANALYTICS.unique_users(), "top_events": _ANALYTICS.top_events() if hasattr(_ANALYTICS, "top_events") else [], "note": "In-memory only - Resets on server restart. PII blocked."}
    except Exception as ex:
        return {"error": str(ex)}
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
def get_story(title="Untitled"):
    try:
        from systems_fj.story_engine import StoryEngine
        e = StoryEngine()
        e.create(title, "fantasy", "tanglish")
        e.add_chapter(title, "Chapter 1", "Once upon a time in BH-OMNI...")
        s = e.get_story(title)
        return {"title": s.get("title", title), "story_id": title, "chapters": s.get("chapters", 0)}
    except Exception as ex:
        return {"error": str(ex)}
def get_voice(name="Aria"):
    try:
        from systems_fj.voice_engine import VoiceEngine
        e = VoiceEngine()
        voices = e.list_voices() if hasattr(e, "list_voices") else [name]
        return {"voice": name, "speed": 1.0, "pitch": 1.0, "available": voices, "note": "Metadata only - NO real TTS audio"}
    except Exception as ex:
        return {"error": str(ex)}
def get_market():
    try:
        from systems_fj.marketplace import Marketplace
        m = Marketplace()
        items = m.list_items() if hasattr(m, "list_items") else []
        return {"message": "Marketplace demo - NO real money!", "balance": 100, "items": len(items) if isinstance(items, list) else str(items)}
    except Exception as ex:
        return {"message": "Marketplace demo", "balance": 100, "items": "demo", "note": str(ex)}
class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=str(Path(__file__).parent), **kw)
    def log_message(self, *a):
        pass
    def send_json(self, obj):
        data = json.dumps(obj).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path == "/api/health":
            self.send_json(get_health())
            return
        if self.path == "/api/regression":
            self.send_json(get_regression())
            return
        if self.path.startswith("/api/story"):
            title = parse_qs(urlparse(self.path).query).get("title", ["Untitled"])[0]
            self.send_json(get_story(title))
            return
        if self.path.startswith("/api/voice"):
            name = parse_qs(urlparse(self.path).query).get("name", ["Aria"])[0]
            self.send_json(get_voice(name))
            return
        if self.path.startswith("/api/market"):
            self.send_json(get_market())
            return
        if self.path.startswith("/api/analytics"):
            track = "track=1" in self.path
            self.send_json(get_analytics(track=track))
            return
        return super().do_GET()
def start_server(port=8000):
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    print(f"BH-OMNI Dashboard V4: http://127.0.0.1:{port}/dashboard.html")
    print("API: /api/health + /api/regression + /api/story + /api/voice + /api/market + /api/analytics")
    print("Press Ctrl+C to stop")
    srv.serve_forever()
if __name__ == "__main__":
    start_server()
