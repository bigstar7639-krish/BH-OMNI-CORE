# BH-OMNI CORE - Phase 7 Step 5 - FINALE - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_finale7_version():
    try:
        v = (BASE / "VERSION.txt").read_text().strip()
        assert "v0.7.0" in v and "270" in v, f"Bad version: {v}"
        print(f"TEST finale7_version: PASS - {v}")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_version: FAIL - {e}")
        return "FAIL"

def test_finale7_complete_doc():
    try:
        t = (BASE / "ui" / "PHASE7_COMPLETE.md").read_text()
        assert "Phase 7 COMPLETE" in t and "270 PASS" in t and "NOT real LLM" in t
        print("TEST finale7_complete_doc: PASS - PHASE7_COMPLETE.md honest + complete")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_complete_doc: FAIL - {e}")
        return "FAIL"

def test_finale7_dashboard_all():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["AI CHAT", "SMART SEARCH", "SMART RECOMMENDATIONS", "MINI QUIZ", "262 PASS", "PHASE 7 COMPLETE"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST finale7_dashboard_all: PASS - All 4 Phase 7 sections + 262 PASS + FINALE")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_dashboard_all: FAIL - {e}")
        return "FAIL"

def test_finale7_all_12_apis():
    try:
        from ui.server import get_health, get_regression, get_story, get_voice, get_market, get_analytics, get_ads, get_export, get_chat, get_search, get_recommend, get_quiz
        assert get_health()["overall"] == "PASS"
        assert get_regression()["overall"] == "PASS"
        assert get_story("Finale7")["chapters"] == 1
        assert get_voice("Aria")["voice"] == "Aria"
        assert "NO real money" in get_market()["message"]
        assert get_analytics(track=True)["total_events"] >= 1
        assert get_ads(action="show")["label"] == "SPONSORED"
        assert "NO secrets" in get_export()["note"]
        assert "Vanakkam" in get_chat("hello")["reply"]
        assert len(get_search("story")["results"]) >= 1
        assert len(get_recommend("demo")["recommendations"]) >= 3
        q = get_quiz("start")
        assert q["qid"] == "Q1" and len(q["options"]) == 4
        print("TEST finale7_all_12_apis: PASS - All 12 APIs work!")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_all_12_apis: FAIL - {e}")
        return "FAIL"

def test_finale7_server_endpoints():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/health", "/api/regression", "/api/story", "/api/voice", "/api/market", "/api/analytics", "/api/ads", "/api/export", "/api/chat", "/api/search", "/api/recommend", "/api/quiz"]:
            assert kw in t, f"Missing endpoint: {kw}"
        print("TEST finale7_server_endpoints: PASS - All 12 endpoints in server.py")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_server_endpoints: FAIL - {e}")
        return "FAIL"

def test_finale7_no_fake():
    try:
        lt = (BASE / "ui" / "PHASE7_LIMITATIONS.md").read_text()
        assert "NOT real LLM" in lt and "NOT vector" in lt and "NOT ML" in lt
        print("TEST finale7_no_fake: PASS - Honest limitations intact")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_no_fake: FAIL - {e}")
        return "FAIL"

def test_finale7_health_regression():
    try:
        from release.health_check import health_check
        from integration.full_regression import run_regression
        assert health_check()["overall"] == "PASS"
        assert run_regression()["overall"] == "PASS"
        print("TEST finale7_health_regression: PASS - Health 16/16 + Regression 8/8")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_health_regression: FAIL - {e}")
        return "FAIL"

def test_finale7_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST finale7_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST finale7_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_finale7_version, test_finale7_complete_doc, test_finale7_dashboard_all, test_finale7_all_12_apis, test_finale7_server_endpoints, test_finale7_no_fake, test_finale7_health_regression, test_finale7_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 7 STEP 5 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase7_5_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
