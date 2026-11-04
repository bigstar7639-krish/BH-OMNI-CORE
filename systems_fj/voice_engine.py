
from typing import Dict, List, Optional

class VoiceError(Exception):
    pass

class VoiceEngine:
    """
    Phase 3 Step 1 - System F - Voice Engine
    - NOT real TTS - Placeholder + Metadata engine (no audio file generated)
    - Voices: tamil-male, tamil-female, english-male, english-female
    - Speed 0.5-2.0, pitch 0.5-2.0
    - Synthesize returns metadata: duration estimate, chars, voice
    - Real TTS needs Android TTS / cloud API - NOT claimed here
    """
    VALID_VOICES = ["tamil-male", "tamil-female", "english-male", "english-female", "hindi-male", "hindi-female"]
    def __init__(self):
        self._history: List[dict] = []

    def _validate(self, text, voice, speed, pitch):
        if text is None or not isinstance(text, str) or len(text.strip()) == 0:
            raise VoiceError("Text cannot be empty")
        if len(text) > 5000:
            raise VoiceError("Text too long - Max 5000 chars")
        if voice not in self.VALID_VOICES:
            raise VoiceError(f"Invalid voice: {voice} - Must be {self.VALID_VOICES}")
        if speed is None or not isinstance(speed, (int, float)) or speed < 0.5 or speed > 2.0:
            raise VoiceError("Speed must be 0.5-2.0")
        if pitch is None or not isinstance(pitch, (int, float)) or pitch < 0.5 or pitch > 2.0:
            raise VoiceError("Pitch must be 0.5-2.0")
        return True

    def synthesize(self, text: str, voice: str = "tamil-female", speed: float = 1.0, pitch: float = 1.0) -> dict:
        self._validate(text, voice, speed, pitch)
        # Estimate: ~800 chars per minute at speed 1.0
        chars = len(text.strip())
        duration_sec = round((chars / 800) * 60 / speed, 2)
        result = {"text_preview": text.strip()[:50], "chars": chars, "voice": voice, "speed": speed, "pitch": pitch, "duration_sec": duration_sec, "audio_file": None, "note": "Metadata only - No real audio generated. Use Android TTS for real audio."}
        self._history.append(result)
        return result

    def list_voices(self) -> List[str]:
        return list(self.VALID_VOICES)

    def history_count(self) -> int:
        return len(self._history)

    def get_info(self) -> dict:
        return {"voices": len(self.VALID_VOICES), "synthesized": len(self._history), "principle": "Metadata only - No fake audio claim"}
