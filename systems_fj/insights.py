
from typing import Dict, List

class InsightsError(Exception):
    pass

class Insights:
    """
    Phase 3 Step 3 - System H - Insights
    - Build insights from Analytics data (passed in, not coupled)
    - Most popular event, most active user, engagement rate
    - Engagement = total_events / unique_users (avg events per user)
    - Verdict: LOW <2, MEDIUM 2-5, HIGH >5
    - Rule-based only - NOT ML prediction
    """
    def __init__(self):
        pass

    def build(self, total_events: int, unique_users: int, per_event: Dict[str, int], per_user: Dict[str, int]) -> dict:
        if total_events is None or not isinstance(total_events, int) or total_events < 0:
            raise InsightsError("total_events must be >=0 int")
        if unique_users is None or not isinstance(unique_users, int) or unique_users < 0:
            raise InsightsError("unique_users must be >=0 int")
        if per_event is None or not isinstance(per_event, dict):
            raise InsightsError("per_event must be dict")
        if per_user is None or not isinstance(per_user, dict):
            raise InsightsError("per_user must be dict")
        if total_events == 0 or unique_users == 0:
            return {"total_events": 0, "unique_users": unique_users, "engagement_per_user": 0.0, "verdict": "NO-DATA", "top_event": None, "top_user": None, "note": "No data yet"}
        engagement = round(total_events / unique_users, 2) if unique_users > 0 else 0.0
        if engagement < 2:
            verdict = "LOW"
        elif engagement <= 5:
            verdict = "MEDIUM"
        else:
            verdict = "HIGH"
        top_event = max(per_event.items(), key=lambda x: x[1])[0] if per_event else None
        top_user = max(per_user.items(), key=lambda x: x[1])[0] if per_user else None
        return {"total_events": total_events, "unique_users": unique_users, "engagement_per_user": engagement, "verdict": verdict, "top_event": top_event, "top_user": top_user, "note": "Rule-based only - Not ML prediction"}
