# OMNI DAILY BRIEFING - Phase 16 Step 1 - SAME PROJECT
# Category 10 - Combines Daily + Habit + Expense + Goal + Mood + Water
from omni_memory import _load

def get_briefing():
    d = _load()
    name = d.get("name") or "Friend"
    todos = d.get("todos", [])
    done = sum(1 for t in todos if t.get("done"))
    habits = d.get("habits", [])
    expenses = d.get("expenses", [])
    total_exp = sum(e.get("amount", 0) for e in expenses)
    goals = d.get("goals", [])
    goal_done = sum(1 for g in goals if g.get("done"))
    moods = d.get("moods", [])
    water = d.get("water_count", 0)
    trips = d.get("trips", [])
    birthdays = d.get("birthdays", [])
    out = f"🌅 OMNI DAILY BRIEFING - Vanakkam {name}!\n\n"
    out += f"📋 Todos: {done}/{len(todos)} mudinjuchu\n"
    out += f"🎯 Habits: {len(habits)} habits\n"
    out += f"💰 Expense Total: Rs.{total_exp}\n"
    out += f"🏆 Goals: {goal_done}/{len(goals)} mudinjuchu\n"
    out += f"💛 Moods: {len(moods)} entries\n"
    out += f"💧 Water: {water} glass\n"
    out += f"✈️ Trips: {len(trips)} trips\n"
    out += f"🎂 Birthdays: {len(birthdays)} saved\n"
    return out

def handle_briefing(msg):
    m = msg.strip().lower()
    if m in ["briefing", "daily briefing", "brief", "summary", "today briefing"]:
        return get_briefing()
    return None
