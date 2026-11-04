from omni_lang import handle_lang, detect_lang
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_lang("translate vanakkam"); check(1,"lang_translate",r is not None and "Hello" in str(r),str(r)[:50])
r=handle_lang("translate hello"); check(2,"lang_translate2",r is not None and "Vanakkam" in str(r),str(r)[:50])
r=handle_lang("detect Vanakkam da"); check(3,"lang_detect",r is not None and "Tanglish" in str(r),str(r)[:50])
r=handle_lang("languages"); check(4,"lang_list",r is not None and "LANGUAGES" in str(r),"list works")
r=handle_lang("hello"); check(5,"lang_unknown",r is None,"unknown-ku None correct")
r=handle_lang("translate xyzabc"); check(6,"lang_not_found",r is not None and "illa" in str(r),str(r)[:50])
r=detect_lang("Hello world"); check(7,"detect_en",r=="English",r)
r=handle_lang("detect Hello"); check(8,"detect_api",r is not None and "English" in str(r),str(r)[:50])
print(f"=== PHASE 18 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
