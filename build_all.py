import pathlib
# Ellam files-um inga dhaan - oru file-la ellam
files = {}
files["omni_habit.py"] = open("omni_habit.py").read() if pathlib.Path("omni_habit.py").exists() else "# habit already - skip"
print("Build All - already irukkura files-a thodamatom, illadha files-a mattum create pannuvom")
# Check enna illa
for f in ["omni_habit.py","omni_expense.py","omni_mood.py","omni_flash.py","omni_water.py","omni_goal.py","omni_birthday.py","omni_travel.py","omni_briefing.py","omni_emergency.py"]:
    print(f, "IRUKKU" if pathlib.Path(f).exists() else "ILLA - create pannanum")
