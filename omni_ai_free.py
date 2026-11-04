# OMNI AI FREE - Phase 29 Step 1 - SAME PROJECT
# FREE: Groq / Gemini - Key irundha LIVE, illa-na rule-based fallback
# Key edukka: Groq - console.groq.com, Gemini - aistudio.google.com - FREE!
import os, urllib.request, json
def ask_free_ai(question):
    # 1. Groq try pannu - Key env-la irundha
    groq = os.environ.get("GROQ_API_KEY", "").strip()
    if groq:
        try:
            body = json.dumps({"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": question}]}).encode()
            req = urllib.request.Request("https://api.groq.com/openai/v1/chat/completions", data=body, headers={"Authorization": f"Bearer {groq}", "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=10) as r:
                d = json.loads(r.read().decode())
                return f"🤖 FREE AI (Groq):\n{d['choices'][0]['message']['content']}\nSource: Groq FREE"
        except Exception as e:
            return f"🤖 Groq fail ({e}) - fallback-ku poaren...\n" + fallback_ai(question)
    # 2. Key illa-na rule-based fallback
    return fallback_ai(question)
def fallback_ai(q):
    ql = q.lower()
    if "vanakkam" in ql or "hello" in ql:
        return "🤖 OMNI (Rule-based): Vanakkam Krish! Key illa, aana naan irukken da! Free key edukka: console.groq.com"
    if "weather" in ql:
        return "🤖 OMNI: Weather-ku 'live weather Chennai' nu try pannu da!"
    if "code" in ql:
        return "🤖 OMNI: Code-ku 'code python' nu try pannu da!"
    return f"🤖 OMNI (Rule-based): '{q}' - purinjiduchu da! Free AI key irundha innum perusa pesuven. Key edukka: console.groq.com (FREE)"
def handle_ai_free(msg):
    m = msg.strip().lower()
    if m.startswith("ai "):
        q = msg.strip()[3:].strip()
        if q:
            return ask_free_ai(q)
        return "🤖 AI: 'ai Vanakkam' nu try pannu da!"
    return None
