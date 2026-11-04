import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_habit" not in t:
    old = 'def get_omni_daily(msg="daily"):'
    new = '''def get_omni_habit(msg="habits"):
    try:
        from omni_habit import handle_habit
        r = handle_habit(msg)
        if r is None:
            r = "Habit illa da! 'habit add Exercise' nu add pannu!"
        return {"reply": r, "source": "omni_habit.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Habit error: {e}", "source": "omni_habit.py"}
def get_omni_daily(msg="daily"):'''
    assert old in t, "server daily function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_habit" not in t:
    old2 = '        if self.path.startswith("/api/omni_daily"):'
    new2 = '''        if self.path.startswith("/api/omni_habit"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "habits"
            self.send_json(get_omni_habit(msg))
        if self.path.startswith("/api/omni_daily"):'''
    assert old2 in t, "server daily route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI HABIT" not in h:
    old3 = '<div class="card"><b>🌅 OMNI DAILY PLANNER'
    assert old3 in h, "dashboard daily card illa!"
    new3 = '''<div class="card"><b>🎯 OMNI HABIT TRACKER - Phase 9 Step 2!</b><br><br>
<div id="habitHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Habit Tracker Ready!</div><br>
<input id="habitInput" value="habits" style="width:65%" onkeydown="if(event.key==='Enter')sendHabit()">
<button onclick="sendHabit()">Send Habit</button>
<script>
async function sendHabit(){
  let msg=document.getElementById('habitInput').value;
  let h=document.getElementById('habitHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_habit?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nHABIT: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🌅 OMNI DAILY PLANNER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P9S2 DONE")
