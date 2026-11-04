
import hashlib
import json
import time
from pathlib import Path
from typing import List, Dict, Optional

class AuditError(Exception):
    pass

class AuditLogger:
    """
    Phase 1 Step 8 - Audit Logs - Tamper-Evident
    - Append-only JSONL: each line = one event
    - Hash chain: each entry hash = SHA256(prev_hash + canonical_json)
    - Verify: recompute chain, any tamper -> FAIL
    - Fields: timestamp, user_id, action, resource, result, details (no secrets)
    - Never log secrets / passwords / tokens
    """
    def __init__(self, log_path=None):
        self.log_path = Path(log_path) if log_path else Path(__file__).parent / "audit.log.jsonl"
        self._prev_hash = "GENESIS"
        # Load existing chain to continue prev_hash
        if self.log_path.exists():
            try:
                lines = self.log_path.read_text(encoding="utf-8").strip().splitlines()
                lines = [l for l in lines if l.strip()]
                if lines:
                    last = json.loads(lines[-1])
                    self._prev_hash = last.get("entry_hash", "GENESIS")
            except Exception as e:
                raise AuditError(f"Corrupted audit log - Cannot load: {type(e).__name__}") from e

    def _validate(self, user_id, action, resource, result):
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise AuditError("Invalid user_id")
        if action is None or not isinstance(action, str) or len(action.strip()) == 0:
            raise AuditError("Invalid action")
        if resource is None or not isinstance(resource, str):
            raise AuditError("Invalid resource")
        if result not in ("SUCCESS", "FAIL", "DENIED", "BLOCKED"):
            raise AuditError(f"Invalid result: {result} - Must be SUCCESS/FAIL/DENIED/BLOCKED")
        return user_id.strip(), action.strip(), resource

    def log(self, user_id: str, action: str, resource: str = "", result: str = "SUCCESS", details: str = "") -> dict:
        user_id, action, resource = self._validate(user_id, action, resource, result)
        if details is None:
            details = ""
        if not isinstance(details, str):
            raise AuditError("details must be str")
        if len(details) > 1000:
            raise AuditError("details too long")
        # Block secrets in details - basic check
        low = details.lower()
        for bad in ["password", "secret", "token", "sk-", "ghp_"]:
            if bad in low:
                raise AuditError(f"Do not log secrets - details contains '{bad}'")
        entry = {"timestamp": int(time.time()), "user_id": user_id, "action": action, "resource": resource, "result": result, "details": details, "prev_hash": self._prev_hash}
        canonical = json.dumps(entry, sort_keys=True, separators=(",", ":"))
        entry_hash = hashlib.sha256(canonical.encode()).hexdigest()
        entry["entry_hash"] = entry_hash
        self._prev_hash = entry_hash
        # Append
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
        return entry

    def verify_chain(self) -> dict:
        if not self.log_path.exists():
            return {"valid": True, "entries": 0, "message": "No log file - Empty chain valid"}
        lines = self.log_path.read_text(encoding="utf-8").strip().splitlines()
        lines = [l for l in lines if l.strip()]
        prev = "GENESIS"
        for idx, line in enumerate(lines):
            try:
                entry = json.loads(line)
            except Exception:
                return {"valid": False, "entries": len(lines), "failed_at": idx, "message": f"Corrupted JSON at entry {idx}"}
            stored_hash = entry.pop("entry_hash", None)
            if stored_hash is None:
                return {"valid": False, "entries": len(lines), "failed_at": idx, "message": f"Missing hash at entry {idx}"}
            # Check prev_hash linkage
            if entry.get("prev_hash") != prev:
                return {"valid": False, "entries": len(lines), "failed_at": idx, "message": f"Prev hash mismatch at entry {idx} - Tampered or reordered"}
            canonical = json.dumps(entry, sort_keys=True, separators=(",", ":"))
            computed = hashlib.sha256(canonical.encode()).hexdigest()
            if computed != stored_hash:
                return {"valid": False, "entries": len(lines), "failed_at": idx, "message": f"Hash mismatch at entry {idx} - Tampered"}
            prev = stored_hash
        return {"valid": True, "entries": len(lines), "message": "Chain valid - No tampering"}

    def get_entries(self, user_id: Optional[str] = None, action: Optional[str] = None, result: Optional[str] = None) -> List[dict]:
        if not self.log_path.exists():
            return []
        out = []
        for line in self.log_path.read_text(encoding="utf-8").strip().splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            if user_id is not None and e.get("user_id") != user_id:
                continue
            if action is not None and e.get("action") != action:
                continue
            if result is not None and e.get("result") != result:
                continue
            out.append(e)
        return out

    def count(self) -> int:
        return len(self.get_entries())

    def get_info(self) -> dict:
        v = self.verify_chain()
        return {"log_file": str(self.log_path), "entries": v.get("entries", 0), "chain_valid": v.get("valid"), "hash": "SHA256 chain"}
