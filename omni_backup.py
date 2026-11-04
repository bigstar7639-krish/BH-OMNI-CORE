# OMNI BACKUP - Phase 24 Step 1 - SAME PROJECT
# NO auto push - status mattum kaatum, push-a nee dhaan pannanum
import subprocess
def get_backup_status():
    try:
        out = subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
        log = subprocess.check_output(["git", "log", "--oneline", "-3"], text=True).strip()
        if not out:
            return f"✅ BACKUP OK - Working tree clean!\nLast 3 commits:\n{log}"
        return f"⚠️ BACKUP PENDING - {len(out.splitlines())} file(s) push panna irukku:\n{out}\nLast 3:\n{log}"
    except Exception as e:
        return f"Backup check error: {e}"
def handle_backup(msg):
    m = msg.strip().lower()
    if m in ["backup", "backup status", "backup check"]:
        return get_backup_status()
    return None
