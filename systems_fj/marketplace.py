
from typing import Dict, List

class MarketplaceError(Exception):
    pass

class Marketplace:
    """
    Phase 3 Step 5 - System J - Marketplace
    - List item: {item_id, title, price_coins, seller, category}
    - Categories: story, voice-pack, theme, template, sticker
    - Buy: buyer coins check via passed balance -> returns new balance (caller manages coins)
    - Duplicate item -> FAIL, sold item cannot be bought again (single copy)
    - Local simulation - NO real money, NO real Play Billing
    """
    VALID_CATEGORIES = ["story", "voice-pack", "theme", "template", "sticker"]
    def __init__(self):
        self._items: Dict[str, dict] = {}

    def list_item(self, item_id: str, title: str, price_coins: int, seller: str, category: str) -> bool:
        if item_id is None or not isinstance(item_id, str) or len(item_id.strip()) == 0:
            raise MarketplaceError("item_id cannot be empty")
        item_id = item_id.strip()
        if title is None or not isinstance(title, str) or len(title.strip()) == 0:
            raise MarketplaceError("title cannot be empty")
        if price_coins is None or not isinstance(price_coins, int) or price_coins < 0 or price_coins > 100000:
            raise MarketplaceError("price_coins must be 0-100000")
        if seller is None or not isinstance(seller, str) or len(seller.strip()) == 0:
            raise MarketplaceError("seller cannot be empty")
        if category not in self.VALID_CATEGORIES:
            raise MarketplaceError(f"Invalid category: {category} - Must be {self.VALID_CATEGORIES}")
        if item_id in self._items:
            raise MarketplaceError(f"Duplicate item: {item_id}")
        self._items[item_id] = {"item_id": item_id, "title": title.strip(), "price_coins": price_coins, "seller": seller.strip(), "category": category, "sold": False, "buyer": None}
        return True

    def buy(self, item_id: str, buyer: str, buyer_coins: int) -> dict:
        if item_id not in self._items:
            raise MarketplaceError(f"Item not found: {item_id}")
        if buyer is None or not isinstance(buyer, str) or len(buyer.strip()) == 0:
            raise MarketplaceError("buyer cannot be empty")
        if buyer_coins is None or not isinstance(buyer_coins, int) or buyer_coins < 0:
            raise MarketplaceError("buyer_coins must be >=0 int")
        item = self._items[item_id]
        if item["sold"]:
            raise MarketplaceError(f"Item already sold: {item_id}")
        if buyer.strip() == item["seller"]:
            raise MarketplaceError("Seller cannot buy own item")
        if buyer_coins < item["price_coins"]:
            raise MarketplaceError(f"Insufficient coins: have {buyer_coins}, need {item['price_coins']}")
        item["sold"] = True
        item["buyer"] = buyer.strip()
        return {"item_id": item_id, "buyer": buyer.strip(), "price_paid": item["price_coins"], "remaining_coins": buyer_coins - item["price_coins"], "seller": item["seller"]}

    def get_item(self, item_id: str) -> dict:
        if item_id not in self._items:
            raise MarketplaceError(f"Item not found: {item_id}")
        return dict(self._items[item_id])

    def list_by_category(self, category: str) -> List[dict]:
        if category not in self.VALID_CATEGORIES:
            raise MarketplaceError(f"Invalid category: {category}")
        return [dict(v) for v in self._items.values() if v["category"] == category]

    def list_all(self) -> List[str]:
        return sorted(list(self._items.keys()))

    def get_info(self) -> dict:
        return {"items": len(self._items), "sold": sum(1 for v in self._items.values() if v["sold"]), "principle": "Local simulation - No real money"}
