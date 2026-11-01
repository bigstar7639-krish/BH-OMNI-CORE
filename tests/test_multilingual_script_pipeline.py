
import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestMultilingualScriptPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def test_all_supported_script_samples(self):
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

        for expected, text in samples.items():
            with self.subTest(script=expected):
                result = self.pipeline.process(text)

                self.assertEqual(
                    result["script_analysis"]["primary_script"],
                    expected
                )
                self.assertEqual(result["feature_count"], 4)
                self.assertEqual(len(result["numeric_features"]), 4)

    def test_mixed_scripts(self):
        result = self.pipeline.process("Hello வணக்கம் مرحبا")

        self.assertEqual(result["script_analysis"]["script_count"], 3)
        self.assertEqual(result["feature_count"], 4)


if __name__ == "__main__":
    unittest.main()
