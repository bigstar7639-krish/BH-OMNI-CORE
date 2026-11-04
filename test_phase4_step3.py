# BH-OMNI CORE - Phase 4 Step 3 - Full Regression - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from integration.full_regression import run_regression

def test_regression_overall():
    try:
        r = run_regression()
        assert r["overall"] == "PASS", f"Regression FAIL: {r}"
        assert r["passed"] == 8
        print(f"TEST regression_overall: PASS - {r['passed']}/{r['total']} checks PASS")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_overall: FAIL - {e}")
        return "FAIL"

def test_regression_p1():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P1-Permissions"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p1: PASS - Phase 1 Permissions ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p1: FAIL - {e}")
        return "FAIL"

def test_regression_p2():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P2-Registry+Gateway"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p2: PASS - Phase 2 Registry+Gateway ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p2: FAIL - {e}")
        return "FAIL"

def test_regression_p3f():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P3F-Voice+Story"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p3f: PASS - System F ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p3f: FAIL - {e}")
        return "FAIL"

def test_regression_p3g():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P3G-Ads+Monetization"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p3g: PASS - System G ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p3g: FAIL - {e}")
        return "FAIL"

def test_regression_p3h():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P3H-Analytics+Insights"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p3h: PASS - System H ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p3h: FAIL - {e}")
        return "FAIL"

def test_regression_p3i_j():
    try:
        r = run_regression()
        for n in ["P3I-Sync+Backup", "P3J-Marketplace+Creator"]:
            c = [x for x in r["checks"] if x["name"] == n][0]
            assert c["status"] == "PASS", f"{n} FAIL"
        print("TEST regression_p3i_j: PASS - System I + J ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p3i_j: FAIL - {e}")
        return "FAIL"

def test_regression_p4():
    try:
        r = run_regression()
        c = [x for x in r["checks"] if x["name"] == "P4-Orchestrator+SecureGateway"][0]
        assert c["status"] == "PASS"
        print("TEST regression_p4: PASS - Phase 4 Integration ok")
        return "PASS"
    except Exception as e:
        print(f"TEST regression_p4: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_regression_overall, test_regression_p1, test_regression_p2, test_regression_p3f, test_regression_p3g, test_regression_p3h, test_regression_p3i_j, test_regression_p4]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 4 STEP 3 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase4_3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
