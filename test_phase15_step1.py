from omni_travel import handle_travel, get_trips
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_travel("trip add Chennai | 10-12"); check(1,"trip_add",r is not None and "Trip added" in str(r),str(r)[:50])
r=handle_travel("trips"); check(2,"trip_list",r is not None and "TRIPS" in str(r),"list vandhuchu")
r=handle_travel("trip"); check(3,"trip_keyword",r is not None,"keyword works")
r=handle_travel("trip list"); check(4,"trip_list_kw",r is not None,"list kw works")
r=handle_travel("hello"); check(5,"trip_unknown",r is None,"unknown-ku None correct")
r=handle_travel("trip add no pipe"); check(6,"trip_no_pipe",r is not None and "Format" in str(r),str(r)[:50])
r=handle_travel("trip add Madurai | 15-12"); check(7,"trip_add2",r is not None and "added" in str(r).lower(),str(r)[:50])
t=get_trips(); check(8,"trip_get",isinstance(t,list) and len(t)>=1,f"{len(t)} trips")
print(f"=== PHASE 15 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
