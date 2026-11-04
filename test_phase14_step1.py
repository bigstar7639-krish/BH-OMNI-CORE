from omni_birthday import handle_birthday, get_birthdays
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_birthday("birthday add Amma | 12-05"); check(1,"bday_add",r is not None and "Birthday added" in str(r),str(r)[:50])
r=handle_birthday("birthdays"); check(2,"bday_list",r is not None and "BIRTHDAYS" in str(r),"list vandhuchu")
r=handle_birthday("birthday"); check(3,"bday_keyword",r is not None,"keyword works")
r=handle_birthday("birthday list"); check(4,"bday_list_kw",r is not None,"list kw works")
r=handle_birthday("hello"); check(5,"bday_unknown",r is None,"unknown-ku None correct")
r=handle_birthday("birthday add no pipe"); check(6,"bday_no_pipe",r is not None and "Format" in str(r),str(r)[:50])
r=handle_birthday("birthday add Appa | 01-01"); check(7,"bday_add2",r is not None and "added" in str(r).lower(),str(r)[:50])
b=get_birthdays(); check(8,"bday_get",isinstance(b,list) and len(b)>=1,f"{len(b)} birthdays")
print(f"=== PHASE 14 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
