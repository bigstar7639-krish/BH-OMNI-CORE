# BH-OMNI CORE - Phase 4 Step 1 - Integration Orchestrator - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.feature_registry import FeatureRegistry
from systems_fj.story_engine import StoryEngine
from systems_fj.voice_engine import VoiceEngine
from systems_fj.marketplace import Marketplace
from integration.app_orchestrator import AppOrchestrator, IntegrationError

def make_orch():
    return AppOrchestrator(FeatureRegistry(), StoryEngine(), VoiceEngine(), Marketplace())

def test_integration_full_flow():
    try:
        o = make_orch()
        r = o.publish_story_with_voice("Chennai Hero", "fantasy", "Ch1 - Start", "Once upon a time in Chennai, a hero woke up...", "tamil-female", "krish", 50)
        assert r["status"] == "published" and r["feature_id"] == "F-101"
        assert r["voice_duration_sec"] > 0 and r["market_item"] == "chennai-hero"
        print(f"TEST integration_full_flow: PASS - Flow {r['flow']}, voice {r['voice_duration_sec']}s, market {r['market_item']}")
        return "PASS"
    except Exception as e:
        print(f"TEST integration_full_flow: FAIL - {e}")
        return "FAIL"

def test_integration_two_flows():
    try:
        o = make_orch()
        o.publish_story_with_voice("Story One", "comedy", "Ch1", "Funny story content here", "tamil-male", "krish", 10)
        r2 = o.publish_story_with_voice("Story Two", "thriller", "Ch1", "Thriller story content here", "english-female", "krish", 20)
        assert r2["feature_id"] == "F-102" and o.flow_count() == 2
        print("TEST integration_two_flows: PASS - 2 flows, F-101 + F-102")
        return "PASS"
    except Exception as e:
        print(f"TEST integration_two_flows: FAIL - {e}")
        return "FAIL"

def test_integration_invalid_genre_fails():
    try:
        o = make_orch()
        try:
            o.publish_story_with_voice("Bad Story", "bad-genre", "Ch1", "content here", "tamil-female", "krish", 10)
            print("TEST integration_invalid_genre_fails: FAIL - Bad genre should fail whole flow")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_invalid_genre_fails: PASS - Bad genre fails whole flow")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_invalid_genre_fails: FAIL - {e}")
        return "FAIL"

def test_integration_invalid_voice_fails():
    try:
        o = make_orch()
        try:
            o.publish_story_with_voice("Voice Fail", "fantasy", "Ch1", "content here", "alien-voice", "krish", 10)
            print("TEST integration_invalid_voice_fails: FAIL - Bad voice should fail")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_invalid_voice_fails: PASS - Bad voice fails whole flow")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_invalid_voice_fails: FAIL - {e}")
        return "FAIL"

def test_integration_duplicate_story_fails():
    try:
        o = make_orch()
        o.publish_story_with_voice("Dup Story", "fantasy", "Ch1", "content here", "tamil-female", "krish", 10)
        try:
            o.publish_story_with_voice("Dup Story", "fantasy", "Ch1", "content again", "tamil-female", "krish", 10)
            print("TEST integration_duplicate_story_fails: FAIL - Duplicate should fail")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_duplicate_story_fails: PASS - Duplicate story fails")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_duplicate_story_fails: FAIL - {e}")
        return "FAIL"

def test_integration_invalid_price():
    try:
        o = make_orch()
        try:
            o.publish_story_with_voice("Price Fail", "fantasy", "Ch1", "content", "tamil-female", "krish", -5)
            print("TEST integration_invalid_price: FAIL - Negative price should fail")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_invalid_price: PASS - Negative price rejected fail-fast")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_invalid_price: FAIL - {e}")
        return "FAIL"

def test_integration_missing_module():
    try:
        try:
            AppOrchestrator(None, StoryEngine(), VoiceEngine(), Marketplace())
            print("TEST integration_missing_module: FAIL - None module should fail")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_missing_module: PASS - Missing module rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_missing_module: FAIL - {e}")
        return "FAIL"

def test_integration_empty_content():
    try:
        o = make_orch()
        try:
            o.publish_story_with_voice("Empty", "fantasy", "Ch1", "", "tamil-female", "krish", 10)
            print("TEST integration_empty_content: FAIL - Empty content should fail")
            return "FAIL"
        except IntegrationError:
            print("TEST integration_empty_content: PASS - Empty content rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST integration_empty_content: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_integration_full_flow, test_integration_two_flows, test_integration_invalid_genre_fails, test_integration_invalid_voice_fails, test_integration_duplicate_story_fails, test_integration_invalid_price, test_integration_missing_module, test_integration_empty_content]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 4 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase4_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
