from omni_quote import handle_quote, get_quote
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_quote("quote"); check(1,"quote",r is not None and "QUOTE" in str(r),str(r)[:60])
r=handle_quote("daily quote"); check(2,"daily_quote",r is not None,"daily quote works")
r=handle_quote("hello"); check(3,"quote_unknown",r is None,"unknown-ku None correct")
r=get_quote(); check(4,"get_quote",r is not None and "QUOTE" in str(r),str(r)[:60])
print(f"=== PHASE 25 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
