
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticEdgeCases(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_empty_text(self):
        result = self.engine.extract("")

        self.assertEqual(result["token_count"], 0)
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_whitespace_only_text(self):
        result = self.engine.extract("   \n\t  ")

        self.assertEqual(result["token_count"], 0)
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_punctuation_only_text(self):
        result = self.engine.extract("...!!!")

        self.assertEqual(result["token_count"], 0)
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_question_mark_without_words(self):
        result = self.engine.extract("???")

        self.assertEqual(result["question_signal"], 1.0)
        self.assertEqual(result["token_count"], 0)

    def test_numeric_text(self):
        result = self.engine.extract("12345")

        self.assertEqual(result["token_count"], 1)
        self.assertEqual(result["sentiment_signal"], 0.0)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            self.engine.extract(None)


if __name__ == "__main__":
    unittest.main()
