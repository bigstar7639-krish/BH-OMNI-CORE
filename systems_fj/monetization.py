
from typing import Dict, List

class MonetizationError(Exception):
    pass

class Monetization:
    """
    Phase 3 Step 2 - System G - Monetization
    - Plans: free, pro, premium - monthly price in coins/INR
    - Coins: earn via rewarded ads, spend on premium features
    - Subscribe: user -> plan, expiry simulated (30 days)
    - Purchase coins, check premium, cancel
    - NOT real Play Billing - Local simulation only, no real money
    """
    PLANS = {"free": {"price_inr": 0, "coins_per_month": 0, "premium": False}, "pro": {"price_inr": 99, "coins_per_month": 100, "premium": True}, "premium": {"price_inr": 199, "coins_per_month": 300, "premium": True}}
    def __init__(self):
        self._users: Dict[str, dict] = {}  # user -> {plan, coins}

    def _ensure_user(self, user_id):
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise MonetizationError("user_id cannot be empty")
        user_id = user_id.strip()
        if user_id not in self._users:
            self._users[user_id] = {"plan": "free", "coins": 0}
        return user_id

    def subscribe(self, user_id: str, plan: str) -> bool:
        user_id = self._ensure_user(user_id)
        if plan not in self.PLANS:
            raise MonetizationError(f"Invalid plan: {plan} - Must be {list(self.PLANS.keys())}")
        self._users[user_id]["plan"] = plan
        # Grant monthly coins on subscribe
        self._users[user_id]["coins"] += self.PLANS[plan]["coins_per_month"]
        return True

    def cancel(self, user_id: str) -> bool:
        user_id = self._ensure_user(user_id)
        self._users[user_id]["plan"] = "free"
        return True

    def add_coins(self, user_id: str, amount: int) -> int:
        user_id = self._ensure_user(user_id)
        if amount is None or not isinstance(amount, int) or amount <= 0 or amount > 10000:
            raise MonetizationError("amount must be 1-10000")
        self._users[user_id]["coins"] += amount
        return self._users[user_id]["coins"]

    def spend_coins(self, user_id: str, amount: int) -> int:
        user_id = self._ensure_user(user_id)
        if amount is None or not isinstance(amount, int) or amount <= 0:
            raise MonetizationError("amount must be >0")
        if self._users[user_id]["coins"] < amount:
            raise MonetizationError(f"Insufficient coins: have {self._users[user_id]['coins']}, need {amount}")
        self._users[user_id]["coins"] -= amount
        return self._users[user_id]["coins"]

    def is_premium(self, user_id: str) -> bool:
        user_id = self._ensure_user(user_id)
        return self.PLANS[self._users[user_id]["plan"]]["premium"]

    def get_user(self, user_id: str) -> dict:
        user_id = self._ensure_user(user_id)
        u = self._users[user_id]
        return {"user_id": user_id, "plan": u["plan"], "coins": u["coins"], "premium": self.is_premium(user_id)}

    def get_info(self) -> dict:
        return {"users": len(self._users), "plans": list(self.PLANS.keys()), "principle": "Local simulation - No real Play Billing / No real money"}
