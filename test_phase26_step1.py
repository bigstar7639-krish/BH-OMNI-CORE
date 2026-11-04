from omni_weather_live import handle_weather_live, get_live_weather
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_weather_live("live weather"); check(1,"live_weather",r is not None and "WEATHER" in str(r),str(r)[:80])
r=handle_weather_live("live weather Chennai"); check(2,"live_chennai",r is not None and "WEATHER" in str(r),str(r)[:80])
r=handle_weather_live("hello"); check(3,"live_unknown",r is None,"unknown-ku None correct")
r=get_live_weather("Chennai"); check(4,"get_live",r is not None and "WEATHER" in str(r),str(r)[:80])
print(f"=== PHASE 26 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
