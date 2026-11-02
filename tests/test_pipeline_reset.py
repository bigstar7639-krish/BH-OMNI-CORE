import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineReset(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_reset_runs_without_error(self):
        self.pipeline.process("Hello world")
        self.pipeline.reset()

    def test_reset_clears_numeric_features(self):
        self.pipeline.process("Hello world")

        self.pipeline.reset()

        numeric_brain = self.pipeline.bridge.get_numeric_brain()
        self.assertEqual(numeric_brain.get_vector(), {})

    def test_pipeline_works_after_reset(self):
        self.pipeline.process("I am happy")
        self.pipeline.reset()

        result = self.pipeline.process("I am sad")

        self.assertEqual(result["original_text"], "I am sad")
        self.assertEqual(result["feature_count"], 4)


if __name__ == "__main__":
    unittest.main()
