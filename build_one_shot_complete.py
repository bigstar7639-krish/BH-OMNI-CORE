# ONE-SHOT COMPLETE - BH-OMNI CORE - ALL PENDING IN ONE GO
# Cat 06 Books + Cat 08 OCR + Cat 09 Files + Cat 13 Network + Cat 18 Health Meds + Cat 19 Finance Budget
# NO fake - Ellaam interface + honest limits, NO API key venam
import pathlib
FILES = {}

FILES["omni_books.py"] = '''# OMNI BOOKS - Cat 06 - Gutenberg FREE API, NO key
import urllib.request, urllib.parse, json
def search_books(q):
    try:
        url = f"https://gutendex.com/books/?search={urllib.parse.quote(q)}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            d = json.loads(r.read().decode())
            if not d.get("results"):
                return f"📚 BOOKS: '{q}' - onnum kedaikala da!"
            out = f"📚 BOOKS - '{q}' (Gutenberg FREE):\\n"
            for b in d["results"][:3]:
                out += f"- {b['title']} - {', '.join([a['name'] for a in b['authors']])}\\n"
            return out
    except Exception as e:
        return f"📚 BOOKS OFFLINE - Internet illa ({e})\\nOffline: Gutenberg.org la paaru da!"
def handle_books(msg):
    m = msg.strip().lower()
    if m.startswith("book "):
        return search_books(msg.strip()[5:].strip())
    if m in ["books", "book list"]:
        return "📚 BOOKS: 'book tamil' / 'book python' nu try pannu da! Source: Gutenberg FREE"
    return None
'''

FILES["omni_ocr.py"] = '''# OMNI OCR - Cat 08 - Interface + pytesseract check - NO fake OCR
import shutil
def ocr_status():
    if shutil.which("tesseract"):
        return "📷 OCR READY - tesseract irukku!\\nUse: tesseract photo.jpg out - Pydroid3/Termux-la photo-a text aakkalam!"
    return "📷 OCR SETUP:\\n pkg install tesseract\\nAppuram photo-a text aakkalam da!\\nNote: Camera permission venum, photo file venum."
def handle_ocr(msg):
    m = msg.strip().lower()
    if m in ["ocr", "ocr status", "scan"]:
        return ocr_status()
    if m.startswith("ocr file "):
        return f"📷 OCR FILE: {msg.strip()[9:].strip()}\\nCommand: tesseract {msg.strip()[9:].strip()} out\\nAdha run panna text kedaikkum da!"
    return None
'''

FILES["omni_files.py"] = '''# OMNI FILES - Cat 09 - TXT/MD reader - Real file read
import pathlib
def read_file(path):
    try:
        p = pathlib.Path(path)
        if not p.exists():
            return f"📄 FILES: '{path}' - file illa da!"
        txt = p.read_text(errors="ignore")
        return f"📄 FILE: {path} ({len(txt)} chars):\\n{txt[:1000]}"
    except Exception as e:
        return f"📄 FILES ERROR: {e}"
def handle_files(msg):
    s = msg.strip()
    m = s.lower()
    if m.startswith("read "):
        return read_file(s[5:].strip())
    if m in ["files", "file list"]:
        return "📄 FILES: 'read README.md' / 'read VERSION.txt' nu try pannu da!"
    return None
'''

FILES["omni_network.py"] = '''# OMNI NETWORK - Cat 13 - Real Termux network check - NO unauthorized scan
import subprocess, socket
def network_status():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return f"📶 NETWORK STATUS:\\nLocal IP: {ip}\\nHost: {socket.gethostname()}\\nNote: Unauthorized device scan PANNAMATTOM - un network mattum paakkurom!"
    except Exception as e:
        return f"📶 NETWORK ERROR: {e}"
def handle_network(msg):
    m = msg.strip().lower()
    if m in ["network", "network status", "wifi"]:
        return network_status()
    return None
'''

FILES["omni_health.py"] = '''# OMNI HEALTH - Cat 18 - Medication reminder - Local only
import json, pathlib
F = pathlib.Path("omni_health.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"meds": []}
def _save(d): F.write_text(json.dumps(d, ensure_ascii=False, indent=2))
def handle_health(msg):
    s = msg.strip(); m = s.lower()
    if m.startswith("med add "):
        med = s[8:].strip()
        d = _load(); d["meds"].append(med); _save(d)
        return f"💊 MED ADDED: {med} - Nyabagam vechuten da! Doctor-a consult pannu!"
    if m in ["meds", "medicines"]:
        d = _load()
        if not d["meds"]: return "💊 MEDS: Onnum illa da! 'med add Paracetamol 9AM' nu add pannu!"
        return "💊 MEDS:\\n" + "\\n".join(f"{i+1}. {x}" for i, x in enumerate(d["meds"]))
    return None
'''

FILES["omni_budget.py"] = '''# OMNI BUDGET - Cat 19 - Budget planner - Expense-oda next level
import json, pathlib
F = pathlib.Path("omni_budget.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"budget": 0, "spent": 0}
def _save(d): F.write_text(json.dumps(d, ensure_ascii=False, indent=2))
def handle_budget(msg):
    s = msg.strip(); m = s.lower()
    if m.startswith("budget set "):
        try: amt = float(s[11:].strip()); d=_load(); d["budget"]=amt; _save(d); return f"💰 BUDGET SET: Rs.{amt}"
        except: return "💰 BUDGET: 'budget set 5000' nu number kodu da!"
    if m in ["budget", "budget status"]:
        d=_load(); left=d["budget"]-d["spent"]
        return f"💰 BUDGET:\\nBudget: Rs.{d['budget']}\\nSpent: Rs.{d['spent']}\\nLeft: Rs.{left}"
    return None
'''

for name, code in FILES.items():
    pathlib.Path(name).write_text(code)
    print(f"CREATED: {name}")
print("ONE-SHOT COMPLETE - 6 FILES DONE!")
