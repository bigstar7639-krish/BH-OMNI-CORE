
from typing import List, Dict, Callable, Optional, Any

class OfflineError(Exception):
    pass

class OfflineFallback:
    """
    Phase 2 Step 5 - Offline Fallback
    - Online/Offline state explicit
    - Online: process via handler immediately
    - Offline: queue request, return fallback response (cached / generic)
    - Back online: replay queued requests in order
    - Queue limit 100 - Overflow -> FAIL (not silent drop)
    - Never lose queued requests silently
    """
    def __init__(self, queue_limit: int = 100):
        if queue_limit < 1 or queue_limit > 1000:
            raise OfflineError("queue_limit must be 1-1000")
        self._online = True
        self._queue: List[dict] = []
        self._queue_limit = queue_limit
        self._processed = 0

    def set_online(self, online: bool) -> bool:
        if online is None or not isinstance(online, bool):
            raise OfflineError("online must be bool")
        self._online = online
        return self._online

    def is_online(self) -> bool:
        return self._online

    def submit(self, request: str, handler: Optional[Callable] = None, fallback: str = "Offline - Request queued, will process when online") -> dict:
        if request is None or not isinstance(request, str) or len(request.strip()) == 0:
            raise OfflineError("Invalid request - Cannot be empty")
        if len(request) > 10000:
            raise OfflineError("Request too long")
        if self._online:
            if handler is None or not callable(handler):
                raise OfflineError("Online mode needs callable handler")
            try:
                result = handler(request)
            except Exception as e:
                raise OfflineError(f"Handler failed: {type(e).__name__}") from e
            self._processed += 1
            return {"status": "online", "request": request, "result": result, "queued": False}
        else:
            # Offline - queue
            if len(self._queue) >= self._queue_limit:
                raise OfflineError(f"Queue full - Limit {self._queue_limit} - Cannot queue more")
            self._queue.append({"request": request, "handler": handler, "fallback": fallback})
            return {"status": "offline-queued", "request": request, "result": fallback, "queued": True, "queue_size": len(self._queue)}

    def queue_size(self) -> int:
        return len(self._queue)

    def get_queued(self) -> List[str]:
        return [q["request"] for q in self._queue]

    def replay(self) -> dict:
        if not self._online:
            raise OfflineError("Cannot replay while offline - Go online first")
        if len(self._queue) == 0:
            return {"replayed": 0, "results": [], "failed": []}
        results = []
        failed = []
        # Copy queue, clear after attempt
        to_replay = list(self._queue)
        self._queue = []
        for item in to_replay:
            handler = item.get("handler")
            req = item["request"]
            try:
                if handler is None or not callable(handler):
                    # No handler - use fallback as result
                    results.append({"request": req, "result": item.get("fallback", "No handler")})
                else:
                    res = handler(req)
                    results.append({"request": req, "result": res})
                self._processed += 1
            except Exception as e:
                failed.append({"request": req, "error": f"{type(e).__name__}"})
                # Re-queue failed? No - report as failed, not silent loss
        return {"replayed": len(results), "results": results, "failed": failed}

    def clear_queue(self) -> int:
        n = len(self._queue)
        self._queue = []
        return n

    def get_info(self) -> dict:
        return {"online": self._online, "queued": len(self._queue), "processed": self._processed, "queue_limit": self._queue_limit, "principle": "Queue when offline + Replay when online + No silent loss"}
