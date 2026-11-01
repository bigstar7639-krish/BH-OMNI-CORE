
import math
from brain.tokenizer import BHTokenizer


class BHTextFeatureEngine:

    def __init__(self):
        self.tokenizer = BHTokenizer()

    def text_to_features(self, text):

        if not isinstance(text, str) or not text.strip():
            return [0.0, 0.0, 0.0, 0.0]

        tokens = self.tokenizer.tokenize(text)

        if not isinstance(tokens, (list, tuple)):
            raise TypeError("Tokenizer must return a list or tuple.")

        tokens = [
            token.casefold()
            for token in tokens
            if isinstance(token, str) and token.strip()
        ]

        if not tokens:
            return [0.0, 0.0, 0.0, 0.0]

        token_count = len(tokens)

        # Feature 1: Normalized text length
        length = min(token_count / 50.0, 1.0)

        # Feature 2: Vocabulary diversity
        unique = len(set(tokens)) / token_count

        # Feature 3: Average normalized token length
        average = min(
            sum(len(token) for token in tokens)
            / (token_count * 20.0),
            1.0
        )

        # Feature 4: Text complexity
        complexity = min(
            math.log1p(token_count) / 5.0,
            1.0
        )

        features = [
            length,
            unique,
            average,
            complexity
        ]

        return [
            round(value, 4)
            for value in features
        ]


if __name__ == "__main__":

    engine = BHTextFeatureEngine()

    result = engine.text_to_features("What is Earth?")

    print("BH-OMNI TEXT FEATURES")
    print(result)

    print("Feature count:", len(result))
    print("All values valid:", all(
        math.isfinite(value) and 0.0 <= value <= 1.0
        for value in result
    ))
