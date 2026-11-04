# OMNI TTS - Phase 28 Step 1 - SAME PROJECT
# FREE: termux-tts-speak - Phone own voice, NO key, NO kasu
# Laptop-la illa-na fallback message mattum
import subprocess, shutil
def speak(text):
    if shutil.which("termux-tts-speak"):
        try:
            subprocess.run(["termux-tts-speak", text], timeout=10)
            return f"🔊 TTS SPEAKING: {text}\nSource: termux-tts-speak - FREE, phone voice"
        except Exception as e:
            return f"🔊 TTS FAIL: {e}\nText: {text}"
    return f"🔊 TTS NOT FOUND - Termux API install pannu:\n pkg install termux-api\nText: {text}\nPhone-la mattum work aagum da!"
def handle_tts(msg):
    m = msg.strip().lower()
    if m.startswith("speak "):
        text = msg.strip()[6:].strip()
        if text:
            return speak(text)
        return "🔊 TTS: 'speak Vanakkam Krish' nu try pannu da!"
    if m in ["speak", "tts", "voice"]:
        return "🔊 TTS READY - 'speak Vanakkam' nu try pannu da!"
    return None
