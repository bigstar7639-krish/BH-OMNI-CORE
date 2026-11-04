# OMNI EMERGENCY - Phase 17 Step 1 - SAME PROJECT
# Category 11 - STOP + SOS record only. NO fake SMS/call.
from omni_memory import _load, _save

def get_emergency():
    d = _load()
    return {"contacts": d.get("emergency_contacts", []), "stop": d.get("automation_stop", False), "events": d.get("sos_events", [])}

def handle_emergency(msg):
    m = msg.strip().lower()
    if m in ["stop", "emergency stop", "automation stop"]:
        d = _load()
        d["automation_stop"] = True
        _save(d)
        return "🛑 EMERGENCY STOP: AI automation stopped. Phone safety functions continue."
    if m in ["resume", "emergency resume", "automation resume"]:
        d = _load()
        d["automation_stop"] = False
        _save(d)
        return "▶️ Automation resumed."
    if m.startswith("sos add "):
        rest = msg.strip()[8:].strip()
        if not rest:
            return "SOS contact sollu da! Ex: sos add Amma 9876543210"
        d = _load()
        contacts = d.get("emergency_contacts", [])
        if len(contacts) >= 10:
            return "Max 10 contacts mattum da!"
        contacts.append(rest)
        d["emergency_contacts"] = contacts
        _save(d)
        return f"🆘 SOS Contact added: {rest} ({len(contacts)}/10)"
    if m in ["sos", "sos contacts", "emergency contacts"]:
        d = _load()
        contacts = d.get("emergency_contacts", [])
        stop = d.get("automation_stop", False)
        out = f"🆘 OMNI EMERGENCY - STOP: {'ON' if stop else 'OFF'}\nContacts: {len(contacts)}/10\n"
        for i, c in enumerate(contacts):
            out += f"{i+1}. {c}\n"
        out += "\nNote: Real SMS/call needs phone permission + network. Idhu local record mattum."
        return out
    if m == "sos trigger":
        d = _load()
        events = d.get("sos_events", [])
        events.append("SOS triggered - local record only")
        d["sos_events"] = events
        _save(d)
        return "🆘 SOS TRIGGERED - Local record saved. Real SMS NOT sent (needs phone permission). Call emergency number manually if needed."
    return None
