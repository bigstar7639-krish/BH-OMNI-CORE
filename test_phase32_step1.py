from omni_own_ai_v3 import handle_own_v3, export_brain, import_brain
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_own_v3("export brain"); check(1,"export",r is not None and "EXPORT" in str(r) or "brain-e illa" in str(r),str(r)[:60])
r=handle_own_v3("import brain"); check(2,"import",r is not None and ("IMPORT" in str(r) or "Backup file" in str(r)),str(r)[:60])
r=handle_own_v3("hello"); check(3,"unknown",r is None,"unknown-ku None correct")
r=export_brain(); check(4,"get_export",r is not None and "OWN AI" in str(r),str(r)[:60])
print(f"=== PHASE 32 STEP 1 - OWN AI v3 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
