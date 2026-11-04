
import time
from collections import deque
from typing import Dict

class RateLimitError(Exception):
    pass

class RateLimiter:
    """
    Phase 1 Step 6 - Rate Limiting + Brute-Force Protection
    - Sliding window: max_requests per window_seconds per key (IP / user / endpoint)
    - Brute-force: LoginAttemptTracker - 5 fails -> 15 min lockout
    - In-memory only - No persistent storage in demo
    """
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        if max_requests <= 0 or window_seconds <= 0:
            raise RateLimitError("Invalid rate limit params")
        self.max_requests = max_requests
        self.window = window_seconds
        self._buckets: Dict[str, deque] = {}

    def _validate_key(self, key):
        if key is None or not isinstance(key, str) or len(key.strip()) == 0:
            raise RateLimitError("Invalid rate limit key")
        return key.strip()

    def is_allowed(self, key: str) -> bool:
        key = self._validate_key(key)
        now = time.time()
        q = self._buckets.get(key)
        if q is None:
            q = deque()
            self._buckets[key] = q
        # Remove old timestamps outside window
        while q and (now - q[0] > self.window):
            q.popleft()
        if len(q) >= self.max_requests:
            return False
        q.append(now)
        return True

    def check(self, key: str):
        if not self.is_allowed(key):
            raise RateLimitError(f"Rate limit exceeded for {key} - Try later")

    def reset(self, key: str):
        key = self._validate_key(key)
        self._buckets.pop(key, None)

    def remaining(self, key: str) -> int:
        key = self._validate_key(key)
        now = time.time()
        q = self._buckets.get(key, deque())
        # Count within window
        cnt = sum(1 for t in q if now - t <= self.window)
        return max(0, self.max_requests - cnt)

    def get_info(self) -> dict:
        return {"max_requests": self.max_requests, "window_seconds": self.window, "tracked_keys": len(self._buckets)}

class LoginAttemptTracker:
    """Brute-force: 5 failed logins -> 15 min lockout per user/IP"""
    def __init__(self, max_failures: int = 5, lockout_seconds: int = 900):
        self.max_failures = max_failures
        self.lockout_seconds = lockout_seconds
        self._failures: Dict[str, list] = {}  # key -> list of timestamps
        self._locked_until: Dict[str, float] = {}

    def _validate_key(self, key):
        if key is None or not isinstance(key, str) or len(key.strip()) == 0:
            raise RateLimitError("Invalid key")
        return key.strip()

    def is_locked(self, key: str) -> bool:
        key = self._validate_key(key)
        until = self._locked_until.get(key, 0)
        if time.time() < until:
            return True
        # Lock expired - clear
        if until != 0:
            self._locked_until.pop(key, None)
            self._failures.pop(key, None)
        return False

    def record_failure(self, key: str):
        key = self._validate_key(key)
        now = time.time()
        lst = self._failures.get(key, [])
        lst.append(now)
        # Keep only recent failures within lockout window
        lst = [t for t in lst if now - t <= self.lockout_seconds]
        self._failures[key] = lst
        if len(lst) >= self.max_failures:
            self._locked_until[key] = now + self.lockout_seconds

    def record_success(self, key: str):
        key = self._validate_key(key)
        self._failures.pop(key, None)
        self._locked_until.pop(key, None)

    def check_allowed(self, key: str):
        if self.is_locked(key):
            raise RateLimitError(f"Account locked - Too many failed attempts - Try after {self.lockout_seconds}s")
