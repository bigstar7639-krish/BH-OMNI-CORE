
import unittest

from brain.sparse_numeric_ops import BHSparseNumericOps


class TestBHSparseNumericOps(unittest.TestCase):

    def test_add(self):
        result = BHSparseNumericOps.add(
            {0: 2, 5: 3},
            {5: 4, 10: 6}
        )

        self.assertEqual(result, {0: 2, 5: 7, 10: 6})

    def test_add_cancels_zero(self):
        result = BHSparseNumericOps.add(
            {1: 5},
            {1: -5}
        )

        self.assertEqual(result, {})

    def test_dot_product(self):
        result = BHSparseNumericOps.dot_product(
            {0: 2, 5: 3, 100: 4},
            {0: 5, 5: 2, 200: 9}
        )

        self.assertEqual(result, 16)

    def test_magnitude(self):
        result = BHSparseNumericOps.magnitude(
            {0: 3, 10: 4}
        )

        self.assertAlmostEqual(result, 5.0)

    def test_cosine_similarity(self):
        result = BHSparseNumericOps.cosine_similarity(
            {0: 1, 1: 2},
            {0: 2, 1: 4}
        )

        self.assertAlmostEqual(result, 1.0)

    def test_zero_vector_similarity(self):
        result = BHSparseNumericOps.cosine_similarity(
            {},
            {0: 5}
        )

        self.assertEqual(result, 0.0)

    def test_invalid_vector(self):
        with self.assertRaises(ValueError):
            BHSparseNumericOps.add(
                {0: 2},
                {-1: 5}
            )

    def test_invalid_numeric_value(self):
        with self.assertRaises(ValueError):
            BHSparseNumericOps.magnitude(
                {0: float("nan")}
            )

    def test_large_feature_id(self):
        result = BHSparseNumericOps.dot_product(
            {999999999999: 7},
            {999999999999: 3}
        )

        self.assertEqual(result, 21)


if __name__ == "__main__":
    unittest.main()
