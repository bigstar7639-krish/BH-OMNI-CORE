import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineResetIsolation(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_previous_text_is_not_reused(self):
        self.pipeline.process("I am happy")
        self.pipeline.reset()

        result = self.pipeline.process("I am sad")

        self.assertEqual(result["original_text"], "I am sad")
        self.assertEqual(
            result["semantic_features"]["sentiment_signal"],
            -1.0,
        )

    def test_numeric_features_are_replaced_after_reset(self):
        self.pipeline.process("First input")
        self.pipeline.reset()

        result = self.pipeline.process("Second input")

        self.assertEqual(result["feature_count"], 4)
        self.assertEqual(
            list(result["numeric_features"].keys()),
            [0, 1, 2, 3],
        )

    def test_repeated_reset_is_safe(self):
        self.pipeline.process("Hello")
        self.pipeline.reset()
        self.pipeline.reset()

        result = self.pipeline.process("Hello again")

        self.assertEqual(result["original_text"], "Hello again")


if __name__ == "__main__":
    unittest.main()
