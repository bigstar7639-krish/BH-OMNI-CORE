# OMNI OWN AI v3 - Phase 32 Step 1 - SAME PROJECT
# 100% OWN - Brain Export / Import - NO API
import json, pathlib, shutil
FILE = pathlib.Path("own_ai_model.json")
BACKUP = pathlib.Path("own_ai_backup.json")
def export_brain():
    if not FILE.exists():
        return "🧠 OWN AI: Export panna brain-e illa da! Teach pannu first!"
    shutil.copy(FILE, BACKUP)
    data = json.loads(FILE.read_text())
    return f"🧠 OWN AI EXPORT DONE!\nFile: own_ai_backup.json\nLessons: {data.get('count', 0)}\nIdha vera phone-ku anuppi restore pannalam da!"
def import_brain():
    if not BACKUP.exists():
        return "🧠 OWN AI: Backup file illa da! Export first pannu!"
    shutil.copy(BACKUP, FILE)
    data = json.loads(FILE.read_text())
    return f"🧠 OWN AI IMPORT DONE!\nLessons restored: {data.get('count', 0)}\nUn brain thirumba vandhuduchu da!"
def handle_own_v3(msg):
    m = msg.strip().lower()
    if m in ["export brain", "backup brain", "my brain export"]:
        return export_brain()
    if m in ["import brain", "restore brain", "my brain import"]:
        return import_brain()
    return None
