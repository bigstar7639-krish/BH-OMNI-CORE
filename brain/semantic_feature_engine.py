
"""BH-OMNI CORE: Initial multilingual semantic signal extractor.

This is a rule-based prototype, not a trained language model.
"""

import unicodedata


class BHSemanticFeatureEngine:
    """Extract basic interpretable language signals."""

    LEXICONS = {
        "negation": {
            "not", "no", "never", "don't", "cannot",
            "இல்லை", "வேண்டாம்", "முடியாது"
        },
        "positive": {
            "good", "great", "happy", "love", "excellent",
            "நல்ல", "நன்று", "மகிழ்ச்சி", "பிடிக்கும்"
        },
        "negative": {
            "bad", "sad", "hate", "angry", "terrible",
            "கெட்ட", "சோகம்", "பிடிக்கவில்லை", "கோபம்"
        },
        "urgency": {
            "urgent", "emergency", "immediately", "asap",
            "அவசரம்", "உடனே"
        },
    }

    def __init__(self):
        self.lexicons = {
            name: {
                unicodedata.normalize("NFC", word).casefold()
                for word in words
            }
            for name, words in self.LEXICONS.items()
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
        positive_count = len(
            token_set & self.lexicons["positive"]
        )
        negative_count = len(
            token_set & self.lexicons["negative"]
        )
        urgency = bool(
            token_set & self.lexicons["urgency"]
        )

        sentiment = 0.0

        if positive_count + negative_count:
            sentiment = (
                positive_count - negative_count
            ) / (positive_count + negative_count)

        return {
            "question_signal": float(
                "?" in text or "?" in normalized
                or "என்ன" in normalized
                or "ஏன்" in normalized
                or "எப்படி" in normalized
            ),
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
        "I do not like this",
        "This is urgent",
        "தமிழ் மொழி அழகானது",
        "எனக்கு இது பிடிக்கவில்லை"
    ]

    for sample in samples:
        print(sample)
        print(engine.extract(sample))
