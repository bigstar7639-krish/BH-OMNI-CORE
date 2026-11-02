
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticNegationBoundaries(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_negation_does_not_affect_later_sentence(self):
        result = self.engine.extract("I am not happy. I am good")
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_negation_does_not_affect_unrelated_later_word(self):
        result = self.engine.extract("Not bad. Great")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_positive_without_negation(self):
        result = self.engine.extract("I feel happy and great")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_negative_without_negation(self):
        result = self.engine.extract("I feel sad and bad")
        self.assertEqual(result["sentiment_signal"], -1.0)

    def test_tamil_negative_expression(self):
        result = self.engine.extract("எனக்கு இது பிடிக்கவில்லை")
        self.assertEqual(result["negation_signal"], 1.0)
        self.assertEqual(result["sentiment_signal"], -1.0)


if __name__ == "__main__":
    unittest.main()
