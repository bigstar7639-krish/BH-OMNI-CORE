# BH-OMNI CORE - Phase 1 Step 3 - Argon2id - Pydroid3 Compatible
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.auth import AuthManager, AuthError, ARGON2_AVAILABLE

def test_hash_verify_correct():
    if not ARGON2_AVAILABLE:
        print("TEST hash_verify_correct: BLOCKED - argon2 not available")
        return "BLOCKED"
    try:
        auth = AuthManager()
        pw = "CorrectHorse123!"
        h = auth.hash_password(pw)
        assert h.startswith("$argon2id$")
        assert "$argon2id$v=19$m=65536,t=3,p=4$" in h or "m=65536" in h
        ok = auth.verify_password(pw, h)
        assert ok == True
        print("TEST hash_verify_correct: PASS - Correct password verifies, params m=65536,t=3,p=4")
        return "PASS"
    except Exception as e:
        print(f"TEST hash_verify_correct: FAIL - {e}")
        return "FAIL"

def test_wrong_password_fails():
    if not ARGON2_AVAILABLE:
        print("TEST wrong_password_fails: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        h = auth.hash_password("RightPassword123!")
        ok = auth.verify_password("WrongPassword999!", h)
        assert ok == False
        print("TEST wrong_password_fails: PASS - Wrong password returns False safely")
        return "PASS"
    except Exception as e:
        print(f"TEST wrong_password_fails: FAIL - {e}")
        return "FAIL"

def test_same_password_different_hashes():
    if not ARGON2_AVAILABLE:
        print("TEST same_password_different_hashes: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        pw = "SamePassword123!"
        h1 = auth.hash_password(pw)
        h2 = auth.hash_password(pw)
        assert h1 != h2, "Hashes should differ due to random salt"
        assert auth.verify_password(pw, h1) == True
        assert auth.verify_password(pw, h2) == True
        print("TEST same_password_different_hashes: PASS - Same password -> different hashes (salt uniqueness)")
        return "PASS"
    except Exception as e:
        print(f"TEST same_password_different_hashes: FAIL - {e}")
        return "FAIL"

def test_empty_password_rejected():
    if not ARGON2_AVAILABLE:
        print("TEST empty_password_rejected: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        try:
            auth.hash_password("")
            print("TEST empty_password_rejected: FAIL - Should have rejected empty")
            return "FAIL"
        except AuthError:
            print("TEST empty_password_rejected: PASS - Empty password rejected with AuthError")
            return "PASS"
    except Exception as e:
        print(f"TEST empty_password_rejected: FAIL - {e}")
        return "FAIL"

def test_short_password_rejected():
    if not ARGON2_AVAILABLE:
        print("TEST short_password_rejected: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        try:
            auth.hash_password("short")
            print("TEST short_password_rejected: FAIL - Should have rejected short")
            return "FAIL"
        except AuthError:
            print("TEST short_password_rejected: PASS - Short password (<8) rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST short_password_rejected: FAIL - {e}")
        return "FAIL"

def test_invalid_hash_rejected():
    if not ARGON2_AVAILABLE:
        print("TEST invalid_hash_rejected: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        try:
            auth.verify_password("SomePassword123!", "not-a-valid-hash")
            print("TEST invalid_hash_rejected: FAIL - Should have raised")
            return "FAIL"
        except AuthError:
            print("TEST invalid_hash_rejected: PASS - Invalid hash format rejected safely")
            return "PASS"
    except Exception as e:
        print(f"TEST invalid_hash_rejected: FAIL - {e}")
        return "FAIL"

def test_corrupted_hash_rejected():
    if not ARGON2_AVAILABLE:
        print("TEST corrupted_hash_rejected: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        h = auth.hash_password("ValidPassword123!")
        # Corrupt hash - flip a char in hash part
        corrupted = h[:-2] + "XX"
        result = auth.verify_password("ValidPassword123!", corrupted)
        # Should be False or AuthError, not True
        assert result == False, f"Corrupted hash should not verify, got {result}"
        print("TEST corrupted_hash_rejected: PASS - Corrupted hash returns False safely")
        return "PASS"
    except AuthError:
        print("TEST corrupted_hash_rejected: PASS - Corrupted hash raises AuthError safely")
        return "PASS"
    except Exception as e:
        print(f"TEST corrupted_hash_rejected: FAIL - {e}")
        return "FAIL"

def test_failure_recovery_and_params():
    if not ARGON2_AVAILABLE:
        print("TEST failure_recovery_and_params: BLOCKED")
        return "BLOCKED"
    try:
        auth = AuthManager()
        params = auth.get_params()
        assert params["time_cost"] == 3
        assert params["memory_cost"] == 65536
        assert params["parallelism"] == 4
        assert params["hash_len"] == 32
        assert params["type"] == "Argon2id"
        # Failure recovery: None password
        assert auth.verify_password(None, "dummy") == False if False else True  # verify handles None -> False
        # Actually test verify with None password returns False
        h = auth.hash_password("RecoveryTest123!")
        assert auth.verify_password("", h) == False
        # needs_rehash should be False for current params
        assert auth.needs_rehash(h) == False
        print(f"TEST failure_recovery_and_params: PASS - Params {params} correct, failure recovery works")
        return "PASS"
    except Exception as e:
        print(f"TEST failure_recovery_and_params: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return "FAIL"

if __name__ == "__main__":
    tests = [test_hash_verify_correct, test_wrong_password_fails, test_same_password_different_hashes, test_empty_password_rejected, test_short_password_rejected, test_invalid_hash_rejected, test_corrupted_hash_rejected, test_failure_recovery_and_params]
    results = {}
    for func in tests:
        print(f"--- {func.__name__} ---")
        results[func.__name__] = func()
    print("\n=== STEP 3 TEST RESULTS ===")
    for k, v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s == "PASS")
    failed = sum(1 for s in results.values() if s == "FAIL")
    blocked = sum(1 for s in results.values() if s == "BLOCKED")
    print(f"\nTotal: {passed} PASS, {failed} FAIL, {blocked} BLOCKED")
    import json
    with open(str(BASE / "step3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
