
import json
from pathlib import Path
from datetime import datetime, timezone


class BHMemory:
    def __init__(self, file_path="database/memories.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        self.memories = []
        self.load()

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

    def remember(self, text, category="general", memory_type="long_term"):
        text = str(text).strip()

        if not text:
            return None

        memory = {
            "id": max(
                (item.get("id", 0) for item in self.memories),
                default=0
            ) + 1,
            "text": text,
            "category": category,
            "memory_type": memory_type,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.memories.append(memory)
        self._save()

        return memory

    def recall(self, keyword=None, category=None, memory_type=None):
        results = []

        for memory in self.memories:
            if category and memory.get("category") != category:
                continue

            if memory_type and memory.get("memory_type", "long_term") != memory_type:
                continue

            if keyword:
                if keyword.lower() not in memory.get("text", "").lower():
                    continue

            results.append(memory)

        return results

    def forget(self, memory_id):
        old_count = len(self.memories)

        self.memories = [
            memory for memory in self.memories
            if memory.get("id") != memory_id
        ]

        if len(self.memories) != old_count:
            self._save()
            return True

        return False

    def clear_short_term(self):
        old_count = len(self.memories)

        self.memories = [
            memory for memory in self.memories
            if memory.get("memory_type", "long_term") != "short_term"
        ]

        if len(self.memories) != old_count:
            self._save()

    def _save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.memories,
                file,
                ensure_ascii=False,
                indent=2
            )


if __name__ == "__main__":
    brain = BHMemory()

    brain.remember(
        "BH-OMNI CORE is my own AI project",
        "project",
        "long_term"
    )

    brain.remember(
        "User is currently testing the brain",
        "session",
        "short_term"
    )

    print("All memories:")
    print(brain.recall())
