
import unicodedata


class BHLanguageAnalyzer:
    """Detects writing systems present in Unicode text."""

    SCRIPT_RANGES = {
        "Latin": [(0x0041, 0x024F), (0x1E00, 0x1EFF)],
        "Tamil": [(0x0B80, 0x0BFF)],
        "Devanagari": [(0x0900, 0x097F)],
        "Bengali": [(0x0980, 0x09FF)],
        "Gurmukhi": [(0x0A00, 0x0A7F)],
        "Gujarati": [(0x0A80, 0x0AFF)],
        "Oriya": [(0x0B00, 0x0B7F)],
        "Telugu": [(0x0C00, 0x0C7F)],
        "Kannada": [(0x0C80, 0x0CFF)],
        "Malayalam": [(0x0D00, 0x0D7F)],
        "Sinhala": [(0x0D80, 0x0DFF)],
        "Thai": [(0x0E00, 0x0E7F)],
        "Lao": [(0x0E80, 0x0EFF)],
        "Tibetan": [(0x0F00, 0x0FFF)],
        "Myanmar": [(0x1000, 0x109F)],
        "Georgian": [(0x10A0, 0x10FF), (0x1C90, 0x1CBF)],
        "Hangul": [(0xAC00, 0xD7AF), (0x1100, 0x11FF)],
        "Ethiopic": [(0x1200, 0x137F)],
        "Cherokee": [(0x13A0, 0x13FF), (0xAB70, 0xABBF)],
        "Canadian Aboriginal": [(0x1400, 0x167F)],
        "Khmer": [(0x1780, 0x17FF)],
        "Mongolian": [(0x1800, 0x18AF)],
        "Hiragana": [(0x3040, 0x309F)],
        "Katakana": [(0x30A0, 0x30FF), (0x31F0, 0x31FF)],
        "CJK": [(0x3400, 0x4DBF), (0x4E00, 0x9FFF)],
        "Arabic": [(0x0600, 0x06FF), (0x0750, 0x077F)],
        "Hebrew": [(0x0590, 0x05FF)],
        "Greek": [(0x0370, 0x03FF)],
        "Cyrillic": [(0x0400, 0x052F)],
        "Armenian": [(0x0530, 0x058F)],
    }

    @classmethod
    def detect_character_script(cls, character):
        code = ord(character)

        for script, ranges in cls.SCRIPT_RANGES.items():
            for start, end in ranges:
                if start <= code <= end:
                    return script

        return "Other"

    @classmethod
    def analyze(cls, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")

        counts = {}

        for character in text:
            if character.isspace():
                continue

            category = unicodedata.category(character)

            if category.startswith(("P", "S", "N")):
                continue

            script = cls.detect_character_script(character)

            if script == "Other":
                continue

            counts[script] = counts.get(script, 0) + 1

        total = sum(counts.values())

        return {
            "scripts": counts,
            "primary_script": (
                max(counts, key=counts.get) if counts else None
            ),
            "script_count": len(counts),
            "recognized_characters": total,
        }
