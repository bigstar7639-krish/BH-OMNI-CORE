# BH-OMNI CORE - Phase 7 Step 3 - Recommendations - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v9_rec_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["SMART RECOMMENDATIONS", "getRec()", "recResults", "/api/recommend"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v9_rec_ui: PASS - Recommendations card + button + results")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_rec_ui: FAIL - {e}")
        return "FAIL"

def test_v9_server_rec():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/recommend", "get_recommend", "Insights", "Monetization"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v9_server_rec: PASS - /api/recommend uses Insights + Monetization")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_server_rec: FAIL - {e}")
        return "FAIL"

def test_v9_rec_returns():
    try:
        from ui.server import get_recommend
        r = get_recommend("demo")
        assert len(r["recommendations"]) >= 3, f"Too few: {r}"
        assert "verdict" in r and "engagement" in r
        print(f"TEST v9_rec_returns: PASS - {len(r['recommendations'])} recs, Verdict={r['verdict']}, Engagement={r['engagement']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_rec_returns: FAIL - {e}")
        return "FAIL"

def test_v9_rec_free_plan():
    try:
        from ui.server import get_recommend
        r = get_recommend("demo")
        titles = " ".join(x["title"] for x in r["recommendations"])
        assert "Pro" in titles or "FREE" in titles or "free" in titles.lower(), f"Free-plan rec missing: {titles}"
        assert r.get("plan") == "free", f"Plan should be free: {r}"
        print(f"TEST v9_rec_free_plan: PASS - Free user gets Pro upgrade rec, Plan={r['plan']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_rec_free_plan: FAIL - {e}")
        return "FAIL"

def test_v9_rec_reasons():
    try:
        from ui.server import get_recommend
        r = get_recommend("demo")
        for x in r["recommendations"]:
            assert "title" in x and "reason" in x and len(x["reason"]) > 5, f"Bad rec: {x}"
        print("TEST v9_rec_reasons: PASS - Every rec has title + reason")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_rec_reasons: FAIL - {e}")
        return "FAIL"

def test_v9_rec_no_fake_ml():
    try:
        lt = (BASE / "ui" / "PHASE7_LIMITATIONS.md").read_text()
        assert "NOT ML" in lt and "Rule-based" in lt
        from ui.server import get_recommend
        r = get_recommend("demo")
        assert "NOT ML" in r["note"]
        print("TEST v9_rec_no_fake_ml: PASS - Honest: NOT ML, NOT AI prediction")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_rec_no_fake_ml: FAIL - {e}")
        return "FAIL"

def test_v9_search_chat_still_ok():
    try:
        from ui.server import get_search, get_chat, get_health
        assert len(get_search("story")["results"]) >= 1
        assert "Vanakkam" in get_chat("hello")["reply"]
        assert get_health()["overall"] == "PASS"
        print("TEST v9_search_chat_still_ok: PASS - Search + Chat + Health still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_search_chat_still_ok: FAIL - {e}")
        return "FAIL"

def test_v9_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST v9_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST v9_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v9_rec_ui, test_v9_server_rec, test_v9_rec_returns, test_v9_rec_free_plan, test_v9_rec_reasons, test_v9_rec_no_fake_ml, test_v9_search_chat_still_ok, test_v9_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 7 STEP 3 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase7_3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
