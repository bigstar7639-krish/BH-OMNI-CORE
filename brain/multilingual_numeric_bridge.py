
import unittest

from brain.multilingual_numeric_bridge import (
    BHMultilingualNumericBridge
)


class TestMultilingualNumericBridge(unittest.TestCase):

    def setUp(self):
        self.bridge = BHMultilingualNumericBridge()

    def test_english_text(self):
        result = self.bridge.encode_text("Hello world")
        self.assertEqual(len(result), 4)
        self.assertTrue(all(isinstance(v, float) for v in result.values()))

    def test_tamil_text(self):
        result = self.bridge.encode_text("வணக்கம் உலகம்")
        self.assertEqual(len(result), 4)

    def test_hindi_text(self):
        result = self.bridge.encode_text("नमस्ते दुनिया")
        self.assertEqual(len(result), 4)

    def test_japanese_text(self):
        result = self.bridge.encode_text("こんにちは世界")
        self.assertEqual(len(result), 4)

    def test_dynamic_feature_ids(self):
        result = self.bridge.encode_text("Hello world")
        self.assertEqual(list(result.keys()), [0, 1, 2, 3])

    def test_new_text_replaces_previous_vector(self):
        self.bridge.encode_text("Hello")
        result = self.bridge.encode_text("வணக்கம்")

        self.assertEqual(len(result), 4)
        self.assertEqual(
            self.bridge.numeric_brain.get_feature_count(),
            4
        )

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            self.bridge.encode_text(123)

    def test_empty_input(self):
        with self.assertRaises(ValueError):
            self.bridge.encode_text("")

    def test_reset(self):
        self.bridge.encode_text("Hello world")
        self.bridge.reset()

        self.assertEqual(
            self.bridge.numeric_brain.get_feature_count(),
            0
        )


if __name__ == "__main__":
    unittest.main()
