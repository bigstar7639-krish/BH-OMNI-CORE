from omni_habit import handle_habit, get_habits
passed = 0
total = 8
def check(n, name, cond, info=""):
    global passed
    if cond:
        passed += 1
        print(f"TEST {n} {name}: PASS - {info}")
    else:
        print(f"TEST {n} {name}: FAIL - {info}")

# Nee already test pannadhu - idhu kandippa PASS aaganum
r1 = handle_habit("habit add ReadingTest")
check(1, "habit_add", r1 is not None and "Habit added" in str(r1), str(r1)[:50])
r2 = handle_habit("habits")
check(2, "habit_list", r2 is not None and "HABITS" in str(r2), "list vandhuchu")
r3 = handle_habit("habit done 1")
check(3, "habit_done", r3 is not None and "times" in str(r3), str(r3)[:50])
r4 = handle_habit("habit")
check(4, "habit_keyword", r4 is not None, "habit keyword works")
r5 = handle_habit("habit list")
check(5, "habit_list_keyword", r5 is not None, "habit list works")
r6 = handle_habit("hello")
check(6, "habit_unknown_none", r6 is None, "unknown-ku None dhaan correct")
r7 = handle_habit("habit add ")
check(7, "habit_empty", r7 is not None and "peru" in str(r7).lower(), str(r7)[:50])
h = get_habits()
check(8, "habit_get", isinstance(h, list) and len(h) >= 1, f"{len(h)} habits")
print(f"=== PHASE 9 STEP 1 ===")
print(f"Total: {passed} PASS, {total-passed} FAIL")
