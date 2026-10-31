
import json
from pathlib import Path
from datetime import datetime, timezone


class BHKnowledge:
    def __init__(self, file_path="database/knowledge.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = json.load(file)
        else:
            self.data = []

    def add(self, title, content, category="general", source="user"):
        entry = {
            "id": len(self.data) + 1,
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
        keyword = keyword.lower()

        return [
            entry for entry in self.data
            if keyword in entry["title"].lower()
            or keyword in entry["content"].lower()
            or keyword in entry["category"].lower()
        ]

    def get_all(self):
        return self.data

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    brain = BHKnowledge()

    brain.add(
        "Earth",
        "Earth is the third planet from the Sun.",
        "science",
        "starter"
    )

    print(brain.search("Earth"))
    print("BH Knowledge Engine ready!")
