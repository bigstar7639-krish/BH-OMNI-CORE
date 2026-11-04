# BH-OMNI CORE - Phase 5 Step 1 - Release Health Check - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from release.health_check import health_check

def test_health_all_ok():
    try:
        r = health_check()
        if r["overall"] != "PASS":
            print(f"Missing modules: {r['missing_modules']}")
            print("TEST health_all_ok: FAIL - Some modules missing, see above")
            return "FAIL"
        print(f"TEST health_all_ok: PASS - {r['ok']}/{r['total']} modules OK")
        return "PASS"
    except Exception as e:
        print(f"TEST health_all_ok: FAIL - {e}")
        return "FAIL"

def test_health_security():
    try:
        r = health_check()
        sec = [x for x in r["details"] if x["module"].startswith("security")]
        assert all(x["status"] == "OK" for x in sec)
        print("TEST health_security: PASS - Security module OK")
        return "PASS"
    except Exception as e:
        print(f"TEST health_security: FAIL - {e}")
        return "FAIL"

def test_health_core():
    try:
        r = health_check()
        core = [x for x in r["details"] if x["module"].startswith("core")]
        assert all(x["status"] == "OK" for x in core)
        print("TEST health_core: PASS - Core modules OK")
        return "PASS"
    except Exception as e:
        print(f"TEST health_core: FAIL - {e}")
        return "FAIL"

def test_health_systems_fj():
    try:
        r = health_check()
        fj = [x for x in r["details"] if x["module"].startswith("systems_fj")]
        assert all(x["status"] == "OK" for x in fj), f"Missing: {[x for x in fj if x['status']!='OK']}"
        print(f"TEST health_systems_fj: PASS - {len(fj)} F-J modules OK (analytics included!)")
        return "PASS"
    except Exception as e:
        print(f"TEST health_systems_fj: FAIL - {e}")
        return "FAIL"

def test_health_integration():
    try:
        r = health_check()
        integ = [x for x in r["details"] if x["module"].startswith("integration")]
        assert all(x["status"] == "OK" for x in integ)
        print("TEST health_integration: PASS - Integration modules OK")
        return "PASS"
    except Exception as e:
        print(f"TEST health_integration: FAIL - {e}")
        return "FAIL"

def test_health_analytics_present():
    try:
        # Specific check for the file that was missing in Termux!
        from systems_fj.analytics import Analytics
        from systems_fj.insights import Insights
        a = Analytics()
        a.track("u1", "app_open")
        assert a.total_events() == 1
        print("TEST health_analytics_present: PASS - analytics.py EXISTS + works!")
        return "PASS"
    except Exception as e:
        print(f"TEST health_analytics_present: FAIL - analytics missing: {e}")
        return "FAIL"

def test_version_file():
    try:
        v = (BASE / "VERSION.txt").read_text().strip()
        assert "BH-OMNI-CORE" in v and "166" in v
        print(f"TEST version_file: PASS - {v}")
        return "PASS"
    except Exception as e:
        print(f"TEST version_file: FAIL - {e}")
        return "FAIL"

def test_readme_file():
    try:
        r = (BASE / "README-BH-OMNI.md").read_text()
        assert "BH-OMNI CORE" in r and "166 PASS" in r and "Honest Limitations" in r
        print("TEST readme_file: PASS - README exists with honest limitations")
        return "PASS"
    except Exception as e:
        print(f"TEST readme_file: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_health_all_ok, test_health_security, test_health_core, test_health_systems_fj, test_health_integration, test_health_analytics_present, test_version_file, test_readme_file]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 5 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase5_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
