# BH-OMNI CORE - Phase 7 Step 1 - AI Chat - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v7_chat_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["AI CHAT", "sendChat()", "chatInput", "chatHistory", "/api/chat", "NOT real LLM"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v7_chat_ui: PASS - Chat card + input + history + honest note")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_chat_ui: FAIL - {e}")
        return "FAIL"

def test_v7_server_chat():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/chat", "get_chat", "ContextManager", "ModelRouter", "AIEvaluation"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v7_server_chat: PASS - /api/chat uses Context + Router + Eval")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_server_chat: FAIL - {e}")
        return "FAIL"

def test_v7_chat_hello():
    try:
        from ui.server import get_chat
        r = get_chat("Hello BH-OMNI!")
        assert "reply" in r and len(r["reply"]) > 0, f"Bad: {r}"
        assert "Vanakkam" in r["reply"] or "BH-OMNI" in r["reply"]
        print(f"TEST v7_chat_hello: PASS - Reply: {r['reply'][:60]}... Score={r['score']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_chat_hello: FAIL - {e}")
        return "FAIL"

def test_v7_chat_help():
    try:
        from ui.server import get_chat
        r = get_chat("help")
        assert "help" in r["reply"].lower() or "Story" in r["reply"]
        print(f"TEST v7_chat_help: PASS - Help reply works")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_chat_help: FAIL - {e}")
        return "FAIL"

def test_v7_chat_score():
    try:
        from ui.server import get_chat
        r = get_chat("What is your score?")
        assert isinstance(r["score"], int) and 0 <= r["score"] <= 100, f"Bad score: {r}"
        assert "NOT real LLM" in r["note"]
        print(f"TEST v7_chat_score: PASS - Rule-based score={r['score']}/100, honest note")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_chat_score: FAIL - {e}")
        return "FAIL"

def test_v7_chat_no_fake_llm():
    try:
        lt = (BASE / "ui" / "PHASE7_LIMITATIONS.md").read_text()
        assert "NOT real LLM" in lt and "NO OpenAI" in lt
        t = (BASE / "ui" / "dashboard.html").read_text()
        assert "NOT real LLM" in t
        print("TEST v7_chat_no_fake_llm: PASS - Honest: NOT real LLM, NO OpenAI")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_chat_no_fake_llm: FAIL - {e}")
        return "FAIL"

def test_v7_old_api_still_ok():
    try:
        from ui.server import get_health, get_regression, get_story, get_ads, get_export
        assert get_health()["overall"] == "PASS"
        assert get_regression()["overall"] == "PASS"
        assert get_story("ChatTest")["chapters"] == 1
        assert get_ads(action="show")["label"] == "SPONSORED"
        assert "NO secrets" in get_export()["note"]
        print("TEST v7_old_api_still_ok: PASS - All old APIs still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_old_api_still_ok: FAIL - {e}")
        return "FAIL"

def test_v7_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST v7_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST v7_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v7_chat_ui, test_v7_server_chat, test_v7_chat_hello, test_v7_chat_help, test_v7_chat_score, test_v7_chat_no_fake_llm, test_v7_old_api_still_ok, test_v7_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 7 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase7_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
