
import math
from typing import Dict


class BHSparseNumericOps:
    """Mathematical operations for sparse numerical vectors."""

    @staticmethod
    def _validate(vector: dict) -> bool:
        if not isinstance(vector, dict):
            return False

        for key, value in vector.items():
            if not isinstance(key, int) or isinstance(key, bool):
                return False

            if key < 0:
                return False

            if not isinstance(value, (int, float)) or isinstance(value, bool):
                return False

            if not math.isfinite(value):
                return False

        return True

    @staticmethod
    def add(first: dict, second: dict) -> Dict[int, float]:
        if not BHSparseNumericOps._validate(first):
            raise ValueError("Invalid first vector")

        if not BHSparseNumericOps._validate(second):
            raise ValueError("Invalid second vector")

        result = dict(first)

        for key, value in second.items():
            result[key] = result.get(key, 0.0) + value

        return {
            key: value
            for key, value in result.items()
            if value != 0
        }

    @staticmethod
    def dot_product(first: dict, second: dict) -> float:
        if not BHSparseNumericOps._validate(first):
            raise ValueError("Invalid first vector")

        if not BHSparseNumericOps._validate(second):
            raise ValueError("Invalid second vector")

        if len(first) > len(second):
            first, second = second, first

        return sum(
            value * second.get(key, 0.0)
            for key, value in first.items()
        )

    @staticmethod
    def magnitude(vector: dict) -> float:
        if not BHSparseNumericOps._validate(vector):
            raise ValueError("Invalid vector")

        return math.sqrt(sum(value * value for value in vector.values()))

    @staticmethod
    def cosine_similarity(first: dict, second: dict) -> float:
        dot = BHSparseNumericOps.dot_product(first, second)

        first_magnitude = BHSparseNumericOps.magnitude(first)
        second_magnitude = BHSparseNumericOps.magnitude(second)

        if first_magnitude == 0 or second_magnitude == 0:
            return 0.0

        return dot / (first_magnitude * second_magnitude)
