
import unittest

from brain.text_feature_engine import BHTextFeatureEngine


class TestTextFeatureEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BHTextFeatureEngine()

    def test_text_to_features(self):
        result = self.engine.text_to_features(
            "What is Earth?"
        )

        self.assertEqual(len(result), 4)

        for value in result:
            self.assertIsInstance(value, (int, float))

    def test_empty_text(self):
        result = self.engine.text_to_features("")

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


if __name__ == "__main__":
    unittest.main()
