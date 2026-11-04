from omni_own_ai import ask_own, teach
from omni_own_ai_v2 import handle_own_v2
from omni_own_ai_v3 import handle_own_v3
from omni_own_ai_auto import handle_auto
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
# 1. Bulk lessons irukka?
r=ask_own("yaaru nee"); check(1,"bulk_yaaru",r is not None and "OWN AI" in str(r),str(r)[:60])
r=ask_own("unakku pudicha food enna"); check(2,"bulk_food",r is not None and "biryani" in str(r).lower() or "OWN" in str(r),str(r)[:60])
# 2. Teach works?
r=teach("final test q", "final test a"); check(3,"teach",r is not None and "LEARNED" in str(r),str(r)[:60])
r=ask_own("final test q"); check(4,"ask_teach",r is not None and "final test a" in str(r),str(r)[:60])
# 3. v2 works?
r=handle_own_v2("my brain"); check(5,"v2_brain",r is not None and "BRAIN" in str(r),str(r)[:60])
# 4. v3 works?
r=handle_own_v3("export brain"); check(6,"v3_export",r is not None and "OWN AI" in str(r),str(r)[:60])
# 5. v4 works?
r=handle_auto("correct final test q | final corrected a"); check(7,"v4_correct",r is not None and "CORRECTED" in str(r),str(r)[:60])
r=ask_own("final test q"); check(8,"v4_ask",r is not None and "final corrected a" in str(r),str(r)[:60])
print(f"=== OWN AI FULL ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
