
"""BH-OMNI CORE: Rule-based multilingual semantic signal extractor.

Experimental prototype. This is not a trained language model.
"""

import unicodedata


class BHSemanticFeatureEngine:
    """Extract basic interpretable language signals."""

    LEXICONS = {
        "negation": {
            "not", "no", "never", "don't", "cannot",
            "இல்லை", "வேண்டாம்", "முடியாது",
            "பிடிக்கவில்லை",
        },
        "positive": {
            "good", "great", "happy", "love", "excellent",
            "நல்ல", "நன்று", "மகிழ்ச்சி", "பிடிக்கும்",
        },
        "negative": {
            "bad", "sad", "hate", "angry", "terrible",
            "கெட்ட", "சோகம்", "பிடிக்கவில்லை", "கோபம்",
        },
        "urgency": {
            "urgent", "emergency", "immediately", "asap",
            "அவசரம்", "உடனே",
        },
    }

    # Negation words that can reverse a nearby sentiment word.
    SCOPE_NEGATIONS = {
        "not", "no", "never", "don't", "cannot",
        "இல்லை", "வேண்டாம்", "முடியாது",
    }

    def __init__(self):
        self.lexicons = {
            name: {
                unicodedata.normalize("NFC", word).casefold()
                for word in words
            }
            for name, words in self.LEXICONS.items()
        }

        self.scope_negations = {
            unicodedata.normalize("NFC", word).casefold()
            for word in self.SCOPE_NEGATIONS
        }

    @staticmethod
    def _validate(text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

    @staticmethod
    def _normalize(text):
        return unicodedata.normalize("NFC", text).casefold().strip()

    @staticmethod
    def _tokenize(text):
        tokens = []
        current = []

        for char in text:
            category = unicodedata.category(char)

            if category.startswith(("L", "N")):
                current.append(char)
            elif category.startswith("M") and current:
                current.append(char)
            else:
                if current:
                    tokens.append("".join(current))
                    current.clear()

        if current:
            tokens.append("".join(current))

        return tokens

    def extract(self, text):
        self._validate(text)

        normalized = self._normalize(text)
        tokens = self._tokenize(normalized)

        if not tokens:
            return {
                "question_signal": 0.0,
                "negation_signal": 0.0,
                "sentiment_signal": 0.0,
                "urgency_signal": 0.0,
                "token_count": 0,
            }

        token_set = set(tokens)

        negation = bool(
            token_set & self.lexicons["negation"]
        )

        positive_words = self.lexicons["positive"]
        negative_words = self.lexicons["negative"]

        positive_count = 0
        negative_count = 0

        for index, token in enumerate(tokens):
            if token not in positive_words and token not in negative_words:
                continue

            # Do not invert words that are themselves Tamil
            # negative expressions, such as "பிடிக்கவில்லை".
            is_self_negative = token in negative_words and token in self.scope_negations

            has_nearby_negation = (
                index > 0
                and tokens[index - 1] in self.scope_negations
            )

            if has_nearby_negation and not is_self_negative:
                if token in positive_words:
                    negative_count += 1
                else:
                    positive_count += 1
            else:
                if token in positive_words:
                    positive_count += 1
                if token in negative_words:
                    negative_count += 1

        total_sentiment_words = positive_count + negative_count

        sentiment = 0.0
        if total_sentiment_words:
            sentiment = (
                positive_count - negative_count
            ) / total_sentiment_words

        urgency = bool(
            token_set & self.lexicons["urgency"]
        )

        question = (
            "?" in text
            or any(
                word in normalized
                for word in ("என்ன", "ஏன்", "எப்படி")
            )
        )

        return {
            "question_signal": float(question),
            "negation_signal": float(negation),
            "sentiment_signal": round(sentiment, 4),
            "urgency_signal": float(urgency),
            "token_count": len(tokens),
        }

    def reset(self):
        return True


if __name__ == "__main__":
    engine = BHSemanticFeatureEngine()

    samples = [
        "I am happy",
        "I am not happy",
        "This is bad",
        "This is not bad",
        "எனக்கு இது பிடிக்கவில்லை",
    ]

    for sample in samples:
        print("Text:", sample)
        print("Features:", engine.extract(sample))
