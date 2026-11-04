# OMNI TRAVEL PLANNER - Phase 15 Step 1 - SAME PROJECT
# Category 21 - Travel - Planner only, NO real booking
from omni_memory import _load, _save

def get_trips():
    d = _load()
    return d.get("trips", [])

def handle_travel(msg):
    m = msg.strip().lower()
    if m.startswith("trip add "):
        rest = msg.strip()[9:].strip()
        if "|" not in rest:
            return "Format: trip add Place | Date"
        place, date = rest.split("|", 1)
        place, date = place.strip(), date.strip()
        if not place or not date:
            return "Place + Date rendum sollu da! Ex: trip add Chennai | 10-12"
        d = _load()
        trips = d.get("trips", [])
        trips.append({"place": place, "date": date})
        d["trips"] = trips
        _save(d)
        return f"✈️ Trip added: {place} - {date}"
    if m in ["trips", "trip", "trip list"]:
        trips = get_trips()
        if not trips:
            return "Trip illa da! 'trip add Chennai | 10-12' nu add pannu!"
        out = "✈️ OMNI TRIPS:\n"
        for i, x in enumerate(trips):
            out += f"{i+1}. {x.get('place')} - {x.get('date')}\n"
        return out
    return None
