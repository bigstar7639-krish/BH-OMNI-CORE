# V41 S2 TESTS - 6 tests - Actual execution!
from omni_chat_v41 import ChatV41, handle_chat_v41
passed=0; total=6
def check(n,name,cond,info=""):
    global passed
    if cond: passed+=1; print(f"TEST {n} {name}: PASS - {info}")
    else: print(f"TEST {n} {name}: FAIL - {info}")
# 1. New conversation init
c = ChatV41(); check(1,"new_init",len(c.history)==0 and c.topic is None and c.turn_count==0,"fresh chat - history 0")
# 2. History stores messages
c.send("joke sollu"); check(2,"history_store",len(c.history)==2 and c.history[0]["role"]=="user","2 msgs stored - user+ai")
# 3. History retains only latest 10 turns (20 msgs)
c2 = ChatV41()
for i in range(12):
    c2.send(f"test msg {i} joke")
check(3,"history_10_turns",len(c2.history)==20 and c2.turn_count==12,f"len={len(c2.history)} - 10 turns mattum! turns={c2.turn_count}")
# 4. Follow-up can access previous context
c3 = ChatV41(); c3.send("weather Chennai"); r=c3.send("adhu eppadi")
check(4,"followup_context",r is not None and "Follow-up" in str(r) and "weather" in str(r).lower(),str(r)[:80])
# 5. Context reset clears
c3.new_chat(); check(5,"reset",len(c3.history)==0 and c3.topic is None and c3.turn_count==0,"reset - history 0")
# 6. Empty / invalid input safe
c4 = ChatV41(); r1=c4.send(""); r2=c4.send("   "); r3=c4.send(None)
check(6,"empty_safe",r1 is not None and r2 is not None and r3 is not None and "Empty" in str(r1),"empty/None safe - no crash!")
print(f"=== V41 S2 ==="); print(f"Total: {passed} PASS, {total-passed} FAIL")
