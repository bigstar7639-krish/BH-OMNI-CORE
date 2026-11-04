# FINAL ALL TEST - Phase 38 - Ella modules-um ore vattiya!
passed=0; total=10
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
try:
    from omni_brain_full import BRAIN; r=BRAIN.reply("joke sollu"); check(1,"brain",r is not None and "BRAIN" in str(r),str(r)[:40])
except Exception as e: check(1,"brain",False,str(e))
try:
    from omni_mega_full import handle_mega; r=handle_mega("mega joke"); check(2,"mega",r is not None,"mega works")
except Exception as e: check(2,"mega",False,str(e))
try:
    from omni_own_ai import ask_own; r=ask_own("yaaru nee"); check(3,"own_ai",r is not None,"own ai works")
except Exception as e: check(3,"own_ai",False,str(e))
try:
    from omni_weather_live import get_live_weather; r=get_live_weather("Chennai"); check(4,"weather_live",r is not None and "WEATHER" in str(r),str(r)[:40])
except Exception as e: check(4,"weather_live",False,str(e))
try:
    from omni_translate_live import live_translate; r=live_translate("hello","en","ta"); check(5,"translate_live",r is not None and "TRANSLATE" in str(r),str(r)[:40])
except Exception as e: check(5,"translate_live",False,str(e))
try:
    from omni_tts import handle_tts; r=handle_tts("speak Vanakkam"); check(6,"tts",r is not None and "TTS" in str(r),str(r)[:40])
except Exception as e: check(6,"tts",False,str(e))
try:
    from omni_quote import handle_quote; r=handle_quote("quote"); check(7,"quote",r is not None,"quote works")
except Exception as e: check(7,"quote",False,str(e))
try:
    from omni_stats import handle_stats; r=handle_stats("stats"); check(8,"stats",r is not None,"stats works")
except Exception as e: check(8,"stats",False,str(e))
try:
    from omni_backup import handle_backup; r=handle_backup("backup"); check(9,"backup",r is not None,"backup works")
except Exception as e: check(9,"backup",False,str(e))
try:
    from omni_poem import handle_poem; r=handle_poem("poem friend"); check(10,"poem",r is not None,"poem works")
except Exception as e: check(10,"poem",False,str(e))
print(f"=== FINAL ALL - PHASE 38 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
