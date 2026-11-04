"""V41 S3 - Chat + Own AI + Memory bridge. Stdlib only. No external AI."""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE, "own_ai_model.json")
MEMORY_PATH = os.path.join(BASE, "chat_v41_memory.json")
MAX_MSGS = 20

def _load_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
            return d if isinstance(d, dict) else default
    except Exception:
        return default

def _save_json_atomic(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

def _norm(s):
    return re.sub(r"[^a-z0-9\u0b80-\u0bff ]+", " ", str(s).lower())

def _tokens(s):
    return [w for w in _norm(s).split() if len(w) >= 3]

def load_lessons():
    """own_ai_model.json la lessons-a thedu. Format vera-a irundhalum handle pannum."""
    data = _load_json(MODEL_PATH, {})
    lessons = []
    # Common shapes: {"lessons": [...]}, {"lessons": {...}}, {"model": {...}}, flat dict
    cand = []
    if isinstance(data, dict):
        for k in ("lessons", "model", "brain", "data"):
            if k in data:
                cand.append(data[k])
        if not cand:
            cand = [data]
    for c in cand:
        if isinstance(c, dict):
            for k, v in c.items():
                if isinstance(v, dict):
                    q = v.get("question") or v.get("q") or k
                    a = v.get("answer") or v.get("a") or v.get("text") or ""
                    lessons.append({"q": str(q), "a": str(a)})
                elif isinstance(v, str):
                    lessons.append({"q": str(k), "a": v})
        elif isinstance(c, list):
            for it in c:
                if isinstance(it, dict):
                    q = it.get("question") or it.get("q") or it.get("prompt") or ""
                    a = it.get("answer") or it.get("a") or it.get("response") or ""
                    if q or a:
                        lessons.append({"q": str(q), "a": str(a)})
    return lessons

def find_lesson(user_text, lessons):
    """Keyword overlap. Fake answer illa - match illana None."""
    toks = set(_tokens(user_text))
    if not toks:
        return None
    best = None
    best_score = 0
    for L in lessons:
        ltoks = set(_tokens(L["q"]))
        if not ltoks:
            continue
        score = len(toks & ltoks)
        if score > best_score:
            best_score = score
            best = L
    if best and best_score >= 1:
        return best
    return None

def load_memory():
    d = _load_json(MEMORY_PATH, {})
    msgs = d.get("messages", []) if isinstance(d, dict) else []
    if not isinstance(msgs, list):
        msgs = []
    return msgs[-MAX_MSGS:]

def save_memory(msgs):
    _save_json_atomic(MEMORY_PATH, {"messages": msgs[-MAX_MSGS:]})

def chat_s3(user_text, lessons=None):
    """Returns (reply, source). source: 'own_ai' | 'fallback' | 'empty'"""
    text = (user_text or "").strip()
    if not text:
        return "Enna kekkanum nu sollu da. Ex: 'vanakkam' / 'teach: ...'", "empty"
    if lessons is None:
        lessons = load_lessons()
    hit = find_lesson(text, lessons)
    if hit:
        reply = hit["a"]
        source = "own_ai"
    else:
        # S2 ChatV41 irundha use pannu, illana fallback - fake answer illa
        try:
            from omni_chat_v41 import ChatV41
            c = ChatV41()
            reply = c.reply(text) if hasattr(c, "reply") else c.chat(text)
            source = "fallback"
        except Exception:
            reply = f"Idhu enaku theriyadhu. Teach pannu: teach: {text} => <answer>"
            source = "fallback"
    msgs = load_memory()
    msgs.append({"role": "user", "text": text})
    msgs.append({"role": "assistant", "text": reply, "source": source})
    save_memory(msgs)
    return reply, source

if __name__ == "__main__":
    print("V41 S3 Chat - type 'exit' to quit. 100% Own AI, no external API.")
    while True:
        try:
            t = input("Nee: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye!")
            break
        if t.lower() in ("exit", "quit", "bye"):
            print("Bye!")
            break
        r, src = chat_s3(t)
        print(f"OMNI [{src}]: {r}")
