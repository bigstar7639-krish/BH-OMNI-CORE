# OMNI OWN AI v2 - Phase 31 Step 1 - SAME PROJECT
# 100% OWN - NO API - Brain management: list / forget / stats
import json, pathlib
FILE = pathlib.Path("own_ai_model.json")
def _load():
    if FILE.exists():
        try: return json.loads(FILE.read_text())
        except: pass
    return {"words": {}, "replies": {}, "count": 0}
def _save(m):
    FILE.write_text(json.dumps(m, ensure_ascii=False, indent=2))
def list_lessons():
    m = _load()
    if not m["replies"]:
        return "🧠 OWN AI: Innum lessons illa da! 'teach Q | A' nu solli kodu!"
    out = f"🧠 OWN AI LESSONS ({m['count']}):\n"
    for i, (q, a) in enumerate(m["replies"].items(), 1):
        out += f"{i}. Q: {q} -> A: {a[:50]}\n"
    return out
def forget_lesson(question):
    m = _load()
    q = question.strip().lower()
    if q in m["replies"]:
        del m["replies"][q]
        m["count"] = len(m["replies"])
        _save(m)
        return f"🧠 OWN AI FORGOT: '{question}' - marandhuten da!"
    return f"🧠 OWN AI: '{question}' - en kitta illa da, marakka onnum illa!"
def handle_own_v2(msg):
    s = msg.strip()
    ml = s.lower()
    if ml == "my lessons":
        return list_lessons()
    if ml.startswith("forget "):
        return forget_lesson(s[7:].strip())
    if ml in ["my brain", "brain stats"]:
        m = _load()
        return f"🧠 OWN AI BRAIN:\nLessons: {m['count']}\nWords: {len(m['words'])}\nFile: own_ai_model.json - 100% OWN!"
    return None
