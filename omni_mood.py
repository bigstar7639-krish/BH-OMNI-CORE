# OMNI MOOD JOURNAL - Phase 10 Step 1 - SAME PROJECT
# Category 5 - Emotion - Estimate only, NOT real feeling detection
from omni_memory import _load, _save

def get_moods():
    d = _load()
    return d.get("moods", [])

def handle_mood(msg):
    m = msg.strip().lower()
    if m.startswith("mood "):
        mood = msg.strip()[5:].strip()
        if not mood:
            return "Mood sollu da! Ex: mood happy"
        d = _load()
        moods = d.get("moods", [])
        moods.append({"mood": mood})
        d["moods"] = moods
        _save(d)
        return f"💛 Mood saved: {mood} - Naan un kooda irukken da!"
    if m in ["moods", "mood", "mood list"]:
        moods = get_moods()
        if not moods:
            return "Mood illa da! 'mood happy' nu save pannu!"
        out = "💛 OMNI MOOD JOURNAL (Estimate only):\n"
        for i, x in enumerate(moods[-10:]):
            out += f"{i+1}. {x.get('mood')}\n"
        return out
    return None
