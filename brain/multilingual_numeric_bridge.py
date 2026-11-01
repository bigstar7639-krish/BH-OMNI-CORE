
import math

from brain.text_feature_engine import BHTextFeatureEngine
from brain.numeric_brain import BHNumericBrain


class BHMultilingualNumericBridge:
    """
    Connects multilingual text features to the sparse numeric brain.

    Uses the existing text feature engine and stores its four
    numerical outputs in stable feature slots.
    """

    def __init__(self):
        self.text_engine = BHTextFeatureEngine()
        self.numeric_brain = BHNumericBrain()

    def encode_text(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")

        features = self.text_engine.text_to_features(text)

        if not isinstance(features, (list, tuple)):
            raise ValueError("Text engine must return a list or tuple")

        if len(features) != 4:
            raise ValueError("Expected exactly four text features")

        for index, value in enumerate(features):
            try:
                number = float(value)
            except (TypeError, ValueError, OverflowError):
                raise ValueError("Invalid numerical text feature")

            if not math.isfinite(number):
                raise ValueError("Text feature must be finite")

            if not self.numeric_brain.set_feature(index, number):
                raise ValueError("Could not store text feature")

        return self.numeric_brain.get_vector()

    def get_numeric_brain(self):
        return self.numeric_brain

    def reset(self):
        self.numeric_brain.clear()
