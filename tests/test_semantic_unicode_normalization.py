
import unittest
import unicodedata

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticUnicodeNormalization(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_tamil_nfc_and_nfd_produce_same_output(self):
        text = "எனக்கு இது பிடிக்கவில்லை"

        nfc_text = unicodedata.normalize("NFC", text)
        nfd_text = unicodedata.normalize("NFD", text)

        nfc_result = self.engine.extract(nfc_text)
        nfd_result = self.engine.extract(nfd_text)

        self.assertEqual(nfc_result, nfd_result)

    def test_english_case_normalization(self):
        lower = self.engine.extract("i am happy")
        upper = self.engine.extract("I AM HAPPY")

        self.assertEqual(lower, upper)

    def test_tamil_text_is_preserved_in_token_count(self):
        result = self.engine.extract("வணக்கம் நண்பா")

        self.assertGreater(result["token_count"], 0)

    def test_unicode_punctuation_does_not_crash(self):
        result = self.engine.extract("வணக்கம்! எப்படி?")

        self.assertIsInstance(result, dict)
        self.assertEqual(result["question_signal"], 1.0)


if __name__ == "__main__":
    unittest.main()
