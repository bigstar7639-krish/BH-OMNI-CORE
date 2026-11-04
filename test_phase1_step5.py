# BH-OMNI CORE - Phase 1 Step 5 - Vault - Termux / Pydroid3 Compatible
from pathlib import Path
import sys
import tempfile
import json
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.vault import VaultManager, VaultError

def _new_vault():
    tmp = tempfile.mkdtemp()
    vp = Path(tmp) / "vault_test.json"
    return VaultManager(vault_path=vp, master_password="TestMaster123!"), vp

def test_store_retrieve():
    try:
        v, _ = _new_vault()
        assert v.store("api_key", "sk-12345-secret") == True
        val = v.retrieve("api_key")
        assert val == "sk-12345-secret"
        print("TEST store_retrieve: PASS - Store + retrieve works")
        return "PASS"
    except Exception as e:
        print(f"TEST store_retrieve: FAIL - {e}")
        return "FAIL"

def test_wrong_password_fails():
    try:
        v, vp = _new_vault()
        v.store("mykey", "mysecret")
        v.lock()
        # Try unlock with wrong password - should fail
        try:
            v2 = VaultManager(vault_path=vp, master_password="WrongPassword999!")
            print("TEST wrong_password_fails: FAIL - Should have rejected wrong password")
            return "FAIL"
        except VaultError:
            print("TEST wrong_password_fails: PASS - Wrong password rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST wrong_password_fails: FAIL - {e}")
        return "FAIL"

def test_list_keys_no_values():
    try:
        v, _ = _new_vault()
        v.store("key1", "secret1")
        v.store("key2", "secret2")
        keys = v.list_keys()
        assert "key1" in keys and "key2" in keys
        assert "__verify__" not in keys
        # Ensure values not leaked in list output - list should only have names
        assert "secret1" not in str(keys)
        print(f"TEST list_keys_no_values: PASS - Keys {keys}, values not leaked")
        return "PASS"
    except Exception as e:
        print(f"TEST list_keys_no_values: FAIL - {e}")
        return "FAIL"

def test_delete_works():
    try:
        v, _ = _new_vault()
        v.store("todelete", "val")
        assert v.has_key("todelete") == True
        assert v.delete("todelete") == True
        assert v.has_key("todelete") == False
        try:
            v.retrieve("todelete")
            print("TEST delete_works: FAIL - Should not retrieve deleted")
            return "FAIL"
        except VaultError:
            print("TEST delete_works: PASS - Delete works, retrieve after delete fails")
            return "PASS"
    except Exception as e:
        print(f"TEST delete_works: FAIL - {e}")
        return "FAIL"

def test_overwrite_updates():
    try:
        v, _ = _new_vault()
        v.store("k", "v1")
        assert v.retrieve("k") == "v1"
        v.store("k", "v2-updated")
        assert v.retrieve("k") == "v2-updated"
        print("TEST overwrite_updates: PASS - Overwrite updates value")
        return "PASS"
    except Exception as e:
        print(f"TEST overwrite_updates: FAIL - {e}")
        return "FAIL"

def test_invalid_key_rejected():
    try:
        v, _ = _new_vault()
        for bad in ["", "   ", "../evil", "a/b", "a\\b"]:
            try:
                v.store(bad, "val")
                print(f"TEST invalid_key_rejected: FAIL - Should reject {repr(bad)}")
                return "FAIL"
            except VaultError:
                pass
        print("TEST invalid_key_rejected: PASS - Invalid keys rejected")
        return "PASS"
    except Exception as e:
        print(f"TEST invalid_key_rejected: FAIL - {e}")
        return "FAIL"

def test_tampered_vault_fails():
    try:
        v, vp = _new_vault()
        v.store("secure", "topsecret")
        v.lock()
        # Tamper file: flip a char in ciphertext
        data = json.loads(vp.read_text())
        # Find secure entry
        rec = data["entries"]["secure"]
        # Corrupt ciphertext - change last 2 chars
        c = rec["c"]
        rec["c"] = c[:-2] + "XX"
        vp.write_text(json.dumps(data))
        # Try unlock + retrieve - should fail
        try:
            v2 = VaultManager(vault_path=vp, master_password="TestMaster123!")
            # Unlock may succeed if verify entry intact, but retrieve should fail
            val = v2.retrieve("secure")
            print(f"TEST tampered_vault_fails: FAIL - Tampered should fail, got {val}")
            return "FAIL"
        except VaultError:
            print("TEST tampered_vault_fails: PASS - Tampered vault rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST tampered_vault_fails: FAIL - {e}")
        return "FAIL"

def test_change_password():
    try:
        v, vp = _new_vault()
        v.store("k1", "v1")
        v.store("k2", "v2")
        assert v.change_password("TestMaster123!", "NewMaster456!") == True
        assert v.retrieve("k1") == "v1"
        assert v.retrieve("k2") == "v2"
        v.lock()
        # Old password should fail now
        try:
            v2 = VaultManager(vault_path=vp, master_password="TestMaster123!")
            print("TEST change_password: FAIL - Old password should fail after change")
            return "FAIL"
        except VaultError:
            pass
        # New password should work
        v3 = VaultManager(vault_path=vp, master_password="NewMaster456!")
        assert v3.retrieve("k1") == "v1"
        print("TEST change_password: PASS - Change works, old fails, new works")
        return "PASS"
    except Exception as e:
        print(f"TEST change_password: FAIL - {e}")
        import traceback
        traceback.print_exc()
        return "FAIL"

if __name__ == "__main__":
    tests = [test_store_retrieve, test_wrong_password_fails, test_list_keys_no_values, test_delete_works, test_overwrite_updates, test_invalid_key_rejected, test_tampered_vault_fails, test_change_password]
    results = {}
    for func in tests:
        print(f"--- {func.__name__} ---")
        results[func.__name__] = func()
    print("\n=== STEP 5 TEST RESULTS ===")
    for k, v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s == "PASS")
    failed = sum(1 for s in results.values() if s == "FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step5_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
