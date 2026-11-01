
import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestBHMultilingualPipeline(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def test_english_processing(self):
        result = self.pipeline.process("Hello world")

        self.assertEqual(result["original_text"], "Hello world")
        self.assertEqual(
            result["script_analysis"]["primary_script"],
            "Latin"
        )
        self.assertEqual(result["feature_count"], 4)

    def test_tamil_processing(self):
        result = self.pipeline.process("வணக்கம் உலகம்")

        self.assertEqual(
            result["script_analysis"]["primary_script"],
            "Tamil"
        )
        self.assertEqual(result["feature_count"], 4)

    def test_hindi_processing(self):
        result = self.pipeline.process("नमस्ते दुनिया")

        self.assertEqual(
            result["script_analysis"]["primary_script"],
            "Devanagari"
        )

    def test_mixed_language_processing(self):
        result = self.pipeline.process("Hello வணக்கம்")

        self.assertEqual(result["script_analysis"]["script_count"], 2)

    def test_numeric_features_exist(self):
        result = self.pipeline.process("Hello")

        self.assertEqual(len(result["numeric_features"]), 4)

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            self.pipeline.process("")

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            self.pipeline.process(123)

    def test_reset(self):
        self.pipeline.process("Hello")
        self.pipeline.reset()

        self.assertEqual(
            self.pipeline.bridge.numeric_brain.get_feature_count(),
            0
        )


if __name__ == "__main__":
    unittest.main()
