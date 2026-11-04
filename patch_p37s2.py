import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_brain" not in t:
    old = 'def get_omni_mega(msg="mega"):'
    new = '''def get_omni_brain(msg="brain"):
    try:
        from omni_brain_full import handle_brain
        r = handle_brain(msg)
        if r is None:
            r = "Brain: 'brain' / 'brain joke sollu' nu try pannu da!"
        return {"reply": r, "source": "omni_brain_full.py - FULL BRAIN"}
    except Exception as e:
        return {"reply": f"Brain error: {e}", "source": "omni_brain_full.py"}
def get_omni_mega(msg="mega"):'''
    assert old in t, "server mega function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_brain" not in t:
    old2 = '        if self.path.startswith("/api/omni_mega"):'
    new2 = '''        if self.path.startswith("/api/omni_brain"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "brain"
            self.send_json(get_omni_brain(msg))
        if self.path.startswith("/api/omni_mega"):'''
    assert old2 in t, "server mega route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "FULL BRAIN" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🧠 FULL BRAIN - Phase 37 Step 2! (Full Logic)</b><br><br>
<div id="brainHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Full Brain Ready! Nee enna kekkurenu purinjikiren!</div><br>
<input id="brainInput" value="brain joke sollu" style="width:65%" onkeydown="if(event.key==='Enter')sendBrain()">
<button onclick="sendBrain()">Ask Brain</button>
<button onclick="sendBrainStatus()">Brain Status</button>
<script>
async function sendBrain(){
  let msg=document.getElementById('brainInput').value;
  let hh=document.getElementById('brainHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_brain?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nBRAIN: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
async function sendBrainStatus(){
  let hh=document.getElementById('brainHistory');
  let r=await fetch('/api/omni_brain?msg='+encodeURIComponent('brain'));
  let j=await r.json();
  hh.textContent+='\\nBRAIN: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P37S2 DONE")
