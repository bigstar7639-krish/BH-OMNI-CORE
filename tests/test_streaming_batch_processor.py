
import unittest

from brain.multilingual_batch_processor import BHMultilingualBatchProcessor


class TestStreamingBatchProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = BHMultilingualBatchProcessor(
            max_batch_size=5,
            max_text_length=100
        )

    def test_returns_generator(self):
        result = self.processor.process_iter(["Hello", "வணக்கம்"])

        self.assertTrue(hasattr(result, "__next__"))

    def test_stream_results_one_by_one(self):
        stream = self.processor.process_iter([
            "Hello",
            "வணக்கம்",
            "नमस्ते"
        ])

        first = next(stream)
        second = next(stream)
        third = next(stream)

        self.assertTrue(first["success"])
        self.assertTrue(second["success"])
        self.assertTrue(third["success"])

        self.assertEqual(first["index"], 0)
        self.assertEqual(second["index"], 1)
        self.assertEqual(third["index"], 2)

    def test_stream_handles_invalid_text(self):
        stream = self.processor.process_iter([
            "Hello",
            123,
            "வணக்கம்"
        ])

        results = list(stream)

        self.assertEqual(len(results), 3)
        self.assertTrue(results[0]["success"])
        self.assertFalse(results[1]["success"])
        self.assertTrue(results[2]["success"])

    def test_stream_batch_limit(self):
        stream = self.processor.process_iter([
            "one", "two", "three", "four", "five", "six"
        ])

        for _ in range(5):
            next(stream)

        with self.assertRaises(ValueError):
            next(stream)

    def test_stream_text_length_limit(self):
        results = list(self.processor.process_iter([
            "Hello",
            "This text is too long"
        ]))

        self.assertTrue(results[0]["success"])
        self.assertFalse(results[1]["success"])

    def test_empty_stream(self):
        results = list(self.processor.process_iter([]))

        self.assertEqual(results, [])

    def test_invalid_stream_input(self):
        with self.assertRaises(TypeError):
            self.processor.process_iter("Hello")

    def test_batch_compatibility(self):
        result = self.processor.process_batch([
            "Hello",
            "வணக்கம்"
        ])

        self.assertEqual(result["total"], 2)
        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 0)


if __name__ == "__main__":
    unittest.main()
