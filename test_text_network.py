
import unittest

from brain.text_network import BHTextNetwork


class TestTextNetwork(unittest.TestCase):

    def setUp(self):
        self.text_brain = BHTextNetwork(seed=42)

    def test_forward_text(self):
        result = self.text_brain.forward_text(
            "What is Earth?"
        )

        self.assertEqual(len(result["features"]), 4)
        self.assertEqual(len(result["output"]), 2)

    def test_output_values(self):
        result = self.text_brain.forward_text(
            "BlackHole Omni Core"
        )

        for value in result["output"]:
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_training(self):
        loss = self.text_brain.train_text(
            "What is Earth?",
            [1.0, 0.0]
        )

        self.assertIsInstance(loss, float)
        self.assertGreaterEqual(loss, 0.0)


if __name__ == "__main__":
    unittest.main()
