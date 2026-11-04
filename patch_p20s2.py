import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_weather" not in t:
    old = 'def get_omni_code(msg="code"):'
    new = '''def get_omni_weather(msg="weather"):
    try:
        from omni_weather import handle_weather
        r = handle_weather(msg)
        if r is None:
            r = "Weather: 'weather rain' nu try pannu da!"
        return {"reply": r, "source": "omni_weather.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Weather error: {e}", "source": "omni_weather.py"}
def get_omni_code(msg="code"):'''
    assert old in t, "server code function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_weather" not in t:
    old2 = '        if self.path.startswith("/api/omni_code"):'
    new2 = '''        if self.path.startswith("/api/omni_weather"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "weather"
            self.send_json(get_omni_weather(msg))
        if self.path.startswith("/api/omni_code"):'''
    assert old2 in t, "server code route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI WEATHER" not in h:
    old3 = '<div class="card"><b>💻 OMNI CODE HELPER'
    assert old3 in h, "dashboard code card illa!"
    new3 = '''<div class="card"><b>🌦️ OMNI WEATHER INFO - Phase 20 Step 2! (Live API illa)</b><br><br>
<div id="weatherHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Weather Info Ready!</div><br>
<input id="weatherInput" value="weather rain" style="width:65%" onkeydown="if(event.key==='Enter')sendWeather()">
<button onclick="sendWeather()">Send Weather</button>
<script>
async function sendWeather(){
  let msg=document.getElementById('weatherInput').value;
  let h=document.getElementById('weatherHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_weather?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nWEATHER: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>💻 OMNI CODE HELPER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P20S2 DONE")
