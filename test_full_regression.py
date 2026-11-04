passed=0; total=0
def check(name, cond, info=""):
    global passed, total
    total+=1
    if cond: passed+=1; print(f"PASS - {name} - {info}")
    else: print(f"FAIL - {name} - {info}")
tests = [
    ("P8 Memory", "omni_memory", "handle_memory", "memory"),
    ("P8 Daily", "omni_daily", "handle_daily", "today"),
    ("P9 Habit", "omni_habit", "handle_habit", "habits"),
    ("P9 Expense", "omni_expense", "handle_expense", "expenses"),
    ("P10 Mood", "omni_mood", "handle_mood", "moods"),
    ("P11 Flash", "omni_flash", "handle_flash", "flashcards"),
    ("P12 Water", "omni_water", "handle_water", "water count"),
    ("P13 Goal", "omni_goal", "handle_goal", "goals"),
    ("P14 Birthday", "omni_birthday", "handle_birthday", "birthdays"),
    ("P15 Travel", "omni_travel", "handle_travel", "trips"),
    ("P16 Briefing", "omni_briefing", "handle_briefing", "briefing"),
    ("P17 Emergency", "omni_emergency", "handle_emergency", "sos"),
]
import importlib
for name, mod, fn, arg in tests:
    try:
        m = importlib.import_module(mod)
        r = getattr(m, fn)(arg)
        check(name, r is not None, f"{mod} works")
    except Exception as e:
        check(name, False, str(e)[:80])
print(f"=== FULL REGRESSION ===")
print(f"Total: {passed} PASS, {total-passed} FAIL, Total {total}")
