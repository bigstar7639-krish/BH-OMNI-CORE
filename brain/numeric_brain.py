
from brain.infinite_numeric_engine import BHInfiniteNumericEngine
from brain.sparse_numeric_ops import BHSparseNumericOps


class BHNumericBrain:
    """Combines dynamic numeric features with sparse math operations."""

    def __init__(self):
        self.engine = BHInfiniteNumericEngine()

    def add_feature(self, value):
        return self.engine.add_feature(value)

    def set_feature(self, feature_id, value):
        return self.engine.set_feature(feature_id, value)

    def get_feature(self, feature_id):
        return self.engine.get_feature(feature_id)

    def remove_feature(self, feature_id):
        return self.engine.remove_feature(feature_id)

    def get_feature_count(self):
        return self.engine.get_feature_count()

    def get_vector(self):
        return self.engine.get_all_features()

    def add_vectors(self, other_vector):
        return BHSparseNumericOps.add(
            self.get_vector(),
            other_vector
        )

    def dot_product(self, other_vector):
        return BHSparseNumericOps.dot_product(
            self.get_vector(),
            other_vector
        )

    def magnitude(self):
        return BHSparseNumericOps.magnitude(
            self.get_vector()
        )

    def similarity(self, other_vector):
        return BHSparseNumericOps.cosine_similarity(
            self.get_vector(),
            other_vector
        )

    def export_data(self):
        return self.engine.export_data()

    def load_data(self, data):
        return self.engine.load_data(data)

    def clear(self):
        self.engine.clear()
