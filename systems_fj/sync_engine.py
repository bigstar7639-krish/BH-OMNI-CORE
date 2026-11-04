
from typing import Dict, List

class SyncError(Exception):
    pass

class SyncEngine:
    """
    Phase 3 Step 4 - System I - Sync Engine
    - Queue local changes: {key, value, timestamp}
    - Sync: push queued to remote (simulated dict), clear queue
    - Conflict: remote newer -> remote wins, local newer -> local wins (Last-Write-Wins)
    - Explicit strategy only - No silent overwrite
    - In-memory simulation - No real cloud sync
    """
    def __init__(self):
        self._local: Dict[str, dict] = {}  # key -> {value, ts}
        self._remote: Dict[str, dict] = {}
        self._queue: List[dict] = []

    def _validate_key(self, key):
        if key is None or not isinstance(key, str) or len(key.strip()) == 0:
            raise SyncError("key cannot be empty")
        if len(key) > 200:
            raise SyncError("key too long")
        return key.strip()

    def set_local(self, key: str, value: str, timestamp: int) -> bool:
        key = self._validate_key(key)
        if value is None or not isinstance(value, str):
            raise SyncError("value must be str")
        if timestamp is None or not isinstance(timestamp, int) or timestamp < 0:
            raise SyncError("timestamp must be >=0 int")
        self._local[key] = {"value": value, "ts": timestamp}
        self._queue.append({"key": key, "value": value, "ts": timestamp})
        return True

    def set_remote(self, key: str, value: str, timestamp: int) -> bool:
        # Test helper - Simulates remote change from another device
        key = self._validate_key(key)
        if timestamp is None or not isinstance(timestamp, int) or timestamp < 0:
            raise SyncError("timestamp must be >=0 int")
        self._remote[key] = {"value": value, "ts": timestamp}
        return True

    def queue_size(self) -> int:
        return len(self._queue)

    def sync(self) -> dict:
        # Push queued, resolve conflicts with Last-Write-Wins
        synced = 0
        conflicts = []
        for item in list(self._queue):
            k = item["key"]
            remote = self._remote.get(k)
            if remote is not None and remote["ts"] > item["ts"]:
                # Remote newer - remote wins, local overwritten
                conflicts.append({"key": k, "winner": "remote", "local_ts": item["ts"], "remote_ts": remote["ts"]})
                self._local[k] = {"value": remote["value"], "ts": remote["ts"]}
            elif remote is not None and remote["ts"] == item["ts"] and remote["value"] != item["value"]:
                # Same ts, different value - remote wins deterministically
                conflicts.append({"key": k, "winner": "remote-tiebreak", "local_ts": item["ts"], "remote_ts": remote["ts"]})
                self._local[k] = {"value": remote["value"], "ts": remote["ts"]}
            else:
                # Local newer or no remote - local wins
                self._remote[k] = {"value": item["value"], "ts": item["ts"]}
                synced += 1
        self._queue = []
        return {"synced": synced, "conflicts": conflicts, "queue_cleared": True}

    def get_local(self, key: str) -> dict:
        key = self._validate_key(key)
        if key not in self._local:
            raise SyncError(f"Local key not found: {key}")
        return dict(self._local[key])

    def get_remote(self, key: str) -> dict:
        key = self._validate_key(key)
        if key not in self._remote:
            raise SyncError(f"Remote key not found: {key}")
        return dict(self._remote[key])

    def get_info(self) -> dict:
        return {"local_keys": len(self._local), "remote_keys": len(self._remote), "queued": len(self._queue), "principle": "Last-Write-Wins + Explicit conflict report"}
