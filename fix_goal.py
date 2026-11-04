import pathlib
p = pathlib.Path("omni_goal.py")
t = p.read_text()
old = '    if m.startswith("goal add "):'
new = '    if m == "goal add" or m.startswith("goal add "):'
assert old in t, "old line illa!"
t = t.replace(old, new)
p.write_text(t)
print("FIX DONE - goal add empty handled")
