import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_tts" not in t:
    old = 'def get_omni_translate_live(msg="translate live hello"):'
    new = '''def get_omni_tts(msg="speak Vanakkam"):
    try:
        from omni_tts import handle_tts
        r = handle_tts(msg)
        if r is None:
            r = "TTS: 'speak Vanakkam' nu try pannu da!"
        return {"reply": r, "source": "omni_tts.py - termux-tts FREE"}
    except Exception as e:
        return {"reply": f"TTS error: {e}", "source": "omni_tts.py"}
def get_omni_translate_live(msg="translate live hello"):'''
    assert old in t, "server translate live function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_tts" not in t:
    old2 = '        if self.path.startswith("/api/omni_translate_live"):'
    new2 = '''        if self.path.startswith("/api/omni_tts"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "speak Vanakkam"
            self.send_json(get_omni_tts(msg))
        if self.path.startswith("/api/omni_translate_live"):'''
    assert old2 in t, "server translate live route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI TTS" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🔊 OMNI TTS - Phase 28 Step 2! (termux-tts FREE)</b><br><br>
<div id="ttsHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">TTS Ready! Phone-la mattum kural varum.</div><br>
<input id="ttsInput" value="speak Vanakkam Krish" style="width:65%" onkeydown="if(event.key==='Enter')sendTTS()">
<button onclick="sendTTS()">Speak</button>
<script>
async function sendTTS(){
  let msg=document.getElementById('ttsInput').value;
  let hh=document.getElementById('ttsHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_tts?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nTTS: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P28S2 DONE")
