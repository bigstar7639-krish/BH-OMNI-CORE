
import unittest
import math

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticOutputStability(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_repeated_input_is_deterministic(self):
        text = "I am not happy. I am good"

        first = self.engine.extract(text)
        second = self.engine.extract(text)

        self.assertEqual(first, second)

    def test_sentiment_is_within_valid_range(self):
        samples = [
            "I am happy",
            "I am sad",
            "I am not happy",
            "I am not bad",
            "Good and bad",
            "எனக்கு இது பிடிக்கவில்லை",
        ]

        for text in samples:
            result = self.engine.extract(text)
            sentiment = result["sentiment_signal"]

            self.assertGreaterEqual(sentiment, -1.0)
            self.assertLessEqual(sentiment, 1.0)

    def test_all_numeric_outputs_are_finite(self):
        result = self.engine.extract("I am happy")

        for value in result.values():
            if isinstance(value, (int, float)):
                self.assertTrue(math.isfinite(value))

    def test_repeated_calls_do_not_change_results(self):
        text = "This is an emergency"

        first = self.engine.extract(text)

        self.engine.extract("I am sad")
        self.engine.reset()

        second = self.engine.extract(text)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
