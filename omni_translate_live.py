# OMNI TRANSLATE LIVE - Phase 27 Step 1 - SAME PROJECT
# FREE API: MyMemory - NO key, NO kasu
# Format: translate live en|ta vanakkam = English to Tamil
import urllib.request, urllib.parse, json
def live_translate(text, src="en", tgt="ta"):
    try:
        q = urllib.parse.quote(text)
        url = f"https://api.mymemory.translated.net/get?q={q}&langpair={src}|{tgt}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            out = data["responseData"]["translatedText"]
            return f"🌐 LIVE TRANSLATE {src} -> {tgt}:\n{text} = {out}\nSource: MyMemory FREE, NO key"
    except Exception as e:
        return f"🌐 TRANSLATE OFFLINE - Internet illa / MyMemory fail ({e})\nOffline: 'translate vanakkam' nu try pannu da!"
def handle_translate_live(msg):
    m = msg.strip().lower()
    if m.startswith("translate live "):
        rest = msg.strip()[15:].strip()
        # Format: en|ta vanakkam  OR  vanakkam
        if "|" in rest and " " in rest:
            pair, text = rest.split(" ", 1)
            src, tgt = pair.split("|")
            return live_translate(text.strip(), src.strip(), tgt.strip())
        return live_translate(rest, "en", "ta")
    return None
