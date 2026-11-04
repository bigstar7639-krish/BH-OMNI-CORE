# OMNI GOAL TRACKER - Phase 13 Step 1 - SAME PROJECT
# Category 10 - Productivity
from omni_memory import _load, _save

def get_goals():
    d = _load()
    return d.get("goals", [])

def handle_goal(msg):
    m = msg.strip().lower()
    if m == "goal add" or m.startswith("goal add "):
        name = msg.strip()[9:].strip()
        if not name:
            return "Goal sollu da! Ex: goal add Learn Python"
        d = _load()
        goals = d.get("goals", [])
        goals.append({"name": name, "done": False})
        d["goals"] = goals
        _save(d)
        return f"🎯 Goal added: {name}"
    if m.startswith("goal done "):
        try:
            n = int(m.split()[-1]) - 1
        except:
            return "goal done <number> nu sollu da!"
        d = _load()
        goals = d.get("goals", [])
        if 0 <= n < len(goals):
            goals[n]["done"] = True
            _save(d)
            return f"🏆 Super! Goal mudinjiduchu: {goals[n]['name']}"
        return "Adha number-la goal illa da!"
    if m in ["goals", "goal", "goal list"]:
        goals = get_goals()
        if not goals:
            return "Goal illa da! 'goal add Learn Python' nu add pannu!"
        done = sum(1 for g in goals if g.get("done"))
        out = f"🎯 OMNI GOALS: {done}/{len(goals)} mudinjuchu\n"
        for i, g in enumerate(goals):
            tick = "✅" if g.get("done") else "⬜"
            out += f"{i+1}. {tick} {g.get('name')}\n"
        return out
    return None
