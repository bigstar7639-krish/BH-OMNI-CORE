import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_lang" not in t:
    old = 'def get_omni_emergency(msg="sos"):'
    if old not in t:
        old = 'def get_omni_briefing(msg="briefing"):'
    new = '''def get_omni_lang(msg="languages"):
    try:
        from omni_lang import handle_lang
        r = handle_lang(msg)
        if r is None:
            r = "Language: 'translate vanakkam' / 'detect Hello' nu try pannu da!"
        return {"reply": r, "source": "omni_lang.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Lang error: {e}", "source": "omni_lang.py"}
'''
    # old function-ku munnadi podu
    assert old in t, "server anchor illa!"
    t = t.replace(old, new + old)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_lang" not in t:
    old2 = '        if self.path.startswith("/api/omni_emergency"):'
    if old2 not in t:
        old2 = '        if self.path.startswith("/api/omni_briefing"):'
    new2 = '''        if self.path.startswith("/api/omni_lang"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "languages"
            self.send_json(get_omni_lang(msg))
'''
    assert old2 in t, "server route anchor illa!"
    t = t.replace(old2, new2 + old2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI LANGUAGE" not in h:
    old3 = '<div class="card"><b>🆘 OMNI EMERGENCY'
    if old3 not in h:
        old3 = '<div class="card"><b>🌅 OMNI BRIEFING'
    assert old3 in h, "dashboard anchor illa!"
    new3 = '''<div class="card"><b>🌐 OMNI LANGUAGE - Phase 18 Step 2!</b><br><br>
<div id="langHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Language Ready!</div><br>
<input id="langInput" value="translate vanakkam" style="width:65%" onkeydown="if(event.key==='Enter')sendLang()">
<button onclick="sendLang()">Send Lang</button>
<script>
async function sendLang(){
  let msg=document.getElementById('langInput').value;
  let h=document.getElementById('langHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_lang?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nLANG: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
'''
    h = h.replace(old3, new3 + old3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P18S2 DONE")
