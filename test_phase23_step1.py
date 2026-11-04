from omni_stats import handle_stats, get_stats
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_stats("stats"); check(1,"stats",r is not None and "STATS" in str(r),str(r)[:60])
r=handle_stats("status"); check(2,"status",r is not None,"status works")
r=handle_stats("hello"); check(3,"stats_unknown",r is None,"unknown-ku None correct")
r=get_stats(); check(4,"get_stats",r is not None and "V22" in str(r),str(r)[:60])
print(f"=== PHASE 23 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
