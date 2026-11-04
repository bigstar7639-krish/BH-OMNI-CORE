# OMNI FULL BRAIN - Phase 37 - En Brain-oda Full Logic - 100% OWN
# Intent + Memory + Routing + Personality + Honesty - Ellaam ore file-la!
import random

PERSONALITY = {
    "greeting": ["Vanakkam da Krish! Enna pannitu irukka?", "Hey da! Vandhuta! Sollu da!"],
    "unknown": ["Idhu enaku theriyala da, solli kodu - naan kathukiren!", "Hmm, idha naan innum kathukala - 'teach' pannu da!"],
    "praise": ["Neeyum super dhaan da!", "Adhu unnala dhaan mudiyum da!"],
}

INTENTS = {
    "joke": ["joke", "sirikkanum", "sirippu"],
    "kadhai": ["kadhai", "story"],
    "motivation": ["motivation", "sogam", "kashtam", "bayam"],
    "weather": ["weather", "rain", "hot", "cold"],
    "translate": ["translate", "mozhi"],
    "code": ["code", "coding", "python"],
    "poem": ["poem", "kavithai"],
    "quiz": ["quiz", "game"],
    "memory": ["peru", "note", "todo", "memory"],
    "habit": ["habit"],
    "expense": ["expense", "money", "cash"],
    "mood": ["mood"],
    "goal": ["goal"],
    "water": ["water", "thanni"],
    "birthday": ["birthday"],
    "travel": ["travel", "trip"],
    "briefing": ["briefing", "summary"],
    "emergency": ["stop", "sos", "emergency"],
    "stats": ["stats", "status"],
    "backup": ["backup"],
    "quote": ["quote"],
    "tts": ["speak", "voice"],
    "own_ai": ["own ai", "my ai", "teach", "my lessons", "my brain", "forget", "correct", "export brain", "import brain"],
    "mega": ["mega"],
}

class OmniBrain:
    def __init__(self):
        self.history = []
        self.name = "BH-OMNI CORE"
        self.creator = "Krish"
        self.mood = "happy"
    def detect_intent(self, msg):
        m = msg.lower()
        for intent, keywords in INTENTS.items():
            for kw in keywords:
                if kw in m:
                    return intent
        return "unknown"
    def think(self, msg):
        """En brain-oda thinking - Intent -> Memory -> Route"""
        intent = self.detect_intent(msg)
        self.history.append({"msg": msg, "intent": intent})
        if len(self.history) > 20:
            self.history = self.history[-20:]
        return intent
    def reply(self, msg):
        intent = self.think(msg)
        # Greeting
        if msg.strip().lower() in ["vanakkam", "hi", "hello", "hey"]:
            return f"🧠 FULL BRAIN: {random.choice(PERSONALITY['greeting'])}\nIntent: greeting | History: {len(self.history)} msgs"
        # Intent routing - brain decides, module handles
        routes = {
            "joke": "Joke-ku: 'mega joke' / 'joke' nu try pannu da!",
            "kadhai": "Kadhai-ku: 'mega kadhai' / 'kadhai' nu try pannu da!",
            "motivation": "Motivation-ku: 'mega motivation' nu try pannu da! Nee mudiyum da!",
            "weather": "Weather-ku: 'live weather Chennai' nu try pannu da!",
            "translate": "Translate-ku: 'translate live en|ta hello' nu try pannu da!",
            "code": "Code-ku: 'code python' nu try pannu da!",
            "poem": "Poem-ku: 'poem friend' nu try pannu da!",
            "quiz": "Quiz-ku: 'mega quiz' / 'flash quiz' nu try pannu da!",
            "memory": "Memory-ku: 'memory' / 'todo' / 'note' nu try pannu da!",
            "habit": "Habit-ku: 'habits' nu try pannu da!",
            "expense": "Expense-ku: 'expenses' nu try pannu da!",
            "mood": "Mood-ku: 'moods' nu try pannu da!",
            "goal": "Goal-ku: 'goals' nu try pannu da!",
            "water": "Water-ku: 'water' nu try pannu da!",
            "birthday": "Birthday-ku: 'birthdays' nu try pannu da!",
            "travel": "Travel-ku: 'trips' nu try pannu da!",
            "briefing": "Briefing-ku: 'briefing' nu try pannu da!",
            "emergency": "Emergency-ku: 'stop' / 'sos' nu try pannu da! Careful-a iru!",
            "stats": "Stats-ku: 'stats' nu try pannu da!",
            "backup": "Backup-ku: 'backup' nu try pannu da!",
            "quote": "Quote-ku: 'quote' nu try pannu da!",
            "tts": "TTS-ku: 'speak Vanakkam' nu try pannu da! Phone-la kural varum!",
            "own_ai": "Own AI-ku: 'own ai' / 'my lessons' / 'teach Q | A' nu try pannu da!",
            "mega": "Mega-ku: 'mega' nu try pannu da! Full content irukku!",
        }
        if intent in routes:
            return f"🧠 FULL BRAIN (Intent: {intent}):\n{routes[intent]}\nHistory: {len(self.history)} msgs | Creator: {self.creator}"
        # Unknown - Honest!
        return f"🧠 FULL BRAIN (Intent: unknown):\n{random.choice(PERSONALITY['unknown'])}\nNee solli kudutha, naan kathukiren da!"
    def get_brain_status(self):
        return f"🧠 FULL BRAIN STATUS:\nName: {self.name}\nCreator: {self.creator}\nMood: {self.mood}\nHistory: {len(self.history)} msgs\nIntents: {len(INTENTS)}\n100% OWN - En brain-oda full logic!"

BRAIN = OmniBrain()
def handle_brain(msg):
    m = msg.strip().lower()
    if m in ["brain", "full brain", "brain status"]:
        return BRAIN.get_brain_status()
    if m.startswith("brain "):
        return BRAIN.reply(msg.strip()[6:].strip())
    return None
