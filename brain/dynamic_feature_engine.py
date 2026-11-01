
"""BH-OMNI CORE: Dynamic multilingual sparse feature engine."""

import math
import unicodedata

from brain.feature_registry import BHFeatureRegistry
from brain.tokenizer import BHTokenizer


class BHDynamicFeatureEngine:
    """
    Extract dynamic sparse features from Unicode text.

    Features are registered as needed. No fixed feature count
    or dense million-element array is allocated.
    """

    def __init__(self, registry=None):
        self.registry = (
            registry
            if registry is not None
            else BHFeatureRegistry()
        )
        self.tokenizer = BHTokenizer()

    @staticmethod
    def normalize(text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        return unicodedata.normalize("NFC", text).casefold()

    @staticmethod
    def _script_name(character):
        code = ord(character)

        # Common Unicode script ranges.
        ranges = [
            (0x0041, 0x024F, "latin"),
            (0x0370, 0x03FF, "greek"),
            (0x0400, 0x052F, "cyrillic"),
            (0x0590, 0x05FF, "hebrew"),
            (0x0600, 0x08FF, "arabic"),
            (0x0900, 0x097F, "devanagari"),
            (0x0980, 0x09FF, "bengali"),
            (0x0A00, 0x0A7F, "gurmukhi"),
            (0x0A80, 0x0AFF, "gujarati"),
            (0x0B00, 0x0B7F, "oriya"),
            (0x0B80, 0x0BFF, "tamil"),
            (0x0C00, 0x0C7F, "telugu"),
            (0x0C80, 0x0CFF, "kannada"),
            (0x0D00, 0x0D7F, "malayalam"),
            (0x0E00, 0x0E7F, "thai"),
            (0x0E80, 0x0EFF, "lao"),
            (0x0F00, 0x0FFF, "tibetan"),
            (0x1000, 0x109F, "myanmar"),
            (0x10A0, 0x10FF, "georgian"),
            (0x1100, 0x11FF, "hangul"),
            (0x3040, 0x309F, "hiragana"),
            (0x30A0, 0x30FF, "katakana"),
            (0x3400, 0x9FFF, "han"),
            (0xAC00, 0xD7AF, "hangul"),
        ]

        for start, end, name in ranges:
            if start <= code <= end:
                return name

        return "other"

    def extract(self, text):
        """Return a sparse feature vector: {feature_id: value}."""
        text = self.normalize(text)

        if not text.strip():
            return {}

        tokens = self.tokenizer.tokenize(text)
        tokens = [
            token for token in tokens
            if token.strip()
        ]

        if not tokens:
            return {}

        features = {}

        def add_feature(name, value):
            if not math.isfinite(value):
                raise ValueError("Feature value must be finite.")

            if value != 0:
                features[name] = float(value)

        # General text features.
        add_feature("text:token_count", len(tokens))
        add_feature("text:character_count", len(text))
        add_feature(
            "text:unique_token_ratio",
            len(set(tokens)) / len(tokens)
        )

        # Token frequency features.
        frequencies = {}

        for token in tokens:
            frequencies[token] = frequencies.get(token, 0) + 1

        for token, count in frequencies.items():
            add_feature(f"token:{token}", count)

        # Unicode script distribution.
        script_counts = {}

        for character in text:
            category = unicodedata.category(character)

            if category.startswith("L"):
                script = self._script_name(character)
                script_counts[script] = (
                    script_counts.get(script, 0) + 1
                )

        total_script_characters = sum(script_counts.values())

        for script, count in script_counts.items():
            add_feature(
                f"script:{script}",
                count / total_script_characters
            )

        # Character category features.
        category_counts = {}

        for character in text:
            category = unicodedata.category(character)
            group = category[0]

            if group in ("L", "M", "N", "P", "S"):
                category_counts[group] = (
                    category_counts.get(group, 0) + 1
                )

        for category, count in category_counts.items():
            add_feature(
                f"unicode_category:{category}",
                count / len(text)
            )

        return self.registry.encode_sparse(features)

    def extract_batch(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("texts must be a list or tuple.")

        return [
            self.extract(text)
            for text in texts
        ]

    def decode(self, sparse_vector):
        return self.registry.decode_sparse(sparse_vector)

    def save_registry(self, path=None):
        return self.registry.save(path)

    def statistics(self):
        return self.registry.stats()


if __name__ == "__main__":
    engine = BHDynamicFeatureEngine()

    samples = [
        "Hello world",
        "வணக்கம் தமிழ் உலகம்",
        "नमस्ते दुनिया",
        "مرحبا بالعالم",
        "你好世界",
        "こんにちは世界",
        "안녕하세요 세계",
        "Привет мир",
        "Bonjour le monde",
    ]

    for sample in samples:
        vector = engine.extract(sample)

        print("Text:", sample)
        print("Sparse features:", vector)
        print("Decoded:", engine.decode(vector))
        print()

    print("Registry statistics:", engine.statistics())
