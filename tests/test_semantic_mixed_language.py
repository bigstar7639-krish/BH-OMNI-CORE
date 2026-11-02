
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticMixedLanguage(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_english_positive_tamil_negative(self):
        result = self.engine.extract(
            "I am happy but இது கெட்ட"
        )
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_tamil_negative_with_english_positive(self):
        result = self.engine.extract(
            "எனக்கு இது பிடிக்கவில்லை but good"
        )
        self.assertEqual(result["negation_signal"], 1.0)
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_mixed_language_urgency(self):
        result = self.engine.extract(
            "இது emergency"
        )
        self.assertEqual(result["urgency_signal"], 1.0)

    def test_mixed_language_question(self):
        result = self.engine.extract(
            "இது என்ன?"
        )
        self.assertEqual(result["question_signal"], 1.0)

    def test_mixed_language_output_is_deterministic(self):
        text = "I am happy ஆனால் இது கெட்ட"

        first = self.engine.extract(text)
        second = self.engine.extract(text)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
