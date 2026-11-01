
import unittest

from brain.infinite_numeric_engine import BHInfiniteNumericEngine


class TestBHInfiniteNumericEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BHInfiniteNumericEngine()

    def test_add_feature(self):
        feature_id = self.engine.add_feature(10)
        self.assertEqual(feature_id, 0)
        self.assertEqual(self.engine.get_feature(0), 10.0)

    def test_dynamic_feature_growth(self):
        for i in range(10000):
            feature_id = self.engine.add_feature(i + 1)
            self.assertEqual(feature_id, i)

        self.assertEqual(self.engine.get_feature_count(), 10000)
        self.assertEqual(self.engine.get_feature(9999), 10000.0)

    def test_feature_removal_does_not_reuse_id(self):
        first = self.engine.add_feature(10)
        second = self.engine.add_feature(20)

        self.assertTrue(self.engine.remove_feature(first))

        third = self.engine.add_feature(30)

        self.assertEqual(second, 1)
        self.assertEqual(third, 2)

    def test_set_feature(self):
        self.assertTrue(self.engine.set_feature(100, 25))
        self.assertEqual(self.engine.get_feature(100), 25.0)

        new_id = self.engine.add_feature(50)
        self.assertEqual(new_id, 101)

    def test_invalid_values(self):
        self.assertIsNone(self.engine.add_feature(float("nan")))
        self.assertIsNone(self.engine.add_feature(float("inf")))
        self.assertIsNone(self.engine.add_feature("invalid"))

        self.assertFalse(self.engine.set_feature(-1, 10))
        self.assertFalse(self.engine.set_feature(1, float("nan")))

    def test_remove_feature(self):
        feature_id = self.engine.add_feature(5)

        self.assertTrue(self.engine.remove_feature(feature_id))
        self.assertIsNone(self.engine.get_feature(feature_id))
        self.assertFalse(self.engine.remove_feature(feature_id))

    def test_export_and_load(self):
        self.engine.add_feature(12)
        self.engine.add_feature(24)

        saved_data = self.engine.export_data()

        new_engine = BHInfiniteNumericEngine()
        self.assertTrue(new_engine.load_data(saved_data))

        self.assertEqual(new_engine.get_feature(0), 12.0)
        self.assertEqual(new_engine.get_feature(1), 24.0)

        next_id = new_engine.add_feature(36)
        self.assertEqual(next_id, 2)

    def test_invalid_load(self):
        invalid_data = {
            "next_id": 1,
            "features": {"5": 10}
        }

        self.assertFalse(self.engine.load_data(invalid_data))
        self.assertEqual(self.engine.get_feature_count(), 0)

    def test_clear(self):
        self.engine.add_feature(10)
        self.engine.clear()

        self.assertEqual(self.engine.get_feature_count(), 0)
        self.assertEqual(self.engine.add_feature(20), 0)


if __name__ == "__main__":
    unittest.main()
