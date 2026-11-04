# OMNI SMART HOME - Cat 14 - SIMULATION ONLY - Real hardware illa!
# Light/Fan/AC/TV - Simulation state, NO real device control - Honest!
import json, pathlib
F = pathlib.Path("omni_smarthome.json")
def _load():
    if F.exists():
        try: return json.loads(F.read_text())
        except: pass
    return {"light": "OFF", "fan": "OFF", "ac": "OFF", "tv": "OFF"}
def _save(d): F.write_text(json.dumps(d, indent=2))
def handle_smarthome(msg):
    s = msg.strip(); m = s.lower()
    d = _load()
    if m.startswith("light "):
        v = "ON" if "on" in m else "OFF"; d["light"]=v; _save(d); return f"💡 SMART HOME (SIMULATION): Light {v} - Real bulb illa, simulation mattum da!"
    if m.startswith("fan "):
        v = "ON" if "on" in m else "OFF"; d["fan"]=v; _save(d); return f"🌀 SMART HOME (SIMULATION): Fan {v} - Real fan illa!"
    if m.startswith("ac "):
        v = "ON" if "on" in m else "OFF"; d["ac"]=v; _save(d); return f"❄️ SMART HOME (SIMULATION): AC {v} - Real AC illa!"
    if m in ["smarthome", "home", "home status"]:
        return f"🏠 SMART HOME (SIMULATION):\nLight: {d['light']}\nFan: {d['fan']}\nAC: {d['ac']}\nTV: {d['tv']}\nNote: Real device-ku Home Assistant + hardware venum!"
    return None
