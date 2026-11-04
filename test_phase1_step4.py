# BH-OMNI CORE - Phase 1 Step 4 - TOTP MFA - Termux / Pydroid3 Compatible
from pathlib import Path
import sys
import time
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.mfa import MFAManager, MFAError, PYOTP_AVAILABLE
# Fallback allows tests even without pyotp - PYOTP_AVAILABLE is for info only, MFAManager works with stdlib fallback

def test_generate_secret():
    try:
        m = MFAManager()
        s1 = m.generate_secret()
        s2 = m.generate_secret()
        assert len(s1) == 32, f"Secret len {len(s1)} != 32"
        assert s1 != s2, "Secrets should differ"
        assert all(c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567" for c in s1)
        print(f"TEST generate_secret: PASS - 32 chars Base32, unique - {s1[:4]}...")
        return "PASS"
    except Exception as e:
        print(f"TEST generate_secret: FAIL - {e}")
        return "FAIL"

def test_generate_verify_correct():
    try:
        m = MFAManager()
        secret = m.generate_secret()
        code = m.generate_code(secret)
        assert len(code) == 6 and code.isdigit()
        ok = m.verify_code(secret, code)
        assert ok == True
        print(f"TEST generate_verify_correct: PASS - Code {code} verifies")
        return "PASS"
    except Exception as e:
        print(f"TEST generate_verify_correct: FAIL - {e}")
        return "FAIL"

def test_wrong_code_fails():
    try:
        m = MFAManager()
        secret = m.generate_secret()
        code = m.generate_code(secret)
        # Make wrong code by +1 mod 1000000
        wrong = f"{(int(code) + 1) % 1000000:06d}"
        if wrong == code:
            wrong = "000000" if code != "000000" else "111111"
        ok = m.verify_code(secret, wrong)
        assert ok == False, f"Wrong code {wrong} should fail, got {ok}"
        print(f"TEST wrong_code_fails: PASS - Wrong code {wrong} returns False")
        return "PASS"
    except Exception as e:
        print(f"TEST wrong_code_fails: FAIL - {e}")
        return "FAIL"

def test_expired_code_fails():
    try:
        m = MFAManager()
        secret = m.generate_secret()
        now = int(time.time())
        old_time = now - 120  # 2 min ago, beyond valid_window=1 (90 sec)
        old_code = m.generate_code(secret, for_time=old_time)
        # Verify old code at now should fail (window=1 allows +-30 sec, not 120)
        ok = m.verify_code(secret, old_code, for_time=now, valid_window=1)
        assert ok == False, "Expired code should fail"
        print("TEST expired_code_fails: PASS - 120 sec old code rejected")
        return "PASS"
    except Exception as e:
        print(f"TEST expired_code_fails: FAIL - {e}")
        return "FAIL"

def test_invalid_secret_rejected():
    try:
        m = MFAManager()
        try:
            m.verify_code("INVALID!!!", "123456")
            print("TEST invalid_secret_rejected: FAIL - Should have raised")
            return "FAIL"
        except MFAError:
            print("TEST invalid_secret_rejected: PASS - Invalid secret rejected with MFAError")
            return "PASS"
    except Exception as e:
        print(f"TEST invalid_secret_rejected: FAIL - {e}")
        return "FAIL"

def test_backup_codes():
    try:
        m = MFAManager()
        codes = m.generate_backup_codes(10)
        assert len(codes) == 10
        assert len(set(codes)) == 10, "Backup codes must be unique"
        # Hash and verify
        hashes = [m.hash_backup_code(c) for c in codes]
        assert m.verify_backup_code(codes[0], hashes) == True
        assert m.verify_backup_code("XXXX-XXXX", hashes) == False
        # Format XXXX-XXXX
        assert all(len(c) == 9 and c[4] == "-" for c in codes)
        print(f"TEST backup_codes: PASS - 10 unique codes, hash verify works - {codes[0]}")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_codes: FAIL - {e}")
        return "FAIL"

def test_provisioning_uri():
    try:
        m = MFAManager()
        secret = m.generate_secret()
        uri = m.get_provisioning_uri(secret, "krish")
        assert uri.startswith("otpauth://totp/")
        assert "BH-OMNI-CORE" in uri
        assert "krish" in uri
        assert secret in uri
        print(f"TEST provisioning_uri: PASS - URI format correct")
        return "PASS"
    except Exception as e:
        print(f"TEST provisioning_uri: FAIL - {e}")
        return "FAIL"

def test_failure_recovery_and_params():
    try:
        m = MFAManager()
        params = m.get_params()
        assert params["digits"] == 6
        assert params["interval"] == 30
        assert params["type"] == "TOTP"
        # Failure recovery: None inputs
        assert m.verify_code("JBSWY3DPEHPK3PXP", None) == False
        assert m.verify_code("JBSWY3DPEHPK3PXP", "") == False
        assert m.verify_code("JBSWY3DPEHPK3PXP", "abc") == False
        # Invalid code length
        assert m.verify_code("JBSWY3DPEHPK3PXP", "123") == False
        print(f"TEST failure_recovery_and_params: PASS - Params {params} correct, failure recovery works")
        return "PASS"
    except Exception as e:
        print(f"TEST failure_recovery_and_params: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_generate_secret, test_generate_verify_correct, test_wrong_code_fails, test_expired_code_fails, test_invalid_secret_rejected, test_backup_codes, test_provisioning_uri, test_failure_recovery_and_params]
    results = {}
    for func in tests:
        print(f"--- {func.__name__} ---")
        results[func.__name__] = func()
    print("\n=== STEP 4 TEST RESULTS ===")
    for k, v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s == "PASS")
    failed = sum(1 for s in results.values() if s == "FAIL")
    blocked = sum(1 for s in results.values() if s == "BLOCKED")
    print(f"\nTotal: {passed} PASS, {failed} FAIL, {blocked} BLOCKED")
    import json
    with open(str(BASE / "step4_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
