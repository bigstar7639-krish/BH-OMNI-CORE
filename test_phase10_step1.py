from omni_mood import handle_mood, get_moods
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_mood("mood happy"); check(1,"mood_add",r is not None and "Mood saved" in str(r),str(r)[:50])
r=handle_mood("moods"); check(2,"mood_list",r is not None and "MOOD" in str(r),"list vandhuchu")
r=handle_mood("mood"); check(3,"mood_keyword",r is not None,"keyword works")
r=handle_mood("mood list"); check(4,"mood_list_kw",r is not None,"list kw works")
r=handle_mood("hello"); check(5,"mood_unknown",r is None,"unknown-ku None correct")
r=handle_mood("mood "); check(6,"mood_space_is_list",r is not None and "MOOD" in str(r),"space strip -> list correct")
r=handle_mood("mood sad"); check(7,"mood_sad",r is not None and "Mood saved" in str(r),str(r)[:50])
moods=get_moods(); check(8,"mood_get",isinstance(moods,list) and len(moods)>=1,f"{len(moods)} moods")
print(f"=== PHASE 10 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
