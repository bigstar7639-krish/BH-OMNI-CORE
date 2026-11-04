from omni_water import handle_water, get_water
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_water("water"); check(1,"water_add",r is not None and "Water done" in str(r),str(r)[:50])
r=handle_water("water count"); check(2,"water_count",r is not None and "Water" in str(r),str(r)[:50])
r=handle_water("water done"); check(3,"water_done",r is not None and "Water done" in str(r),str(r)[:50])
r=handle_water("water total"); check(4,"water_total",r is not None,"total works")
r=handle_water("hello"); check(5,"water_unknown",r is None,"unknown-ku None correct")
r=handle_water("water status"); check(6,"water_status",r is not None and "Water" in str(r),str(r)[:50])
r=handle_water("water reset"); check(7,"water_reset",r is not None and "reset" in str(r).lower(),str(r)[:50])
c=get_water(); check(8,"water_get",isinstance(c,int) and c==0,f"count reset to {c}")
print(f"=== PHASE 12 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
