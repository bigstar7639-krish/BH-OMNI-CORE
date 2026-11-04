import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_goal" not in t:
    old = 'def get_omni_water(msg="water count"):'
    new = '''def get_omni_goal(msg="goals"):
    try:
        from omni_goal import handle_goal
        r = handle_goal(msg)
        if r is None:
            r = "Goal illa da! 'goal add Learn Python' nu add pannu!"
        return {"reply": r, "source": "omni_goal.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Goal error: {e}", "source": "omni_goal.py"}
def get_omni_water(msg="water count"):'''
    assert old in t, "server water function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_goal" not in t:
    old2 = '        if self.path.startswith("/api/omni_water"):'
    new2 = '''        if self.path.startswith("/api/omni_goal"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "goals"
            self.send_json(get_omni_goal(msg))
        if self.path.startswith("/api/omni_water"):'''
    assert old2 in t, "server water route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI GOAL" not in h:
    old3 = '<div class="card"><b>💧 OMNI WATER REMINDER'
    assert old3 in h, "dashboard water card illa!"
    new3 = '''<div class="card"><b>🎯 OMNI GOAL TRACKER - Phase 13 Step 2!</b><br><br>
<div id="goalHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Goal Tracker Ready!</div><br>
<input id="goalInput" value="goals" style="width:65%" onkeydown="if(event.key==='Enter')sendGoal()">
<button onclick="sendGoal()">Send Goal</button>
<script>
async function sendGoal(){
  let msg=document.getElementById('goalInput').value;
  let h=document.getElementById('goalHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_goal?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nGOAL: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>💧 OMNI WATER REMINDER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P13S2 DONE")
