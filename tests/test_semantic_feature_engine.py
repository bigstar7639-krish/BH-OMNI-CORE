
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticFeatureEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_empty_text_returns_zero_signals(self):
        result = self.engine.extract("")

        self.assertEqual(result["token_count"], 0)
        self.assertEqual(result["sentiment_signal"], 0.0)
        self.assertEqual(result["urgency_signal"], 0.0)

    def test_positive_sentiment(self):
        result = self.engine.extract("I am happy and good")

        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_negative_sentiment(self):
        result = self.engine.extract("This is bad and sad")

        self.assertEqual(result["sentiment_signal"], -1.0)

    def test_mixed_sentiment(self):
        result = self.engine.extract("good but bad")

        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_negation_detection(self):
        result = self.engine.extract("I do not like this")

        self.assertEqual(result["negation_signal"], 1.0)

    def test_urgency_detection(self):
        result = self.engine.extract("This is urgent")

        self.assertEqual(result["urgency_signal"], 1.0)

    def test_question_detection(self):
        result = self.engine.extract("Why is this happening?")

        self.assertEqual(result["question_signal"], 1.0)

    def test_tamil_negation(self):
        result = self.engine.extract("எனக்கு இது பிடிக்கவில்லை")

        self.assertEqual(result["negation_signal"], 1.0)
        self.assertEqual(result["sentiment_signal"], -1.0)

    def test_tamil_question(self):
        result = self.engine.extract("இது என்ன?")

        self.assertEqual(result["question_signal"], 1.0)

    def test_non_string_input(self):
        with self.assertRaises(TypeError):
            self.engine.extract(123)

    def test_result_structure(self):
        result = self.engine.extract("Hello world")

        expected = {
            "question_signal",
            "negation_signal",
            "sentiment_signal",
            "urgency_signal",
            "token_count",
        }

        self.assertEqual(set(result.keys()), expected)

    def test_reset(self):
        self.assertTrue(self.engine.reset())


if __name__ == "__main__":
    unittest.main()
