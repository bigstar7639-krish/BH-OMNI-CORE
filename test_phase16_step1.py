from omni_briefing import handle_briefing, get_briefing
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=get_briefing(); check(1,"brief_get",r is not None and "BRIEFING" in str(r),str(r)[:50])
r=handle_briefing("briefing"); check(2,"brief_keyword",r is not None and "BRIEFING" in str(r),"briefing works")
r=handle_briefing("daily briefing"); check(3,"brief_daily",r is not None,"daily briefing works")
r=handle_briefing("summary"); check(4,"brief_summary",r is not None,"summary works")
r=handle_briefing("hello"); check(5,"brief_unknown",r is None,"unknown-ku None correct")
r=get_briefing(); check(6,"brief_todos",r is not None and "Todos" in str(r),"todos section irukku")
r=get_briefing(); check(7,"brief_expense",r is not None and "Expense" in str(r),"expense section irukku")
r=get_briefing(); check(8,"brief_all_sections",all(x in str(r) for x in ["Habits","Goals","Moods","Water","Trips","Birthdays"]),"ella sections irukku")
print(f"=== PHASE 16 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
