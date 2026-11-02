
import json
import tempfile
import unittest
from pathlib import Path

from brain.feature_registry import BHFeatureRegistry


class TestBHFeatureRegistry(unittest.TestCase):

    def setUp(self):
        self.registry = BHFeatureRegistry()

    def test_register_and_get_id(self):
        feature_id = self.registry.register("language:tamil")
        self.assertEqual(feature_id, 0)
        self.assertEqual(
            self.registry.get_id("language:tamil"),
            feature_id
        )

    def test_duplicate_registration_reuses_same_id(self):
        first = self.registry.register("token:hello")
        second = self.registry.register("token:hello")
        self.assertEqual(first, second)

    def test_remove_does_not_reuse_id(self):
        first = self.registry.register("feature:a")
        self.registry.remove("feature:a")
        second = self.registry.register("feature:b")

        self.assertGreater(second, first)

    def test_clear_does_not_reset_next_id(self):
        first = self.registry.register("feature:a")
        self.registry.clear()
        second = self.registry.register("feature:b")

        self.assertGreater(second, first)

    def test_sparse_encode_and_decode(self):
        encoded = self.registry.encode_sparse({
            "feature:a": 2.5,
            "feature:b": 0,
        })

        decoded = self.registry.decode_sparse(encoded)

        self.assertEqual(decoded, {"feature:a": 2.5})

    def test_save_and_load_preserves_next_id(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "registry.json"

            first = self.registry.register("feature:a")
            self.registry.remove("feature:a")
            self.registry.save(path)

            loaded = BHFeatureRegistry(path)
            second = loaded.register("feature:b")

            self.assertGreater(second, first)

    def test_invalid_feature_value(self):
        with self.assertRaises(ValueError):
            self.registry.encode_sparse({"feature:a": float("nan")})

    def test_invalid_feature_name(self):
        with self.assertRaises(ValueError):
            self.registry.register("   ")


if __name__ == "__main__":
    unittest.main()
