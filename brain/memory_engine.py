import json
import re
from copy import deepcopy
from pathlib import Path
from datetime import datetime, timezone


class BHMemory:

    VALID_MEMORY_TYPES = ("short_term", "long_term")

    def __init__(self, file_path="database/memories.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.memories = []
        self.load()

    def _now(self):
        return datetime.now(timezone.utc).isoformat()

    def load(self):
        if not self.file_path.exists():
            self.memories = []
            return True

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Memory database contains invalid JSON: {error}"
            ) from error

        except OSError as error:
            raise OSError(
                f"Could not read memory database: {error}"
            ) from error

        if not isinstance(data, list):
            raise ValueError("Memory database must contain a JSON list.")

        validated = []

        for item in data:
            if not isinstance(item, dict):
                continue

            if "id" not in item or "text" not in item:
                continue

            if not isinstance(item["text"], str):
                continue

            validated.append(item)

        self.memories = validated
        return True

    def _save(self):
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.memories,
                    file,
                    ensure_ascii=False,
                    indent=2
                )

            temp_path.replace(self.file_path)

        except OSError:
            if temp_path.exists():
                temp_path.unlink()
            raise

        return True

    def _next_id(self):
        valid_ids = [
            item["id"]
            for item in self.memories
            if isinstance(item.get("id"), int)
            and not isinstance(item.get("id"), bool)
        ]

        return max(valid_ids, default=0) + 1

    @staticmethod
    def _validate_memory_type(memory_type):
        if memory_type not in BHMemory.VALID_MEMORY_TYPES:
            raise ValueError("Invalid memory type")

    @staticmethod
    def _validate_importance(importance):
        importance = int(importance)
        return max(1, min(10, importance))

    def remember(
        self,
        text,
        category="general",
        memory_type="long_term",
        importance=5
    ):
        if not isinstance(text, str):
            raise TypeError("Memory text must be a string.")

        text = text.strip()

        if not text:
            return None

        self._validate_memory_type(memory_type)
        importance = self._validate_importance(importance)

        for memory in self.memories:
            if (
                memory.get("text", "").casefold() == text.casefold()
                and memory.get("category") == category
                and memory.get("memory_type") == memory_type
            ):
                memory["importance"] = max(
                    memory.get("importance", 5),
                    importance
                )

                memory["last_accessed"] = self._now()
                memory["access_count"] = (
                    memory.get("access_count", 0) + 1
                )

                self._save()
                return deepcopy(memory)

        memory = {
            "id": self._next_id(),
            "text": text,
            "category": category,
            "memory_type": memory_type,
            "importance": importance,
            "access_count": 0,
            "created_at": self._now(),
            "updated_at": None,
            "last_accessed": None
        }

        self.memories.append(memory)
        self._save()

        return deepcopy(memory)

    def recall(
        self,
        keyword=None,
        category=None,
        memory_type=None,
        min_importance=None,
        limit=None
    ):
        if memory_type is not None:
            self._validate_memory_type(memory_type)

        if min_importance is not None:
            min_importance = int(min_importance)

        if limit is not None:
            limit = max(0, int(limit))

        query_words = (
            set(re.findall(r"\w+", str(keyword).casefold()))
            if keyword else set()
        )

        results = []

        for memory in self.memories:

            if category is not None:
                if memory.get("category") != category:
                    continue

            if memory_type is not None:
                if memory.get("memory_type") != memory_type:
                    continue

            importance = memory.get("importance", 5)

            if min_importance is not None:
                if importance < min_importance:
                    continue

            if query_words:
                text_words = set(
                    re.findall(
                        r"\w+",
                        memory.get("text", "").casefold()
                    )
                )

                if not query_words.intersection(text_words):
                    continue

            results.append(memory)

        results.sort(
            key=lambda item: (
                item.get("importance", 5),
                item.get("created_at", "")
            ),
            reverse=True
        )

        if limit is not None:
            results = results[:limit]

        for memory in results:
            memory["access_count"] = (
                memory.get("access_count", 0) + 1
            )
            memory["last_accessed"] = self._now()

        if results:
            self._save()

        return deepcopy(results)

    def update(
        self,
        memory_id,
        text=None,
        category=None,
        memory_type=None,
        importance=None
    ):
        for memory in self.memories:

            if memory.get("id") != memory_id:
                continue

            if text is not None:
                if not isinstance(text, str):
                    raise TypeError("Memory text must be a string.")

                if not text.strip():
                    return None

                memory["text"] = text.strip()

            if category is not None:
                memory["category"] = category

            if memory_type is not None:
                self._validate_memory_type(memory_type)
                memory["memory_type"] = memory_type

            if importance is not None:
                memory["importance"] = (
                    self._validate_importance(importance)
                )

            memory["updated_at"] = self._now()
            self._save()

            return deepcopy(memory)

        return None

    def forget(self, memory_id):
        old_count = len(self.memories)

        self.memories = [
            memory
            for memory in self.memories
            if memory.get("id") != memory_id
        ]

        if len(self.memories) == old_count:
            return False

        self._save()
        return True

    def clear_short_term(self):
        old_count = len(self.memories)

        self.memories = [
            memory
            for memory in self.memories
            if memory.get("memory_type", "long_term") != "short_term"
        ]

        removed = old_count - len(self.memories)

        if removed:
            self._save()

        return removed

    def count(self, memory_type=None):
        if memory_type is None:
            return len(self.memories)

        self._validate_memory_type(memory_type)

        return sum(
            1
            for memory in self.memories
            if memory.get("memory_type") == memory_type
        )

    def get_all(self):
        return deepcopy(self.memories)

    def save(self):
        return self._save()


if __name__ == "__main__":

    brain = BHMemory()

    brain.remember(
        "BH-OMNI CORE is my own AI project",
        "project",
        "long_term",
        importance=10
    )

    brain.remember(
        "User is currently testing the brain",
        "session",
        "short_term",
        importance=5
    )

    print("All memories:", brain.get_all())
    print("Long-term:", brain.recall(memory_type="long_term"))
    print("Total memories:", brain.count())
