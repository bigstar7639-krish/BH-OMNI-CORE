from omni_brain_full import handle_brain, BRAIN
passed=0; total=6
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_brain("brain"); check(1,"brain_status",r is not None and "BRAIN" in str(r),str(r)[:60])
r=handle_brain("brain vanakkam"); check(2,"brain_greet",r is not None and "BRAIN" in str(r),str(r)[:60])
r=handle_brain("brain joke sollu"); check(3,"brain_joke",r is not None and "joke" in str(r).lower(),str(r)[:60])
r=handle_brain("brain weather eppadi"); check(4,"brain_weather",r is not None and "weather" in str(r).lower(),str(r)[:60])
r=handle_brain("brain xyzabc123"); check(5,"brain_unknown",r is not None and "theriyala" in str(r) or "kathukala" in str(r),str(r)[:60])
r=handle_brain("hello"); check(6,"brain_unknown2",r is None,"unknown-ku None correct")
print(f"=== PHASE 37 - FULL BRAIN ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
