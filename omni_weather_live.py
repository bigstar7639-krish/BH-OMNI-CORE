# OMNI WEATHER LIVE - Phase 26 Step 1 - SAME PROJECT
# FREE API: wttr.in - NO key, NO kasu
# Internet illa-na offline guidance-ku fallback
import urllib.request, urllib.parse, json
def get_live_weather(city="Chennai"):
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
        req = urllib.request.Request(url, headers={"User-Agent": "curl"})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read().decode())
            cur = data["current_condition"][0]
            area = data["nearest_area"][0]["areaName"][0]["value"]
            return f"🌦️ LIVE WEATHER - {area}:\nTemp: {cur['temp_C']}°C (Feels: {cur['FeelsLikeC']}°C)\nSky: {cur['weatherDesc'][0]['value']}\nHumidity: {cur['humidity']}%\nWind: {cur['windspeedKmph']} km/h\nSource: wttr.in - FREE, NO key"
    except Exception as e:
        return f"🌦️ WEATHER OFFLINE - Internet illa / wttr.in fail ({e})\nOffline guidance: 'weather rain' nu try pannu da!\nOfficial: mausam.【entity-imd¦canonical_name=IMD】.gov.in paaru da!"
def handle_weather_live(msg):
    m = msg.strip().lower()
    if m.startswith("live weather"):
        city = msg.strip()[12:].strip() or "Chennai"
        return get_live_weather(city)
    if m in ["live weather", "weather live"]:
        return get_live_weather("Chennai")
    return None
