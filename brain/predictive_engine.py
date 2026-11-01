
import re
import hashlib
from copy import deepcopy


class PredictiveEngine:

    def __init__(self, knowledge_engine, max_cache_size=256):
        if not hasattr(knowledge_engine, "search"):
            raise TypeError("Knowledge engine must provide a search method.")

        if (
            not isinstance(max_cache_size, int)
            or isinstance(max_cache_size, bool)
            or max_cache_size < 1
        ):
            raise ValueError("max_cache_size must be a positive integer.")

        self.knowledge = knowledge_engine
        self.max_cache_size = max_cache_size
        self.cache = {}

    def normalize(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string.")

        text = text.casefold().strip()
        text = re.sub(r"\s+", " ", text)
        return text

    def make_key(self, text):
        normalized = self.normalize(text)

        return hashlib.sha256(
            normalized.encode("utf-8")
        ).hexdigest()

    def _store_cache(self, key, candidate):
        if key in self.cache:
            del self.cache[key]

        self.cache[key] = deepcopy(candidate)

        while len(self.cache) > self.max_cache_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]

    def prepare(self, typed_text):
        """
        Prepare a knowledge search candidate while typing.
        This does not generate or verify an AI answer.
        """
        text = self.normalize(typed_text)

        if len(text) < 3:
            return None

        key = self.make_key(text)

        if key in self.cache:
            return deepcopy(self.cache[key])

        results = self.knowledge.search(text)

        candidate = {
            "question": text,
            "results": results,
            "status": "prepared"
        }

        self._store_cache(key, candidate)

        return deepcopy(candidate)

    def get_on_send(self, final_question):
        """
        Reuse a prepared result only when the normalized
        final question exactly matches the cached question.
        """
        text = self.normalize(final_question)

        if not text:
            return None

        key = self.make_key(text)
        candidate = self.cache.get(key)

        if candidate is None:
            return self.prepare(text)

        return deepcopy(candidate)

    def clear_cache(self):
        self.cache.clear()

    def cache_size(self):
        return len(self.cache)


if __name__ == "__main__":
    class DemoKnowledge:
        def search(self, keyword):
            return [{
                "title": "Earth",
                "content": "Earth is the third planet from the Sun."
            }]

    engine = PredictiveEngine(DemoKnowledge())

    print("Prepared:", engine.prepare("What is Earth?"))
    print("On send:", engine.get_on_send("What is Earth?"))
    print("Cache size:", engine.cache_size())

    engine.clear_cache()
    print("Cache cleared:", engine.cache_size() == 0)
    print("BH-OMNI CORE Predictive Engine ready!")
