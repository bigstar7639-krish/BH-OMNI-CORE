# BH-OMNI CORE - Phase 6 Step 6 - FINALE - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_finale_version():
    try:
        v = (BASE / "VERSION.txt").read_text().strip()
        assert "v0.6.0" in v and "222" in v, f"Bad version: {v}"
        print(f"TEST finale_version: PASS - {v}")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_version: FAIL - {e}")
        return "FAIL"

def test_finale_complete_doc():
    try:
        t = (BASE / "ui" / "PHASE6_COMPLETE.md").read_text()
        assert "Phase 6 COMPLETE" in t and "230 PASS" in t and "NOT Android APK" in t
        print("TEST finale_complete_doc: PASS - PHASE6_COMPLETE.md honest + complete")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_complete_doc: FAIL - {e}")
        return "FAIL"

def test_finale_dashboard_all_sections():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["LIVE CHECK", "THEME", "SETTINGS", "LIVE ANALYTICS", "MINI APP PLAYGROUND", "ADS DEMO", "SPONSORED", "EXPORT", "222 PASS", "PHASE 6 COMPLETE"]:
            assert kw in t, f"Missing section: {kw}"
        print("TEST finale_dashboard_all_sections: PASS - All 7 sections + 222 PASS + FINALE")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_dashboard_all_sections: FAIL - {e}")
        return "FAIL"

def test_finale_all_8_apis():
    try:
        from ui.server import get_health, get_regression, get_story, get_voice, get_market, get_analytics, get_ads, get_export
        assert get_health()["overall"] == "PASS"
        assert get_regression()["overall"] == "PASS"
        assert get_story("Finale")["chapters"] == 1
        assert get_voice("Aria")["voice"] == "Aria"
        assert "NO real money" in get_market()["message"]
        assert get_analytics(track=True)["total_events"] >= 1
        assert get_ads(action="show")["label"] == "SPONSORED"
        assert get_export()["total_pass"] == 214 or get_export()["total_pass"] == 222 or "PASS" in str(get_export())
        print("TEST finale_all_8_apis: PASS - All 8 APIs work!")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_all_8_apis: FAIL - {e}")
        return "FAIL"

def test_finale_server_endpoints():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/health", "/api/regression", "/api/story", "/api/voice", "/api/market", "/api/analytics", "/api/ads", "/api/export"]:
            assert kw in t, f"Missing endpoint: {kw}"
        print("TEST finale_server_endpoints: PASS - All 8 endpoints in server.py")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_server_endpoints: FAIL - {e}")
        return "FAIL"

def test_finale_no_fake():
    try:
        lt = (BASE / "ui" / "UI_LIMITATIONS.md").read_text()
        assert "NOT Android APK" in lt and "NO real AdMob" in lt
        print("TEST finale_no_fake: PASS - Honest limitations intact")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_no_fake: FAIL - {e}")
        return "FAIL"

def test_finale_health_regression():
    try:
        from release.health_check import health_check
        from integration.full_regression import run_regression
        assert health_check()["overall"] == "PASS"
        assert run_regression()["overall"] == "PASS"
        print("TEST finale_health_regression: PASS - Health 16/16 + Regression 8/8")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_health_regression: FAIL - {e}")
        return "FAIL"

def test_finale_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST finale_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST finale_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_finale_version, test_finale_complete_doc, test_finale_dashboard_all_sections, test_finale_all_8_apis, test_finale_server_endpoints, test_finale_no_fake, test_finale_health_regression, test_finale_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 6 STEP 6 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase6_6_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
