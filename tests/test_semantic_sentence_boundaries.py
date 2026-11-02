
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine


class TestSemanticSentenceBoundaries(unittest.TestCase):

    def setUp(self):
        self.engine = BHSemanticFeatureEngine()

    def test_full_stop_resets_negation_scope(self):
        result = self.engine.extract("Not. Happy")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_question_mark_resets_negation_scope(self):
        result = self.engine.extract("Not? Happy")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_newline_resets_negation_scope(self):
        result = self.engine.extract("Not\nHappy")
        self.assertEqual(result["sentiment_signal"], 1.0)

    def test_negation_inside_sentence_still_works(self):
        result = self.engine.extract("Not happy")
        self.assertEqual(result["sentiment_signal"], -1.0)

    def test_tamil_negation_still_works(self):
        result = self.engine.extract("எனக்கு இது பிடிக்கவில்லை")
        self.assertEqual(result["sentiment_signal"], -1.0)


if __name__ == "__main__":
    unittest.main()
