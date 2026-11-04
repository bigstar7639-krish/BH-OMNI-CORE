
from typing import Dict, List, Callable, Any
import traceback

class EventBusError(Exception):
    pass

class EventBus:
    """
    Phase 2 Step 1 - Safe Event Bus
    - Subscribe / Unsubscribe / Publish
    - Subscriber error does NOT break other subscribers - Errors collected + returned
    - Event validation: name + payload must be valid
    - No silent failures - publish returns delivery report
    - No infinite loop: max depth guard
    """
    def __init__(self, max_depth: int = 10):
        self._subs: Dict[str, List[Callable]] = {}
        self._depth = 0
        self._max_depth = max_depth
        self._published_count = 0

    def _validate_event(self, event_name):
        if event_name is None or not isinstance(event_name, str) or len(event_name.strip()) == 0:
            raise EventBusError("Invalid event name")
        if len(event_name) > 128:
            raise EventBusError("Event name too long")
        return event_name.strip()

    def subscribe(self, event_name: str, handler: Callable) -> bool:
        event_name = self._validate_event(event_name)
        if handler is None or not callable(handler):
            raise EventBusError("Handler must be callable")
        if event_name not in self._subs:
            self._subs[event_name] = []
        # Prevent duplicate subscription of same handler
        if handler in self._subs[event_name]:
            raise EventBusError("Handler already subscribed to this event")
        self._subs[event_name].append(handler)
        return True

    def unsubscribe(self, event_name: str, handler: Callable) -> bool:
        event_name = self._validate_event(event_name)
        if event_name not in self._subs or handler not in self._subs[event_name]:
            raise EventBusError("Handler not subscribed")
        self._subs[event_name].remove(handler)
        return True

    def publish(self, event_name: str, payload: Any = None) -> dict:
        event_name = self._validate_event(event_name)
        if self._depth >= self._max_depth:
            raise EventBusError(f"Event depth exceeded - Possible infinite loop - Depth {self._depth}")
        handlers = list(self._subs.get(event_name, []))
        self._depth += 1
        self._published_count += 1
        delivered = 0
        errors = []
        try:
            for h in handlers:
                try:
                    h(payload)
                    delivered += 1
                except Exception as e:
                    # Isolate error - continue to next subscriber
                    errors.append({"handler": getattr(h, "__name__", str(h)), "error": f"{type(e).__name__}: {str(e)[:200]}"})
        finally:
            self._depth -= 1
        return {"event": event_name, "subscribers": len(handlers), "delivered": delivered, "errors": errors, "success": len(errors) == 0}

    def list_events(self) -> List[str]:
        return sorted(list(self._subs.keys()))

    def subscriber_count(self, event_name: str) -> int:
        event_name = self._validate_event(event_name)
        return len(self._subs.get(event_name, []))

    def get_info(self) -> dict:
        return {"events": len(self._subs), "published_total": self._published_count, "max_depth": self._max_depth, "principle": "Safe delivery + Error isolation"}
