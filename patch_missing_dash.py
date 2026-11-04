import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
# Briefing + Emergency server - illa-na mattum add
for fname, funcname, mod, handler, default in [
    ("Briefing", "get_omni_briefing", "omni_briefing", "handle_briefing", "briefing"),
    ("Emergency", "get_omni_emergency", "omni_emergency", "handle_emergency", "sos"),
]:
    if funcname not in t:
        # Travel function-ku munnadi podu - adhu kandippa irukku
        old = 'def get_omni_travel(msg="trips"):'
        new = f'''def {funcname}(msg="{default}"):
    try:
        from {mod} import {handler}
        r = {handler}(msg)
        if r is None:
            r = "{fname} illa da!"
        return {{"reply": r, "source": "{mod}.py - SAME PROJECT"}}
    except Exception as e:
        return {{"reply": f"{fname} error: {{e}}", "source": "{mod}.py"}}
def get_omni_travel(msg="trips"):'''
        assert old in t
        t = t.replace(old, new)
        print(f"Server {fname} added")
    else:
        print(f"Server {fname} already irukku")
    route = f"/api/{funcname.replace('get_','')}"
    # get_omni_briefing -> /api/omni_briefing
    route = f"/api/omni_{fname.lower()}"
    if route not in t:
        old2 = '        if self.path.startswith("/api/omni_travel"):'
        new2 = f'''        if self.path.startswith("{route}"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "{default}"
            self.send_json({funcname}(msg))
        if self.path.startswith("/api/omni_travel"):'''
        assert old2 in t
        t = t.replace(old2, new2)
        print(f"Route {route} added")
    else:
        print(f"Route {route} already irukku")
s.write_text(t)

d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
# Briefing card
if "OMNI BRIEFING" not in h:
    old3 = '<div class="card"><b>✈ OMNI TRAVEL PLANNER'
    assert old3 in h
    new3 = '''<div class="card"><b>🌅 OMNI BRIEFING - Phase 16 Step 2!</b><br><br>
<div id="briefHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Briefing Ready!</div><br>
<input id="briefInput" value="briefing" style="width:65%" onkeydown="if(event.key==='Enter')sendBrief()">
<button onclick="sendBrief()">Send Briefing</button>
<script>
async function sendBrief(){
  let msg=document.getElementById('briefInput').value;
  let h=document.getElementById('briefHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_briefing?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nBRIEFING: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>✈ OMNI TRAVEL PLANNER'''
    h = h.replace(old3, new3)
    print("Dashboard Briefing added")
else:
    print("Dashboard Briefing already irukku")
# Emergency card
if "OMNI EMERGENCY" not in h:
    old4 = '<div class="card"><b>🌅 OMNI BRIEFING'
    assert old4 in h
    new4 = '''<div class="card"><b>🆘 OMNI EMERGENCY - Phase 17 Step 1! (Local record only)</b><br><br>
<div id="emHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Emergency Ready! Real SMS illa.</div><br>
<input id="emInput" value="sos" style="width:65%" onkeydown="if(event.key==='Enter')sendEm()">
<button onclick="sendEm()">Send Emergency</button>
<script>
async function sendEm(){
  let msg=document.getElementById('emInput').value;
  let h=document.getElementById('emHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_emergency?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nEMERGENCY: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🌅 OMNI BRIEFING'''
    h = h.replace(old4, new4)
    print("Dashboard Emergency added")
else:
    print("Dashboard Emergency already irukku")
d.write_text(h)
print("PATCH MISSING DASH DONE")
