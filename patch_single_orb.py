import pathlib
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "single-orb-mode" in h:
    print("Single Orb Mode already irukku")
else:
    # CSS - Orb-a perusa center-la podu, cards-a hide pannu
    css = """
<style id="single-orb-mode">
.single-orb-on .card{display:none !important}
.single-orb-on .omni-orb-wrap{display:block !important;text-align:center}
.single-orb-on .omni-orb{width:200px !important;height:200px !important}
.single-orb-on #orbFeature{display:block !important}
#orbFeature{display:none;background:#020617;border:2px solid #06b6d4;border-radius:16px;padding:16px;margin:16px auto;max-width:500px;text-align:center}
#orbFeature h2{margin:0 0 8px 0}
#orbFeature p{margin:0;opacity:.9}
.orb-btn{margin:6px;padding:8px 14px;border-radius:10px;border:1px solid #06b6d4;background:#0b1026;color:#fff;cursor:pointer}
</style>
"""
    if "</head>" in h:
        h = h.replace("</head>", css + "</head>", 1)
    else:
        h = css + h
    # Orb-ku keezha - Feature display + Buttons
    orb_html = '''<div id="orbFeature"><h2 id="orbFeatureTitle">BH-OMNI CORE</h2><p id="orbFeatureText">Orb-a paaru da - Features auto-a maarum!</p><br><button class="orb-btn" onclick="orbPrev()">◀ Prev</button><button class="orb-btn" onclick="orbNext()">Next ▶</button><button class="orb-btn" onclick="orbToggleAuto()">Auto: ON</button></div>
<script>
let orbFeatures = [
  ["🧠 OWN AI", "Nee solli kodu, naan kathukiren! 100 lessons! - 'own ai' nu kekku"],
  ["🌦️ LIVE WEATHER", "Chennai weather live-a paaru! - 'live weather Chennai'"],
  ["🌐 LIVE TRANSLATE", "English to Tamil live! - 'translate live en|ta hello'"],
  ["🔊 TTS", "Phone-la kural varum! - 'speak Vanakkam'"],
  ["📚 BOOKS", "Gutenberg free books! - 'book tamil'"],
  ["💰 BUDGET", "Budget + Expense track! - 'budget'"],
  ["🎯 HABIT + GOAL", "Daily habit + goal! - 'habits' / 'goals'"],
  ["📝 POETRY + MEGA", "Kadhai + Joke + Quiz! - 'mega'"],
  ["🧠 FULL BRAIN", "En brain - Intent purinjikiren! - 'brain joke sollu'"],
  ["💊 HEALTH", "Meds + Water! - 'meds' / 'water'"],
  ["🏠 SMART HOME", "Simulation - Light/Fan/AC! - 'home'"],
  ["🤖 AUTOMATION", "Auto tasks! - 'auto'"],
  ["📊 STATS + BACKUP", "Project stats! - 'stats' / 'backup'"],
  ["🎤 STT", "Voice to Text! - 'stt'"],
  ["📷 OCR", "Photo-la irundhu text! - 'ocr'"],
  ["💡 MOTIVATION", "Daily quote! - 'quote'"],
];
let orbIdx = 0, orbAuto = true, orbTimer = null;
function orbShow(i){
  orbIdx = (i + orbFeatures.length) % orbFeatures.length;
  document.getElementById('orbFeatureTitle').textContent = orbFeatures[orbIdx][0];
  document.getElementById('orbFeatureText').textContent = orbFeatures[orbIdx][1];
}
function orbNext(){ orbShow(orbIdx+1); }
function orbPrev(){ orbShow(orbIdx-1); }
function orbToggleAuto(){
  orbAuto = !orbAuto;
  event.target.textContent = 'Auto: ' + (orbAuto ? 'ON' : 'OFF');
  if(orbAuto) orbStart(); else clearInterval(orbTimer);
}
function orbStart(){
  clearInterval(orbTimer);
  orbTimer = setInterval(()=>{ if(orbAuto) orbShow(orbIdx+1); }, 4000);
}
// Single Orb Mode ON - Ella cards-um hide, Orb + 1 Feature mattum!
document.body.classList.add('single-orb-on');
orbShow(0); orbStart();
</script>
'''
    # Orb wrap-ku appuram podu - orbFeature div-a
    if '<div class="omni-orb-wrap">' in h:
        # Orb wrap mudiyura idathula - simple-a orb label-ku appuram podu
        h = h.replace('</div>\n</div>', '</div>\n</div>\n' + orb_html, 1) if False else h
        # Safe: body start-la podu - orb-ku munnadi
        h = h.replace('<body>', '<body>\n' + orb_html, 1) if '<body>' in h else orb_html + h
    else:
        h = orb_html + h
    d.write_text(h)
    print("SINGLE ORB MODE ADDED - 1=1=1")
print("PATCH SINGLE ORB DONE")
