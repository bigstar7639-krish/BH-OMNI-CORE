import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_birthday" not in t:
    old = 'def get_omni_goal(msg="goals"):'
    new = '''def get_omni_birthday(msg="birthdays"):
    try:
        from omni_birthday import handle_birthday
        r = handle_birthday(msg)
        if r is None:
            r = "Birthday illa da! 'birthday add Amma | 12-05' nu add pannu!"
        return {"reply": r, "source": "omni_birthday.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Birthday error: {e}", "source": "omni_birthday.py"}
def get_omni_goal(msg="goals"):'''
    assert old in t, "server goal function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_birthday" not in t:
    old2 = '        if self.path.startswith("/api/omni_goal"):'
    new2 = '''        if self.path.startswith("/api/omni_birthday"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "birthdays"
            self.send_json(get_omni_birthday(msg))
        if self.path.startswith("/api/omni_goal"):'''
    assert old2 in t, "server goal route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI BIRTHDAY" not in h:
    old3 = '<div class="card"><b>🎯 OMNI GOAL TRACKER'
    assert old3 in h, "dashboard goal card illa!"
    new3 = '''<div class="card"><b>🎂 OMNI BIRTHDAY REMINDER - Phase 14 Step 2!</b><br><br>
<div id="bdayHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Birthday Reminder Ready!</div><br>
<input id="bdayInput" value="birthdays" style="width:65%" onkeydown="if(event.key==='Enter')sendBday()">
<button onclick="sendBday()">Send Birthday</button>
<script>
async function sendBday(){
  let msg=document.getElementById('bdayInput').value;
  let h=document.getElementById('bdayHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_birthday?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nBIRTHDAY: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🎯 OMNI GOAL TRACKER'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P14S2 DONE")
