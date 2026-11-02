
"""BH-OMNI CORE: Dynamic sparse feature registry."""

import json
import math
import os
import tempfile
from pathlib import Path


class BHFeatureRegistry:
    """Register sparse features with stable, non-reused IDs."""

    VERSION = 2

    def __init__(self, file_path=None):
        self.file_path = Path(file_path) if file_path else None
        self.features = {}
        self.reverse_features = {}
        self.next_id = 0

        if self.file_path and self.file_path.exists():
            self.load()

    @staticmethod
    def _validate_name(name):
        if not isinstance(name, str):
            raise TypeError("Feature name must be a string.")

        name = name.strip()
        if not name:
            raise ValueError("Feature name cannot be empty.")

        return name

    @staticmethod
    def _validate_value(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Feature values must be numeric.")

        value = float(value)
        if not math.isfinite(value):
            raise ValueError("Feature values must be finite.")

        return value

    def register(self, name):
        """Register a feature and return its permanent ID."""
        name = self._validate_name(name)

        if name in self.features:
            return self.features[name]

        feature_id = self.next_id
        self.next_id += 1

        self.features[name] = feature_id
        self.reverse_features[feature_id] = name

        return feature_id

    def register_many(self, names):
        if not isinstance(names, (list, tuple, set)):
            raise TypeError("names must be a list, tuple or set.")

        return [self.register(name) for name in names]

    def get_id(self, name):
        name = self._validate_name(name)
        return self.features.get(name)

    def get_name(self, feature_id):
        if isinstance(feature_id, bool) or not isinstance(feature_id, int):
            raise TypeError("feature_id must be an integer.")

        return self.reverse_features.get(feature_id)

    def encode_sparse(self, values):
        if not isinstance(values, dict):
            raise TypeError("values must be a dictionary.")

        result = {}

        for name, raw_value in values.items():
            name = self._validate_name(name)
            value = self._validate_value(raw_value)

            if value != 0.0:
                feature_id = self.register(name)
                result[feature_id] = value

        return result

    def decode_sparse(self, vector):
        if not isinstance(vector, dict):
            raise TypeError("vector must be a dictionary.")

        result = {}

        for feature_id, raw_value in vector.items():
            if isinstance(feature_id, bool) or not isinstance(feature_id, int):
                raise TypeError("Feature IDs must be integers.")

            name = self.get_name(feature_id)
            if name is None:
                raise ValueError(f"Unknown feature ID: {feature_id}")

            value = self._validate_value(raw_value)

            if value != 0.0:
                result[name] = value

        return result

    def remove(self, name):
        """Remove a feature without reusing its ID."""
        name = self._validate_name(name)
        feature_id = self.features.pop(name, None)

        if feature_id is None:
            return False

        self.reverse_features.pop(feature_id, None)
        return True

    def save(self, path=None):
        target = Path(path) if path else self.file_path

        if target is None:
            raise ValueError("A save path is required.")

        target.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "version": self.VERSION,
            "next_id": self.next_id,
            "features": self.features
        }

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(target.parent),
                suffix=".tmp",
                delete=False
            ) as file:
                temp_path = Path(file.name)
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.flush()
                os.fsync(file.fileno())

            temp_path.replace(target)
            self.file_path = target
            return True

        finally:
            if temp_path is not None and temp_path.exists():
                temp_path.unlink()

    def load(self, path=None):
        target = Path(path) if path else self.file_path

        if target is None:
            raise ValueError("A load path is required.")

        with target.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Invalid registry file.")

        if data.get("version") != self.VERSION:
            raise ValueError("Unsupported registry version.")

        saved_features = data.get("features")
        if not isinstance(saved_features, dict):
            raise ValueError("Invalid saved features.")

        new_features = {}
        new_reverse = {}

        for raw_name, feature_id in saved_features.items():
            name = self._validate_name(raw_name)

            if isinstance(feature_id, bool) or not isinstance(feature_id, int):
                raise ValueError("Feature IDs must be integers.")

            if feature_id < 0:
                raise ValueError("Feature IDs cannot be negative.")

            if name in new_features or feature_id in new_reverse:
                raise ValueError("Duplicate feature name or ID.")

            new_features[name] = feature_id
            new_reverse[feature_id] = name

        next_id = data.get("next_id")

        if (
            isinstance(next_id, bool)
            or not isinstance(next_id, int)
            or next_id < 0
        ):
            raise ValueError("Invalid next feature ID.")

        minimum_next_id = max(new_reverse, default=-1) + 1

        if next_id < minimum_next_id:
            raise ValueError("Saved next ID conflicts with registered features.")

        self.features = new_features
        self.reverse_features = new_reverse
        self.next_id = next_id
        self.file_path = target

        return True

    def stats(self):
        return {
            "registered_features": len(self.features),
            "next_available_id": self.next_id,
            "fixed_capacity": None,
            "storage_type": "sparse"
        }

    def clear(self):
        self.features.clear()
        self.reverse_features.clear()
        self.next_id = 0
        return True
