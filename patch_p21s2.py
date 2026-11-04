import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_poem" not in t:
    old = 'def get_omni_weather(msg="weather"):'
    new = '''def get_omni_poem(msg="poem"):
    try:
        from omni_poem import handle_poem
        r = handle_poem(msg)
        if r is None:
            r = "Poem: 'poem friend' nu try pannu da!"
        return {"reply": r, "source": "omni_poem.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Poem error: {e}", "source": "omni_poem.py"}
def get_omni_weather(msg="weather"):'''
    assert old in t, "server weather function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_poem" not in t:
    old2 = '        if self.path.startswith("/api/omni_weather"):'
    new2 = '''        if self.path.startswith("/api/omni_poem"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "poem"
            self.send_json(get_omni_poem(msg))
        if self.path.startswith("/api/omni_weather"):'''
    assert old2 in t, "server weather route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI POEM" not in h:
    old3 = '<div class="card"><b>🌦️ OMNI WEATHER INFO'
    assert old3 in h, "dashboard weather card illa!"
    new3 = '''<div class="card"><b>📝 OMNI POETRY - Phase 21 Step 2!</b><br><br>
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
<div class="card"><b>🌦️ OMNI WEATHER INFO'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P21S2 DONE")
