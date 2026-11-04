import pathlib
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI POEM" in h:
    print("Dashboard card already irukku")
else:
    idx = h.find("OMNI WEATHER")
    assert idx != -1, "weather card-e illa!"
    # Weather card-oda <div> start-a kandu pidikkarom
    start = h.rfind('<div class="card">', 0, idx)
    card = '''<div class="card"><b>📝 OMNI POETRY - Phase 21 Step 2!</b><br><br>
<div id="poemHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Poetry Ready!</div><br>
<input id="poemInput" value="poem friend" style="width:65%" onkeydown="if(event.key==='Enter')sendPoem()">
<button onclick="sendPoem()">Send Poem</button>
<script>
async function sendPoem(){
  let msg=document.getElementById('poemInput').value;
  let h=document.getElementById('poemHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_poem?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nPOEM: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
'''
    h = h[:start] + card + h[start:]
    d.write_text(h)
    print("Dashboard card added - FIXED")
print("FIX DONE")
