# OMNI CHAT V41 S2 - Conversation Engine ONLY - SAME PROJECT
# V40 preserved - Pudhusa isolated module mattum!
# NO new trained model - Local conversation-context engine mattum!
# Stdlib mattum - NO paid, NO API key, NO external AI
import re

# V40 Brain-oda intents-a reuse pannrom - copy illa, import pannrom!
# Import fail aana - fallback list use pannu - V40-a break pannadha!
try:
    from omni_brain_full import INTENTS as V40_INTENTS
except Exception:
    V40_INTENTS = {"unknown": []}

FOLLOWUP_WORDS = ["adhu", "adha", "adhukku", "adhula", "appuram", "adha pathi", "idhu", "idha", "adhoda", "adhai", "avlo dhaan", "vera", "mattrum"]

class ChatV41:
    """V41 S2 - Conversation Engine - Latest 10 turns mattum!"""
    def __init__(self):
        self.history = []  # [{"role": "user"/"ai", "text": "...", "intent": "..."}]
        self.topic = None
        self.turn_count = 0
    def _detect_intent(self, msg):
        m = msg.lower()
        for intent, kws in V40_INTENTS.items():
            for kw in kws:
                if kw and kw in m:
                    return intent
        return "unknown"
    def _is_followup(self, msg):
        m = msg.strip().lower()
        for w in FOLLOWUP_WORDS:
            if m == w or m.startswith(w + " ") or m.startswith(w + "?") or " " + w + " " in " " + m + " ":
                return True
        # "?" mattum - "Enna?" mathiri short follow-up
        if len(m.split()) <= 2 and m.endswith("?"):
            return True
        return False
    def _last_user_topic(self):
        for h in reversed(self.history):
            if h["role"] == "user":
                return h
        return None
    def new_chat(self):
        """Context reset - Pazhaya conversation-a azhichidu!"""
        self.history = []
        self.topic = None
        self.turn_count = 0
        return "🧠 V41 CHAT: New conversation started! Pazhaya context azhchiten da!"
    def send(self, msg):
        """Main - User msg -> Context + Intent + Reply"""
        # Empty / invalid input - Safe handling!
        if msg is None or not isinstance(msg, str) or not msg.strip():
            return "🧠 V41 CHAT: Empty message da! Edhachum type pannu - 'vanakkam' nu try pannu!"
        text = msg.strip()
        # Follow-up check - Munnadi context irukka?
        is_follow = self._is_followup(text)
        prev = self._last_user_topic()
        intent = self._detect_intent(text)
        # Follow-up-na, topic-a preserve pannu - Intent-a prev-la irundhu edu!
        if is_follow and prev is not None:
            if intent == "unknown":
                intent = prev["intent"]
            reply = f"🧠 V41 CHAT (Follow-up | Topic: {prev['text'][:40]} | Intent: {intent}):\nNee '{prev['text']}' pathi kekkura-nu puriyudhu da! Adha pathi konjam detail-a sollu - naan adha vachu reply panren!"
        elif intent == "unknown":
            reply = f"🧠 V41 CHAT (New | Intent: unknown):\n'{text}' - idhu enaku theriyala da! Context illa, solli kodu - 'teach {text} | answer' nu!"
        else:
            reply = f"🧠 V41 CHAT (New | Intent: {intent} | Topic: {text[:40]}):\nPuriyudhu da! '{text}' - {intent} pathi kekkura! Tool-ku: '{intent}' nu route pannalam!"
            self.topic = text
        # History-la save - Latest 10 turns mattum!
        self.history.append({"role": "user", "text": text, "intent": intent})
        self.history.append({"role": "ai", "text": reply, "intent": intent})
        # 10 turns = 20 msgs (user+ai) - Adhukku mela trim pannu!
        if len(self.history) > 20:
            self.history = self.history[-20:]
        self.turn_count += 1
        return reply
    def get_history(self):
        return list(self.history)
    def get_context(self):
        if not self.history:
            return "🧠 V41 CHAT: Context illa da - New conversation!"
        last = self.history[-1]
        return f"🧠 V41 CHAT CONTEXT:\nTurns: {self.turn_count}\nHistory msgs: {len(self.history)}\nTopic: {self.topic}\nLast: {last['role']} - {last['text'][:60]}"

CHAT = ChatV41()
def handle_chat_v41(msg):
    s = msg.strip() if isinstance(msg, str) else ""
    ml = s.lower()
    if ml in ["new chat", "new conversation", "reset chat", "chat reset"]:
        return CHAT.new_chat()
    if ml in ["chat history", "history", "chat context"]:
        return CHAT.get_context()
    if ml.startswith("chat "):
        return CHAT.send(s[5:].strip())
    return None
