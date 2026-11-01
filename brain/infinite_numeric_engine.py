
import math
from typing import Dict, Optional


class BHInfiniteNumericEngine:
    """
    Sparse numerical feature engine.

    - No hardcoded feature-count limit.
    - Stores only non-zero values.
    - Feature IDs grow dynamically.
    - Storage is limited by available system resources.
    """

    def __init__(self):
        self.features: Dict[int, float] = {}
        self.next_id = 0

    def add_feature(self, value: float) -> Optional[int]:
        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return None

        if not math.isfinite(number):
            return None

        feature_id = self.next_id
        self.features[feature_id] = number
        self.next_id += 1

        return feature_id

    def set_feature(self, feature_id: int, value: float) -> bool:
        if not isinstance(feature_id, int) or isinstance(feature_id, bool):
            return False

        if feature_id < 0:
            return False

        try:
            number = float(value)
        except (TypeError, ValueError, OverflowError):
            return False

        if not math.isfinite(number):
            return False

        self.features[feature_id] = number

        if feature_id >= self.next_id:
            self.next_id = feature_id + 1

        return True

    def get_feature(self, feature_id: int) -> Optional[float]:
        return self.features.get(feature_id)

    def remove_feature(self, feature_id: int) -> bool:
        if feature_id not in self.features:
            return False

        del self.features[feature_id]
        return True

    def get_feature_count(self) -> int:
        return len(self.features)

    def get_all_features(self) -> Dict[int, float]:
        return self.features.copy()

    def clear(self) -> None:
        self.features.clear()
        self.next_id = 0

    def export_data(self) -> dict:
        return {
            "version": 1,
            "next_id": self.next_id,
            "features": {
                str(key): value
                for key, value in self.features.items()
            },
        }

    def load_data(self, data: dict) -> bool:
        if not isinstance(data, dict):
            return False

        raw_features = data.get("features")
        raw_next_id = data.get("next_id")

        if not isinstance(raw_features, dict):
            return False

        if not isinstance(raw_next_id, int) or isinstance(raw_next_id, bool):
            return False

        if raw_next_id < 0:
            return False

        loaded = {}

        try:
            for key, value in raw_features.items():
                feature_id = int(key)

                if feature_id < 0:
                    return False

                if str(feature_id) != str(key):
                    return False

                number = float(value)

                if not math.isfinite(number):
                    return False

                loaded[feature_id] = number

        except (TypeError, ValueError, OverflowError):
            return False

        minimum_next_id = max(loaded.keys(), default=-1) + 1

        if raw_next_id < minimum_next_id:
            return False

        self.features = loaded
        self.next_id = raw_next_id
        return True
