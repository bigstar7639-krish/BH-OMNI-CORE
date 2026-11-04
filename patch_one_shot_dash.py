import pathlib
s = pathlib.Path("ui/server.py")
t = s.read_text()
mods = [
    ("books", "omni_books", "handle_books", "Books: 'book tamil'"),
    ("ocr", "omni_ocr", "handle_ocr", "OCR: 'ocr'"),
    ("files", "omni_files", "handle_files", "Files: 'read VERSION.txt'"),
    ("network", "omni_network", "handle_network", "Network: 'network'"),
    ("health", "omni_health", "handle_health", "Health: 'meds'"),
    ("budget", "omni_budget", "handle_budget", "Budget: 'budget'"),
]
for key, mod, func, hint in mods:
    fname = f"get_omni_{key}"
    if fname not in t:
        # Brain function-ku munnadi podu - adhu kandippa irukku
        old = 'def get_omni_brain(msg="brain"):'
        new = f'''def {fname}(msg="{hint}"):
    try:
        from {mod} import {func}
        r = {func}(msg)
        if r is None:
            r = "{hint} nu try pannu da!"
        return {{"reply": r, "source": "{mod}.py - ONE-SHOT"}}
    except Exception as e:
        return {{"reply": f"{key} error: {{e}}", "source": "{mod}.py"}}
def get_omni_brain(msg="brain"):'''
        assert old in t, "brain function illa!"
        t = t.replace(old, new)
        print(f"Server {key} added")
    route = f"/api/omni_{key}"
    if route not in t:
        old2 = '        if self.path.startswith("/api/omni_brain"):'
        new2 = f'''        if self.path.startswith("{route}"):
            msg = self.path.split("msg=")[-1] if "msg=" in self.path else "{hint}"
            self.send_json({fname}(msg))
        if self.path.startswith("/api/omni_brain"):'''
        assert old2 in t, "brain route illa!"
        t = t.replace(old2, new2)
        print(f"Route {key} added")
s.write_text(t)
d = pathlib.Path("ui/dashboard.html")
h = d.read_text()
cards = {
    "books": ("📚 OMNI BOOKS - One-Shot! (Gutenberg FREE)", "book tamil", "Books"),
    "ocr": ("📷 OMNI OCR - One-Shot! (tesseract)", "ocr", "OCR"),
    "files": ("📄 OMNI FILES - One-Shot! (TXT Reader)", "read VERSION.txt", "Files"),
    "network": ("📶 OMNI NETWORK - One-Shot!", "network", "Network"),
    "health": ("💊 OMNI HEALTH - One-Shot! (Meds)", "meds", "Health"),
    "budget": ("💰 OMNI BUDGET - One-Shot!", "budget", "Budget"),
}
for key, (title, default, label) in cards.items():
    if title.split(" - ")[0] not in h and f"OMNI {label.upper()}" not in h:
        anchor = '<div class="omni-orb-wrap">'
        card = f'''<div class="card"><b>{title}</b><br><br>
<div id="{key}History" style="background:#020617;border-radius:10px;padding:12px;min-height:60px;max-height:180px;overflow-y:auto;font-family:monospace;font-size:13px;white-space:pre-wrap">{label} Ready!</div><br>
<input id="{key}Input" value="{default}" style="width:65%" onkeydown="if(event.key==='Enter')send{key.capitalize()}()">
<button onclick="send{key.capitalize()}()">Send {label}</button>
<script>
async function send{key.capitalize()}{{
  let msg=document.getElementById('{key}Input').value;
  let hh=document.getElementById('{key}History');
  hh.textContent+='\\n\\nNEE: '+msg;
  let r=await fetch('/api/omni_{key}?msg='+encodeURIComponent(msg));
  let j=await r.json();
  hh.textContent+='\\n{label.upper()}: '+j.reply; hh.scrollTop=hh.scrollHeight;
}}
</script></div>
'''
        h = h.replace(anchor, card + anchor)
        print(f"Card {key} added")
d.write_text(h)
print("PATCH ONE-SHOT DASH DONE")
