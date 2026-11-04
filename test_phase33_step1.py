from omni_own_ai_auto import handle_auto, correct
from omni_own_ai import ask_own
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=correct("auto test q", "auto test correct a"); check(1,"correct",r is not None and "CORRECTED" in str(r),str(r)[:60])
r=ask_own("auto test q"); check(2,"ask_corrected",r is not None and "auto test correct a" in str(r),str(r)[:60])
r=handle_auto("correct auto test q2 | auto a2"); check(3,"handle_correct",r is not None and "CORRECTED" in str(r),str(r)[:60])
r=handle_auto("hello"); check(4,"unknown",r is None,"unknown-ku None correct")
print(f"=== PHASE 33 STEP 1 - OWN AI v4 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
