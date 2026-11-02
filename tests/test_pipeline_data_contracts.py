
import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineDataContracts(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_original_text_is_string(self):
        result = self.pipeline.process("Hello world")
        self.assertIsInstance(result["original_text"], str)

    def test_numeric_features_are_dictionary(self):
        result = self.pipeline.process("Hello world")
        self.assertIsInstance(result["numeric_features"], dict)

    def test_numeric_feature_count_matches(self):
        result = self.pipeline.process("Hello world")
        self.assertEqual(
            result["feature_count"],
            len(result["numeric_features"]),
        )

    def test_numeric_feature_values_are_numeric(self):
        result = self.pipeline.process("Hello world")

        for value in result["numeric_features"].values():
            self.assertIsInstance(value, (int, float))

    def test_semantic_features_are_dictionary(self):
        result = self.pipeline.process("I am happy")
        self.assertIsInstance(result["semantic_features"], dict)

    def test_semantic_values_are_numeric(self):
        result = self.pipeline.process("I am happy")

        for key in (
            "question_signal",
            "negation_signal",
            "sentiment_signal",
            "urgency_signal",
        ):
            self.assertIsInstance(
                result["semantic_features"][key],
                (int, float),
            )

    def test_empty_text_is_rejected(self):
        with self.assertRaises(ValueError):
            self.pipeline.process("   ")


if __name__ == "__main__":
    unittest.main()
