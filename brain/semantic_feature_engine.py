
"""BH-OMNI CORE: Rule-based multilingual semantic signal extractor.

Experimental prototype. This is not a trained language model.
"""

import unicodedata
import re


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

    @staticmethod
    def _split_sentences(text):
        # Preserve sentence boundaries before tokenization.
        return [
            part.strip()
            for part in re.split(r"[.!?।\n]+", text)
            if part.strip()
        ]

    def extract(self, text):
        self._validate(text)
        normalized = self._normalize(text)

        sentences = self._split_sentences(normalized)
        all_tokens = []

        positive_count = 0
        negative_count = 0

        positive_words = self.lexicons["positive"]
        negative_words = self.lexicons["negative"]

        for sentence in sentences:
            tokens = self._tokenize(sentence)
            all_tokens.extend(tokens)

            for index, token in enumerate(tokens):
                is_positive = token in positive_words
                is_negative = token in negative_words

                if not is_positive and not is_negative:
                    continue

                is_self_negative = (
                    is_negative
                    and token in self.lexicons["negation"]
                )

                has_nearby_negation = (
                    index > 0
                    and tokens[index - 1] in self.scope_negations
                )

                if has_nearby_negation and not is_self_negative:
                    if is_positive:
                        negative_count += 1
                    else:
                        positive_count += 1
                else:
                    if is_positive:
                        positive_count += 1
                    if is_negative:
                        negative_count += 1

        token_set = set(all_tokens)

        negation = bool(
            token_set & self.lexicons["negation"]
        )

        urgency = bool(
            token_set & self.lexicons["urgency"]
        )

        total_sentiment = positive_count + negative_count

        sentiment = 0.0
        if total_sentiment:
            sentiment = (
                positive_count - negative_count
            ) / total_sentiment

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
            "token_count": len(all_tokens),
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
        "I am not happy. I am good",
        "Not bad. Great",
        "எனக்கு இது பிடிக்கவில்லை",
    ]

    for sample in samples:
        print("Text:", sample)
        print("Features:", engine.extract(sample))
