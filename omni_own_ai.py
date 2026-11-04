# OMNI OWN AI v1 - Phase 30 Step 1 - SAME PROJECT
# 100% OWN - NO API, NO Groq, NO Gemini, NO internet venam!
# Nee solli kodutha data-la irundhu mattum kathukkum
import json, pathlib, random
FILE = pathlib.Path("own_ai_model.json")
def _load():
    if FILE.exists():
        try: return json.loads(FILE.read_text())
        except: pass
    return {"words": {}, "replies": {}, "count": 0}
def _save(m):
    FILE.write_text(json.dumps(m, ensure_ascii=False, indent=2))
def teach(question, answer):
    """Nee-e solli kodu - idhu dhaan training!"""
    m = _load()
    q = question.strip().lower()
    m["replies"][q] = answer
    for w in q.split():
        m["words"][w] = m["words"].get(w, 0) + 1
    m["count"] += 1
    _save(m)
    return f"🧠 OWN AI LEARNED! ({m['count']} lessons)\nQ: {question}\nA: {answer}\nIdhu en memory-la save aayiduchu da!"
def ask_own(question):
    m = _load()
    q = question.strip().lower()
    # 1. Exact-a therindha - adha sollu
    if q in m["replies"]:
        return f"🧠 OWN AI (En Memory):\n{m['replies'][q]}"
    # 2. Oru word match aana - adha sollu
    for k, v in m["replies"].items():
        for w in q.split():
            if w in k and len(w) > 2:
                return f"🧠 OWN AI (Similar Memory):\n{v}\nNote: Exact-a theriyala, similar-a irundha solliten da!"
    # 3. Theriyalana - kathukudu-nu kelu - idhu dhaan own AI!
    return f"🧠 OWN AI: '{question}' - idhu enaku theriyala da!\nEnaku solli kodu: 'teach {question} | answer' nu type pannu - naan kathukiren!"
def handle_own_ai(msg):
    s = msg.strip()
    m = s.lower()
    if m.startswith("teach "):
        rest = s[6:].strip()
        if " | " in rest:
            q, a = rest.split(" | ", 1)
            return teach(q.strip(), a.strip())
        return "🧠 TEACH: 'teach vanakkam | Vanakkam Krish!' - ippadi | potu solli kodu da!"
    if m.startswith("own ai "):
        return ask_own(s[7:].strip())
    if m in ["own ai", "my ai"]:
        mod = _load()
        return f"🧠 OWN AI STATUS:\nLessons: {mod['count']}\nWords: {len(mod['words'])}\nReplies: {len(mod['replies'])}\n100% OWN - NO API!"
    return None
