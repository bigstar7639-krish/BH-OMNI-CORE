
import json
import re
from pathlib import Path
from datetime import datetime, timezone


class BHMemory:

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
            return

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.memories = data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            self.memories = []

    def _save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(
                self.memories,
                file,
                ensure_ascii=False,
                indent=2
            )

        temp_path.replace(self.file_path)

    def _next_id(self):
        return max(
            (
                item.get("id", 0)
                for item in self.memories
                if isinstance(item.get("id", 0), int)
            ),
            default=0
        ) + 1

    def remember(
        self,
        text,
        category="general",
        memory_type="long_term",
        importance=5
    ):
        text = str(text).strip()

        if not text:
            return None

        if memory_type not in ("short_term", "long_term"):
            raise ValueError("Invalid memory type")

        importance = max(1, min(10, int(importance)))

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
                return memory

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

        return memory

    def recall(
        self,
        keyword=None,
        category=None,
        memory_type=None,
        min_importance=None,
        limit=None
    ):
        results = []

        query_words = (
            set(re.findall(r"\w+", str(keyword).casefold()))
            if keyword else set()
        )

        for memory in self.memories:

            if category and memory.get("category") != category:
                continue

            if memory_type and memory.get(
                "memory_type", "long_term"
            ) != memory_type:
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
            results = results[:max(0, int(limit))]

        for memory in results:
            memory["access_count"] = (
                memory.get("access_count", 0) + 1
            )
            memory["last_accessed"] = self._now()

        if results:
            self._save()

        return results

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
                if not str(text).strip():
                    return None

                memory["text"] = str(text).strip()

            if category is not None:
                memory["category"] = category

            if memory_type is not None:
                if memory_type not in ("short_term", "long_term"):
                    raise ValueError("Invalid memory type")

                memory["memory_type"] = memory_type

            if importance is not None:
                memory["importance"] = max(
                    1, min(10, int(importance))
                )

            memory["updated_at"] = self._now()
            self._save()

            return memory

        return None

    def forget(self, memory_id):
        old_count = len(self.memories)

        self.memories = [
            memory for memory in self.memories
            if memory.get("id") != memory_id
        ]

        if len(self.memories) == old_count:
            return False

        self._save()
        return True

    def clear_short_term(self):
        old_count = len(self.memories)

        self.memories = [
            memory for memory in self.memories
            if memory.get("memory_type", "long_term") != "short_term"
        ]

        removed = old_count - len(self.memories)

        if removed:
            self._save()

        return removed

    def count(self, memory_type=None):
        if memory_type is None:
            return len(self.memories)

        return sum(
            1 for memory in self.memories
            if memory.get("memory_type") == memory_type
        )

    def get_all(self):
        return list(self.memories)

    def save(self):
        self._save()


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
