
import unittest

from brain.language_analyzer import BHLanguageAnalyzer


class TestBHLanguageAnalyzer(unittest.TestCase):

    def test_tamil_script(self):
        result = BHLanguageAnalyzer.analyze("வணக்கம்")
        self.assertEqual(result["primary_script"], "Tamil")

    def test_latin_script(self):
        result = BHLanguageAnalyzer.analyze("Hello world")
        self.assertEqual(result["primary_script"], "Latin")

    def test_devanagari_script(self):
        result = BHLanguageAnalyzer.analyze("नमस्ते")
        self.assertEqual(result["primary_script"], "Devanagari")

    def test_arabic_script(self):
        result = BHLanguageAnalyzer.analyze("مرحبا")
        self.assertEqual(result["primary_script"], "Arabic")

    def test_japanese_scripts(self):
        result = BHLanguageAnalyzer.analyze("こんにちは")
        self.assertEqual(result["primary_script"], "Hiragana")

    def test_mixed_scripts(self):
        result = BHLanguageAnalyzer.analyze("Hello வணக்கம்")

        self.assertEqual(result["script_count"], 2)
        self.assertIn("Latin", result["scripts"])
        self.assertIn("Tamil", result["scripts"])

    def test_empty_text(self):
        result = BHLanguageAnalyzer.analyze("")

        self.assertIsNone(result["primary_script"])
        self.assertEqual(result["script_count"], 0)

    def test_punctuation_and_numbers(self):
        result = BHLanguageAnalyzer.analyze("123 !!!")

        self.assertEqual(result["recognized_characters"], 0)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            BHLanguageAnalyzer.analyze(123)


if __name__ == "__main__":
    unittest.main()
