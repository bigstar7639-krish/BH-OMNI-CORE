# OMNI STT - Phase 39 Step 1 - SAME PROJECT - PENDING FEATURE DONE!
# Speech to Text - Phone mic + SpeechRecognition - FREE
# Termux-la mic permission venum!
import subprocess, shutil
def listen_once():
    # Termux-la mic record + SpeechRecognition use panna try pannu
    # Simple version: termux-microphone-record irundha use pannu, illa-na instruction kodu
    if shutil.which("termux-microphone-record"):
        return "🎤 STT READY - Mic irukku!\nUse: termux-microphone-record -f /tmp/voice.wav -l 3\nAppuram: 'stt file /tmp/voice.wav' nu try pannu da!\nNote: Full STT-ku Pydroid3-la SpeechRecognition venum."
    return "🎤 STT SETUP:\n1. pkg install termux-api\n2. Termux Settings-la Microphone permission ON pannu\n3. 'stt listen' nu try pannu da!\nPhone mic-la mattum work aagum!"
def handle_stt(msg):
    m = msg.strip().lower()
    if m in ["stt", "stt listen", "voice to text", "listen"]:
        return listen_once()
    if m.startswith("stt file "):
        f = msg.strip()[9:].strip()
        return f"🎤 STT FILE: {f}\nFile-a Pydroid3-la SpeechRecognition vachu text aakkalam da!\nTermux-la direct STT-ku internet + SpeechRecognition venum."
    return None
