# BH-OMNI CORE - Phase 1 Step 6 - Sessions + Rate Limit - Termux / Pydroid3
from pathlib import Path
import sys, time
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.sessions import SessionManager, SessionError
from security.rate_limit import RateLimiter, LoginAttemptTracker, RateLimitError

SECRET = "test-secret-key-for-step6-must-be-32-chars-long-12345"

def test_create_validate_access():
    try:
        m = SessionManager(secret_key=SECRET)
        s = m.create_session("user1", ["user"])
        assert "access_token" in s and "refresh_token" in s
        payload = m.validate_access_token(s["access_token"])
        assert payload["user_id"] == "user1"
        print("TEST create_validate_access: PASS - Create + validate works")
        return "PASS"
    except Exception as e:
        print(f"TEST create_validate_access: FAIL - {e}")
        return "FAIL"

def test_expired_access_rejected():
    try:
        m = SessionManager(secret_key=SECRET, access_expiry_seconds=1)
        s = m.create_session("user1")
        time.sleep(2)
        try:
            m.validate_access_token(s["access_token"])
            print("TEST expired_access_rejected: FAIL - Expired should be rejected")
            return "FAIL"
        except SessionError:
            print("TEST expired_access_rejected: PASS - Expired rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST expired_access_rejected: FAIL - {e}")
        return "FAIL"

def test_refresh_rotation():
    try:
        m = SessionManager(secret_key=SECRET)
        s1 = m.create_session("user1")
        s2 = m.refresh_session(s1["refresh_token"])
        assert s2["refresh_token"] != s1["refresh_token"]
        # Old refresh should now be unusable (reuse -> revokes all)
        # But first check new refresh works for validation via new access
        payload = m.validate_access_token(s2["access_token"])
        assert payload["user_id"] == "user1"
        # Old access still valid until expiry (JWT stateless) - expected, refresh rotation is what matters
        print("TEST refresh_rotation: PASS - Rotation creates new refresh, old rotated")
        return "PASS"
    except Exception as e:
        print(f"TEST refresh_rotation: FAIL - {e}")
        import traceback; traceback.print_exc()
        return "FAIL"

def test_refresh_reuse_detection():
    try:
        m = SessionManager(secret_key=SECRET)
        s1 = m.create_session("victim")
        s2 = m.refresh_session(s1["refresh_token"])  # Rotates, s1 old
        # Attacker reuses old s1 refresh -> should detect reuse + revoke ALL
        try:
            m.refresh_session(s1["refresh_token"])
            print("TEST refresh_reuse_detection: FAIL - Reuse should be detected")
            return "FAIL"
        except SessionError as e:
            assert "reuse" in str(e).lower() or "revoked" in str(e).lower()
        # After reuse detection, even new s2 refresh should be revoked
        try:
            m.refresh_session(s2["refresh_token"])
            print("TEST refresh_reuse_detection: FAIL - After reuse, all should be revoked")
            return "FAIL"
        except SessionError:
            print("TEST refresh_reuse_detection: PASS - Reuse detected, all sessions revoked")
            return "PASS"
    except Exception as e:
        print(f"TEST refresh_reuse_detection: FAIL - {e}")
        return "FAIL"

def test_revoke_session():
    try:
        m = SessionManager(secret_key=SECRET)
        s = m.create_session("user1")
        assert m.revoke_session(s["refresh_token"]) == True
        try:
            m.refresh_session(s["refresh_token"])
            print("TEST revoke_session: FAIL - Revoked should fail refresh")
            return "FAIL"
        except SessionError:
            print("TEST revoke_session: PASS - Revoke works")
            return "PASS"
    except Exception as e:
        print(f"TEST revoke_session: FAIL - {e}")
        return "FAIL"

def test_rate_limit_blocks():
    try:
        rl = RateLimiter(max_requests=3, window_seconds=60)
        assert rl.is_allowed("ip1") == True
        assert rl.is_allowed("ip1") == True
        assert rl.is_allowed("ip1") == True
        assert rl.is_allowed("ip1") == False, "4th should be blocked"
        # Different key independent
        assert rl.is_allowed("ip2") == True
        print("TEST rate_limit_blocks: PASS - Blocks after limit, keys independent")
        return "PASS"
    except Exception as e:
        print(f"TEST rate_limit_blocks: FAIL - {e}")
        return "FAIL"

def test_rate_limit_reset_window():
    try:
        rl = RateLimiter(max_requests=2, window_seconds=1)
        assert rl.is_allowed("k") == True
        assert rl.is_allowed("k") == True
        assert rl.is_allowed("k") == False
        time.sleep(1.2)
        assert rl.is_allowed("k") == True, "After window, should allow again"
        print("TEST rate_limit_reset_window: PASS - Window reset works")
        return "PASS"
    except Exception as e:
        print(f"TEST rate_limit_reset_window: FAIL - {e}")
        return "FAIL"

def test_brute_force_lockout():
    try:
        t = LoginAttemptTracker(max_failures=5, lockout_seconds=60)
        key = "user-victim"
        for i in range(5):
            t.record_failure(key)
        assert t.is_locked(key) == True, "Should be locked after 5 fails"
        try:
            t.check_allowed(key)
            print("TEST brute_force_lockout: FAIL - Locked should raise")
            return "FAIL"
        except RateLimitError:
            pass
        # Success clears
        t.record_success(key)
        assert t.is_locked(key) == False
        print("TEST brute_force_lockout: PASS - 5 fails locks, success clears")
        return "PASS"
    except Exception as e:
        print(f"TEST brute_force_lockout: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_create_validate_access, test_expired_access_rejected, test_refresh_rotation, test_refresh_reuse_detection, test_revoke_session, test_rate_limit_blocks, test_rate_limit_reset_window, test_brute_force_lockout]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== STEP 6 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step6_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
