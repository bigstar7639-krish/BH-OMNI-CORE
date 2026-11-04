import pathlib
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
if "omni-orb" in h:
    print("Orb already irukku")
else:
    # CSS - <style> illa-na <head>-la podu, irundha adhukulla podu
    css = """
<style>
.omni-orb-wrap{text-align:center;padding:10px 0 4px}
.omni-orb{width:110px;height:110px;margin:0 auto;border-radius:50%;
background:radial-gradient(circle at 35% 35%, #a78bfa, #06b6d4 45%, #0b1026 75%);
box-shadow:0 0 30px #06b6d4, 0 0 60px #a78bfa inset;
animation:orb-spin 12s linear infinite;position:relative}
.omni-orb::after{content:"";position:absolute;inset:10px;border-radius:50%;
border:2px dashed rgba(255,255,255,.6);animation:orb-spin-rev 8s linear infinite}
@keyframes orb-spin{to{transform:rotate(360deg)}}
@keyframes orb-spin-rev{to{transform:rotate(-360deg)}}
@media (prefers-reduced-motion: reduce){.omni-orb,.omni-orb::after{animation:none}}
.omni-orb-label{font-size:12px;opacity:.8;margin-top:6px}
</style>
"""
    if "<style>" in h:
        h = h.replace("<style>", css + "<style>", 1)
    elif "</head>" in h:
        h = h.replace("</head>", css + "</head>", 1)
    else:
        h = css + h
    # Orb HTML - H1-ku munnadi podu
    orb = '''<div class="omni-orb-wrap"><div class="omni-orb"></div><div class="omni-orb-label">BH-OMNI CORE - Aurora Orb - CSS Animation Only</div></div>
'''
    if "<h1>" in h:
        h = h.replace("<h1>", orb + "<h1>", 1)
    else:
        h = orb + h
    d.write_text(h)
    print("ORB ADDED")
print("PATCH ORB DONE")
