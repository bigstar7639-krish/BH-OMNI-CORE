import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_mood" not in t:
    old = 'def get_omni_expense(msg="expenses"):'
    new = '''def get_omni_mood(msg="moods"):
    try:
        from omni_mood import handle_mood
        r = handle_mood(msg)
        if r is None:
            r = "Mood illa da! 'mood happy' nu save pannu!"
        return {"reply": r, "source": "omni_mood.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Mood error: {e}", "source": "omni_mood.py"}
def get_omni_expense(msg="expenses"):'''
    assert old in t, "server expense function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_mood" not in t:
    old2 = '        if self.path.startswith("/api/omni_expense"):'
    new2 = '''        if self.path.startswith("/api/omni_mood"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "moods"
            self.send_json(get_omni_mood(msg))
        if self.path.startswith("/api/omni_expense"):'''
    assert old2 in t, "server expense route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI MOOD" not in h:
    old3 = '<div class="card"><b>💰 OMNI EXPENSE TRACKER'
    assert old3 in h, "dashboard expense card illa!"
    new3 = '''<div class="card"><b>💛 OMNI MOOD JOURNAL - Phase 10 Step 2! (Estimate only)</b><br><br>
<div id="moodHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Mood Journal Ready!</div><br>
<input id="moodInput" value="moods" style="width:65%" onkeydown="if(event.key==='Enter')sendMood()">
<button onclick="sendMood()">Send Mood</button>
<script>
async function sendMood(){
  let msg=document.getElementById('moodInput').value;
  let h=document.getElementById('moodHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_mood?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nMOOD: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>💰 OMNI EXPENSE TRACKER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P10S2 DONE")
