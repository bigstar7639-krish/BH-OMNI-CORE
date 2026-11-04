# BH-OMNI CORE - Phase 1 Step 8 - Audit + Backup - Termux / Pydroid3
from pathlib import Path
import sys, tempfile, json, time
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from security.audit import AuditLogger, AuditError
from security.backup_verify import BackupVerifier, BackupError

SECRET = "backup-secret-key-for-step8-must-be-32-chars-long-12345"

def _new_audit():
    tmp = tempfile.mkdtemp()
    lp = Path(tmp) / "audit.jsonl"
    return AuditLogger(log_path=lp), lp

def test_log_creates_entry():
    try:
        a, _ = _new_audit()
        e = a.log("user1", "login", "auth", "SUCCESS", "Login ok")
        assert e["user_id"] == "user1" and e["action"] == "login"
        assert "entry_hash" in e and "prev_hash" in e
        assert a.count() == 1
        print("TEST log_creates_entry: PASS - Entry created with hash chain")
        return "PASS"
    except Exception as e:
        print(f"TEST log_creates_entry: FAIL - {e}")
        return "FAIL"

def test_chain_hash_links():
    try:
        a, _ = _new_audit()
        a.log("u1", "login", "auth", "SUCCESS", "ok1")
        a.log("u1", "read_vault", "vault", "SUCCESS", "ok2")
        a.log("u2", "login", "auth", "FAIL", "wrong pw")
        entries = a.get_entries()
        assert entries[1]["prev_hash"] == entries[0]["entry_hash"]
        assert entries[2]["prev_hash"] == entries[1]["entry_hash"]
        v = a.verify_chain()
        assert v["valid"] == True and v["entries"] == 3
        print("TEST chain_hash_links: PASS - Chain linked, verify valid")
        return "PASS"
    except Exception as e:
        print(f"TEST chain_hash_links: FAIL - {e}")
        return "FAIL"

def test_tampered_log_detected():
    try:
        a, lp = _new_audit()
        a.log("u1", "login", "auth", "SUCCESS", "ok")
        a.log("u1", "delete", "vault", "SUCCESS", "ok2")
        # Tamper: change action in second line
        lines = lp.read_text().strip().splitlines()
        obj = json.loads(lines[1])
        obj["action"] = "HACKED"
        lines[1] = json.dumps(obj)
        lp.write_text("\n".join(lines) + "\n")
        v = a.verify_chain()
        assert v["valid"] == False, f"Should detect tamper, got {v}"
        print(f"TEST tampered_log_detected: PASS - Tamper detected: {v['message']}")
        return "PASS"
    except Exception as e:
        print(f"TEST tampered_log_detected: FAIL - {e}")
        return "FAIL"

def test_log_filtering():
    try:
        a, _ = _new_audit()
        a.log("u1", "login", "auth", "SUCCESS", "ok")
        a.log("u2", "login", "auth", "FAIL", "fail")
        a.log("u1", "read_vault", "vault", "SUCCESS", "ok")
        assert len(a.get_entries(user_id="u1")) == 2
        assert len(a.get_entries(action="login")) == 2
        assert len(a.get_entries(result="FAIL")) == 1
        print("TEST log_filtering: PASS - Filter by user/action/result works")
        return "PASS"
    except Exception as e:
        print(f"TEST log_filtering: FAIL - {e}")
        return "FAIL"

def test_backup_create_manifest():
    try:
        tmp = tempfile.mkdtemp()
        base = Path(tmp)
        (base / "file1.txt").write_text("hello backup")
        (base / "file2.txt").write_text("second file")
        bv = BackupVerifier(SECRET)
        m = bv.create_manifest(base, ["file1.txt", "file2.txt"])
        assert "signature" in m and len(m["files"]) == 2
        assert len(m["files"]["file1.txt"]) == 64  # SHA256 hex
        print("TEST backup_create_manifest: PASS - Manifest with SHA256 + signature")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_create_manifest: FAIL - {e}")
        return "FAIL"

def test_backup_verify_pass():
    try:
        tmp = tempfile.mkdtemp()
        base = Path(tmp)
        (base / "a.txt").write_text("data1")
        bv = BackupVerifier(SECRET)
        m = bv.create_manifest(base, ["a.txt"])
        v = bv.verify_manifest(base, m)
        assert v["valid"] == True
        print(f"TEST backup_verify_pass: PASS - {v['message']}")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_verify_pass: FAIL - {e}")
        return "FAIL"

def test_backup_verify_modified_file():
    try:
        tmp = tempfile.mkdtemp()
        base = Path(tmp)
        (base / "a.txt").write_text("original")
        bv = BackupVerifier(SECRET)
        m = bv.create_manifest(base, ["a.txt"])
        # Modify file
        (base / "a.txt").write_text("HACKED-modified")
        v = bv.verify_manifest(base, m)
        assert v["valid"] == False and "modified" in v["message"].lower()
        print(f"TEST backup_verify_modified_file: PASS - Modified detected: {v['message']}")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_verify_modified_file: FAIL - {e}")
        return "FAIL"

def test_backup_signature_tamper():
    try:
        tmp = tempfile.mkdtemp()
        base = Path(tmp)
        (base / "a.txt").write_text("data")
        bv = BackupVerifier(SECRET)
        m = bv.create_manifest(base, ["a.txt"])
        # Tamper manifest: change hash without updating signature
        m["files"]["a.txt"] = "0"*64
        v = bv.verify_manifest(base, m)
        assert v["valid"] == False and "signature" in v["message"].lower()
        print(f"TEST backup_signature_tamper: PASS - Manifest tamper detected: {v['message']}")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_signature_tamper: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_log_creates_entry, test_chain_hash_links, test_tampered_log_detected, test_log_filtering, test_backup_create_manifest, test_backup_verify_pass, test_backup_verify_modified_file, test_backup_signature_tamper]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== STEP 8 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step8_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
