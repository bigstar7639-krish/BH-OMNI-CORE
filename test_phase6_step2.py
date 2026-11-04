# BH-OMNI CORE - Phase 6 Step 2 - Interactive Dashboard - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v2_buttons():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["checkHealth()", "checkRegression()", "showModules()", "Interactive V2"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v2_buttons: PASS - 3 buttons + V2 present")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_buttons: FAIL - {e}")
        return "FAIL"

def test_v2_fetch_api():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        assert "/api/health" in t and "/api/regression" in t and "fetch(" in t
        print("TEST v2_fetch_api: PASS - fetch() calls /api/health + /api/regression")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_fetch_api: FAIL - {e}")
        return "FAIL"

def test_v2_server_api():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        assert "/api/health" in t and "/api/regression" in t and "get_health" in t and "get_regression" in t
        print("TEST v2_server_api: PASS - Server handles /api/health + /api/regression")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_server_api: FAIL - {e}")
        return "FAIL"

def test_v2_api_health_real():
    try:
        from ui.server import get_health
        r = get_health()
        assert r["overall"] == "PASS", f"Health FAIL: {r}"
        assert r["ok"] == 16
        print(f"TEST v2_api_health_real: PASS - REAL health {r['ok']}/{r['total']} OK (not fake!)")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_api_health_real: FAIL - {e}")
        return "FAIL"

def test_v2_api_regression_real():
    try:
        from ui.server import get_regression
        r = get_regression()
        assert r["overall"] == "PASS", f"Regression FAIL: {r}"
        print(f"TEST v2_api_regression_real: PASS - REAL regression {r['passed']}/{r['total']} OK")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_api_regression_real: FAIL - {e}")
        return "FAIL"

def test_v2_no_fake():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text().lower()
        assert "no apk" in t
        print("TEST v2_no_fake: PASS - Honest: NO APK claim")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_no_fake: FAIL - {e}")
        return "FAIL"

def test_v2_limitations():
    try:
        t = (BASE / "ui" / "UI_LIMITATIONS.md").read_text()
        assert "NOT Android APK" in t and "/api/health" in t
        print("TEST v2_limitations: PASS - UI_LIMITATIONS.md updated for V2")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_limitations: FAIL - {e}")
        return "FAIL"

def test_v2_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST v2_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST v2_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v2_buttons, test_v2_fetch_api, test_v2_server_api, test_v2_api_health_real, test_v2_api_regression_real, test_v2_no_fake, test_v2_limitations, test_v2_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 6 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase6_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
