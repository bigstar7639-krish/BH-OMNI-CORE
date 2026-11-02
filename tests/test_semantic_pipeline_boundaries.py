
import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestSemanticPipelineBoundaries(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_full_stop_boundary_through_pipeline(self):
        result = self.pipeline.process("Not. Happy")
        self.assertEqual(
            result["semantic_features"]["sentiment_signal"],
            1.0,
        )

    def test_question_boundary_through_pipeline(self):
        result = self.pipeline.process("Not? Happy")
        self.assertEqual(
            result["semantic_features"]["sentiment_signal"],
            1.0,
        )

    def test_newline_boundary_through_pipeline(self):
        result = self.pipeline.process("Not\nHappy")
        self.assertEqual(
            result["semantic_features"]["sentiment_signal"],
            1.0,
        )

    def test_same_sentence_negation_through_pipeline(self):
        result = self.pipeline.process("Not happy")
        self.assertEqual(
            result["semantic_features"]["sentiment_signal"],
            -1.0,
        )

    def test_numeric_features_remain_available(self):
        result = self.pipeline.process("Not. Happy")
        self.assertEqual(result["feature_count"], 4)
        self.assertEqual(len(result["numeric_features"]), 4)


if __name__ == "__main__":
    unittest.main()
