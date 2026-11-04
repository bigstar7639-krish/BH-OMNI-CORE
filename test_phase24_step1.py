from omni_backup import handle_backup, get_backup_status
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_backup("backup"); check(1,"backup",r is not None and "BACKUP" in str(r),str(r)[:60])
r=handle_backup("backup status"); check(2,"backup_status",r is not None,"status works")
r=handle_backup("hello"); check(3,"backup_unknown",r is None,"unknown-ku None correct")
r=get_backup_status(); check(4,"get_backup",r is not None and "BACKUP" in str(r),str(r)[:60])
print(f"=== PHASE 24 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
