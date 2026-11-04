import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_own_v3" not in t:
    old = 'def get_omni_own_v2(msg="my lessons"):'
    new = '''def get_omni_own_v3(msg="export brain"):
    try:
        from omni_own_ai_v3 import handle_own_v3
        r = handle_own_v3(msg)
        if r is None:
            r = "Own AI v3: 'export brain' / 'import brain' nu try pannu da!"
        return {"reply": r, "source": "omni_own_ai_v3.py - 100% OWN"}
    except Exception as e:
        return {"reply": f"Own AI v3 error: {e}", "source": "omni_own_ai_v3.py"}
def get_omni_own_v2(msg="my lessons"):'''
    assert old in t, "server own v2 function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_own_v3" not in t:
    old2 = '        if self.path.startswith("/api/omni_own_v2"):'
    new2 = '''        if self.path.startswith("/api/omni_own_v3"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "export brain"
            self.send_json(get_omni_own_v3(msg))
        if self.path.startswith("/api/omni_own_v2"):'''
    assert old2 in t, "server own v2 route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OWN AI v3" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🧠 OWN AI v3 - Phase 32 Step 2! (Brain Backup)</b><br><br>
<div id="ownV3History" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Own AI v3 Ready!</div><br>
<button onclick="sendOwnV3('export brain')">Export Brain</button>
<button onclick="sendOwnV3('import brain')">Import Brain</button>
<script>
async function sendOwnV3(msg){
  let hh=document.getElementById('ownV3History');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_own_v3?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nOWN AI v3: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P32S2 DONE")
