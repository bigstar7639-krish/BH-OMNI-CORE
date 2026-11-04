import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_briefing" not in t:
    old = 'def get_omni_travel(msg="trips"):'
    new = '''def get_omni_briefing(msg="briefing"):
    try:
        from omni_briefing import handle_briefing
        r = handle_briefing(msg)
        if r is None:
            r = "Briefing: 'briefing' nu type pannu da!"
        return {"reply": r, "source": "omni_briefing.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Briefing error: {e}", "source": "omni_briefing.py"}
def get_omni_travel(msg="trips"):'''
    assert old in t, "server travel function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_briefing" not in t:
    old2 = '        if self.path.startswith("/api/omni_travel"):'
    new2 = '''        if self.path.startswith("/api/omni_briefing"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "briefing"
            self.send_json(get_omni_briefing(msg))
        if self.path.startswith("/api/omni_travel"):'''
    assert old2 in t, "server travel route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI BRIEFING" not in h:
    old3 = '<div class="card"><b>✈️ OMNI TRAVEL PLANNER'
    assert old3 in h, "dashboard travel card illa!"
    new3 = '''<div class="card"><b>🌅 OMNI DAILY BRIEFING - Phase 16 Step 2!</b><br><br>
<div id="briefHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Daily Briefing Ready!</div><br>
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
<div class="card"><b>✈️ OMNI TRAVEL PLANNER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P16S2 DONE")
