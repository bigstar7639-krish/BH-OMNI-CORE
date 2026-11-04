from omni_own_ai import handle_own_ai, teach, ask_own
import pathlib
# Test-ku thani file use pannu - real model-a azhikadha
passed=0; total=5
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=teach("test vanakkam", "Test Vanakkam Krish!"); check(1,"teach",r is not None and "LEARNED" in str(r),str(r)[:60])
r=ask_own("test vanakkam"); check(2,"ask_exact",r is not None and "Test Vanakkam" in str(r),str(r)[:60])
r=handle_own_ai("own ai"); check(3,"status",r is not None and "OWN AI" in str(r),str(r)[:60])
r=handle_own_ai("own ai xyzabc123notfound"); check(4,"ask_new",r is not None and "theriyala" in str(r),str(r)[:60])
r=handle_own_ai("hello"); check(5,"unknown",r is None,"unknown-ku None correct")
print(f"=== PHASE 30 STEP 1 - OWN AI ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
