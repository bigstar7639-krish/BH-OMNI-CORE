
import math
import unittest

from brain.text_network import BHTextNetwork


class TestTextNetwork(unittest.TestCase):

    def setUp(self):
        self.text_brain = BHTextNetwork(seed=42)

    def test_forward_text(self):
        result = self.text_brain.forward_text("What is Earth?")

        self.assertIsInstance(result, dict)
        self.assertIn("features", result)
        self.assertIn("output", result)

        self.assertEqual(len(result["features"]), 4)
        self.assertEqual(len(result["output"]), 2)

    def test_feature_values_are_finite(self):
        result = self.text_brain.forward_text("BlackHole Omni Core")

        for value in result["features"]:
            self.assertIsInstance(value, (int, float))
            self.assertTrue(math.isfinite(value))

    def test_output_values_are_valid(self):
        result = self.text_brain.forward_text("BlackHole Omni Core")

        for value in result["output"]:
            self.assertIsInstance(value, (int, float))
            self.assertTrue(math.isfinite(value))
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_training_returns_valid_loss(self):
        loss = self.text_brain.train_text(
            "What is Earth?",
            [1.0, 0.0]
        )

        self.assertIsInstance(loss, float)
        self.assertTrue(math.isfinite(loss))
        self.assertGreaterEqual(loss, 0.0)

    def test_same_seed_produces_same_initial_output(self):
        first = BHTextNetwork(seed=42)
        second = BHTextNetwork(seed=42)

        first_result = first.forward_text("Hello BH OMNI")
        second_result = second.forward_text("Hello BH OMNI")

        self.assertEqual(
            first_result["features"],
            second_result["features"]
        )

        self.assertEqual(
            first_result["output"],
            second_result["output"]
        )


if __name__ == "__main__":
    unittest.main()
