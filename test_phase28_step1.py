from omni_tts import handle_tts, speak
passed=0; total=4
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
r=handle_tts("speak Vanakkam"); check(1,"tts_speak",r is not None and "TTS" in str(r),str(r)[:80])
r=handle_tts("speak"); check(2,"tts_ready",r is not None and "TTS" in str(r),str(r)[:80])
r=handle_tts("hello"); check(3,"tts_unknown",r is None,"unknown-ku None correct")
r=speak("test"); check(4,"get_speak",r is not None and "TTS" in str(r),str(r)[:80])
print(f"=== PHASE 28 STEP 1 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
