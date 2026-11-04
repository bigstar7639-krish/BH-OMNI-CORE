# OMNI WEATHER INFO - Phase 20 Step 1 - SAME PROJECT
# Category 12 - NO live API. Official source guidance + safety only.
TIPS = {
    "rain": "Rain: Umbrella eduthu po da! Official: 【entity-IMD¦canonical_name=IMD】 - mausam.【entity-imd¦canonical_name=IMD】.gov.in",
    "flood": "Flood: Low area-la irundha safe place-ku po! Emergency: 112",
    "cyclone": "Cyclone: Official 【entity-IMD¦canonical_name=IMD】 alert paaru! Veetla iru, travel venam!",
    "heat": "Heat: Thanni kudichu iru! 11-3 mani velila pogadha!",
    "earthquake": "Earthquake: Drop, Cover, Hold! Lift use pannaadha!",
    "lightning": "Lightning: Maram keezha nikkadha! Veetla iru!",
}

def handle_weather(msg):
    m = msg.strip().lower()
    if m.startswith("weather "):
        topic = msg.strip()[8:].strip().lower()
        if topic in TIPS:
            return f"🌦️ WEATHER INFO - {topic}:\n{TIPS[topic]}\nNote: Live forecast illa - official IMD site paaru da!"
        return f"🌦️ WEATHER: '{topic}' - topics: {', '.join(TIPS.keys())}"
    if m in ["weather", "weather list"]:
        return "🌦️ OMNI WEATHER TOPICS:\n" + "\n".join(f"- {k}" for k in TIPS.keys()) + "\nNote: Live API illa, guidance mattum."
    return None
