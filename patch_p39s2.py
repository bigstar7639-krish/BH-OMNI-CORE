import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_stt" not in t:
    old = 'def get_omni_brain(msg="brain"):'
    new = '''def get_omni_stt(msg="stt"):
    try:
        from omni_stt import handle_stt
        r = handle_stt(msg)
        if r is None:
            r = "STT: 'stt' / 'stt listen' nu try pannu da!"
        return {"reply": r, "source": "omni_stt.py - Voice to Text"}
    except Exception as e:
        return {"reply": f"STT error: {e}", "source": "omni_stt.py"}
def get_omni_brain(msg="brain"):'''
    assert old in t, "server brain function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_stt" not in t:
    old2 = '        if self.path.startswith("/api/omni_brain"):'
    new2 = '''        if self.path.startswith("/api/omni_stt"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "stt"
            self.send_json(get_omni_stt(msg))
        if self.path.startswith("/api/omni_brain"):'''
    assert old2 in t, "server brain route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI STT" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🎤 OMNI STT - Phase 39 Step 2! (Voice to Text)</b><br><br>
<div id="sttHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">STT Ready! Phone mic venum.</div><br>
<button onclick="sendSTT()">Check STT</button>
<script>
async function sendSTT(){
  let hh=document.getElementById('sttHistory');
  let r=await fetch('/api/omni_stt?msg='+encodeURIComponent('stt'));
  let j=await r.json();
  hh.textContent='STT: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P39S2 DONE")
