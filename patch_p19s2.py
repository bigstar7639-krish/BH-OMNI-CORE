import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_code" not in t:
    old = 'def get_omni_lang(msg="languages"):'
    new = '''def get_omni_code(msg="code"):
    try:
        from omni_code import handle_code
        r = handle_code(msg)
        if r is None:
            r = "Code: 'code python' nu try pannu da!"
        return {"reply": r, "source": "omni_code.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Code error: {e}", "source": "omni_code.py"}
def get_omni_lang(msg="languages"):'''
    assert old in t, "server lang function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_code" not in t:
    old2 = '        if self.path.startswith("/api/omni_lang"):'
    new2 = '''        if self.path.startswith("/api/omni_code"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "code"
            self.send_json(get_omni_code(msg))
        if self.path.startswith("/api/omni_lang"):'''
    assert old2 in t, "server lang route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI CODE" not in h:
    old3 = '<div class="card"><b>🌐 OMNI LANGUAGE'
    assert old3 in h, "dashboard lang card illa!"
    new3 = '''<div class="card"><b>💻 OMNI CODE HELPER - Phase 19 Step 2!</b><br><br>
<div id="codeHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Code Helper Ready!</div><br>
<input id="codeInput" value="code python" style="width:65%" onkeydown="if(event.key==='Enter')sendCode()">
<button onclick="sendCode()">Send Code</button>
<script>
async function sendCode(){
  let msg=document.getElementById('codeInput').value;
  let h=document.getElementById('codeHistory');
  h.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_code?msg='+encodeURIComponent(msg));
  let j=await r.json();
  h.textContent+='\\nCODE: '+j.reply; h.scrollTop=h.scrollHeight;
}
</script></div>
<div class="card"><b>🌐 OMNI LANGUAGE'''
    h = h.replace(old3, new3)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P19S2 DONE")
