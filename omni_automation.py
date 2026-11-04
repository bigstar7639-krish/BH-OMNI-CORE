# OMNI AUTOMATION - Cat 17 - Simple scheduled tasks - Local only
import json, pathlib
F = pathlib.Path("omni_automation.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"tasks": []}
def _save(d): F.write_text(json.dumps(d, ensure_ascii=False, indent=2))
def handle_automation(msg):
    s = msg.strip(); m = s.lower()
    if m.startswith("auto add "):
        task = s[9:].strip(); d=_load(); d["tasks"].append(task); _save(d)
        return f"🤖 AUTOMATION ADDED: {task} - Manual-a run pannanum, auto-run illa da! STOP-ku 'stop' nu sollu!"
    if m in ["auto", "automations", "auto list"]:
        d=_load()
        if not d["tasks"]: return "🤖 AUTOMATIONS: Onnum illa! 'auto add 6AM briefing' nu add pannu!"
        return "🤖 AUTOMATIONS:\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(d["tasks"]))
    return None
