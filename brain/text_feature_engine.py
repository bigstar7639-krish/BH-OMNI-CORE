import math
from brain.tokenizer import BHTokenizer


class BHTextFeatureEngine:

    def __init__(self):
        self.tokenizer = BHTokenizer()

    def text_to_features(self, text):

        # Handle empty or invalid input
        if not isinstance(text, str) or not text.strip():
            return [0.0, 0.0, 0.0, 0.0]

        # Tokenize without learning new vocabulary
        tokens = self.tokenizer.tokenize(text)

        if not tokens:
            return [0.0, 0.0, 0.0, 0.0]

        # Generate 4 numeric features
        length = min(len(tokens) / 50, 1.0)

        unique = min(
            len(set(tokens)) / len(tokens),
            1.0
        )

        average = min(
            sum(
                self.tokenizer.vocab.get(token, 0)
                for token in tokens
            ) / (len(tokens) * 100),
            1.0
        )

        complexity = min(
            math.log(len(tokens) + 1) / 5,
            1.0
        )

        return [
            round(length, 4),
            round(unique, 4),
            round(average, 4),
            round(complexity, 4)
        ]


if __name__ == "__main__":

    engine = BHTextFeatureEngine()

    result = engine.text_to_features("What is Earth?")

    print("BH-OMNI TEXT FEATURES")
    print(result)
