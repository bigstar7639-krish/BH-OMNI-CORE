from pathlib import Path
p = Path("ui/dashboard.html")
t = p.read_text()
daily = """<div class="card"><b>🌅 OMNI DAILY PLANNER - Phase 8 Step 4!</b><br><br>
<div id="dailyHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Daily Planner Ready! 'daily' nu click pannu!</div><br>
<button onclick="showDaily()">Show Daily Planner</button>
</div>
<script>
async function showDaily(){
  const h=document.getElementById('dailyHistory');
  h.textContent += '\\n\\n... Daily Planner loading ...';
  try{ const r=await fetch('/api/omni_daily?msg='+encodeURIComponent('daily')); const j=await r.json();
    h.textContent += '\\n\\n'+j.reply; h.scrollTop=h.scrollHeight;
  }catch(e){ h.textContent += '\\nError: '+e; } }
</script>
"""
if "OMNI DAILY" not in t:
    t = t.replace('<div class="card"><b>📤 EXPORT', daily + '<div class="card"><b>📤 EXPORT')
    print("Dashboard V14 - DAILY card added!")
else:
    print("Dashboard already has DAILY card!")
p.write_text(t)
print("Dashboard done!")
s = Path("ui/server.py").read_text()
fn = '''
def get_omni_daily(msg="daily"):
    try:
        from omni_daily import handle_daily
        r = handle_daily(msg)
        if r is not None:
            return {"reply": r, "source": "omni_daily.py - SAME PROJECT"}
        return {"reply": "Daily Planner Ready! 'daily' nu type pannu!"}
    except Exception as ex:
        return {"reply": f"Daily error: {ex}"}

'''
if "get_omni_daily" not in s:
    s = s.replace('def get_analytics', fn + 'def get_analytics')
    print("Server - get_omni_daily added!")
if "/api/omni_daily" not in s:
    s = s.replace('        if self.path.startswith("/api/omni"):', '        if self.path.startswith("/api/omni_daily"):\n            msg = parse_qs(urlparse(self.path).query).get("msg", ["daily"])[0]\n            self.send_json(get_omni_daily(msg))\n            return\n        if self.path.startswith("/api/omni"):')
    print("Server - /api/omni_daily route added!")
Path("ui/server.py").write_text(s)
print("PATCH P8 S4 DONE!")
