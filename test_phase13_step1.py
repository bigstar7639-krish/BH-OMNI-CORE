from omni_goal import handle_goal, get_goals
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_goal("goal add Learn Python"); check(1,"goal_add",r is not None and "Goal added" in str(r),str(r)[:50])
r=handle_goal("goals"); check(2,"goal_list",r is not None and "GOALS" in str(r),"list vandhuchu")
r=handle_goal("goal done 1"); check(3,"goal_done",r is not None and "Super" in str(r),str(r)[:50])
r=handle_goal("goal"); check(4,"goal_keyword",r is not None,"keyword works")
r=handle_goal("goal list"); check(5,"goal_list_kw",r is not None,"list kw works")
r=handle_goal("hello"); check(6,"goal_unknown",r is None,"unknown-ku None correct")
r=handle_goal("goal add "); check(7,"goal_empty",r is not None and "Goal sollu" in str(r),str(r)[:50])
g=get_goals(); check(8,"goal_get",isinstance(g,list) and len(g)>=1,f"{len(g)} goals")
print(f"=== PHASE 13 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
