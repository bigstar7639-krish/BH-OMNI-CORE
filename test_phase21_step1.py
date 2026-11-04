from omni_poem import handle_poem
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_poem("poem friend"); check(1,"poem_friend",r is not None and "Nanban" in str(r),str(r)[:50])
r=handle_poem("poem amma"); check(2,"poem_amma",r is not None and "Amma" in str(r),str(r)[:50])
r=handle_poem("poem"); check(3,"poem_list",r is not None and "POEMS" in str(r),"list works")
r=handle_poem("poem list"); check(4,"poem_list_kw",r is not None,"list kw works")
r=handle_poem("hello"); check(5,"poem_unknown",r is None,"unknown-ku None correct")
r=handle_poem("poem xyzabc"); check(6,"poem_notfound",r is not None and "topics" in str(r).lower(),str(r)[:50])
r=handle_poem("poem dream"); check(7,"poem_dream",r is not None and "Kanavu" in str(r),str(r)[:50])
r=handle_poem("poem rain"); check(8,"poem_rain",r is not None and "Mazhai" in str(r),str(r)[:50])
print(f"=== PHASE 21 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
