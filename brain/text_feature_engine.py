import math
from brain.tokenizer import BHTokenizer


class BHTextFeatureEngine:

    def __init__(self):
        self.tokenizer = BHTokenizer()

    def text_to_features(self, text):

        self.tokenizer.learn(text)
        tokens = self.tokenizer.encode(text)

        if not tokens:
            return [0.0, 0.0, 0.0, 0.0]

        length = min(len(tokens) / 50, 1.0)
        unique = min(len(set(tokens)) / max(len(tokens), 1), 1.0)
        average = min(sum(tokens) / (len(tokens) * 100), 1.0)
        complexity = min(math.log(len(tokens) + 1) / 5, 1.0)

        return [
            round(length, 4),
            round(unique, 4),
            round(average, 4),
            round(complexity, 4)
        ]


if __name__ == "__main__":
    engine = BHTextFeatureEngine()

    print(engine.text_to_features("What is Earth?"))
