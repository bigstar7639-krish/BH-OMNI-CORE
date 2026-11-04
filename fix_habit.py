import pathlib
p = pathlib.Path("omni_habit.py")
t = p.read_text()
old = '    if m.startswith("habit add "):'
new = '    if m == "habit add" or m.startswith("habit add "):'
assert old in t, "old line illa!"
t = t.replace(old, new)
p.write_text(t)
print("FIX DONE - habit add empty handled")
