
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticNegationScope(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_not_happy_is_not_positive(self):
        result = self.engine.extract("I am not happy")
        self.assertEqual(result["negation_signal"], 1.0)
        self.assertLessEqual(result["sentiment_signal"], 0.0)

    def test_not_bad_is_not_negative(self):
        result = self.engine.extract("This is not bad")
        self.assertEqual(result["negation_signal"], 1.0)
        self.assertGreaterEqual(result["sentiment_signal"], 0.0)

    def test_without_negation_positive_stays_positive(self):
        result = self.engine.extract("I am happy")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_without_negation_negative_stays_negative(self):
        result = self.engine.extract("This is bad")
        self.assertEqual(result["sentiment_signal"], -1.0)


if __name__ == "__main__":
    unittest.main()
