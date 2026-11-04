from omni_daily import get_daily, handle_daily

def t1(): d=get_daily(); assert "OMNI DAILY PLANNER" in d; print("TEST 1 daily_title: PASS")
def t2(): r=handle_daily("today"); assert r is not None and "MOTIVATION" in r; print("TEST 2 daily_today: PASS")
def t3(): r=handle_daily("daily"); assert r is not None; print("TEST 3 daily_keyword_daily: PASS")
def t4(): r=handle_daily("innaiku"); assert r is not None; print("TEST 4 daily_keyword_innaiku: PASS")
def t5(): r=handle_daily("planner"); assert r is not None; print("TEST 5 daily_keyword_planner: PASS")
def t6(): r=handle_daily("plan"); assert r is None; print("TEST 6 daily_unknown_returns_none: PASS - correct behaviour")
def t7(): r=handle_daily(""); assert r is None; print("TEST 7 daily_empty_returns_none: PASS")
def t8():
    d=get_daily()
    assert "TODOS" in d and "NOTES" in d and "NIGHT SUMMARY" in d
    print("TEST 8 daily_sections: PASS - Todos+Notes+Night Summary irukku")

t1();t2();t3();t4();t5();t6();t7();t8()
print("=== PHASE 8 STEP 4 TEST RESULTS ===")
print("Total: 8 PASS, 0 FAIL")
