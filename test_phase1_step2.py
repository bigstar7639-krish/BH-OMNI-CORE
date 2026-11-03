# BH-OMNI CORE - Phase 1 Step 2 - Pydroid3 CLEAN - No /mnt/data paths
from pathlib import Path
import os
import sys
import base64
import threading
from concurrent.futures import ThreadPoolExecutor

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

from security.encryption import AESGCMEncryption, KeyManager, NonceManager, EncryptionError, CRYPTO_AVAILABLE

def get_keys_file(name):
    return BASE / f"tmp_{name}.json"

def cleanup(name):
    f = get_keys_file(name)
    if f.exists():
        try:
            f.unlink()
        except:
            pass

def test1_round_trip():
    if not CRYPTO_AVAILABLE:
        print("TEST encrypt_decrypt_round_trip: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("roundtrip")
        km = KeyManager(keys_file=get_keys_file("roundtrip"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt = b"Hello BH-OMNI CORE - Secret data - 12345"
        encrypted = enc.encrypt(pt)
        dec = enc.decrypt(encrypted)
        assert dec == pt
        print("TEST encrypt_decrypt_round_trip: PASS - 40 bytes")
        cleanup("roundtrip")
        return "PASS"
    except Exception as e:
        print(f"TEST encrypt_decrypt_round_trip: FAIL - {e}")
        return "FAIL"

def test2_same_plaintext():
    if not CRYPTO_AVAILABLE:
        print("TEST same_plaintext_different_ciphertext: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("diff")
        km = KeyManager(keys_file=get_keys_file("diff"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt = b"Same plaintext"
        e1 = enc.encrypt(pt)
        e2 = enc.encrypt(pt)
        assert e1["n"] != e2["n"]
        assert e1["c"] != e2["c"]
        assert enc.decrypt(e1) == pt and enc.decrypt(e2) == pt
        print("TEST same_plaintext_different_ciphertext: PASS - Nonces different")
        cleanup("diff")
        return "PASS"
    except Exception as e:
        print(f"TEST same_plaintext_different_ciphertext: FAIL - {e}")
        return "FAIL"

def test3_wrong_key():
    if not CRYPTO_AVAILABLE:
        print("TEST wrong_key_decryption_fails_safely: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("wrong1")
        cleanup("wrong2")
        km1 = KeyManager(keys_file=get_keys_file("wrong1"))
        enc1 = AESGCMEncryption(key_manager=km1, nonce_manager=NonceManager())
        km2 = KeyManager(keys_file=get_keys_file("wrong2"))
        enc2 = AESGCMEncryption(key_manager=km2, nonce_manager=NonceManager())
        pt = b"Secret data"
        encrypted = enc1.encrypt(pt)
        try:
            dec = enc2.decrypt(encrypted)
            print("TEST wrong_key_decryption_fails_safely: FAIL - Should have failed")
            return "FAIL"
        except Exception as e:
            print(f"TEST wrong_key_decryption_fails_safely: PASS - Failed safely: {type(e).__name__}")
            cleanup("wrong1")
            cleanup("wrong2")
            return "PASS"
    except Exception as e:
        print(f"TEST wrong_key_decryption_fails_safely: FAIL - {e}")
        return "FAIL"

def test4_tampered():
    if not CRYPTO_AVAILABLE:
        print("TEST tampered_ciphertext_rejected: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("tamper")
        km = KeyManager(keys_file=get_keys_file("tamper"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt = b"Data to tamper"
        encrypted = enc.encrypt(pt)
        c_bytes = base64.b64decode(encrypted["c"])
        tampered = bytearray(c_bytes)
        tampered[0] ^= 0xFF
        enc_tampered = {"v": encrypted["v"], "n": encrypted["n"], "c": base64.b64encode(bytes(tampered)).decode()}
        try:
            dec = enc.decrypt(enc_tampered)
            print("TEST tampered_ciphertext_rejected: FAIL")
            return "FAIL"
        except Exception as e:
            print(f"TEST tampered_ciphertext_rejected: PASS - Rejected: {type(e).__name__}")
            cleanup("tamper")
            return "PASS"
    except Exception as e:
        print(f"TEST tampered_ciphertext_rejected: FAIL - {e}")
        return "FAIL"

def test5_old_key():
    if not CRYPTO_AVAILABLE:
        print("TEST old_key_decryption_after_rotation: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("rotation")
        km = KeyManager(keys_file=get_keys_file("rotation"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt1 = b"Data v1"
        enc_v1 = enc.encrypt(pt1)
        v1 = enc_v1["v"]
        new_v = km.rotate_key()
        pt2 = b"Data v2"
        enc_v2 = enc.encrypt(pt2)
        assert enc.decrypt(enc_v1) == pt1
        assert enc.decrypt(enc_v2) == pt2
        print(f"TEST old_key_decryption_after_rotation: PASS - {v1} preserved after rotation to {new_v}")
        cleanup("rotation")
        return "PASS"
    except Exception as e:
        print(f"TEST old_key_decryption_after_rotation: FAIL - {e}")
        return "FAIL"

def test6_unknown():
    if not CRYPTO_AVAILABLE:
        print("TEST unknown_key_version_rejected: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("unknown")
        km = KeyManager(keys_file=get_keys_file("unknown"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt = b"Test"
        encrypted = enc.encrypt(pt)
        enc_unknown = {"v": "v999", "n": encrypted["n"], "c": encrypted["c"]}
        try:
            dec = enc.decrypt(enc_unknown)
            print("TEST unknown_key_version_rejected: FAIL")
            return "FAIL"
        except Exception as e:
            print("TEST unknown_key_version_rejected: PASS - Rejected v999")
            cleanup("unknown")
            return "PASS"
    except Exception as e:
        print(f"TEST unknown_key_version_rejected: FAIL - {e}")
        return "FAIL"

def test7_concurrent():
    if not CRYPTO_AVAILABLE:
        print("TEST concurrent_nonce_uniqueness: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("concurrent")
        km = KeyManager(keys_file=get_keys_file("concurrent"))
        nm = NonceManager()
        enc = AESGCMEncryption(key_manager=km, nonce_manager=nm)
        nonces = []
        lock = threading.Lock()
        def task():
            local = []
            for _ in range(20):
                e = enc.encrypt(os.urandom(16))
                local.append(e["n"])
            with lock:
                nonces.extend(local)
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(task) for _ in range(10)]
            for f in futures:
                f.result()
        unique = set(nonces)
        if len(nonces) == len(unique):
            print(f"TEST concurrent_nonce_uniqueness: PASS - {len(nonces)} nonces all unique under 10 threads")
            cleanup("concurrent")
            return "PASS"
        else:
            print(f"TEST concurrent_nonce_uniqueness: FAIL - duplicates found")
            cleanup("concurrent")
            return "FAIL"
    except Exception as e:
        print(f"TEST concurrent_nonce_uniqueness: FAIL - {e}")
        return "FAIL"

def test8_recovery():
    if not CRYPTO_AVAILABLE:
        print("TEST rotation_and_failure_recovery: BLOCKED")
        return "BLOCKED"
    try:
        cleanup("recovery")
        km = KeyManager(keys_file=get_keys_file("recovery"))
        enc = AESGCMEncryption(key_manager=km, nonce_manager=NonceManager())
        pt1 = b"Before"
        enc1 = enc.encrypt(pt1)
        new_v = km.rotate_key()
        pt2 = b"After"
        enc2 = enc.encrypt(pt2)
        assert enc.decrypt(enc1) == pt1
        assert enc.decrypt(enc2) == pt2
        invalid_cases = [
            {"v": "v1", "n": "invalid!", "c": enc1["c"]},
            {"v": "v1", "n": enc1["n"], "c": "invalid!"},
        ]
        for inv in invalid_cases:
            try:
                enc.decrypt(inv)
                print("TEST rotation_and_failure_recovery: FAIL - Should have failed")
                return "FAIL"
            except:
                pass
        print("TEST rotation_and_failure_recovery: PASS - Rotation preserves old + failure recovery")
        cleanup("recovery")
        return "PASS"
    except Exception as e:
        print(f"TEST rotation_and_failure_recovery: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test1_round_trip, test2_same_plaintext, test3_wrong_key, test4_tampered, test5_old_key, test6_unknown, test7_concurrent, test8_recovery]
    results = {}
    for func in tests:
        print(f"--- {func.__name__} ---")
        results[func.__name__] = func()
    print("\n=== STEP 2 TEST RESULTS ===")
    for k, v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s == "PASS")
    failed = sum(1 for s in results.values() if s == "FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
