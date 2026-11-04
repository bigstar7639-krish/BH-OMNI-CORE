import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_flash" not in t:
    old = 'def get_omni_mood(msg="moods"):'
    new = '''def get_omni_flash(msg="flashcards"):
    try:
        from omni_flash import handle_flash
        r = handle_flash(msg)
        if r is None:
            r = "Flashcard illa da! 'flash add Q | A' nu add pannu!"
        return {"reply": r, "source": "omni_flash.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Flash error: {e}", "source": "omni_flash.py"}
def get_omni_mood(msg="moods"):'''
    assert old in t, "server mood function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_flash" not in t:
    old2 = '        if self.path.startswith("/api/omni_mood"):'
    new2 = '''        if self.path.startswith("/api/omni_flash"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "flashcards"
            self.send_json(get_omni_flash(msg))
        if self.path.startswith("/api/omni_mood"):'''
    assert old2 in t, "server mood route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI FLASH" not in h:
    old3 = '<div class="card"><b>💛 OMNI MOOD JOURNAL'
    assert old3 in h, "dashboard mood card illa!"
    new3 = '''<div class="card"><b>📚 OMNI FLASHCARDS - Phase 11 Step 2!</b><br><br>
<div id="flashHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Flashcards Ready!</div><br>
<input id="flashInput" value="flashcards" style="width:65%" onkeydown="if(event.key==='Enter')sendFlash()">
<button onclick="sendFlash()">Send Flash</button>
<script>
async function sendFlash(){
  let msg=document.getElementById('flashInput').value;
  let h=document.getElementById('flashHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_flash?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nFLASH: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>💛 OMNI MOOD JOURNAL'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P11S2 DONE")
