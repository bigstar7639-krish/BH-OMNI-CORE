
import unittest

from brain.language_analyzer import BHLanguageAnalyzer


class TestScriptCoverage(unittest.TestCase):

    def test_script_samples(self):
        samples = {
            "Latin": "Hello",
            "Tamil": "வணக்கம்",
            "Devanagari": "नमस्ते",
            "Bengali": "বাংলা",
            "Gurmukhi": "ਪੰਜਾਬੀ",
            "Gujarati": "ગુજરાતી",
            "Oriya": "ଓଡ଼ିଆ",
            "Telugu": "తెలుగు",
            "Kannada": "ಕನ್ನಡ",
            "Malayalam": "മലയാളം",
            "Sinhala": "සිංහල",
            "Thai": "ภาษาไทย",
            "Lao": "ພາສາລາວ",
            "Tibetan": "བོད་ཡིག",
            "Myanmar": "မြန်မာ",
            "Georgian": "ქართული",
            "Hangul": "한국어",
            "Ethiopic": "አማርኛ",
            "Cherokee": "ᎠᏂᏴᏫᏯ",
            "Canadian Aboriginal": "ᐃᓄᒃᑎᑐᑦ",
            "Khmer": "ភាសាខ្មែរ",
            "Mongolian": "ᠮᠣᠩᠭᠣᠯ",
            "Hiragana": "こんにちは",
            "Katakana": "カタカナ",
            "CJK": "中文",
            "Arabic": "مرحبا",
            "Hebrew": "שלום",
            "Greek": "Ελληνικά",
            "Cyrillic": "Русский",
            "Armenian": "Հայերեն",
        }

        for expected_script, sample in samples.items():
            with self.subTest(script=expected_script):
                result = BHLanguageAnalyzer.analyze(sample)
                self.assertIn(
                    expected_script,
                    result["scripts"],
                    f"{expected_script} was not detected"
                )


if __name__ == "__main__":
    unittest.main()
