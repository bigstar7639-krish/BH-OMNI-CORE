# BH-OMNI CORE - Phase 2 Step 5 - Offline + Eval - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.offline_fallback import OfflineFallback, OfflineError
from core.ai_evaluation import AIEvaluation, EvalError

def test_offline_queue():
    try:
        o = OfflineFallback()
        o.set_online(False)
        assert o.is_online() == False
        r = o.submit("hello", handler=lambda x: "hi", fallback="queued-fallback")
        assert r["status"] == "offline-queued" and r["queued"] == True
        assert o.queue_size() == 1
        print("TEST offline_queue: PASS - Offline queues request")
        return "PASS"
    except Exception as e:
        print(f"TEST offline_queue: FAIL - {e}")
        return "FAIL"

def test_online_processes():
    try:
        o = OfflineFallback()
        o.set_online(True)
        r = o.submit("hello", handler=lambda x: f"echo:{x}")
        assert r["status"] == "online" and r["result"] == "echo:hello"
        assert o.queue_size() == 0
        print("TEST online_processes: PASS - Online processes immediately")
        return "PASS"
    except Exception as e:
        print(f"TEST online_processes: FAIL - {e}")
        return "FAIL"

def test_replay_queued():
    try:
        o = OfflineFallback()
        o.set_online(False)
        o.submit("req1", handler=lambda x: f"done:{x}")
        o.submit("req2", handler=lambda x: f"done:{x}")
        assert o.queue_size() == 2
        o.set_online(True)
        res = o.replay()
        assert res["replayed"] == 2 and o.queue_size() == 0
        assert res["results"][0]["result"] == "done:req1"
        print("TEST replay_queued: PASS - Replay processes queued in order")
        return "PASS"
    except Exception as e:
        print(f"TEST replay_queued: FAIL - {e}")
        return "FAIL"

def test_offline_fallback_response():
    try:
        o = OfflineFallback()
        o.set_online(False)
        r = o.submit("need weather", handler=None, fallback="Offline - Weather unavailable, try later")
        assert "Offline" in r["result"]
        # Replay while offline should fail
        try:
            o.replay()
            print("TEST offline_fallback_response: FAIL - Replay offline should fail")
            return "FAIL"
        except OfflineError:
            print("TEST offline_fallback_response: PASS - Fallback + replay offline blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST offline_fallback_response: FAIL - {e}")
        return "FAIL"

def test_eval_good_high():
    try:
        ev = AIEvaluation()
        r = ev.evaluate("Chennai weather is sunny and warm today, temperature 32 degrees", ["Chennai", "weather", "sunny"])
        assert r["score"] >= 60 and r["passed"] == True
        print(f"TEST eval_good_high: PASS - Good response score {r['score']}")
        return "PASS"
    except Exception as e:
        print(f"TEST eval_good_high: FAIL - {e}")
        return "FAIL"

def test_eval_empty_low():
    try:
        ev = AIEvaluation()
        r = ev.evaluate("   ", ["weather"])
        assert r["score"] == 0 and r["passed"] == False
        print("TEST eval_empty_low: PASS - Empty scores 0")
        return "PASS"
    except Exception as e:
        print(f"TEST eval_empty_low: FAIL - {e}")
        return "FAIL"

def test_eval_secret_flagged():
    try:
        ev = AIEvaluation()
        r = ev.evaluate("Here is password=12345 for you", ["password"])
        assert r["safety"] == 0 and r["passed"] == False and "FAIL-SAFETY" in r["verdict"]
        print("TEST eval_secret_flagged: PASS - Secret leak flagged, safety 0")
        return "PASS"
    except Exception as e:
        print(f"TEST eval_secret_flagged: FAIL - {e}")
        return "FAIL"

def test_eval_invalid_rejected():
    try:
        ev = AIEvaluation()
        try:
            ev.evaluate(None, ["x"])
            print("TEST eval_invalid_rejected: FAIL - None should fail")
            return "FAIL"
        except EvalError:
            pass
        try:
            ev.evaluate("hi", "not-list")
            print("TEST eval_invalid_rejected: FAIL - Non-list keywords should fail")
            return "FAIL"
        except EvalError:
            print("TEST eval_invalid_rejected: PASS - Invalid inputs rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST eval_invalid_rejected: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_offline_queue, test_online_processes, test_replay_queued, test_offline_fallback_response, test_eval_good_high, test_eval_empty_low, test_eval_secret_flagged, test_eval_invalid_rejected]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 2 STEP 5 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase2_5_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
