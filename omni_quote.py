# OMNI QUOTE - Phase 25 Step 1 - SAME PROJECT
import random
QUOTES = [
    "Muyarchi thiruvinai aakum - try pannu da, mudiyum!",
    "Innaiku oru chinna step - naalaiku periya victory!",
    "Failure = lesson, NOT stop!",
    "Unnala mudiyum da - nee nenaikuradha vida perusa!",
    "Sinnadha start pannu, perusa mudiyum!",
    "Discipline > Motivation - daily pannu!",
]
def get_quote():
    return "💬 QUOTE: " + random.choice(QUOTES)
def handle_quote(msg):
    m = msg.strip().lower()
    if m in ["quote", "daily quote", "motivation", "quote of the day"]:
        return get_quote()
    return None
