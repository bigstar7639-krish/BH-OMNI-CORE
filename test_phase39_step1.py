from omni_stt import handle_stt, listen_once
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_stt("stt"); check(1,"stt",r is not None and "STT" in str(r),str(r)[:60])
r=handle_stt("stt listen"); check(2,"stt_listen",r is not None,"listen works")
r=handle_stt("hello"); check(3,"stt_unknown",r is None,"unknown-ku None correct")
r=listen_once(); check(4,"get_listen",r is not None and "STT" in str(r),str(r)[:60])
print(f"=== PHASE 39 STEP 1 - STT ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
