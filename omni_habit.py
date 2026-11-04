# OMNI HABIT TRACKER - Phase 9 Step 1 - SAME PROJECT
# Category 10 - Productivity
from omni_memory import _load, _save

def get_habits():
    d = _load()
    return d.get("habits", [])

def handle_habit(msg):
    m = msg.strip().lower()
    if m == "habit add" or m.startswith("habit add "):
        name = msg.strip()[10:].strip()
        if not name:
            return "Habit peru sollu da! Ex: habit add Exercise"
        d = _load()
        habits = d.get("habits", [])
        habits.append({"name": name, "count": 0})
        d["habits"] = habits
        _save(d)
        return f"✅ Habit added: {name}"
    if m.startswith("habit done "):
        try:
            n = int(m.split()[-1]) - 1
        except:
            return "habit done <number> nu sollu da!"
        d = _load()
        habits = d.get("habits", [])
        if 0 <= n < len(habits):
            habits[n]["count"] += 1
            _save(d)
            return f"🎉 Super! {habits[n]['name']} - {habits[n]['count']} times mudinjuchu!"
        return "Adha number-la habit illa da!"
    if m in ["habits", "habit", "habit list"]:
        habits = get_habits()
        if not habits:
            return "Habit illa da! 'habit add Exercise' nu add pannu!"
        out = "🎯 OMNI HABITS:\n"
        for i, h in enumerate(habits):
            out += f"{i+1}. {h['name']} - {h['count']} times\n"
        return out
    return None
