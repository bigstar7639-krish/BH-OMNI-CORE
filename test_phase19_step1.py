from omni_code import handle_code
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_code("code python"); check(1,"code_python",r is not None and "Python" in str(r),str(r)[:50])
r=handle_code("code git"); check(2,"code_git",r is not None and "git" in str(r).lower(),str(r)[:50])
r=handle_code("code"); check(3,"code_list",r is not None and "TOPICS" in str(r),"list works")
r=handle_code("code list"); check(4,"code_list_kw",r is not None,"list kw works")
r=handle_code("hello"); check(5,"code_unknown",r is None,"unknown-ku None correct")
r=handle_code("code xyzabc"); check(6,"code_notfound",r is not None and "topics" in str(r).lower(),str(r)[:50])
r=handle_code("code loop"); check(7,"code_loop",r is not None and "Loop" in str(r),str(r)[:50])
r=handle_code("code dict"); check(8,"code_dict",r is not None and "Dict" in str(r),str(r)[:50])
print(f"=== PHASE 19 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
