import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineOutputStructure(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_output_contains_required_keys(self):
        result = self.pipeline.process("Hello world")

        expected_keys = {
            "original_text",
            "script_analysis",
            "numeric_features",
            "feature_count",
            "semantic_features",
        }

        self.assertEqual(set(result.keys()), expected_keys)

    def test_script_analysis_is_dictionary(self):
        result = self.pipeline.process("Hello world")
        self.assertIsInstance(result["script_analysis"], dict)

    def test_numeric_feature_count_is_integer(self):
        result = self.pipeline.process("Hello world")
        self.assertIsInstance(result["feature_count"], int)

    def test_feature_count_is_four(self):
        result = self.pipeline.process("Hello world")
        self.assertEqual(result["feature_count"], 4)

    def test_original_text_is_preserved(self):
        text = "Hello world!"
        result = self.pipeline.process(text)
        self.assertEqual(result["original_text"], text)


if __name__ == "__main__":
    unittest.main()
