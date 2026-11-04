import pathlib
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
anchor = '<div class="card"><b>🌅 OMNI DAILY BRIEFING'
assert anchor in h, "briefing card illa!"
cards = ""
if "OMNI LANGUAGE" not in h:
    cards += '''<div class="card"><b>🌐 OMNI LANGUAGE - Phase 18 Step 2!</b><br><br>
<div id="langHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Language Ready!</div><br>
<input id="langInput" value="translate vanakkam" style="width:65%" onkeydown="if(event.key==='Enter')sendLang()">
<button onclick="sendLang()">Send Lang</button>
<script>
async function sendLang(){
  let msg=document.getElementById('langInput').value;
  let hh=document.getElementById('langHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_lang?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nLANG: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    print("Lang card ready")
if "OMNI CODE" not in h:
    cards += '''<div class="card"><b>💻 OMNI CODE HELPER - Phase 19 Step 2!</b><br><br>
<div id="codeHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Code Helper Ready!</div><br>
<input id="codeInput" value="code python" style="width:65%" onkeydown="if(event.key==='Enter')sendCode()">
<button onclick="sendCode()">Send Code</button>
<script>
async function sendCode(){
  let msg=document.getElementById('codeInput').value;
  let hh=document.getElementById('codeHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_code?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nCODE: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    print("Code card ready")
if "OMNI WEATHER" not in h:
    cards += '''<div class="card"><b>🌦️ OMNI WEATHER INFO - Phase 20 Step 2! (Live API illa)</b><br><br>
<div id="weatherHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Weather Info Ready!</div><br>
<input id="weatherInput" value="weather rain" style="width:65%" onkeydown="if(event.key==='Enter')sendWeather()">
<button onclick="sendWeather()">Send Weather</button>
<script>
async function sendWeather(){
  let msg=document.getElementById('weatherInput').value;
  let hh=document.getElementById('weatherHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_weather?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nWEATHER: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    print("Weather card ready")
if "OMNI POEM" not in h and "OMNI POETRY" not in h:
    cards += '''<div class="card"><b>📝 OMNI POETRY - Phase 21 Step 2!</b><br><br>
<div id="poemHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Poetry Ready!</div><br>
<input id="poemInput" value="poem friend" style="width:65%" onkeydown="if(event.key==='Enter')sendPoem()">
<button onclick="sendPoem()">Send Poem</button>
<script>
async function sendPoem(){
  let msg=document.getElementById('poemInput').value;
  let hh=document.getElementById('poemHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_poem?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nPOEM: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    print("Poem card ready")
h = h.replace(anchor, cards + anchor)
d.write_text(h)
print("PATCH MISSING 4 DONE")
