# OMNI FLASHCARDS - Phase 11 Step 1 - SAME PROJECT
# Category 7 - Education
from omni_memory import _load, _save

def get_flash():
    d = _load()
    return d.get("flashcards", [])

def handle_flash(msg):
    m = msg.strip().lower()
    if m.startswith("flash add "):
        rest = msg.strip()[10:].strip()
        if "|" not in rest:
            return "Flash format: flash add question | answer"
        q, a = rest.split("|", 1)
        q, a = q.strip(), a.strip()
        if not q or not a:
            return "Question + Answer rendum sollu da! Ex: flash add Tamil Nadu capital? | Chennai"
        d = _load()
        f = d.get("flashcards", [])
        f.append({"q": q, "a": a})
        d["flashcards"] = f
        _save(d)
        return f"✅ Flashcard added: {q}"
    if m in ["flash", "flashcards", "flash list"]:
        f = get_flash()
        if not f:
            return "Flashcard illa da! 'flash add Q | A' nu add pannu!"
        out = "📚 OMNI FLASHCARDS:\n"
        for i, x in enumerate(f[-10:]):
            out += f"{i+1}. Q: {x.get('q')} | A: {x.get('a')}\n"
        return out
    if m.startswith("flash quiz"):
        f = get_flash()
        if not f:
            return "Flashcard illa da! First add pannu!"
        import random
        x = random.choice(f)
        return f"❓ FLASH QUIZ:\nQ: {x.get('q')}\n(Badhil theriyuma? 'flash' nu paaru!)"
    return None
