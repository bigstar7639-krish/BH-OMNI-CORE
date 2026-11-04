import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_own_ai" not in t:
    old = 'def get_omni_tts(msg="speak Vanakkam"):'
    new = '''def get_omni_own_ai(msg="own ai"):
    try:
        from omni_own_ai import handle_own_ai
        r = handle_own_ai(msg)
        if r is None:
            r = "Own AI: 'own ai Vanakkam' / 'teach Q | A' nu try pannu da!"
        return {"reply": r, "source": "omni_own_ai.py - 100% OWN, NO API"}
    except Exception as e:
        return {"reply": f"Own AI error: {e}", "source": "omni_own_ai.py"}
def get_omni_tts(msg="speak Vanakkam"):'''
    assert old in t, "server tts function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_own_ai" not in t:
    old2 = '        if self.path.startswith("/api/omni_tts"):'
    new2 = '''        if self.path.startswith("/api/omni_own_ai"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "own ai"
            self.send_json(get_omni_own_ai(msg))
        if self.path.startswith("/api/omni_tts"):'''
    assert old2 in t, "server tts route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OWN AI" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🧠 OWN AI - Phase 30 Step 2! (100% OWN, NO API)</b><br><br>
<div id="ownAiHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Own AI Ready! Nee solli kodu, naan kathukiren!</div><br>
<input id="ownAiInput" value="own ai" style="width:65%" onkeydown="if(event.key==='Enter')sendOwnAi()">
<button onclick="sendOwnAi()">Ask Own AI</button><br><br>
<input id="ownAiTeach" value="teach vanakkam | Vanakkam Krish!" style="width:65%" onkeydown="if(event.key==='Enter')teachOwnAi()">
<button onclick="teachOwnAi()">Teach Me</button>
<script>
async function sendOwnAi(){
  let msg=document.getElementById('ownAiInput').value;
  let hh=document.getElementById('ownAiHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_own_ai?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nOWN AI: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
async function teachOwnAi(){
  let msg=document.getElementById('ownAiTeach').value;
  let hh=document.getElementById('ownAiHistory');
  hh.textContent+='\\n\\nTEACH: '+msg;
  let r=await fetch('/api/omni_own_ai?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nOWN AI: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P30S2 DONE")
