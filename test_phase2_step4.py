# BH-OMNI CORE - Phase 2 Step 4 - Router + Context - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.model_router import ModelRouter, RouterError
from core.context_manager import ContextManager, ContextError

def test_router_register():
    try:
        r = ModelRouter()
        assert r.register("model-a", ["chat", "voice"], cost_level=2) == True
        assert len(r.list_models()) == 1
        print("TEST router_register: PASS - Model registered")
        return "PASS"
    except Exception as e:
        print(f"TEST router_register: FAIL - {e}")
        return "FAIL"

def test_router_route_capability():
    try:
        r = ModelRouter()
        r.register("cheap-chat", ["chat"], cost_level=1)
        r.register("expensive-chat", ["chat"], cost_level=5)
        r.register("voice-only", ["voice"], cost_level=1)
        chosen = r.route("chat")
        assert chosen["model"] == "cheap-chat", f"Should pick cheapest, got {chosen}"
        chosen2 = r.route("voice")
        assert chosen2["model"] == "voice-only"
        print("TEST router_route_capability: PASS - Picks cheapest capable")
        return "PASS"
    except Exception as e:
        print(f"TEST router_route_capability: FAIL - {e}")
        return "FAIL"

def test_router_no_capable_fails():
    try:
        r = ModelRouter()
        r.register("chat-only", ["chat"], cost_level=1)
        try:
            r.route("image")
            print("TEST router_no_capable_fails: FAIL - Should fail, no image model")
            return "FAIL"
        except RouterError:
            print("TEST router_no_capable_fails: PASS - No capable model fails")
            return "PASS"
    except Exception as e:
        print(f"TEST router_no_capable_fails: FAIL - {e}")
        return "FAIL"

def test_router_duplicate():
    try:
        r = ModelRouter()
        r.register("m1", ["chat"], cost_level=1)
        try:
            r.register("m1", ["chat"], cost_level=2)
            print("TEST router_duplicate: FAIL - Duplicate should fail")
            return "FAIL"
        except RouterError:
            print("TEST router_duplicate: PASS - Duplicate rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST router_duplicate: FAIL - {e}")
        return "FAIL"

def test_router_fallback():
    try:
        r = ModelRouter()
        r.register("default-model", ["chat"], cost_level=2, is_default=True)
        # No image model, but fallback to default
        res = r.route_with_fallback("image")
        assert res["model"] == "default-model" and res.get("fallback") == True
        # No default + no model -> fail
        r2 = ModelRouter()
        try:
            r2.route_with_fallback("image")
            print("TEST router_fallback: FAIL - No default should fail")
            return "FAIL"
        except RouterError:
            print("TEST router_fallback: PASS - Fallback works, no-default fails")
            return "PASS"
    except Exception as e:
        print(f"TEST router_fallback: FAIL - {e}")
        return "FAIL"

def test_context_add_get():
    try:
        c = ContextManager(max_tokens=4000)
        c.add("system", "You are BH-OMNI")
        c.add("user", "Hello")
        c.add("assistant", "Hi there!")
        ctx = c.get_context()
        assert len(ctx) == 3 and ctx[1]["role"] == "user"
        print("TEST context_add_get: PASS - Add + get works")
        return "PASS"
    except Exception as e:
        print(f"TEST context_add_get: FAIL - {e}")
        return "FAIL"

def test_context_trim():
    try:
        c = ContextManager(max_tokens=100)
        c.add("system", "System prompt keep me")
        # Add many large messages - should trim oldest non-system
        for i in range(10):
            c.add("user", "x" * 200)  # ~50 tokens each
            c.add("assistant", "y" * 200)
        # System should still be there
        ctx = c.get_context()
        assert ctx[0]["role"] == "system", "System must be kept"
        assert c.total_tokens() <= 100 or len(ctx) == 1, f"Should trim to limit, tokens {c.total_tokens()}"
        print(f"TEST context_trim: PASS - Trimmed, kept system, tokens {c.total_tokens()}, msgs {len(ctx)}")
        return "PASS"
    except Exception as e:
        print(f"TEST context_trim: FAIL - {e}")
        return "FAIL"

def test_context_clear_invalid():
    try:
        c = ContextManager()
        c.add("user", "hi")
        assert c.count() == 1
        assert c.clear() == True
        assert c.count() == 0
        try:
            c.add("badrole", "hi")
            print("TEST context_clear_invalid: FAIL - Bad role should fail")
            return "FAIL"
        except ContextError:
            pass
        try:
            c.add("user", "   ")
            print("TEST context_clear_invalid: FAIL - Empty should fail")
            return "FAIL"
        except ContextError:
            print("TEST context_clear_invalid: PASS - Clear + invalid rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST context_clear_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_router_register, test_router_route_capability, test_router_no_capable_fails, test_router_duplicate, test_router_fallback, test_context_add_get, test_context_trim, test_context_clear_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 2 STEP 4 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase2_4_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
