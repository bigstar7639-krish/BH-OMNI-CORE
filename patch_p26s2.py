import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_weather_live" not in t:
    old = 'def get_omni_backup(msg="backup"):'
    new = '''def get_omni_weather_live(msg="live weather"):
    try:
        from omni_weather_live import handle_weather_live
        r = handle_weather_live(msg)
        if r is None:
            r = "Live Weather: 'live weather Chennai' nu try pannu da!"
        return {"reply": r, "source": "omni_weather_live.py - wttr.in FREE"}
    except Exception as e:
        return {"reply": f"Live Weather error: {e}", "source": "omni_weather_live.py"}
def get_omni_backup(msg="backup"):'''
    assert old in t, "server backup function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_weather_live" not in t:
    old2 = '        if self.path.startswith("/api/omni_backup"):'
    new2 = '''        if self.path.startswith("/api/omni_weather_live"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "live weather"
            self.send_json(get_omni_weather_live(msg))
        if self.path.startswith("/api/omni_backup"):'''
    assert old2 in t, "server backup route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "LIVE WEATHER" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🌦️ LIVE WEATHER - Phase 26 Step 2! (wttr.in FREE)</b><br><br>
<div id="liveWeatherHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Live Weather Ready!</div><br>
<input id="liveWeatherInput" value="live weather Chennai" style="width:65%" onkeydown="if(event.key==='Enter')sendLiveWeather()">
<button onclick="sendLiveWeather()">Live Weather</button>
<script>
async function sendLiveWeather(){
  let msg=document.getElementById('liveWeatherInput').value;
  let hh=document.getElementById('liveWeatherHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_weather_live?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nLIVE: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P26S2 DONE")
