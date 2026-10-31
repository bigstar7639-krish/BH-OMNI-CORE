
import json
from pathlib import Path
from datetime import datetime, timezone


class BHMemory:
    def __init__(self, file_path="database/memories.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.memories = json.load(file)
        else:
            self.memories = []

    def remember(self, text, category="general"):
        memory = {
            "id": len(self.memories) + 1,
            "text": text,
            "category": category,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.memories.append(memory)
        self._save()

        return memory

    def recall(self, keyword=None, category=None):
        results = []

        for memory in self.memories:
            if category and memory["category"] != category:
                continue

            if keyword:
                if keyword.lower() not in memory["text"].lower():
                    continue

            results.append(memory)

        return results

    def forget(self, memory_id):
        old_count = len(self.memories)

        self.memories = [
            memory for memory in self.memories
            if memory["id"] != memory_id
        ]

        if len(self.memories) != old_count:
            self._save()
            return True

        return False

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
        "project"
    )

    print("Saved memories:")
    print(brain.recall())
