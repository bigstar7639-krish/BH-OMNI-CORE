# OMNI WATER REMINDER - Phase 12 Step 1 - SAME PROJECT
# Category 18 - Health - Reminder only, NOT medical advice
from omni_memory import _load, _save

def get_water():
    d = _load()
    return d.get("water_count", 0)

def handle_water(msg):
    m = msg.strip().lower()
    if m in ["water", "water drink", "water done", "water add"]:
        d = _load()
        c = d.get("water_count", 0) + 1
        d["water_count"] = c
        _save(d)
        return f"💧 Water done! Innaiku {c} glass kudichita! Super da!"
    if m in ["water count", "water total", "water status"]:
        c = get_water()
        return f"💧 Innaiku Water: {c} glass"
    if m == "water reset":
        d = _load()
        d["water_count"] = 0
        _save(d)
        return "💧 Water count reset panniten! Pudhu naal, pudhu start!"
    return None
