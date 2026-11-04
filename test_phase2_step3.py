# BH-OMNI CORE - Phase 2 Step 3 - Gateway + Registry - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from core.api_gateway import SecureAPIGateway, GatewayError
from core.feature_registry import FeatureRegistry, RegistryError

def test_gateway_register():
    try:
        g = SecureAPIGateway()
        assert g.register_route("/api/ai/chat", "POST", "use_ai", lambda p: {"reply": "hi"}) == True
        lst = g.list_routes()
        assert len(lst) == 1 and lst[0]["path"] == "/api/ai/chat"
        print("TEST gateway_register: PASS - Route registered")
        return "PASS"
    except Exception as e:
        print(f"TEST gateway_register: FAIL - {e}")
        return "FAIL"

def test_gateway_authorized():
    try:
        g = SecureAPIGateway()
        g.register_route("/api/ai/chat", "POST", "use_ai", lambda p: {"echo": p.get("msg")})
        r = g.handle_request("/api/ai/chat", "POST", ["use_ai"], {"msg": "hello"})
        assert r["status"] == 200 and r["data"]["echo"] == "hello"
        print("TEST gateway_authorized: PASS - Authorized delivers")
        return "PASS"
    except Exception as e:
        print(f"TEST gateway_authorized: FAIL - {e}")
        return "FAIL"

def test_gateway_unauthorized_403():
    try:
        g = SecureAPIGateway()
        g.register_route("/api/admin/users", "GET", "manage_users", lambda p: [])
        r = g.handle_request("/api/admin/users", "GET", ["use_ai"], {})
        assert r["status"] == 403 and "manage_users" in r["error"]
        print("TEST gateway_unauthorized_403: PASS - 403 without permission")
        return "PASS"
    except Exception as e:
        print(f"TEST gateway_unauthorized_403: FAIL - {e}")
        return "FAIL"

def test_gateway_unknown_404():
    try:
        g = SecureAPIGateway()
        r = g.handle_request("/nope", "GET", ["use_ai"], {})
        assert r["status"] == 404
        print("TEST gateway_unknown_404: PASS - 404 for unknown route")
        return "PASS"
    except Exception as e:
        print(f"TEST gateway_unknown_404: FAIL - {e}")
        return "FAIL"

def test_gateway_invalid_route():
    try:
        g = SecureAPIGateway()
        for bad_path, bad_method in [("no-slash", "GET"), ("/api", "FETCH"), ("/api", "GET")]:
            try:
                if bad_path == "/api" and bad_method == "GET":
                    # This one is valid - test duplicate instead
                    g.register_route("/api", "GET", "read_public", lambda p: 1)
                    g.register_route("/api", "GET", "read_public", lambda p: 1)
                    print("TEST gateway_invalid_route: FAIL - Duplicate should fail")
                    return "FAIL"
                else:
                    g.register_route(bad_path, bad_method, "read_public", lambda p: 1)
                    print(f"TEST gateway_invalid_route: FAIL - Should reject {bad_path} {bad_method}")
                    return "FAIL"
            except GatewayError:
                pass
        print("TEST gateway_invalid_route: PASS - Invalid + duplicate rejected")
        return "PASS"
    except Exception as e:
        print(f"TEST gateway_invalid_route: FAIL - {e}")
        return "FAIL"

def test_registry_register():
    try:
        r = FeatureRegistry()
        assert r.register("F-001", "Voice Chat", "Voice", "mod_05") == True
        f = r.get("F-001")
        assert f["name"] == "Voice Chat" and r.count() == 1
        print("TEST registry_register: PASS - Feature registered")
        return "PASS"
    except Exception as e:
        print(f"TEST registry_register: FAIL - {e}")
        return "FAIL"

def test_registry_duplicate_id():
    try:
        r = FeatureRegistry()
        r.register("F-001", "A", "Voice", "mod_05")
        try:
            r.register("F-001", "B", "Voice", "mod_05")
            print("TEST registry_duplicate_id: FAIL - Duplicate ID should fail")
            return "FAIL"
        except RegistryError:
            print("TEST registry_duplicate_id: PASS - Duplicate ID rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST registry_duplicate_id: FAIL - {e}")
        return "FAIL"

def test_registry_duplicate_name_list():
    try:
        r = FeatureRegistry()
        r.register("F-001", "Voice Chat", "Voice", "mod_05")
        # Same name same category -> fail
        try:
            r.register("F-002", "voice chat", "Voice", "mod_06")
            print("TEST registry_duplicate_name_list: FAIL - Duplicate name should fail")
            return "FAIL"
        except RegistryError:
            pass
        # Same name different category -> ok
        r.register("F-002", "Voice Chat", "AI", "mod_06")
        # List by category
        assert len(r.list_by_category("Voice")) == 1
        assert len(r.list_by_module("mod_05")) == 1
        print("TEST registry_duplicate_name_list: PASS - Duplicate name blocked, list works")
        return "PASS"
    except Exception as e:
        print(f"TEST registry_duplicate_name_list: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_gateway_register, test_gateway_authorized, test_gateway_unauthorized_403, test_gateway_unknown_404, test_gateway_invalid_route, test_registry_register, test_registry_duplicate_id, test_registry_duplicate_name_list]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 2 STEP 3 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase2_3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
