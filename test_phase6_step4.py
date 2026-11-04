# BH-OMNI CORE - Phase 6 Step 4 - Theme + Analytics - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v4_theme_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["THEME", "setTheme(", "Neon", "Light", "localStorage"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v4_theme_ui: PASS - Theme switcher + localStorage present")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_theme_ui: FAIL - {e}")
        return "FAIL"

def test_v4_analytics_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["LIVE ANALYTICS", "showAnalytics()", "trackEvent()", "/api/analytics"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v4_analytics_ui: PASS - Analytics card + buttons present")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_analytics_ui: FAIL - {e}")
        return "FAIL"

def test_v4_server_analytics():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/analytics", "get_analytics", "_ANALYTICS"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v4_server_analytics: PASS - /api/analytics endpoint present")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_server_analytics: FAIL - {e}")
        return "FAIL"

def test_v4_analytics_real():
    try:
        from ui.server import get_analytics
        r1 = get_analytics(track=True)
        assert r1["total_events"] >= 1, f"Bad: {r1}"
        assert "PII blocked" in r1["note"] or "In-memory" in r1["note"]
        r2 = get_analytics(track=True)
        assert r2["total_events"] == r1["total_events"] + 1, f"Not counting: {r1} -> {r2}"
        print(f"TEST v4_analytics_real: PASS - REAL Analytics counting: {r1['total_events']} -> {r2['total_events']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_analytics_real: FAIL - {e}")
        return "FAIL"

def test_v4_old_api_still_ok():
    try:
        from ui.server import get_health, get_regression, get_story, get_voice, get_market
        assert get_health()["overall"] == "PASS"
        assert get_regression()["overall"] == "PASS"
        assert get_story("T4")["chapters"] == 1
        assert get_voice("Aria")["voice"] == "Aria"
        assert "NO real money" in get_market()["message"]
        print("TEST v4_old_api_still_ok: PASS - All 5 old APIs still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_old_api_still_ok: FAIL - {e}")
        return "FAIL"

def test_v4_no_fake():
    try:
        lt = (BASE / "ui" / "UI_LIMITATIONS.md").read_text()
        assert "NOT Android APK" in lt and "In-memory only" in lt
        t = (BASE / "ui" / "dashboard.html").read_text().lower()
        assert "no apk" in t
        print("TEST v4_no_fake: PASS - Honest: NO APK, in-memory analytics")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_no_fake: FAIL - {e}")
        return "FAIL"

def test_v4_playground_still_ok():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["MINI APP PLAYGROUND", "createStory()", "tryVoice()", "buyItem()"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v4_playground_still_ok: PASS - V3 Playground still present")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_playground_still_ok: FAIL - {e}")
        return "FAIL"

def test_v4_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST v4_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST v4_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v4_theme_ui, test_v4_analytics_ui, test_v4_server_analytics, test_v4_analytics_real, test_v4_old_api_still_ok, test_v4_no_fake, test_v4_playground_still_ok, test_v4_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 6 STEP 4 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase6_4_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
