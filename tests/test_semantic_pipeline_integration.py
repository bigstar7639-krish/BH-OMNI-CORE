
import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestSemanticPipelineIntegration(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_semantic_features_are_returned(self):
        result = self.pipeline.process("I am happy")

        self.assertIn("semantic_features", result)
        self.assertIsInstance(result["semantic_features"], dict)

    def test_tamil_negation_through_pipeline(self):
        result = self.pipeline.process("எனக்கு இது பிடிக்கவில்லை")

        semantic = result["semantic_features"]

        self.assertEqual(semantic["negation_signal"], 1.0)
        self.assertEqual(semantic["sentiment_signal"], -1.0)

    def test_english_question_through_pipeline(self):
        result = self.pipeline.process("What is artificial intelligence?")

        self.assertEqual(
            result["semantic_features"]["question_signal"],
            1.0
        )

    def test_urgency_through_pipeline(self):
        result = self.pipeline.process("This is an emergency")

        self.assertEqual(
            result["semantic_features"]["urgency_signal"],
            1.0
        )

    def test_numeric_features_remain_available(self):
        result = self.pipeline.process("Hello world")

        self.assertIn("numeric_features", result)
        self.assertEqual(result["feature_count"], 4)

    def test_original_text_is_preserved(self):
        text = "வணக்கம் நண்பா"

        result = self.pipeline.process(text)

        self.assertEqual(result["original_text"], text)

    def test_invalid_input_is_rejected(self):
        with self.assertRaises(TypeError):
            self.pipeline.process(123)

    def test_empty_input_is_rejected(self):
        with self.assertRaises(ValueError):
            self.pipeline.process("   ")


if __name__ == "__main__":
    unittest.main()
