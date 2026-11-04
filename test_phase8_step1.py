# BH-OMNI CORE - Phase 8 Step 1 - SAME PROJECT - OMNI Merged - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_p8_same_project_file():
    try:
        p = BASE / "omni_infinity.py"
        assert p.exists(), "omni_infinity.py missing - SAME PROJECT file!"
        t = p.read_text()
        assert "OMNI_REPLIES" in t and "KADHAIKAL" in t and "QUIZ_QS" in t
        print(f"TEST p8_same_project_file: PASS - omni_infinity.py in SAME PROJECT ({len(t)} chars)")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_same_project_file: FAIL - {e}")
        return "FAIL"

def test_p8_omni_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["OMNI INFINITY", "sendOmni()", "omniInput", "omniHistory", "/api/omni", "SAME PROJECT"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST p8_omni_ui: PASS - OMNI INFINITY card in SAME dashboard")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_omni_ui: FAIL - {e}")
        return "FAIL"

def test_p8_server_omni():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/omni", "get_omni", "omni_infinity"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST p8_server_omni: PASS - /api/omni uses omni_infinity.py")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_server_omni: FAIL - {e}")
        return "FAIL"

def test_p8_omni_hello():
    try:
        from ui.server import get_omni
        r = get_omni("hello")
        assert "OMNI" in r["reply"] or "Vanakkam" in r["reply"], f"Bad: {r}"
        assert "SAME PROJECT" in r["source"]
        print(f"TEST p8_omni_hello: PASS - Reply: {r['reply'][:60]}...")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_omni_hello: FAIL - {e}")
        return "FAIL"

def test_p8_omni_kadhai():
    try:
        from ui.server import get_omni
        r = get_omni("kadhai")
        assert "Kadhai" in r["reply"], f"Bad: {r}"
        print("TEST p8_omni_kadhai: PASS - OMNI INFINITY kadhai via Dashboard API!")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_omni_kadhai: FAIL - {e}")
        return "FAIL"

def test_p8_omni_quiz_search():
    try:
        from ui.server import get_omni
        q = get_omni("quiz")
        assert "QUIZ" in q["reply"], f"Quiz fail: {q}"
        s = get_omni("search story")
        assert "Found" in s["reply"], f"Search fail: {s}"
        print("TEST p8_omni_quiz_search: PASS - Quiz + Search via SAME PROJECT API!")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_omni_quiz_search: FAIL - {e}")
        return "FAIL"

def test_p8_omni_no_fake():
    try:
        lt = (BASE / "ui" / "PHASE8_LIMITATIONS.md").read_text()
        assert "SAME PROJECT" in lt and "NOT real LLM" in lt
        print("TEST p8_omni_no_fake: PASS - SAME PROJECT + Honest: NOT real LLM")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_omni_no_fake: FAIL - {e}")
        return "FAIL"

def test_p8_old_still_ok():
    try:
        from ui.server import get_chat, get_search, get_recommend, get_quiz, get_health
        assert "Vanakkam" in get_chat("hello")["reply"]
        assert len(get_search("story")["results"]) >= 1
        assert len(get_recommend("demo")["recommendations"]) >= 3
        assert get_quiz("start")["qid"] == "Q1"
        assert get_health()["overall"] == "PASS"
        print("TEST p8_old_still_ok: PASS - Chat + Search + Recommend + Quiz + Health still work - SAME PROJECT intact!")
        return "PASS"
    except Exception as e:
        print(f"TEST p8_old_still_ok: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_p8_same_project_file, test_p8_omni_ui, test_p8_server_omni, test_p8_omni_hello, test_p8_omni_kadhai, test_p8_omni_quiz_search, test_p8_omni_no_fake, test_p8_old_still_ok]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 8 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase8_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
