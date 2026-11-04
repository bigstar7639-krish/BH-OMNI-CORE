# OMNI LANGUAGE - Phase 18 Step 1 - SAME PROJECT
# Category 3 - Detection + small dictionary only. NOT full 100+ translation.
WORDS = {
    "vanakkam": "Hello",
    "hello": "Vanakkam",
    "nandri": "Thank you",
    "thank you": "Nandri",
    "sapadu": "Food / Meals",
    "food": "Sapadu",
    "thanni": "Water",
    "water": "Thanni",
    "veedu": "Home",
    "home": "Veedu",
}

def detect_lang(msg):
    tamil_chars = sum(1 for c in msg if '\u0b80' <= c <= '\u0bff')
    if tamil_chars > 0:
        return "Tamil (Tamil script)"
    low = msg.lower()
    tanglish = ["vanakkam", "epdi", "enna", "sapadu", "thanni", "veedu", "nandri", "da", "pa"]
    if any(w in low for w in tanglish):
        return "Tanglish (Tamil in English letters)"
    return "English"

def handle_lang(msg):
    m = msg.strip().lower()
    if m.startswith("translate "):
        word = msg.strip()[10:].strip().lower()
        if word in WORDS:
            return f"🌐 Translate: {word} -> {WORDS[word]}"
        return f"🌐 Translate: '{word}' - dictionary-la illa da! Ippo 10 words mattum irukku."
    if m.startswith("detect "):
        text = msg.strip()[7:].strip()
        lang = detect_lang(text)
        return f"🌐 Detected: {lang}"
    if m in ["languages", "lang", "lang list"]:
        return "🌐 OMNI LANGUAGES:\n- Tamil\n- English\n- Tanglish\n- Hindi (soon)\nNote: 100+ languages target, ippo base mattum."
    return None
