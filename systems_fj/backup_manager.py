
import hashlib
from typing import Dict, List

class BackupError(Exception):
    pass

class BackupManager:
    """
    Phase 3 Step 4 - System I - Backup Manager
    - Create backup: dict of filename -> content -> SHA256 per file + manifest
    - Verify: recompute hashes, report tampered/missing files
    - Restore: return content if verified, else FAIL
    - In-memory only - No real file backup, no cloud
    """
    def __init__(self):
        self._backups: Dict[str, dict] = {}  # backup_id -> {files, manifest}

    def create(self, backup_id: str, files: Dict[str, str]) -> dict:
        if backup_id is None or not isinstance(backup_id, str) or len(backup_id.strip()) == 0:
            raise BackupError("backup_id cannot be empty")
        backup_id = backup_id.strip()
        if files is None or not isinstance(files, dict) or len(files) == 0:
            raise BackupError("files must be non-empty dict")
        if backup_id in self._backups:
            raise BackupError(f"Duplicate backup: {backup_id}")
        manifest = {}
        for fname, content in files.items():
            if not isinstance(fname, str) or len(fname.strip()) == 0:
                raise BackupError("filename cannot be empty")
            if not isinstance(content, str):
                raise BackupError("content must be str")
            h = hashlib.sha256(content.encode("utf-8")).hexdigest()
            manifest[fname] = h
        self._backups[backup_id] = {"files": dict(files), "manifest": manifest}
        return {"backup_id": backup_id, "files": len(files), "manifest": manifest}

    def verify(self, backup_id: str) -> dict:
        if backup_id not in self._backups:
            raise BackupError(f"Backup not found: {backup_id}")
        b = self._backups[backup_id]
        tampered = []
        for fname, expected in b["manifest"].items():
            actual = hashlib.sha256(b["files"][fname].encode("utf-8")).hexdigest()
            if actual != expected:
                tampered.append(fname)
        return {"backup_id": backup_id, "verified": len(tampered) == 0, "tampered": tampered, "files": len(b["manifest"])}

    def restore(self, backup_id: str) -> Dict[str, str]:
        v = self.verify(backup_id)
        if not v["verified"]:
            raise BackupError(f"Backup tampered: {v['tampered']} - Restore blocked")
        return dict(self._backups[backup_id]["files"])

    def tamper_for_test(self, backup_id: str, filename: str) -> bool:
        # Test helper only - Simulates tampering
        if backup_id not in self._backups:
            raise BackupError(f"Backup not found: {backup_id}")
        if filename not in self._backups[backup_id]["files"]:
            raise BackupError(f"File not found: {filename}")
        self._backups[backup_id]["files"][filename] += "TAMPERED"
        return True

    def list_backups(self) -> List[str]:
        return sorted(list(self._backups.keys()))

    def get_info(self) -> dict:
        return {"backups": len(self._backups), "principle": "SHA256 manifest + Verify before restore"}
