# BH-OMNI CORE - Phase 2 Step 1 - Dependency + EventBus - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.dependency_engine import DependencyEngine, DependencyError
from core.event_bus import EventBus, EventBusError

def test_dep_resolve_order():
    try:
        d = DependencyEngine()
        d.register("mod_01", [])
        d.register("mod_02", ["mod_01"])
        d.register("mod_03", ["mod_01", "mod_02"])
        order = d.resolve_order()
        assert order.index("mod_01") < order.index("mod_02") < order.index("mod_03")
        print(f"TEST dep_resolve_order: PASS - Order {order}")
        return "PASS"
    except Exception as e:
        print(f"TEST dep_resolve_order: FAIL - {e}")
        return "FAIL"

def test_dep_missing_fails():
    try:
        d = DependencyEngine()
        d.register("mod_02", ["mod_01"])  # mod_01 missing
        try:
            d.resolve_order()
            print("TEST dep_missing_fails: FAIL - Should fail on missing")
            return "FAIL"
        except DependencyError as e:
            assert "Missing" in str(e)
            print(f"TEST dep_missing_fails: PASS - Missing detected: {e}")
            return "PASS"
    except Exception as e:
        print(f"TEST dep_missing_fails: FAIL - {e}")
        return "FAIL"

def test_dep_circular():
    try:
        d = DependencyEngine()
        d.register("a", ["b"])
        d.register("b", ["a"])
        try:
            d.resolve_order()
            print("TEST dep_circular: FAIL - Should detect cycle")
            return "FAIL"
        except DependencyError as e:
            assert "Circular" in str(e)
            print(f"TEST dep_circular: PASS - Cycle detected: {e}")
            return "PASS"
    except Exception as e:
        print(f"TEST dep_circular: FAIL - {e}")
        return "FAIL"

def test_dep_duplicate_rejected():
    try:
        d = DependencyEngine()
        d.register("mod_01", [])
        try:
            d.register("mod_01", [])
            print("TEST dep_duplicate_rejected: FAIL - Duplicate should be rejected")
            return "FAIL"
        except DependencyError:
            print("TEST dep_duplicate_rejected: PASS - Duplicate rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST dep_duplicate_rejected: FAIL - {e}")
        return "FAIL"

def test_event_publish_delivers():
    try:
        bus = EventBus()
        received = []
        def h1(p): received.append(("h1", p))
        def h2(p): received.append(("h2", p))
        bus.subscribe("user_login", h1)
        bus.subscribe("user_login", h2)
        r = bus.publish("user_login", {"user": "u1"})
        assert r["delivered"] == 2 and r["success"] == True
        assert len(received) == 2
        print("TEST event_publish_delivers: PASS - Both handlers delivered")
        return "PASS"
    except Exception as e:
        print(f"TEST event_publish_delivers: FAIL - {e}")
        return "FAIL"

def test_event_error_isolated():
    try:
        bus = EventBus()
        received = []
        def bad(p): raise ValueError("boom")
        def good(p): received.append(p)
        bus.subscribe("evt", bad)
        bus.subscribe("evt", good)
        r = bus.publish("evt", "data")
        assert r["delivered"] == 1 and len(r["errors"]) == 1
        assert received == ["data"]
        print("TEST event_error_isolated: PASS - Bad handler did not break good handler")
        return "PASS"
    except Exception as e:
        print(f"TEST event_error_isolated: FAIL - {e}")
        return "FAIL"

def test_event_unsubscribe():
    try:
        bus = EventBus()
        called = []
        def h(p): called.append(p)
        bus.subscribe("evt", h)
        bus.unsubscribe("evt", h)
        r = bus.publish("evt", "x")
        assert r["delivered"] == 0 and len(called) == 0
        print("TEST event_unsubscribe: PASS - Unsubscribe works")
        return "PASS"
    except Exception as e:
        print(f"TEST event_unsubscribe: FAIL - {e}")
        return "FAIL"

def test_event_validation():
    try:
        bus = EventBus()
        for bad in ["", "   ", None]:
            try:
                bus.publish(bad, "x")
                print(f"TEST event_validation: FAIL - Should reject {repr(bad)}")
                return "FAIL"
            except EventBusError:
                pass
        try:
            bus.subscribe("evt", "not-callable")
            print("TEST event_validation: FAIL - Should reject non-callable")
            return "FAIL"
        except EventBusError:
            print("TEST event_validation: PASS - Invalid events/handlers rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST event_validation: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_dep_resolve_order, test_dep_missing_fails, test_dep_circular, test_dep_duplicate_rejected, test_event_publish_delivers, test_event_error_isolated, test_event_unsubscribe, test_event_validation]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 2 STEP 1 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase2_1_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
