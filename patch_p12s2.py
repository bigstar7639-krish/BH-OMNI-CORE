import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_water" not in t:
    old = 'def get_omni_flash(msg="flashcards"):'
    new = '''def get_omni_water(msg="water count"):
    try:
        from omni_water import handle_water
        r = handle_water(msg)
        if r is None:
            r = "Water: 'water' nu type pannu da!"
        return {"reply": r, "source": "omni_water.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Water error: {e}", "source": "omni_water.py"}
def get_omni_flash(msg="flashcards"):'''
    assert old in t, "server flash function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_water" not in t:
    old2 = '        if self.path.startswith("/api/omni_flash"):'
    new2 = '''        if self.path.startswith("/api/omni_water"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "water count"
            self.send_json(get_omni_water(msg))
        if self.path.startswith("/api/omni_flash"):'''
    assert old2 in t, "server flash route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI WATER" not in h:
    old3 = '<div class="card"><b>📚 OMNI FLASHCARDS'
    assert old3 in h, "dashboard flash card illa!"
    new3 = '''<div class="card"><b>💧 OMNI WATER REMINDER - Phase 12 Step 2!</b><br><br>
<div id="waterHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Water Reminder Ready!</div><br>
<input id="waterInput" value="water count" style="width:65%" onkeydown="if(event.key==='Enter')sendWater()">
<button onclick="sendWater()">Send Water</button>
<script>
async function sendWater(){
  let msg=document.getElementById('waterInput').value;
  let h=document.getElementById('waterHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_water?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nWATER: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>📚 OMNI FLASHCARDS'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P12S2 DONE")
