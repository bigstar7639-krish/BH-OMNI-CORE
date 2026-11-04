# OMNI DAILY PLANNER - Phase 8 Step 4 - SAME PROJECT
from omni_memory import _load
from omni_infinity import MOTIVATIONS
import random

def get_daily():
    d = _load()
    name = d.get("name") or "Friend"
    todos = d.get("todos", [])
    notes = d.get("notes", [])
    done = sum(1 for t in todos if t.get("done"))
    pending = len(todos) - done
    mot = random.choice(MOTIVATIONS)
    out = f"🌅 OMNI DAILY PLANNER - Vanakkam {name}!\n\n"
    out += f"💡 INNAIKU MOTIVATION:\n{mot}\n\n"
    out += f"📋 INNAIKU TODOS: {done}/{len(todos)} mudinjuchu, {pending} pending!\n"
    if todos:
        for i, t in enumerate(todos):
            tick = "✅" if t.get("done") else "⬜"
            out += f"{i+1}. {tick} {t.get('task')}\n"
    else:
        out += "Todo illa da! 'todo <ethuvum>' nu add pannu!\n"
    out += f"\n📝 NOTES: {len(notes)}\n"
    if notes:
        for i, n in enumerate(notes[-3:]):
            out += f"- {n}\n"
    out += f"\n🌙 NIGHT SUMMARY:\n"
    if len(todos) == 0:
        out += "Innaiku todo illa - Naalaiku plan pannu da!\n"
    elif done == len(todos):
        out += f"Super da {name}! Ellam mudinjuchu! 🎉\n"
    else:
        out += f"{done} mudinjuchu, {pending} pending - Naalaiku mudichidalam!\n"
    out += f"\nChat Count: {d.get('chat_count', 0)} | Quiz Best: {d.get('quiz_best', 0)}/20"
    return out

def handle_daily(msg):
    if msg.strip().lower() in ["daily", "innaiku", "today", "planner"]:
        return get_daily()
    return None
