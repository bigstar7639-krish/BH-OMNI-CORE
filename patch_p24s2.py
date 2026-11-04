import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "get_omni_backup" not in t:
    old = 'def get_omni_stats(msg="stats"):'
    new = '''def get_omni_backup(msg="backup"):
    try:
        from omni_backup import handle_backup
        r = handle_backup(msg)
        if r is None:
            r = "Backup: 'backup' nu try pannu da!"
        return {"reply": r, "source": "omni_backup.py - SAME PROJECT"}
    except Exception as e:
        return {"reply": f"Backup error: {e}", "source": "omni_backup.py"}
def get_omni_stats(msg="stats"):'''
    assert old in t, "server stats function illa!"
    t = t.replace(old, new)
    print("Server function added")
else:
    print("Server function already irukku")
if "/api/omni_backup" not in t:
    old2 = '        if self.path.startswith("/api/omni_stats"):'
    new2 = '''        if self.path.startswith("/api/omni_backup"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "backup"
            self.send_json(get_omni_backup(msg))
        if self.path.startswith("/api/omni_stats"):'''
    assert old2 in t, "server stats route illa!"
    t = t.replace(old2, new2)
    print("Server route added")
else:
    print("Server route already irukku")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "OMNI BACKUP" not in h:
    anchor = '<div class="omni-orb-wrap">'
    assert anchor in h, "orb wrap illa!"
    card = '''<div class="card"><b>💾 OMNI BACKUP - Phase 24 Step 2!</b><br><br>
<div id="backupHistory" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">Backup Ready!</div><br>
<button onclick="sendBackup()">Check Backup</button>
<script>
async function sendBackup(){
  let hh=document.getElementById('backupHistory');
  let r=await fetch('/api/omni_backup?msg='+encodeURIComponent('backup'));
  let j=await r.json();
  hh.textContent='BACKUP: '+j.reply; hh.scrollTop=hh.scrollHeight;
}
</script></div>
'''
    h = h.replace(anchor, card + anchor)
    d.write_text(h)
    print("Dashboard card added")
else:
    print("Dashboard card already irukku")
print("PATCH P24S2 DONE")
