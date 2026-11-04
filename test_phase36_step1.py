from omni_mega_full import handle_mega
passed=0; total=6
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_mega("mega"); check(1,"mega_menu",r is not None and "MEGA" in str(r),str(r)[:50])
r=handle_mega("mega joke"); check(2,"mega_joke",r is not None and "JOKE" in str(r),str(r)[:50])
r=handle_mega("mega kadhai"); check(3,"mega_kadhai",r is not None and "KADHAI" in str(r),str(r)[:50])
r=handle_mega("mega motivation"); check(4,"mega_motivation",r is not None and "MOTIVATION" in str(r),str(r)[:50])
r=handle_mega("mega quiz"); check(5,"mega_quiz",r is not None and "QUIZ" in str(r),str(r)[:50])
r=handle_mega("hello"); check(6,"mega_unknown",r is None,"unknown-ku None correct")
print(f"=== PHASE 36 - MEGA FULL ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
