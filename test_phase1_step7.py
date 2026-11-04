# BH-OMNI CORE - Phase 1 Step 7 - Permissions - Termux / Pydroid3
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.permissions import PermissionManager, PermissionError

def test_default_deny():
    try:
        m = PermissionManager()
        assert m.has_permission("unknown_user", "read_public") == False
        assert m.has_permission("unknown_user", "manage_users") == False
        try:
            m.require_permission("unknown_user", "read_public")
            print("TEST default_deny: FAIL - Should deny")
            return "FAIL"
        except PermissionError:
            print("TEST default_deny: PASS - Deny by default")
            return "PASS"
    except Exception as e:
        print(f"TEST default_deny: FAIL - {e}")
        return "FAIL"

def test_assign_role_grants():
    try:
        m = PermissionManager()
        m.assign_role("u1", "user")
        assert m.has_permission("u1", "read_own") == True
        assert m.has_permission("u1", "use_ai") == True
        assert m.has_permission("u1", "manage_users") == False
        print("TEST assign_role_grants: PASS - User role grants own perms, not admin")
        return "PASS"
    except Exception as e:
        print(f"TEST assign_role_grants: FAIL - {e}")
        return "FAIL"

def test_admin_guest_least_privilege():
    try:
        m = PermissionManager()
        m.assign_role("g1", "guest")
        assert m.has_permission("g1", "read_public") == True
        assert m.has_permission("g1", "write_own") == False
        assert m.has_permission("g1", "use_vault") == False
        m.assign_role("a1", "admin", granted_by_is_admin=True)
        assert m.has_permission("a1", "manage_users") == True
        assert m.has_permission("a1", "delete_all") == True
        assert m.has_permission("a1", "read_public") == True
        print("TEST admin_guest_least_privilege: PASS - Guest minimal, admin all")
        return "PASS"
    except Exception as e:
        print(f"TEST admin_guest_least_privilege: FAIL - {e}")
        return "FAIL"

def test_revoke_role():
    try:
        m = PermissionManager()
        m.assign_role("u1", "user")
        assert m.has_permission("u1", "use_ai") == True
        m.revoke_role("u1", "user")
        assert m.has_permission("u1", "use_ai") == False
        assert m.get_roles("u1") == []
        print("TEST revoke_role: PASS - Revoke removes perms")
        return "PASS"
    except Exception as e:
        print(f"TEST revoke_role: FAIL - {e}")
        return "FAIL"

def test_user_cannot_admin():
    try:
        m = PermissionManager()
        m.assign_role("u1", "user")
        # User cannot do admin actions
        assert m.has_permission("u1", "manage_system") == False
        assert m.has_permission("u1", "manage_security") == False
        # User cannot grant self admin-only direct perm without admin
        try:
            m.grant_direct_permission("u1", "manage_users", granted_by_is_admin=False)
            print("TEST user_cannot_admin: FAIL - Should block self-grant admin")
            return "FAIL"
        except PermissionError:
            pass
        # User cannot assign admin role to self without admin
        try:
            m.assign_role("u1", "admin", granted_by_is_admin=False)
            print("TEST user_cannot_admin: FAIL - Should block admin escalation")
            return "FAIL"
        except PermissionError:
            print("TEST user_cannot_admin: PASS - Escalation blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST user_cannot_admin: FAIL - {e}")
        return "FAIL"

def test_resource_ownership():
    try:
        m = PermissionManager()
        m.assign_role("owner", "user")
        m.assign_role("other", "user")
        m.assign_role("admin1", "admin", granted_by_is_admin=True)
        # Owner can read/write own
        assert m.can_access_resource("owner", "read", "owner") == True
        assert m.can_access_resource("owner", "write", "owner") == True
        # Other cannot read/write owner's
        assert m.can_access_resource("other", "read", "owner") == False
        assert m.can_access_resource("other", "write", "owner") == False
        # Admin can read/write others
        assert m.can_access_resource("admin1", "read", "owner") == True
        assert m.can_access_resource("admin1", "write", "owner") == True
        # Delete always admin - even owner cannot delete own via own perms
        assert m.can_access_resource("owner", "delete", "owner") == False
        assert m.can_access_resource("admin1", "delete", "owner") == True
        print("TEST resource_ownership: PASS - Owner vs other vs admin correct")
        return "PASS"
    except Exception as e:
        print(f"TEST resource_ownership: FAIL - {e}")
        return "FAIL"

def test_invalid_role_rejected():
    try:
        m = PermissionManager()
        for bad in ["superuser", "", "ADMIN", "root", None]:
            try:
                m.assign_role("u1", bad)
                print(f"TEST invalid_role_rejected: FAIL - Should reject {repr(bad)}")
                return "FAIL"
            except PermissionError:
                pass
        print("TEST invalid_role_rejected: PASS - Invalid roles rejected")
        return "PASS"
    except Exception as e:
        print(f"TEST invalid_role_rejected: FAIL - {e}")
        return "FAIL"

def test_multiple_roles_union():
    try:
        m = PermissionManager()
        m.assign_role("u1", "guest")
        m.assign_role("u1", "user")
        perms = m.get_permissions("u1")
        assert "read_public" in perms and "use_ai" in perms and "use_vault" in perms
        assert "manage_users" not in perms
        assert m.get_roles("u1") == ["guest", "user"]
        print(f"TEST multiple_roles_union: PASS - Union works, perms={perms}")
        return "PASS"
    except Exception as e:
        print(f"TEST multiple_roles_union: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_default_deny, test_assign_role_grants, test_admin_guest_least_privilege, test_revoke_role, test_user_cannot_admin, test_resource_ownership, test_invalid_role_rejected, test_multiple_roles_union]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== STEP 7 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step7_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
