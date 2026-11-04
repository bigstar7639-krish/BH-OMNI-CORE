from omni_ai_free import handle_ai_free, ask_free_ai
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_ai_free("ai Vanakkam"); check(1,"ai_hello",r is not None and "OMNI" in str(r) or "Groq" in str(r),str(r)[:80])
r=handle_ai_free("ai weather"); check(2,"ai_weather",r is not None,"ai weather works")
r=handle_ai_free("hello"); check(3,"ai_unknown",r is None,"unknown-ku None correct")
r=ask_free_ai("hello"); check(4,"get_ai",r is not None and len(str(r))>10,str(r)[:80])
print(f"=== PHASE 29 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
