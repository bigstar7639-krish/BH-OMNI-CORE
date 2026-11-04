# BH-OMNI CORE - Phase 4 Step 2 - Secure Gateway - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.permissions import PermissionManager
from core.api_gateway import SecureAPIGateway
from integration.secure_gateway import SecureGateway, SecureIntegrationError

def make_secure():
    pm = PermissionManager()
    gw = SecureAPIGateway()
    sg = SecureGateway(pm, gw)
    sg.register_route("/story", "POST", "write_own", lambda p: {"created": p.get("title", "untitled")})
    sg.register_route("/admin/users", "GET", "manage_users", lambda p: {"users": ["u1", "u2"]})
    sg.register_route("/public", "GET", "read_public", lambda p: {"hello": "world"})
    return pm, sg

def test_secure_user_allowed():
    try:
        pm, sg = make_secure()
        pm.assign_role("u1", "user")
        r = sg.request("u1", "/story", "POST", {"title": "Chennai Hero"})
        assert r["status"] == 200 and r["data"]["created"] == "Chennai Hero"
        print("TEST secure_user_allowed: PASS - User can create story")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_user_allowed: FAIL - {e}")
        return "FAIL"

def test_secure_guest_blocked():
    try:
        pm, sg = make_secure()
        pm.assign_role("guest1", "guest")
        r = sg.request("guest1", "/story", "POST", {"title": "X"})
        assert r["status"] == 403, f"Guest should be 403, got {r}"
        print("TEST secure_guest_blocked: PASS - Guest blocked from write_own")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_guest_blocked: FAIL - {e}")
        return "FAIL"

def test_secure_admin_only():
    try:
        pm, sg = make_secure()
        pm.assign_role("u1", "user")
        r = sg.request("u1", "/admin/users", "GET")
        assert r["status"] == 403
        pm.assign_role("admin1", "admin", granted_by_is_admin=True)
        r2 = sg.request("admin1", "/admin/users", "GET")
        assert r2["status"] == 200
        print("TEST secure_admin_only: PASS - User blocked, Admin allowed")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_admin_only: FAIL - {e}")
        return "FAIL"

def test_secure_unknown_route_404():
    try:
        pm, sg = make_secure()
        pm.assign_role("u1", "user")
        r = sg.request("u1", "/nope", "GET")
        assert r["status"] == 404
        print("TEST secure_unknown_route_404: PASS - Unknown route 404")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_unknown_route_404: FAIL - {e}")
        return "FAIL"

def test_secure_unknown_user_403():
    try:
        pm, sg = make_secure()
        r = sg.request("nobody", "/public", "GET")
        # Nobody has no roles -> get_permissions returns [] -> gateway 403 for read_public? Check: if no perms, gateway returns 403
        assert r["status"] == 403, f"Unknown user should be 403, got {r}"
        print("TEST secure_unknown_user_403: PASS - Unknown user blocked")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_unknown_user_403: FAIL - {e}")
        return "FAIL"

def test_secure_public_guest():
    try:
        pm, sg = make_secure()
        pm.assign_role("g1", "guest")
        r = sg.request("g1", "/public", "GET")
        assert r["status"] == 200
        print("TEST secure_public_guest: PASS - Guest can read public")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_public_guest: FAIL - {e}")
        return "FAIL"

def test_secure_handler_crash_500():
    try:
        pm, sg = make_secure()
        pm.assign_role("u1", "user")
        sg.register_route("/crash", "GET", "read_public", lambda p: 1/0)
        # Guest has read_public, so handler runs and crashes -> 500 no leak
        pm.assign_role("g1", "guest")
        r = sg.request("g1", "/crash", "GET")
        assert r["status"] == 500 and "ZeroDivision" not in str(r)
        print("TEST secure_handler_crash_500: PASS - Crash -> 500, no leak")
        return "PASS"
    except Exception as e:
        print(f"TEST secure_handler_crash_500: FAIL - {e}")
        return "FAIL"

def test_secure_missing_module():
    try:
        try:
            SecureGateway(None, SecureAPIGateway())
            print("TEST secure_missing_module: FAIL - None perm should fail")
            return "FAIL"
        except SecureIntegrationError:
            print("TEST secure_missing_module: PASS - Missing module rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST secure_missing_module: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_secure_user_allowed, test_secure_guest_blocked, test_secure_admin_only, test_secure_unknown_route_404, test_secure_unknown_user_403, test_secure_public_guest, test_secure_handler_crash_500, test_secure_missing_module]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 4 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase4_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
