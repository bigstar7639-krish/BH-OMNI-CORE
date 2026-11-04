# BH-OMNI CORE - Phase 2 Step 2 - Plugin + Health - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.plugin_loader import PluginLoader, PluginError
from core.health_monitor import ModuleHealthMonitor, HealthError

def test_plugin_register_valid():
    try:
        p = PluginLoader()
        assert p.register({"name": "weather", "version": "1.0.0", "description": "Weather plugin", "entry": lambda: "ok"}) == True
        lst = p.list_plugins()
        assert len(lst) == 1 and lst[0]["name"] == "weather" and lst[0]["loaded"] == False
        print("TEST plugin_register_valid: PASS - Register works")
        return "PASS"
    except Exception as e:
        print(f"TEST plugin_register_valid: FAIL - {e}")
        return "FAIL"

def test_plugin_invalid_manifest():
    try:
        p = PluginLoader()
        # Missing field
        try:
            p.register({"name": "x", "version": "1.0.0", "description": "d"})
            print("TEST plugin_invalid_manifest: FAIL - Missing entry should fail")
            return "FAIL"
        except PluginError:
            pass
        # Bad version
        try:
            p.register({"name": "x", "version": "1.0", "description": "d", "entry": lambda: 1})
            print("TEST plugin_invalid_manifest: FAIL - Bad version should fail")
            return "FAIL"
        except PluginError:
            pass
        # Non-callable entry
        try:
            p.register({"name": "x", "version": "1.0.0", "description": "d", "entry": "not-callable"})
            print("TEST plugin_invalid_manifest: FAIL - Non-callable should fail")
            return "FAIL"
        except PluginError:
            print("TEST plugin_invalid_manifest: PASS - Invalid manifests rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST plugin_invalid_manifest: FAIL - {e}")
        return "FAIL"

def test_plugin_duplicate():
    try:
        p = PluginLoader()
        p.register({"name": "a", "version": "1.0.0", "description": "d", "entry": lambda: 1})
        try:
            p.register({"name": "a", "version": "2.0.0", "description": "d2", "entry": lambda: 2})
            print("TEST plugin_duplicate: FAIL - Duplicate should fail")
            return "FAIL"
        except PluginError:
            print("TEST plugin_duplicate: PASS - Duplicate rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST plugin_duplicate: FAIL - {e}")
        return "FAIL"

def test_plugin_load_unload():
    try:
        p = PluginLoader()
        called = []
        def entry():
            called.append(1)
            return "loaded-ok"
        p.register({"name": "plug", "version": "1.0.0", "description": "d", "entry": entry})
        assert p.load("plug") == "loaded-ok"
        assert p.is_loaded("plug") == True
        assert p.unload("plug") == True
        assert p.is_loaded("plug") == False
        print("TEST plugin_load_unload: PASS - Load/unload works")
        return "PASS"
    except Exception as e:
        print(f"TEST plugin_load_unload: FAIL - {e}")
        return "FAIL"

def test_plugin_load_missing():
    try:
        p = PluginLoader()
        try:
            p.load("nope")
            print("TEST plugin_load_missing: FAIL - Missing should fail")
            return "FAIL"
        except PluginError:
            print("TEST plugin_load_missing: PASS - Missing load rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST plugin_load_missing: FAIL - {e}")
        return "FAIL"

def test_health_register_healthy():
    try:
        h = ModuleHealthMonitor()
        h.register("mod_01")
        assert h.get_status("mod_01")["status"] == "UNKNOWN"
        h.report("mod_01", "HEALTHY", "All good")
        assert h.is_healthy("mod_01") == True
        print("TEST health_register_healthy: PASS - Register UNKNOWN -> HEALTHY")
        return "PASS"
    except Exception as e:
        print(f"TEST health_register_healthy: FAIL - {e}")
        return "FAIL"

def test_health_unhealthy_list():
    try:
        h = ModuleHealthMonitor()
        h.register("m1"); h.register("m2"); h.register("m3")
        h.report("m1", "HEALTHY", "ok")
        h.report("m2", "DEGRADED", "slow")
        h.report("m3", "DOWN", "crashed")
        un = h.list_unhealthy()
        names = [x["name"] for x in un]
        assert "m2" in names and "m3" in names and "m1" not in names
        print(f"TEST health_unhealthy_list: PASS - Unhealthy {names}")
        return "PASS"
    except Exception as e:
        print(f"TEST health_unhealthy_list: FAIL - {e}")
        return "FAIL"

def test_health_unknown_fails():
    try:
        h = ModuleHealthMonitor()
        try:
            h.report("ghost", "HEALTHY", "x")
            print("TEST health_unknown_fails: FAIL - Unknown should fail")
            return "FAIL"
        except HealthError:
            pass
        try:
            h.report("ghost2", "BADSTATUS", "x")
            print("TEST health_unknown_fails: FAIL - Bad status should fail")
            return "FAIL"
        except HealthError:
            print("TEST health_unknown_fails: PASS - Unknown + bad status rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST health_unknown_fails: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_plugin_register_valid, test_plugin_invalid_manifest, test_plugin_duplicate, test_plugin_load_unload, test_plugin_load_missing, test_health_register_healthy, test_health_unhealthy_list, test_health_unknown_fails]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 2 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase2_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
