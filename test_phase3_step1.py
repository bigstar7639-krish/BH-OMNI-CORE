# BH-OMNI CORE - Phase 3 Step 1 - System F - Voice + Story - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from systems_fj.voice_engine import VoiceEngine, VoiceError
from systems_fj.story_engine import StoryEngine, StoryError

def test_voice_synthesize():
    try:
        v = VoiceEngine()
        r = v.synthesize("Vanakkam Chennai!", voice="tamil-female", speed=1.0)
        assert r["voice"] == "tamil-female" and r["duration_sec"] > 0
        assert r["audio_file"] is None  # Honest - no fake audio
        print(f"TEST voice_synthesize: PASS - Duration {r['duration_sec']}s, metadata only")
        return "PASS"
    except Exception as e:
        print(f"TEST voice_synthesize: FAIL - {e}")
        return "FAIL"

def test_voice_list():
    try:
        v = VoiceEngine()
        voices = v.list_voices()
        assert "tamil-female" in voices and len(voices) >= 4
        print(f"TEST voice_list: PASS - {len(voices)} voices")
        return "PASS"
    except Exception as e:
        print(f"TEST voice_list: FAIL - {e}")
        return "FAIL"

def test_voice_invalid():
    try:
        v = VoiceEngine()
        try:
            v.synthesize("hi", voice="alien-voice")
            print("TEST voice_invalid: FAIL - Bad voice should fail")
            return "FAIL"
        except VoiceError:
            pass
        try:
            v.synthesize("   ")
            print("TEST voice_invalid: FAIL - Empty should fail")
            return "FAIL"
        except VoiceError:
            pass
        try:
            v.synthesize("hi", speed=5.0)
            print("TEST voice_invalid: FAIL - Bad speed should fail")
            return "FAIL"
        except VoiceError:
            print("TEST voice_invalid: PASS - Invalid voice/text/speed rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST voice_invalid: FAIL - {e}")
        return "FAIL"

def test_voice_speed_duration():
    try:
        v = VoiceEngine()
        r1 = v.synthesize("x"*800, speed=1.0)
        r2 = v.synthesize("x"*800, speed=2.0)
        assert r2["duration_sec"] < r1["duration_sec"], "Faster speed = shorter duration"
        print(f"TEST voice_speed_duration: PASS - 1.0x {r1['duration_sec']}s vs 2.0x {r2['duration_sec']}s")
        return "PASS"
    except Exception as e:
        print(f"TEST voice_speed_duration: FAIL - {e}")
        return "FAIL"

def test_story_create():
    try:
        s = StoryEngine()
        assert s.create("Chennai Hero", "fantasy", "tanglish") == True
        assert "Chennai Hero" in s.list_stories()
        print("TEST story_create: PASS - Story created")
        return "PASS"
    except Exception as e:
        print(f"TEST story_create: FAIL - {e}")
        return "FAIL"

def test_story_chapter():
    try:
        s = StoryEngine()
        s.create("My Story", "thriller")
        s.add_chapter("My Story", "Chapter 1 - Start", "Once upon a time in Chennai...")
        info = s.get_story("My Story")
        assert info["chapters"] == 1 and info["total_chars"] > 0
        print(f"TEST story_chapter: PASS - 1 chapter, {info['total_chars']} chars")
        return "PASS"
    except Exception as e:
        print(f"TEST story_chapter: FAIL - {e}")
        return "FAIL"

def test_story_duplicate():
    try:
        s = StoryEngine()
        s.create("Dup Story", "comedy")
        try:
            s.create("Dup Story", "comedy")
            print("TEST story_duplicate: FAIL - Duplicate should fail")
            return "FAIL"
        except StoryError:
            print("TEST story_duplicate: PASS - Duplicate rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST story_duplicate: FAIL - {e}")
        return "FAIL"

def test_story_invalid():
    try:
        s = StoryEngine()
        try:
            s.create("Bad", "unknown-genre")
            print("TEST story_invalid: FAIL - Bad genre should fail")
            return "FAIL"
        except StoryError:
            pass
        try:
            s.add_chapter("No Story", "Ch1", "content")
            print("TEST story_invalid: FAIL - Missing story should fail")
            return "FAIL"
        except StoryError:
            print("TEST story_invalid: PASS - Invalid genre/missing story rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST story_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_voice_synthesize, test_voice_list, test_voice_invalid, test_voice_speed_duration, test_story_create, test_story_chapter, test_story_duplicate, test_story_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 3 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase3_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
