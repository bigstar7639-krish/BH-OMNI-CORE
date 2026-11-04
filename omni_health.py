# OMNI HEALTH - Cat 18 - Medication reminder - Local only
import json, pathlib
F = pathlib.Path("omni_health.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"meds": []}
def _save(d): F.write_text(json.dumps(d, ensure_ascii=False, indent=2))
def handle_health(msg):
    s = msg.strip(); m = s.lower()
    if m.startswith("med add "):
        med = s[8:].strip()
        d = _load(); d["meds"].append(med); _save(d)
        return f"💊 MED ADDED: {med} - Nyabagam vechuten da! Doctor-a consult pannu!"
    if m in ["meds", "medicines"]:
        d = _load()
        if not d["meds"]: return "💊 MEDS: Onnum illa da! 'med add Paracetamol 9AM' nu add pannu!"
        return "💊 MEDS:\n" + "\n".join(f"{i+1}. {x}" for i, x in enumerate(d["meds"]))
    return None
