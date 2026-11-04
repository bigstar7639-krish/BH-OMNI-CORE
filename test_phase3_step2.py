# BH-OMNI CORE - Phase 3 Step 2 - System G - Ads + Monetization - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from systems_fj.ads_engine import AdsEngine, AdsError
from systems_fj.monetization import Monetization, MonetizationError

def test_ads_create():
    try:
        a = AdsEngine()
        assert a.create("ad1", "Super App", "banner") == True
        assert "ad1" in a.list_ads()
        print("TEST ads_create: PASS - Ad created")
        return "PASS"
    except Exception as e:
        print(f"TEST ads_create: FAIL - {e}")
        return "FAIL"

def test_ads_show_click():
    try:
        a = AdsEngine()
        a.create("ad1", "Reward Ad", "rewarded", reward_coins=10)
        r = a.show("ad1", "user1")
        assert r["shown"] == True and r["reward_coins"] == 10
        a.click("ad1")
        s = a.stats("ad1")
        assert s["impressions"] == 1 and s["clicks"] == 1 and s["ctr_percent"] == 100.0
        print(f"TEST ads_show_click: PASS - CTR {s['ctr_percent']}%")
        return "PASS"
    except Exception as e:
        print(f"TEST ads_show_click: FAIL - {e}")
        return "FAIL"

def test_ads_freq_cap():
    try:
        a = AdsEngine(freq_cap=2)
        a.create("ad1", "Test", "banner")
        a.show("ad1", "u1"); a.show("ad1", "u1")
        try:
            a.show("ad1", "u1")
            print("TEST ads_freq_cap: FAIL - Cap should block 3rd show")
            return "FAIL"
        except AdsError:
            # Different user should still work
            a.show("ad1", "u2")
            print("TEST ads_freq_cap: PASS - Cap blocks same user, other user ok")
            return "PASS"
    except Exception as e:
        print(f"TEST ads_freq_cap: FAIL - {e}")
        return "FAIL"

def test_ads_invalid():
    try:
        a = AdsEngine()
        try:
            a.create("ad1", "X", "badtype")
            print("TEST ads_invalid: FAIL - Bad type should fail")
            return "FAIL"
        except AdsError:
            pass
        try:
            a.create("ad1", "X", "banner", reward_coins=10)
            print("TEST ads_invalid: FAIL - Banner with reward should fail")
            return "FAIL"
        except AdsError:
            print("TEST ads_invalid: PASS - Invalid type/reward rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST ads_invalid: FAIL - {e}")
        return "FAIL"

def test_monet_subscribe():
    try:
        m = Monetization()
        m.subscribe("u1", "pro")
        u = m.get_user("u1")
        assert u["plan"] == "pro" and u["premium"] == True and u["coins"] == 100
        m.cancel("u1")
        assert m.get_user("u1")["plan"] == "free"
        print("TEST monet_subscribe: PASS - Pro 100 coins, cancel to free")
        return "PASS"
    except Exception as e:
        print(f"TEST monet_subscribe: FAIL - {e}")
        return "FAIL"

def test_monet_coins():
    try:
        m = Monetization()
        assert m.add_coins("u1", 50) == 50
        assert m.spend_coins("u1", 20) == 30
        try:
            m.spend_coins("u1", 100)
            print("TEST monet_coins: FAIL - Overspend should fail")
            return "FAIL"
        except MonetizationError:
            print("TEST monet_coins: PASS - Add/spend/overspend blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST monet_coins: FAIL - {e}")
        return "FAIL"

def test_monet_premium_check():
    try:
        m = Monetization()
        assert m.is_premium("newuser") == False
        m.subscribe("newuser", "premium")
        assert m.is_premium("newuser") == True
        print("TEST monet_premium_check: PASS - Free not premium, Premium is premium")
        return "PASS"
    except Exception as e:
        print(f"TEST monet_premium_check: FAIL - {e}")
        return "FAIL"

def test_monet_invalid():
    try:
        m = Monetization()
        try:
            m.subscribe("u1", "ultra")
            print("TEST monet_invalid: FAIL - Bad plan should fail")
            return "FAIL"
        except MonetizationError:
            pass
        try:
            m.add_coins("u1", -5)
            print("TEST monet_invalid: FAIL - Negative coins should fail")
            return "FAIL"
        except MonetizationError:
            print("TEST monet_invalid: PASS - Invalid plan/coins rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST monet_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_ads_create, test_ads_show_click, test_ads_freq_cap, test_ads_invalid, test_monet_subscribe, test_monet_coins, test_monet_premium_check, test_monet_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 3 STEP 2 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase3_2_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
