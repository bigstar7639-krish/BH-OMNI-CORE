import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_translate_live" not in t:
    old = 'def get_omni_weather_live(msg="live weather"):'
    new = '''def get_omni_translate_live(msg="translate live hello"):
    try:
        from omni_translate_live import handle_translate_live
        r = handle_translate_live(msg)
        if r is None:
            r = "Live Translate: 'translate live en|ta hello' nu try pannu da!"
        return {"reply": r, "source": "omni_translate_live.py - MyMemory FREE"}
    except Exception as e:
        return {"reply": f"Live Translate error: {e}", "source": "omni_translate_live.py"}
def get_omni_weather_live(msg="live weather"):'''
    assert old in t, "server weather live function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_translate_live" not in t:
    old2 = '        if self.path.startswith("/api/omni_weather_live"):'
    new2 = '''        if self.path.startswith("/api/omni_translate_live"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "translate live hello"
            self.send_json(get_omni_translate_live(msg))
        if self.path.startswith("/api/omni_weather_live"):'''
    assert old2 in t, "server weather live route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "LIVE TRANSLATE" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🌐 LIVE TRANSLATE - Phase 27 Step 2! (MyMemory FREE)</b><br><br>
<div id="transLiveHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Live Translate Ready!</div><br>
<input id="transLiveInput" value="translate live en|ta hello" style="width:65%" onkeydown="if(event.key==='Enter')sendTransLive()">
<button onclick="sendTransLive()">Translate Live</button>
<script>
async function sendTransLive(){
  let msg=document.getElementById('transLiveInput').value;
  let hh=document.getElementById('transLiveHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_translate_live?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nTRANS: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P27S2 DONE")
