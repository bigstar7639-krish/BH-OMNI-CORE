
import json
import re
from pathlib import Path
from datetime import datetime, timezone


class BHKnowledge:
    def __init__(self, file_path="database/knowledge.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    self.data = json.load(file)
            except (json.JSONDecodeError, OSError):
                self.data = []
        else:
            self.data = []

    def add(self, title, content, category="general", source="user"):
        entry = {
            "id": max(
                (item.get("id", 0) for item in self.data),
                default=0
            ) + 1,
            "title": title,
            "content": content,
            "category": category,
            "source": source,
            "created_at": datetime.now(timezone.utc).isoformat()
        }

        self.data.append(entry)
        self.save()
        return entry

    def search(self, keyword):
        words = set(re.findall(r"\w+", keyword.lower()))

        if not words:
            return []

        results = []

        for entry in self.data:
            searchable = " ".join([
                str(entry.get("title", "")),
                str(entry.get("content", "")),
                str(entry.get("category", ""))
            ]).lower()

            searchable_words = set(re.findall(r"\w+", searchable))
            score = len(words & searchable_words)

            if score > 0:
                results.append((score, entry))

        results.sort(key=lambda item: item[0], reverse=True)

        return [entry for score, entry in results]

    def get_all(self):
        return self.data

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2
            )


if __name__ == "__main__":
    brain = BHKnowledge()

    brain.add(
        "Earth",
        "Earth is the third planet from the Sun.",
        "science",
        "starter"
    )

    print(brain.search("what is Earth"))
    print("BH Knowledge Engine ready!")
