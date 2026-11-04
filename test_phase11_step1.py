from omni_flash import handle_flash, get_flash
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_flash("flash add Tamil Nadu capital? | Chennai"); check(1,"flash_add",r is not None and "Flashcard added" in str(r),str(r)[:50])
r=handle_flash("flashcards"); check(2,"flash_list",r is not None and "FLASHCARDS" in str(r),"list vandhuchu")
r=handle_flash("flash"); check(3,"flash_keyword",r is not None,"keyword works")
r=handle_flash("flash quiz"); check(4,"flash_quiz",r is not None and "QUIZ" in str(r),str(r)[:50])
r=handle_flash("hello"); check(5,"flash_unknown",r is None,"unknown-ku None correct")
r=handle_flash("flash add no pipe"); check(6,"flash_no_pipe",r is not None and "format" in str(r).lower(),str(r)[:50])
r=handle_flash("flash add Q? | A"); check(7,"flash_add2",r is not None and "added" in str(r).lower(),str(r)[:50])
f=get_flash(); check(8,"flash_get",isinstance(f,list) and len(f)>=1,f"{len(f)} flashcards")
print(f"=== PHASE 11 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
