import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_travel" not in t:
    old = 'def get_omni_birthday(msg="birthdays"):'
    new = '''def get_omni_travel(msg="trips"):
    try:
        from omni_travel import handle_travel
        r = handle_travel(msg)
        if r is None:
            r = "Trip illa da! 'trip add Chennai | 10-12' nu add pannu!"
        return {"reply": r, "source": "omni_travel.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Travel error: {e}", "source": "omni_travel.py"}
def get_omni_birthday(msg="birthdays"):'''
    assert old in t, "server birthday function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_travel" not in t:
    old2 = '        if self.path.startswith("/api/omni_birthday"):'
    new2 = '''        if self.path.startswith("/api/omni_travel"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "trips"
            self.send_json(get_omni_travel(msg))
        if self.path.startswith("/api/omni_birthday"):'''
    assert old2 in t, "server birthday route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI TRAVEL" not in h:
    old3 = '<div class="card"><b>🎂 OMNI BIRTHDAY REMINDER'
    assert old3 in h, "dashboard birthday card illa!"
    new3 = '''<div class="card"><b>✈️ OMNI TRAVEL PLANNER - Phase 15 Step 2!</b><br><br>
<div id="travelHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Travel Planner Ready!</div><br>
<input id="travelInput" value="trips" style="width:65%" onkeydown="if(event.key==='Enter')sendTravel()">
<button onclick="sendTravel()">Send Travel</button>
<script>
async function sendTravel(){
  let msg=document.getElementById('travelInput').value;
  let h=document.getElementById('travelHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_travel?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nTRAVEL: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🎂 OMNI BIRTHDAY REMINDER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P15S2 DONE")
