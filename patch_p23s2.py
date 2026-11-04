import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_stats" not in t:
    old = 'def get_omni_poem(msg="poem"):'
    new = '''def get_omni_stats(msg="stats"):
    try:
        from omni_stats import handle_stats
        r = handle_stats(msg)
        if r is None:
            r = "Stats: 'stats' nu try pannu da!"
        return {"reply": r, "source": "omni_stats.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Stats error: {e}", "source": "omni_stats.py"}
def get_omni_poem(msg="poem"):'''
    assert old in t, "server poem function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_stats" not in t:
    old2 = '        if self.path.startswith("/api/omni_poem"):'
    new2 = '''        if self.path.startswith("/api/omni_stats"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "stats"
            self.send_json(get_omni_stats(msg))
        if self.path.startswith("/api/omni_poem"):'''
    assert old2 in t, "server poem route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI STATS" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>📊 OMNI STATS - Phase 23 Step 2!</b><br><br>
<div id="statsHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Stats Ready!</div><br>
<button onclick="sendStats()">Show Stats</button>
<script>
async function sendStats(){
  let hh=document.getElementById('statsHistory');
  let r=await fetch('/api/omni_stats?msg='+encodeURIComponent('stats'));
  let j=await r.json();
  hh.textContent='STATS: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P23S2 DONE")
