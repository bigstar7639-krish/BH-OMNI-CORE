import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_own_v4" not in t:
    old = 'def get_omni_own_v3(msg="export brain"):'
    new = '''def get_omni_own_v4(msg="correct test | answer"):
    try:
        from omni_own_ai_auto import handle_auto
        r = handle_auto(msg)
        if r is None:
            r = "Own AI v4: 'correct Q | correct answer' nu try pannu da!"
        return {"reply": r, "source": "omni_own_ai_auto.py - 100% OWN"}
    except Exception as e:
        return {"reply": f"Own AI v4 error: {e}", "source": "omni_own_ai_auto.py"}
def get_omni_own_v3(msg="export brain"):'''
    assert old in t, "server own v3 function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_own_v4" not in t:
    old2 = '        if self.path.startswith("/api/omni_own_v3"):'
    new2 = '''        if self.path.startswith("/api/omni_own_v4"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "correct test | answer"
            self.send_json(get_omni_own_v4(msg))
        if self.path.startswith("/api/omni_own_v3"):'''
    assert old2 in t, "server own v3 route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OWN AI v4" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🧠 OWN AI v4 - Phase 33 Step 2! (Auto-Learn Correction)</b><br><br>
<div id="ownV4History" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Own AI v4 Ready! Thappa sonna thiruthi kodu!</div><br>
<input id="ownV4Input" value="correct en peru enna | Un peru Krish!" style="width:65%" onkeydown="if(event.key==='Enter')sendOwnV4()">
<button onclick="sendOwnV4()">Correct Me</button>
<script>
async function sendOwnV4(){
  let msg=document.getElementById('ownV4Input').value;
  let hh=document.getElementById('ownV4History');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_own_v4?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nOWN AI v4: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P33S2 DONE")
