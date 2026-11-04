# BH-OMNI CORE - Phase 5 Step 2 - Final Verify - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from release.final_verify import final_verify

def test_final_overall():
    try:
        r = final_verify(str(BASE))
        if r["overall"] != "PASS":
            for c in r["checks"]:
                if c["status"] == "FAIL":
                    print(f"  FAIL: {c['name']} - {c['detail']}")
            print(f"TEST final_overall: FAIL - {r['passed']}/{r['total']} PASS")
            return "FAIL"
        print(f"TEST final_overall: PASS - {r['passed']}/{r['total']} checks PASS")
        return "PASS"
    except Exception as e:
        print(f"TEST final_overall: FAIL - {e}")
        return "FAIL"

def test_final_gitignore():
    try:
        r = final_verify(str(BASE))
        for n in ["gitignore_exists", "gitignore_blocks_vault", "gitignore_blocks_pycache"]:
            c = [x for x in r["checks"] if x["name"] == n][0]
            assert c["status"] == "PASS", f"{n} FAIL: {c['detail']}"
        print("TEST final_gitignore: PASS - .gitignore blocks vault + pycache")
        return "PASS"
    except Exception as e:
        print(f"TEST final_gitignore: FAIL - {e}")
        return "FAIL"

def test_final_no_secrets():
    try:
        r = final_verify(str(BASE))
        c = [x for x in r["checks"] if x["name"] == "no_vault_data"][0]
        assert c["status"] == "PASS", c["detail"]
        print("TEST final_no_secrets: PASS - No vault_data.json in repo")
        return "PASS"
    except Exception as e:
        print(f"TEST final_no_secrets: FAIL - {e}")
        return "FAIL"

def test_final_docs():
    try:
        r = final_verify(str(BASE))
        for n in ["version_exists", "readme_exists"]:
            c = [x for x in r["checks"] if x["name"] == n][0]
            assert c["status"] == "PASS"
        print("TEST final_docs: PASS - VERSION + README exist")
        return "PASS"
    except Exception as e:
        print(f"TEST final_docs: FAIL - {e}")
        return "FAIL"

def test_final_folders():
    try:
        r = final_verify(str(BASE))
        for folder in ["security", "core", "systems_fj", "integration", "release"]:
            c = [x for x in r["checks"] if x["name"] == f"folder_{folder}"][0]
            assert c["status"] == "PASS", f"{folder} missing"
        print("TEST final_folders: PASS - All 5 folders exist")
        return "PASS"
    except Exception as e:
        print(f"TEST final_folders: FAIL - {e}")
        return "FAIL"

def test_final_test_count():
    try:
        r = final_verify(str(BASE))
        c = [x for x in r["checks"] if x["name"] == "test_files_count"][0]
        assert c["status"] == "PASS", c["detail"]
        print(f"TEST final_test_count: PASS - {c['detail']}")
        return "PASS"
    except Exception as e:
        print(f"TEST final_test_count: FAIL - {e}")
        return "FAIL"

def test_final_health_still_ok():
    try:
        from release.health_check import health_check
        r = health_check()
        assert r["overall"] == "PASS", f"Missing: {r['missing_modules']}"
        print(f"TEST final_health_still_ok: PASS - {r['ok']}/{r['total']} modules OK")
        return "PASS"
    except Exception as e:
        print(f"TEST final_health_still_ok: FAIL - {e}")
        return "FAIL"

def test_final_regression_still_ok():
    try:
        from integration.full_regression import run_regression
        r = run_regression()
        assert r["overall"] == "PASS", f"Regression FAIL: {r}"
        print(f"TEST final_regression_still_ok: PASS - Regression {r['passed']}/{r['total']} OK")
        return "PASS"
    except Exception as e:
        print(f"TEST final_regression_still_ok: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_final_overall, test_final_gitignore, test_final_no_secrets, test_final_docs, test_final_folders, test_final_test_count, test_final_health_still_ok, test_final_regression_still_ok]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 5 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase5_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
