from omni_emergency import handle_emergency, get_emergency
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_emergency("stop"); check(1,"em_stop",r is not None and "STOP" in str(r),str(r)[:50])
r=handle_emergency("resume"); check(2,"em_resume",r is not None and "resumed" in str(r).lower(),str(r)[:50])
r=handle_emergency("sos add Test 12345"); check(3,"sos_add",r is not None and "SOS Contact" in str(r),str(r)[:50])
r=handle_emergency("sos"); check(4,"sos_list",r is not None and "EMERGENCY" in str(r),"sos list works")
r=handle_emergency("sos trigger"); check(5,"sos_trigger",r is not None and "SOS TRIGGERED" in str(r),str(r)[:50])
r=handle_emergency("hello"); check(6,"em_unknown",r is None,"unknown-ku None correct")
r=handle_emergency("emergency stop"); check(7,"em_stop_kw",r is not None and "STOP" in str(r),str(r)[:50])
e=get_emergency(); check(8,"em_get",isinstance(e,dict) and "contacts" in e,f"contacts {len(e['contacts'])}")
print(f"=== PHASE 17 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
