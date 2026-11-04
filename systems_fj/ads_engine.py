
from typing import Dict, List

class AdsError(Exception):
    pass

class AdsEngine:
    """
    Phase 3 Step 2 - System G - Ads Engine
    - Create ad: {title, type banner/interstitial/rewarded, reward_coins}
    - Show ad: impression++, frequency cap 5/day per user per ad -> FAIL if exceeded
    - Click: click++, reward only for rewarded ads
    - Stats: impressions, clicks, CTR
    - NOT real AdMob - Local simulation only, no real revenue
    """
    VALID_TYPES = ["banner", "interstitial", "rewarded"]
    def __init__(self, freq_cap: int = 5):
        if freq_cap < 1 or freq_cap > 20:
            raise AdsError("freq_cap must be 1-20")
        self._ads: Dict[str, dict] = {}
        self._freq_cap = freq_cap
        self._views: Dict[str, Dict[str, int]] = {}  # user -> ad_id -> count

    def create(self, ad_id: str, title: str, ad_type: str, reward_coins: int = 0) -> bool:
        if ad_id is None or not isinstance(ad_id, str) or len(ad_id.strip()) == 0:
            raise AdsError("ad_id cannot be empty")
        ad_id = ad_id.strip()
        if title is None or not isinstance(title, str) or len(title.strip()) == 0:
            raise AdsError("title cannot be empty")
        if ad_type not in self.VALID_TYPES:
            raise AdsError(f"Invalid ad_type: {ad_type} - Must be {self.VALID_TYPES}")
        if reward_coins is None or not isinstance(reward_coins, int) or reward_coins < 0 or reward_coins > 1000:
            raise AdsError("reward_coins must be 0-1000")
        if ad_type != "rewarded" and reward_coins != 0:
            raise AdsError("Only rewarded ads can have reward_coins")
        if ad_id in self._ads:
            raise AdsError(f"Duplicate ad: {ad_id}")
        self._ads[ad_id] = {"ad_id": ad_id, "title": title.strip(), "type": ad_type, "reward_coins": reward_coins, "impressions": 0, "clicks": 0}
        return True

    def show(self, ad_id: str, user_id: str) -> dict:
        if ad_id not in self._ads:
            raise AdsError(f"Ad not found: {ad_id}")
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise AdsError("user_id cannot be empty")
        user_id = user_id.strip()
        key = f"{user_id}:{ad_id}"
        count = self._views.get(key, 0)
        if count >= self._freq_cap:
            raise AdsError(f"Frequency cap reached: {self._freq_cap}/day for {ad_id}")
        self._views[key] = count + 1
        self._ads[ad_id]["impressions"] += 1
        return {"ad_id": ad_id, "shown": True, "views_today": count+1, "reward_coins": self._ads[ad_id]["reward_coins"] if self._ads[ad_id]["type"]=="rewarded" else 0}

    def click(self, ad_id: str) -> bool:
        if ad_id not in self._ads:
            raise AdsError(f"Ad not found: {ad_id}")
        self._ads[ad_id]["clicks"] += 1
        return True

    def stats(self, ad_id: str) -> dict:
        if ad_id not in self._ads:
            raise AdsError(f"Ad not found: {ad_id}")
        a = self._ads[ad_id]
        ctr = round((a["clicks"] / a["impressions"] * 100) if a["impressions"]>0 else 0.0, 2)
        return {"ad_id": ad_id, "impressions": a["impressions"], "clicks": a["clicks"], "ctr_percent": ctr}

    def list_ads(self) -> List[str]:
        return sorted(list(self._ads.keys()))

    def get_info(self) -> dict:
        return {"ads": len(self._ads), "freq_cap": self._freq_cap, "principle": "Local simulation - No real AdMob / No real revenue"}
