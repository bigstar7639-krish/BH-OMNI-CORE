# BH-OMNI CORE - Phase 3 Step 3 - System H - Analytics + Insights - Termux
from pathlib import Path
import sys
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
from systems_fj.analytics import Analytics, AnalyticsError
from systems_fj.insights import Insights, InsightsError

def test_analytics_track():
    try:
        a = Analytics()
        assert a.track("u1", "app_open") == True
        assert a.track("u1", "story_read", {"story": "Chennai Hero"}) == True
        assert a.total_events() == 2
        print("TEST analytics_track: PASS - 2 events tracked")
        return "PASS"
    except Exception as e:
        print(f"TEST analytics_track: FAIL - {e}")
        return "FAIL"

def test_analytics_counts():
    try:
        a = Analytics()
        a.track("u1", "app_open"); a.track("u1", "app_open"); a.track("u2", "search")
        assert a.event_count("app_open") == 2
        assert a.user_count("u1") == 2
        assert a.unique_users() == 2
        print("TEST analytics_counts: PASS - Per-event/user counts ok")
        return "PASS"
    except Exception as e:
        print(f"TEST analytics_counts: FAIL - {e}")
        return "FAIL"

def test_analytics_top():
    try:
        a = Analytics()
        a.track("u1", "search"); a.track("u1", "search"); a.track("u1", "app_open")
        top = a.top_events(2)
        assert top[0]["event"] == "search" and top[0]["count"] == 2
        print(f"TEST analytics_top: PASS - Top {top[0]['event']} {top[0]['count']}")
        return "PASS"
    except Exception as e:
        print(f"TEST analytics_top: FAIL - {e}")
        return "FAIL"

def test_analytics_pii_blocked():
    try:
        a = Analytics()
        try:
            a.track("u1", "login", {"email": "test@test.com"})
            print("TEST analytics_pii_blocked: FAIL - Email should be blocked")
            return "FAIL"
        except AnalyticsError:
            pass
        try:
            a.track("u1", "bad_event")
            print("TEST analytics_pii_blocked: FAIL - Bad event should fail")
            return "FAIL"
        except AnalyticsError:
            print("TEST analytics_pii_blocked: PASS - PII + bad event blocked")
            return "PASS"
    except Exception as e:
        print(f"TEST analytics_pii_blocked: FAIL - {e}")
        return "FAIL"

def test_insights_build():
    try:
        ins = Insights()
        r = ins.build(10, 2, {"search": 6, "app_open": 4}, {"u1": 7, "u2": 3})
        assert r["engagement_per_user"] == 5.0 and r["verdict"] == "MEDIUM"
        assert r["top_event"] == "search" and r["top_user"] == "u1"
        print(f"TEST insights_build: PASS - Engagement {r['engagement_per_user']}, {r['verdict']}")
        return "PASS"
    except Exception as e:
        print(f"TEST insights_build: FAIL - {e}")
        return "FAIL"

def test_insights_no_data():
    try:
        ins = Insights()
        r = ins.build(0, 0, {}, {})
        assert r["verdict"] == "NO-DATA" and r["top_event"] is None
        print("TEST insights_no_data: PASS - No-data handled")
        return "PASS"
    except Exception as e:
        print(f"TEST insights_no_data: FAIL - {e}")
        return "FAIL"

def test_insights_verdicts():
    try:
        ins = Insights()
        low = ins.build(2, 2, {"app_open": 2}, {"u1": 1, "u2": 1})
        high = ins.build(20, 2, {"search": 20}, {"u1": 20})
        assert low["verdict"] == "LOW" and high["verdict"] == "HIGH"
        print(f"TEST insights_verdicts: PASS - LOW {low['engagement_per_user']} vs HIGH {high['engagement_per_user']}")
        return "PASS"
    except Exception as e:
        print(f"TEST insights_verdicts: FAIL - {e}")
        return "FAIL"

def test_insights_invalid():
    try:
        ins = Insights()
        try:
            ins.build(-1, 1, {}, {})
            print("TEST insights_invalid: FAIL - Negative should fail")
            return "FAIL"
        except InsightsError:
            print("TEST insights_invalid: PASS - Invalid inputs rejected")
            return "PASS"
    except Exception as e:
        print(f"TEST insights_invalid: FAIL - {e}")
        return "FAIL"

if __name__ == "__main__":
    tests = [test_analytics_track, test_analytics_counts, test_analytics_top, test_analytics_pii_blocked, test_insights_build, test_insights_no_data, test_insights_verdicts, test_insights_invalid]
    results = {}
    for f in tests:
        print(f"--- {f.__name__} ---")
        results[f.__name__] = f()
    print("\n=== PHASE 3 STEP 3 TEST RESULTS ===")
    for k,v in results.items():
        print(f"{k}: {v}")
    passed = sum(1 for s in results.values() if s=="PASS")
    failed = sum(1 for s in results.values() if s=="FAIL")
    print(f"\nTotal: {passed} PASS, {failed} FAIL")
    import json
    with open(str(BASE / "step_phase3_3_test_results.json"), "w") as f:
        json.dump(results, f, indent=2)
