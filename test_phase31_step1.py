from omni_own_ai_v2 import handle_own_v2, list_lessons
from omni_own_ai import teach
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
teach("v2 test q", "v2 test a")
r=handle_own_v2("my lessons"); check(1,"list",r is not None and "LESSONS" in str(r),str(r)[:60])
r=handle_own_v2("my brain"); check(2,"brain",r is not None and "BRAIN" in str(r),str(r)[:60])
r=handle_own_v2("forget v2 test q"); check(3,"forget",r is not None and "FORGOT" in str(r),str(r)[:60])
r=handle_own_v2("hello"); check(4,"unknown",r is None,"unknown-ku None correct")
print(f"=== PHASE 31 STEP 1 - OWN AI v2 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
