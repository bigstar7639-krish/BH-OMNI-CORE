import hashlib
import math
from brain.tokenizer import BHTokenizer


class BHTextFeatureEngine:
    """Create stable numeric features without changing tokenizer vocabulary."""

    FEATURE_SIZE = 4

    def __init__(self, tokenizer=None):
        self.tokenizer = tokenizer or BHTokenizer()

    @staticmethod
    def _stable_value(token):
        digest = hashlib.blake2b(
            token.encode("utf-8"), digest_size=4
        ).digest()
        return int.from_bytes(digest, "big") / 4294967295.0

    def text_to_features(self, text):
        if not isinstance(text, str) or not text.strip():
            return [0.0] * self.FEATURE_SIZE

        tokens = self.tokenizer.tokenize(text)
        if not tokens:
            return [0.0] * self.FEATURE_SIZE

        length = min(len(tokens) / 50.0, 1.0)
        unique_ratio = len(set(tokens)) / len(tokens)
        signature = sum(self._stable_value(t) for t in tokens) / len(tokens)
        complexity = min(math.log1p(len(tokens)) / 5.0, 1.0)

        return [
            round(length, 6),
            round(unique_ratio, 6),
            round(signature, 6),
            round(complexity, 6),
        ]
