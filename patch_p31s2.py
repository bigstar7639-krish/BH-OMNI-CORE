import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_own_v2" not in t:
    old = 'def get_omni_own_ai(msg="own ai"):'
    new = '''def get_omni_own_v2(msg="my lessons"):
    try:
        from omni_own_ai_v2 import handle_own_v2
        r = handle_own_v2(msg)
        if r is None:
            r = "Own AI v2: 'my lessons' / 'my brain' / 'forget Q' nu try pannu da!"
        return {"reply": r, "source": "omni_own_ai_v2.py - 100% OWN"}
    except Exception as e:
        return {"reply": f"Own AI v2 error: {e}", "source": "omni_own_ai_v2.py"}
def get_omni_own_ai(msg="own ai"):'''
    assert old in t, "server own ai function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_own_v2" not in t:
    old2 = '        if self.path.startswith("/api/omni_own_ai"):'
    new2 = '''        if self.path.startswith("/api/omni_own_v2"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "my lessons"
            self.send_json(get_omni_own_v2(msg))
        if self.path.startswith("/api/omni_own_ai"):'''
    assert old2 in t, "server own ai route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OWN AI v2" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🧠 OWN AI v2 - Phase 31 Step 2! (Brain Manager)</b><br><br>
<div id="ownV2History" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Own AI v2 Ready!</div><br>
<button onclick="sendOwnV2('my lessons')">My Lessons</button>
<button onclick="sendOwnV2('my brain')">My Brain</button><br><br>
<input id="ownV2Forget" value="forget vanakkam" style="width:65%" onkeydown="if(event.key==='Enter')sendOwnV2Forget()">
<button onclick="sendOwnV2Forget()">Forget</button>
<script>
async function sendOwnV2(msg){
  let hh=document.getElementById('ownV2History');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_own_v2?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nOWN AI v2: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
async function sendOwnV2Forget(){
  let msg=document.getElementById('ownV2Forget').value;
  sendOwnV2(msg);
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P31S2 DONE")
