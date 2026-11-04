# BH-OMNI CORE - Phase 7 Step 2 - Smart Search - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v8_search_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["SMART SEARCH", "doSearch()", "searchInput", "searchResults", "/api/search"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v8_search_ui: PASS - Search card + input + results")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_ui: FAIL - {e}")
        return "FAIL"

def test_v8_server_search():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/search", "get_search", "FeatureRegistry", "Marketplace"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v8_server_search: PASS - /api/search uses Registry + Marketplace")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_server_search: FAIL - {e}")
        return "FAIL"

def test_v8_search_story():
    try:
        from ui.server import get_search
        r = get_search("story")
        assert len(r["results"]) >= 1, f"No results: {r}"
        assert any("Story" in x["title"] for x in r["results"]), f"Story not found: {r}"
        print(f"TEST v8_search_story: PASS - Found {len(r['results'])} result(s), top: {r['results'][0]['title']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_story: FAIL - {e}")
        return "FAIL"

def test_v8_search_voice_market():
    try:
        from ui.server import get_search
        r = get_search("voice")
        assert len(r["results"]) >= 2, f"Expected >=2 (feature+market): {r}"
        types = set(x["type"] for x in r["results"])
        assert "FEATURE" in types and "MARKET" in types, f"Need both types: {types}"
        print(f"TEST v8_search_voice_market: PASS - FEATURE + MARKET both found")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_voice_market: FAIL - {e}")
        return "FAIL"

def test_v8_search_ranking():
    try:
        from ui.server import get_search
        r = get_search("vault")
        assert r["results"][0]["score"] >= r["results"][-1]["score"], "Not sorted!"
        assert "Vault" in r["results"][0]["title"] or "vault" in r["results"][0]["title"].lower()
        print(f"TEST v8_search_ranking: PASS - Sorted by score, top={r['results'][0]['title']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_ranking: FAIL - {e}")
        return "FAIL"

def test_v8_search_no_results():
    try:
        from ui.server import get_search
        r = get_search("zzzzqqqxxx")
        assert len(r["results"]) == 0, f"Should be empty: {r}"
        print("TEST v8_search_no_results: PASS - Unknown query = 0 results (no fake)")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_no_results: FAIL - {e}")
        return "FAIL"

def test_v8_search_no_fake_ml():
    try:
        lt = (BASE / "ui" / "PHASE7_LIMITATIONS.md").read_text()
        assert "NOT vector" in lt and "NOT ML" in lt
        print("TEST v8_search_no_fake_ml: PASS - Honest: NOT vector, NOT ML")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_search_no_fake_ml: FAIL - {e}")
        return "FAIL"

def test_v8_chat_still_ok():
    try:
        from ui.server import get_chat, get_health, get_search
        c = get_chat("hello")
        assert "Vanakkam" in c["reply"]
        assert get_health()["overall"] == "PASS"
        print("TEST v8_chat_still_ok: PASS - Chat + Health still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v8_chat_still_ok: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v8_search_ui, test_v8_server_search, test_v8_search_story, test_v8_search_voice_market, test_v8_search_ranking, test_v8_search_no_results, test_v8_search_no_fake_ml, test_v8_chat_still_ok]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 7 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase7_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
