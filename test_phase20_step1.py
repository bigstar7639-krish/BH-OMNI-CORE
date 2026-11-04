from omni_weather import handle_weather
passed=0; total=8
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_weather("weather rain"); check(1,"weather_rain",r is not None and "Rain" in str(r),str(r)[:50])
r=handle_weather("weather flood"); check(2,"weather_flood",r is not None and "Flood" in str(r),str(r)[:50])
r=handle_weather("weather"); check(3,"weather_list",r is not None and "TOPICS" in str(r),"list works")
r=handle_weather("weather list"); check(4,"weather_list_kw",r is not None,"list kw works")
r=handle_weather("hello"); check(5,"weather_unknown",r is None,"unknown-ku None correct")
r=handle_weather("weather xyzabc"); check(6,"weather_notfound",r is not None and "topics" in str(r).lower(),str(r)[:50])
r=handle_weather("weather heat"); check(7,"weather_heat",r is not None and "Heat" in str(r),str(r)[:50])
r=handle_weather("weather earthquake"); check(8,"weather_quake",r is not None and "Earthquake" in str(r),str(r)[:50])
print(f"=== PHASE 20 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
