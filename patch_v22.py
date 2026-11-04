import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
if "V12" in t:
    t = t.replace("V12", "V22")
    s.write_text(t)
    print("Server V12 -> V22 DONE")
else:
    print("V12 illa, already V22")
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "V22" not in h:
    # 270 PASS card-ku pakkathula V22 badge podu
    h = h.replace("270 PASS, 0 FAIL", "270 PASS, 0 FAIL - V22", 1)
    d.write_text(h)
    print("Dashboard V22 badge DONE")
else:
    print("Dashboard already V22")
print("PATCH V22 DONE")
