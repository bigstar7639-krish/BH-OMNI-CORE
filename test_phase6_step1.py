# BH-OMNI CORE - Phase 6 Step 1 - Dashboard UI - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_dashboard_exists():
    try:
        p = BASE / "ui" / "dashboard.html"
        assert p.exists(), "dashboard.html missing!"
        print("TEST dashboard_exists: PASS - ui/dashboard.html found")
        return "PASS"
    except Exception as e:
        print(f"TEST dashboard_exists: FAIL - {e}")
        return "FAIL"

def test_dashboard_content():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["BH-OMNI CORE", "182 PASS", "Phase 1", "Phase 5", "Honest Limitations"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST dashboard_content: PASS - All sections present (182 PASS + Limitations)")
        return "PASS"
    except Exception as e:
        print(f"TEST dashboard_content: FAIL - {e}")
        return "FAIL"

def test_dashboard_no_fake_claims():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text().lower()
        # Must NOT claim APK built
        assert "apk built" not in t or "no apk" in t, "Fake APK claim!"
        assert "no apk" in t, "Must say NO APK yet!"
        print("TEST dashboard_no_fake_claims: PASS - Honest: NO APK claim")
        return "PASS"
    except Exception as e:
        print(f"TEST dashboard_no_fake_claims: FAIL - {e}")
        return "FAIL"

def test_server_exists():
    try:
        p = BASE / "ui" / "server.py"
        assert p.exists()
        t = p.read_text()
        assert "8000" in t and "ThreadingHTTPServer" in t
        print("TEST server_exists: PASS - ui/server.py found, port 8000")
        return "PASS"
    except Exception as e:
        print(f"TEST server_exists: FAIL - {e}")
        return "FAIL"

def test_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST server_imports: FAIL - {e}")
        return "FAIL"

def test_ui_limitations():
    try:
        t = (BASE / "ui" / "UI_LIMITATIONS.md").read_text()
        assert "NOT Android APK" in t
        print("TEST ui_limitations: PASS - UI_LIMITATIONS.md honest")
        return "PASS"
    except Exception as e:
        print(f"TEST ui_limitations: FAIL - {e}")
        return "FAIL"

def test_health_still_ok():
    try:
        from release.health_check import health_check
        r = health_check()
        assert r["overall"] == "PASS"
        print(f"TEST health_still_ok: PASS - {r['ok']}/{r['total']} modules OK")
        return "PASS"
    except Exception as e:
        print(f"TEST health_still_ok: FAIL - {e}")
        return "FAIL"

def test_regression_still_ok():
    try:
        from integration.full_regression import run_regression
        r = run_regression()
        assert r["overall"] == "PASS"
        print(f"TEST regression_still_ok: PASS - Regression {r['passed']}/{r['total']} OK")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_still_ok: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_dashboard_exists, test_dashboard_content, test_dashboard_no_fake_claims, test_server_exists, test_server_imports, test_ui_limitations, test_health_still_ok, test_regression_still_ok]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 6 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase6_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
