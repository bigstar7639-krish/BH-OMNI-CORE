passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
try:
    from omni_smarthome import handle_smarthome; r=handle_smarthome("light on"); check(1,"smarthome",r is not None and "SMART HOME" in str(r),str(r)[:50])
except Exception as e: check(1,"smarthome",False,str(e))
try:
    from omni_smarthome import handle_smarthome; r=handle_smarthome("home"); check(2,"home_status",r is not None and "SMART HOME" in str(r),str(r)[:50])
except Exception as e: check(2,"home_status",False,str(e))
try:
    from omni_automation import handle_automation; r=handle_automation("auto add 6AM briefing"); check(3,"automation",r is not None and "AUTOMATION" in str(r),str(r)[:50])
except Exception as e: check(3,"automation",False,str(e))
try:
    from omni_automation import handle_automation; r=handle_automation("auto"); check(4,"auto_list",r is not None,"auto list works")
except Exception as e: check(4,"auto_list",False,str(e))
print(f"=== FINAL PENDING ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
