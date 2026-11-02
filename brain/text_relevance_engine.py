
"""BH-OMNI CORE: Unicode-aware text relevance engine."""

import math
import unicodedata
from collections import Counter


class BHTextRelevanceEngine:
    """Ranks text candidates using Unicode-aware lexical similarity."""

    def tokenize(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        normalized = unicodedata.normalize("NFKC", text).casefold()

        tokens = []
        current = []

        for char in normalized:
            category = unicodedata.category(char)

            # Letters, numbers and combining marks are retained.
            if category.startswith("L") or category.startswith("N"):
                current.append(char)

            elif category.startswith("M") and current:
                current.append(char)

            else:
                if current:
                    tokens.append("".join(current))
                    current = []

        if current:
            tokens.append("".join(current))

        return tokens

    @staticmethod
    def _cosine_similarity(first, second):
        common = set(first) & set(second)

        dot = sum(first[key] * second[key] for key in common)

        norm_first = math.sqrt(
            sum(value * value for value in first.values())
        )
        norm_second = math.sqrt(
            sum(value * value for value in second.values())
        )

        if norm_first == 0 or norm_second == 0:
            return 0.0

        return dot / (norm_first * norm_second)

    @staticmethod
    def _jaccard_similarity(first, second):
        set_first = set(first)
        set_second = set(second)
        union = set_first | set_second

        if not union:
            return 0.0

        return len(set_first & set_second) / len(union)

    def score(self, query, candidate):
        query_tokens = self.tokenize(query)
        candidate_tokens = self.tokenize(candidate)

        if not query_tokens or not candidate_tokens:
            return 0.0

        query_counts = Counter(query_tokens)
        candidate_counts = Counter(candidate_tokens)

        cosine = self._cosine_similarity(
            query_counts,
            candidate_counts
        )

        jaccard = self._jaccard_similarity(
            query_tokens,
            candidate_tokens
        )

        result = (0.7 * cosine) + (0.3 * jaccard)

        return round(max(0.0, min(result, 1.0)), 6)

    def rank(self, query, candidates, limit=None):
        if not isinstance(candidates, (list, tuple)):
            raise TypeError("Candidates must be a list or tuple.")

        if limit is not None:
            if isinstance(limit, bool) or not isinstance(limit, int):
                raise TypeError("limit must be an integer.")
            if limit < 0:
                raise ValueError("limit cannot be negative.")

        results = []

        for index, candidate in enumerate(candidates):
            if not isinstance(candidate, str):
                raise TypeError("Every candidate must be a string.")

            results.append({
                "text": candidate,
                "score": self.score(query, candidate),
                "index": index
            })

        results.sort(
            key=lambda item: (-item["score"], item["index"])
        )

        if limit is not None:
            results = results[:limit]

        return results
