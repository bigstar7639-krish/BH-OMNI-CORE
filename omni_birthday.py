# OMNI BIRTHDAY REMINDER - Phase 14 Step 1 - SAME PROJECT
# Category 10 - Productivity
from omni_memory import _load, _save

def get_birthdays():
    d = _load()
    return d.get("birthdays", [])

def handle_birthday(msg):
    m = msg.strip().lower()
    if m.startswith("birthday add "):
        rest = msg.strip()[13:].strip()
        if "|" not in rest:
            return "Format: birthday add Name | DD-MM"
        name, date = rest.split("|", 1)
        name, date = name.strip(), date.strip()
        if not name or not date:
            return "Name + Date rendum sollu da! Ex: birthday add Amma | 12-05"
        d = _load()
        b = d.get("birthdays", [])
        b.append({"name": name, "date": date})
        d["birthdays"] = b
        _save(d)
        return f"🎂 Birthday added: {name} - {date}"
    if m in ["birthdays", "birthday", "birthday list"]:
        b = get_birthdays()
        if not b:
            return "Birthday illa da! 'birthday add Amma | 12-05' nu add pannu!"
        out = "🎂 OMNI BIRTHDAYS:\n"
        for i, x in enumerate(b):
            out += f"{i+1}. {x.get('name')} - {x.get('date')}\n"
        return out
    return None
