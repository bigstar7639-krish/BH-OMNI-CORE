from omni_translate_live import handle_translate_live, live_translate
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_translate_live("translate live hello"); check(1,"trans_live",r is not None and "TRANSLATE" in str(r),str(r)[:80])
r=handle_translate_live("translate live en|ta hello"); check(2,"trans_pair",r is not None and "TRANSLATE" in str(r),str(r)[:80])
r=handle_translate_live("hello"); check(3,"trans_unknown",r is None,"unknown-ku None correct")
r=live_translate("hello","en","ta"); check(4,"get_trans",r is not None and "TRANSLATE" in str(r),str(r)[:80])
print(f"=== PHASE 27 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
