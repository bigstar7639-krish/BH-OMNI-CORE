
from typing import Dict, List

class AnalyticsError(Exception):
    pass

class Analytics:
    """
    Phase 3 Step 3 - System H - Analytics
    - Track event: {user_id, event_name, props}
    - Valid events: app_open, story_read, voice_play, ad_click, purchase, search
    - Counts per event, per user, total events
    - No PII - user_id is opaque id only, no name/email/phone stored
    - In-memory only
    """
    VALID_EVENTS = ["app_open", "story_read", "voice_play", "ad_click", "purchase", "search", "login", "logout"]
    def __init__(self):
        self._events: List[dict] = []
        self._per_event: Dict[str, int] = {}
        self._per_user: Dict[str, int] = {}

    def track(self, user_id: str, event_name: str, props: dict = None) -> bool:
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise AnalyticsError("user_id cannot be empty")
        if event_name not in self.VALID_EVENTS:
            raise AnalyticsError(f"Invalid event: {event_name} - Must be {self.VALID_EVENTS}")
        if props is not None and not isinstance(props, dict):
            raise AnalyticsError("props must be dict")
        # PII blocklist - never store name/email/phone
        if props:
            for k in props.keys():
                lk = str(k).lower()
                if lk in ("name", "email", "phone", "password", "token"):
                    raise AnalyticsError(f"PII blocked: {k} cannot be tracked")
        user_id = user_id.strip()
        self._events.append({"user_id": user_id, "event": event_name, "props": dict(props) if props else {}})
        self._per_event[event_name] = self._per_event.get(event_name, 0) + 1
        self._per_user[user_id] = self._per_user.get(user_id, 0) + 1
        return True

    def event_count(self, event_name: str) -> int:
        if event_name not in self.VALID_EVENTS:
            raise AnalyticsError(f"Invalid event: {event_name}")
        return self._per_event.get(event_name, 0)

    def user_count(self, user_id: str) -> int:
        return self._per_user.get(user_id.strip() if isinstance(user_id, str) else "", 0)

    def total_events(self) -> int:
        return len(self._events)

    def unique_users(self) -> int:
        return len(self._per_user)

    def top_events(self, n: int = 3) -> List[dict]:
        if n < 1 or n > 10:
            raise AnalyticsError("n must be 1-10")
        sorted_e = sorted(self._per_event.items(), key=lambda x: (-x[1], x[0]))
        return [{"event": k, "count": v} for k, v in sorted_e[:n]]

    def get_info(self) -> dict:
        return {"total_events": len(self._events), "unique_users": len(self._per_user), "principle": "No PII - Opaque user_id only"}
