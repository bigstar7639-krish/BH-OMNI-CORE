passed=0; total=6
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
try:
    from omni_books import handle_books; r=handle_books("books"); check(1,"books",r is not None and "BOOKS" in str(r),str(r)[:40])
except Exception as e: check(1,"books",False,str(e))
try:
    from omni_ocr import handle_ocr; r=handle_ocr("ocr"); check(2,"ocr",r is not None and "OCR" in str(r),str(r)[:40])
except Exception as e: check(2,"ocr",False,str(e))
try:
    from omni_files import handle_files; r=handle_files("read VERSION.txt"); check(3,"files",r is not None and "FILE" in str(r),str(r)[:40])
except Exception as e: check(3,"files",False,str(e))
try:
    from omni_network import handle_network; r=handle_network("network"); check(4,"network",r is not None and "NETWORK" in str(r),str(r)[:40])
except Exception as e: check(4,"network",False,str(e))
try:
    from omni_health import handle_health; r=handle_health("med add Test 9AM"); check(5,"health",r is not None and "MED" in str(r),str(r)[:40])
except Exception as e: check(5,"health",False,str(e))
try:
    from omni_budget import handle_budget; r=handle_budget("budget set 5000"); check(6,"budget",r is not None and "BUDGET" in str(r),str(r)[:40])
except Exception as e: check(6,"budget",False,str(e))
print(f"=== ONE-SHOT COMPLETE ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
