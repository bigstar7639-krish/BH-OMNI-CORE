
import unittest

from brain.multilingual_batch_processor import BHMultilingualBatchProcessor


class TestBatchMemorySafety(unittest.TestCase):

    def test_default_limits(self):
        processor = BHMultilingualBatchProcessor()

        self.assertEqual(processor.max_batch_size, 100)
        self.assertEqual(processor.max_text_length, 10000)

    def test_custom_limits(self):
        processor = BHMultilingualBatchProcessor(
            max_batch_size=5,
            max_text_length=100
        )

        self.assertEqual(processor.max_batch_size, 5)
        self.assertEqual(processor.max_text_length, 100)

    def test_batch_size_limit(self):
        processor = BHMultilingualBatchProcessor(max_batch_size=2)

        with self.assertRaises(ValueError):
            processor.process_batch(["one", "two", "three"])

    def test_text_length_limit(self):
        processor = BHMultilingualBatchProcessor(max_text_length=5)

        result = processor.process_batch([
            "Hello",
            "Too long text"
        ])

        self.assertEqual(result["successful"], 1)
        self.assertEqual(result["failed"], 1)

    def test_invalid_zero_limit(self):
        with self.assertRaises(ValueError):
            BHMultilingualBatchProcessor(max_batch_size=0)

    def test_invalid_negative_limit(self):
        with self.assertRaises(ValueError):
            BHMultilingualBatchProcessor(max_text_length=-1)

    def test_boolean_limit_rejected(self):
        with self.assertRaises(ValueError):
            BHMultilingualBatchProcessor(max_batch_size=True)

    def test_other_items_continue_after_failure(self):
        processor = BHMultilingualBatchProcessor(max_text_length=5)

        result = processor.process_batch([
            "Hello",
            "This is too long",
            "Hi"
        ])

        self.assertEqual(result["successful"], 2)
        self.assertEqual(result["failed"], 1)


if __name__ == "__main__":
    unittest.main()
