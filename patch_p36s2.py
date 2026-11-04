import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_mega" not in t:
    old = 'def get_omni_own_v4(msg="correct test | answer"):'
    new = '''def get_omni_mega(msg="mega"):
    try:
        from omni_mega_full import handle_mega
        r = handle_mega(msg)
        if r is None:
            r = "Mega: 'mega' / 'mega joke' / 'mega kadhai' / 'mega quiz' nu try pannu da!"
        return {"reply": r, "source": "omni_mega_full.py - FULL CONTENT"}
    except Exception as e:
        return {"reply": f"Mega error: {e}", "source": "omni_mega_full.py"}
def get_omni_own_v4(msg="correct test | answer"):'''
    assert old in t, "server own v4 function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_mega" not in t:
    old2 = '        if self.path.startswith("/api/omni_own_v4"):'
    new2 = '''        if self.path.startswith("/api/omni_mega"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "mega"
            self.send_json(get_omni_mega(msg))
        if self.path.startswith("/api/omni_own_v4"):'''
    assert old2 in t, "server own v4 route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI MEGA" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>🌟 OMNI MEGA FULL - Phase 36 Step 2! (Full Content)</b><br><br>
<div id="megaHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Mega Ready!</div><br>
<button onclick="sendMega('mega joke')">Mega Joke</button>
<button onclick="sendMega('mega kadhai')">Mega Kadhai</button>
<button onclick="sendMega('mega quiz')">Mega Quiz</button>
<button onclick="sendMega('mega motivation')">Mega Motivation</button>
<script>
async function sendMega(msg){
  let hh=document.getElementById('megaHistory');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_mega?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\nMEGA: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P36S2 DONE")
