# BH-OMNI CORE - Phase 6 Step 3 - Playground - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

def test_v3_playground_ui():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text()
        for kw in ["MINI APP PLAYGROUND", "createStory()", "tryVoice()", "buyItem()", "Playground V3"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v3_playground_ui: PASS - Playground + 3 buttons present")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_playground_ui: FAIL - {e}")
        return "FAIL"

def test_v3_server_endpoints():
    try:
        t = (BASE / "ui" / "server.py").read_text()
        for kw in ["/api/story", "/api/voice", "/api/market", "get_story", "get_voice", "get_market"]:
            assert kw in t, f"Missing: {kw}"
        print("TEST v3_server_endpoints: PASS - 3 new API endpoints present")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_server_endpoints: FAIL - {e}")
        return "FAIL"

def test_v3_story_real():
    try:
        from ui.server import get_story
        r = get_story("Test Story")
        assert "story_id" in r and r["title"] == "Test Story" and r["chapters"] == 1, f"Bad: {r}"
        print(f"TEST v3_story_real: PASS - REAL StoryEngine: {r['title']} chapters={r['chapters']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_story_real: FAIL - {e}")
        return "FAIL"

def test_v3_voice_real():
    try:
        from ui.server import get_voice
        r = get_voice("Aria")
        assert r["voice"] == "Aria" and "NO real TTS" in r["note"], f"Bad: {r}"
        print(f"TEST v3_voice_real: PASS - REAL VoiceEngine metadata: {r['voice']} - {r['note']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_voice_real: FAIL - {e}")
        return "FAIL"

def test_v3_market_real():
    try:
        from ui.server import get_market
        r = get_market()
        assert "NO real money" in r["message"], f"Bad: {r}"
        print(f"TEST v3_market_real: PASS - REAL Marketplace: {r['message']}")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_market_real: FAIL - {e}")
        return "FAIL"

def test_v3_old_api_still_ok():
    try:
        from ui.server import get_health, get_regression
        assert get_health()["overall"] == "PASS"
        assert get_regression()["overall"] == "PASS"
        print("TEST v3_old_api_still_ok: PASS - Old /api/health + /api/regression still work")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_old_api_still_ok: FAIL - {e}")
        return "FAIL"

def test_v3_no_fake():
    try:
        t = (BASE / "ui" / "dashboard.html").read_text().lower()
        assert "no apk" in t
        lt = (BASE / "ui" / "UI_LIMITATIONS.md").read_text()
        assert "NO real TTS" in lt and "NO real money" in lt
        print("TEST v3_no_fake: PASS - Honest: NO APK, NO real TTS, NO real money")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_no_fake: FAIL - {e}")
        return "FAIL"

def test_v3_server_imports():
    try:
        from ui.server import start_server
        assert callable(start_server)
        print("TEST v3_server_imports: PASS - start_server importable")
        return "PASS"
    except Exception as e:
        print(f"TEST v3_server_imports: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_v3_playground_ui, test_v3_server_endpoints, test_v3_story_real, test_v3_voice_real, test_v3_market_real, test_v3_old_api_still_ok, test_v3_no_fake, test_v3_server_imports]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 6 STEP 3 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase6_3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
