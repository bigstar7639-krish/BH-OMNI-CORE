# BH-OMNI CORE - Phase 3 Step 4 - System I - Sync + Backup - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from systems_fj.sync_engine import SyncEngine, SyncError
from systems_fj.backup_manager import BackupManager, BackupError

def test_sync_queue():
    try:
        s = SyncEngine()
        s.set_local("note1", "hello", 100)
        assert s.queue_size() == 1
        print("TEST sync_queue: PASS - Change queued")
        return "PASS"
    except Exception as e:
        print(f"TEST sync_queue: FAIL - {e}")
        return "FAIL"

def test_sync_push():
    try:
        s = SyncEngine()
        s.set_local("note1", "hello", 100)
        r = s.sync()
        assert r["synced"] == 1 and s.queue_size() == 0
        assert s.get_remote("note1")["value"] == "hello"
        print("TEST sync_push: PASS - Queued pushed to remote")
        return "PASS"
    except Exception as e:
        print(f"TEST sync_push: FAIL - {e}")
        return "FAIL"

def test_sync_conflict_remote_wins():
    try:
        s = SyncEngine()
        s.set_local("note1", "local-old", 100)
        s.set_remote("note1", "remote-new", 200)  # Remote newer
        r = s.sync()
        assert len(r["conflicts"]) == 1 and r["conflicts"][0]["winner"] == "remote"
        assert s.get_local("note1")["value"] == "remote-new"
        print("TEST sync_conflict_remote_wins: PASS - Remote newer wins")
        return "PASS"
    except Exception as e:
        print(f"TEST sync_conflict_remote_wins: FAIL - {e}")
        return "FAIL"

def test_sync_conflict_local_wins():
    try:
        s = SyncEngine()
        s.set_local("note1", "local-new", 300)
        s.set_remote("note1", "remote-old", 100)
        r = s.sync()
        assert r["synced"] == 1 and len(r["conflicts"]) == 0
        assert s.get_remote("note1")["value"] == "local-new"
        print("TEST sync_conflict_local_wins: PASS - Local newer wins")
        return "PASS"
    except Exception as e:
        print(f"TEST sync_conflict_local_wins: FAIL - {e}")
        return "FAIL"

def test_backup_create_verify():
    try:
        b = BackupManager()
        r = b.create("bk1", {"a.txt": "hello", "b.txt": "world"})
        assert r["files"] == 2
        v = b.verify("bk1")
        assert v["verified"] == True
        print("TEST backup_create_verify: PASS - Backup verified")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_create_verify: FAIL - {e}")
        return "FAIL"

def test_backup_restore():
    try:
        b = BackupManager()
        b.create("bk1", {"a.txt": "hello"})
        files = b.restore("bk1")
        assert files["a.txt"] == "hello"
        print("TEST backup_restore: PASS - Restore returns files")
        return "PASS"
    except Exception as e:
        print(f"TEST backup_restore: FAIL - {e}")
        return "FAIL"

def test_backup_tamper_blocked():
    try:
        b = BackupManager()
        b.create("bk1", {"a.txt": "hello"})
        b.tamper_for_test("bk1", "a.txt")
        v = b.verify("bk1")
        assert v["verified"] == False and "a.txt" in v["tampered"]
        try:
            b.restore("bk1")
            print("TEST backup_tamper_blocked: FAIL - Tampered restore should fail")
            return "FAIL"
        except BackupError:
            print("TEST backup_tamper_blocked: PASS - Tamper detected, restore blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST backup_tamper_blocked: FAIL - {e}")
        return "FAIL"

def test_sync_backup_invalid():
    try:
        s = SyncEngine(); b = BackupManager()
        try:
            s.set_local("", "x", 1)
            print("TEST sync_backup_invalid: FAIL - Empty key should fail")
            return "FAIL"
        except SyncError:
            pass
        try:
            b.create("bk1", {})
            print("TEST sync_backup_invalid: FAIL - Empty files should fail")
            return "FAIL"
        except BackupError:
            print("TEST sync_backup_invalid: PASS - Invalid inputs rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST sync_backup_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_sync_queue, test_sync_push, test_sync_conflict_remote_wins, test_sync_conflict_local_wins, test_backup_create_verify, test_backup_restore, test_backup_tamper_blocked, test_sync_backup_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 3 STEP 4 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase3_4_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
