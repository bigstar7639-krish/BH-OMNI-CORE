from pathlib import Path
p = Path("ui/dashboard.html")
t = p.read_text()
mem = """<div class="card"><b>🧠 OMNI MEMORY</b><br>
<div id="memHistory">OMNI MEMORY Ready!</div><br>
<input id="memInput" value="memory">
<button onclick="sendMem()">Save</button>
</div>
<script>
async function sendMem(){
  const msg=document.getElementById('memInput').value.trim();
  if(!msg) return;
  const h=document.getElementById('memHistory');
  h.textContent += '\\n\\nNEE: '+msg;
  try{ const r=await fetch('/api/omni_memory?msg='+encodeURIComponent(msg)); const j=await r.json();
    h.textContent += '\\nOMNI MEMORY: '+j.reply; h.scrollTop=h.scrollHeight;
  }catch(e){ h.textContent += '\\nError: '+e; } }
</script>
"""
if "OMNI MEMORY" not in t:
    t = t.replace('<div class="card"><b>📤 EXPORT', mem + '<div class="card"><b>📤 EXPORT')
    print("Dashboard V13 - MEMORY card added!")
else:
    print("Dashboard already has MEMORY card!")
p.write_text(t)
print("Dashboard done!")

s = Path("ui/server.py").read_text()
fn = '''
def get_omni_memory(msg="memory"):
    try:
        from omni_memory import handle_memory
        r = handle_memory(msg)
        if r is not None:
            return {"reply": r, "source": "omni_memory.py - SAME PROJECT"}
        from omni_infinity import omni_reply
        return {"reply": omni_reply(msg), "source": "omni_infinity.py"}
    except Exception as ex:
        return {"reply": f"Memory error: {ex}"}

'''
if "get_omni_memory" not in s:
    s = s.replace('def get_analytics', fn + 'def get_analytics')
    print("Server - get_omni_memory added!")
if "/api/omni_memory" not in s:
    s = s.replace('        if self.path.startswith("/api/omni"):', '        if self.path.startswith("/api/omni_memory"):\n            msg = parse_qs(urlparse(self.path).query).get("msg", ["memory"])[0]\n            self.send_json(get_omni_memory(msg))\n            return\n        if self.path.startswith("/api/omni"):')
    print("Server - /api/omni_memory route added!")
Path("ui/server.py").write_text(s)
print("PATCH P8 S3 DONE!")
