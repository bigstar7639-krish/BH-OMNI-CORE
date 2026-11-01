
import math
import unittest

from brain.text_feature_engine import BHTextFeatureEngine


class TestTextFeatureEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BHTextFeatureEngine()

    def test_text_to_features(self):
        result = self.engine.text_to_features("What is Earth?")

        self.assertEqual(len(result), 4)

        for value in result:
            self.assertIsInstance(value, (int, float))
            self.assertTrue(math.isfinite(value))

    def test_empty_text(self):
        result = self.engine.text_to_features("")

        self.assertEqual(
            result,
            [0.0, 0.0, 0.0, 0.0]
        )

    def test_whitespace_only_text(self):
        result = self.engine.text_to_features("   \n\t ")

        self.assertEqual(
            result,
            [0.0, 0.0, 0.0, 0.0]
        )

    def test_feature_values_are_valid(self):
        result = self.engine.text_to_features(
            "BlackHole Omni Core"
        )

        for value in result:
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_tamil_unicode_text(self):
        result = self.engine.text_to_features(
            "தமிழ் மொழி அழகானது"
        )

        self.assertEqual(len(result), 4)

        self.assertTrue(
            any(value > 0.0 for value in result),
            "Tamil text should produce meaningful features."
        )

    def test_deterministic_output(self):
        text = "BH OMNI CORE intelligence"

        first = self.engine.text_to_features(text)
        second = self.engine.text_to_features(text)

        self.assertEqual(first, second)

    def test_feature_range(self):
        samples = [
            "Hello",
            "What is artificial intelligence?",
            "தமிழ் மொழி",
            "123456789",
            "A" * 100
        ]

        for text in samples:
            with self.subTest(text=text):
                result = self.engine.text_to_features(text)

                self.assertEqual(len(result), 4)

                for value in result:
                    self.assertTrue(math.isfinite(value))
                    self.assertGreaterEqual(value, 0.0)
                    self.assertLessEqual(value, 1.0)


if __name__ == "__main__":
    unittest.main()
