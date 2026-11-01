
import unittest

from brain.numeric_brain import BHNumericBrain


class TestBHNumericBrain(unittest.TestCase):

    def setUp(self):
        self.brain = BHNumericBrain()

    def test_add_and_get_feature(self):
        feature_id = self.brain.add_feature(25)

        self.assertEqual(feature_id, 0)
        self.assertEqual(self.brain.get_feature(feature_id), 25.0)

    def test_dynamic_features(self):
        for i in range(1000):
            self.brain.add_feature(i + 1)

        self.assertEqual(self.brain.get_feature_count(), 1000)

    def test_set_and_remove(self):
        self.assertTrue(self.brain.set_feature(50, 12))
        self.assertEqual(self.brain.get_feature(50), 12.0)

        self.assertTrue(self.brain.remove_feature(50))
        self.assertIsNone(self.brain.get_feature(50))

    def test_vector_addition(self):
        self.brain.add_feature(2)
        self.brain.add_feature(3)

        result = self.brain.add_vectors({0: 5, 2: 10})

        self.assertEqual(result, {0: 7.0, 1: 3.0, 2: 10})

    def test_dot_product(self):
        self.brain.add_feature(2)
        self.brain.add_feature(3)

        self.assertEqual(
            self.brain.dot_product({0: 4, 1: 5}),
            23.0
        )

    def test_magnitude(self):
        self.brain.add_feature(3)
        self.brain.add_feature(4)

        self.assertAlmostEqual(self.brain.magnitude(), 5.0)

    def test_similarity(self):
        self.brain.add_feature(1)
        self.brain.add_feature(2)

        self.assertAlmostEqual(
            self.brain.similarity({0: 2, 1: 4}),
            1.0
        )

    def test_export_and_restore(self):
        self.brain.add_feature(10)
        self.brain.add_feature(20)

        saved = self.brain.export_data()

        restored = BHNumericBrain()
        self.assertTrue(restored.load_data(saved))

        self.assertEqual(restored.get_vector(), {0: 10.0, 1: 20.0})

    def test_clear(self):
        self.brain.add_feature(10)
        self.brain.clear()

        self.assertEqual(self.brain.get_feature_count(), 0)


if __name__ == "__main__":
    unittest.main()
