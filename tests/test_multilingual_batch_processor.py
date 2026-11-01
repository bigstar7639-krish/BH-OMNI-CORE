
import unittest

from brain.multilingual_batch_processor import BHMultilingualBatchProcessor


class TestMultilingualBatchProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = BHMultilingualBatchProcessor()

    def test_multiple_languages(self):
        texts = [
            "Hello world",
            "வணக்கம் உலகம்",
            "नमस्ते दुनिया",
            "こんにちは世界",
        ]

        result = self.processor.process_batch(texts)

        self.assertEqual(result["total"], 4)
        self.assertEqual(result["successful"], 4)
        self.assertEqual(result["failed"], 0)

    def test_batch_results_keep_separate_features(self):
        result = self.processor.process_batch([
            "Hello",
            "வணக்கம்",
        ])

        first = result["results"][0]["result"]["numeric_features"]
        second = result["results"][1]["result"]["numeric_features"]

        self.assertEqual(len(first), 4)
        self.assertEqual(len(second), 4)
        self.assertIsNot(first, second)

    def test_invalid_input_in_batch(self):
        result = self.processor.process_batch([
            "Hello",
            123,
            "வணக்கம்",
        ])

        self.assertEqual(result["total"], 3)
        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 1)

    def test_empty_batch(self):
        result = self.processor.process_batch([])

        self.assertEqual(result["total"], 0)
        self.assertEqual(result["successful"], 0)
        self.assertEqual(result["failed"], 0)

    def test_invalid_batch_type(self):
        with self.assertRaises(TypeError):
            self.processor.process_batch("Hello")

    def test_empty_text_item(self):
        result = self.processor.process_batch([
            "Hello",
            "",
        ])

        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)


if __name__ == "__main__":
    unittest.main()
