import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineIntegrationConsistency(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_numeric_count_matches_vector_size(self):
        result = self.pipeline.process("Hello world")

        self.assertEqual(
            result["feature_count"],
            len(result["numeric_features"]),
        )

    def test_numeric_feature_ids_are_unique(self):
        result = self.pipeline.process("Hello world")

        feature_ids = list(result["numeric_features"].keys())

        self.assertEqual(len(feature_ids), len(set(feature_ids)))

    def test_semantic_output_has_expected_signals(self):
        result = self.pipeline.process("I am happy")

        expected = {
            "question_signal",
            "negation_signal",
            "sentiment_signal",
            "urgency_signal",
            "token_count",
        }

        self.assertTrue(
            expected.issubset(result["semantic_features"].keys())
        )

    def test_original_text_matches_input(self):
        text = "Hello நண்பா!"
        result = self.pipeline.process(text)

        self.assertEqual(result["original_text"], text)


if __name__ == "__main__":
    unittest.main()
