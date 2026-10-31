import re
import hashlib


class PredictiveEngine:
    def __init__(self, knowledge_engine):
        self.knowledge = knowledge_engine
        self.cache = {}

    def normalize(self, text):
        text = text.lower().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def make_key(self, text):
        normalized = self.normalize(text)
        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

    def prepare(self, typed_text):
        """
        Prepare a search candidate while the user types.
        This does not generate or verify an AI answer.
        """
        text = self.normalize(typed_text)

        if len(text) < 3:
            return None

        key = self.make_key(text)

        if key in self.cache:
            return self.cache[key]

        try:
            results = self.knowledge.search(text)
        except Exception:
            results = []

        candidate = {
            "question": text,
            "results": results,
            "status": "prepared"
        }

        self.cache[key] = candidate
        return candidate

    def get_on_send(self, final_question):
        """
        Reuse a prepared result only when the final
        question exactly matches the cached question.
        """
        text = self.normalize(final_question)

        if not text:
            return None

        key = self.make_key(text)
        candidate = self.cache.get(key)

        if candidate is None:
            candidate = self.prepare(text)

        if candidate is None:
            return None

        return candidate

    def clear_cache(self):
        self.cache.clear()
