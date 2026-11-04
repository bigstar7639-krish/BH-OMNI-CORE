# BH-OMNI CORE - Phase 3 Step 5 - System J - Marketplace + Creator - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from systems_fj.marketplace import Marketplace, MarketplaceError
from systems_fj.creator_hub import CreatorHub, CreatorError

def test_market_list():
    try:
        m = Marketplace()
        assert m.list_item("item1", "Chennai Story", 50, "seller1", "story") == True
        assert "item1" in m.list_all()
        print("TEST market_list: PASS - Item listed")
        return "PASS"
    except Exception as e:
        print(f"TEST market_list: FAIL - {e}")
        return "FAIL"

def test_market_buy():
    try:
        m = Marketplace()
        m.list_item("item1", "Story", 50, "seller1", "story")
        r = m.buy("item1", "buyer1", 100)
        assert r["remaining_coins"] == 50 and r["price_paid"] == 50
        assert m.get_item("item1")["sold"] == True
        print(f"TEST market_buy: PASS - Bought, remaining {r['remaining_coins']} coins")
        return "PASS"
    except Exception as e:
        print(f"TEST market_buy: FAIL - {e}")
        return "FAIL"

def test_market_insufficient_sold():
    try:
        m = Marketplace()
        m.list_item("item1", "Story", 100, "seller1", "story")
        try:
            m.buy("item1", "buyer1", 10)
            print("TEST market_insufficient_sold: FAIL - Insufficient should fail")
            return "FAIL"
        except MarketplaceError:
            pass
        m.buy("item1", "buyer1", 200)
        try:
            m.buy("item1", "buyer2", 200)
            print("TEST market_insufficient_sold: FAIL - Sold item should fail")
            return "FAIL"
        except MarketplaceError:
            print("TEST market_insufficient_sold: PASS - Insufficient + sold blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST market_insufficient_sold: FAIL - {e}")
        return "FAIL"

def test_market_invalid():
    try:
        m = Marketplace()
        try:
            m.list_item("i1", "X", 10, "s1", "badcat")
            print("TEST market_invalid: FAIL - Bad category should fail")
            return "FAIL"
        except MarketplaceError:
            pass
        m.list_item("i1", "X", 10, "s1", "theme")
        try:
            m.buy("i1", "s1", 100)
            print("TEST market_invalid: FAIL - Self-buy should fail")
            return "FAIL"
        except MarketplaceError:
            print("TEST market_invalid: PASS - Bad category + self-buy blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST market_invalid: FAIL - {e}")
        return "FAIL"

def test_creator_register():
    try:
        c = CreatorHub()
        assert c.register("creator1", "Krish") == True
        info = c.get_creator("creator1")
        assert info["name"] == "Krish" and info["followers"] == 0
        print("TEST creator_register: PASS - Creator registered")
        return "PASS"
    except Exception as e:
        print(f"TEST creator_register: FAIL - {e}")
        return "FAIL"

def test_creator_publish():
    try:
        c = CreatorHub()
        c.register("creator1", "Krish")
        assert c.publish("creator1", "c1", "My Story", "story") == True
        assert c.get_creator("creator1")["content_count"] == 1
        print("TEST creator_publish: PASS - Content published")
        return "PASS"
    except Exception as e:
        print(f"TEST creator_publish: FAIL - {e}")
        return "FAIL"

def test_creator_follow():
    try:
        c = CreatorHub()
        c.register("creator1", "Krish")
        assert c.follow("creator1", "user1") == True
        assert c.follower_count("creator1") == 1
        assert c.unfollow("creator1", "user1") == True
        assert c.follower_count("creator1") == 0
        print("TEST creator_follow: PASS - Follow/unfollow works")
        return "PASS"
    except Exception as e:
        print(f"TEST creator_follow: FAIL - {e}")
        return "FAIL"

def test_creator_invalid():
    try:
        c = CreatorHub()
        c.register("creator1", "Krish")
        try:
            c.follow("creator1", "creator1")
            print("TEST creator_invalid: FAIL - Self-follow should fail")
            return "FAIL"
        except CreatorError:
            pass
        try:
            c.publish("creator1", "c1", "X", "badtype")
            print("TEST creator_invalid: FAIL - Bad type should fail")
            return "FAIL"
        except CreatorError:
            print("TEST creator_invalid: PASS - Self-follow + bad type blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST creator_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_market_list, test_market_buy, test_market_insufficient_sold, test_market_invalid, test_creator_register, test_creator_publish, test_creator_follow, test_creator_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 3 STEP 5 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase3_5_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
