
import json
import re
from pathlib import Path
from datetime import datetime, timezone


class BHKnowledge:

    def __init__(self, file_path="database/knowledge.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()

    def _load(self):
        if not self.file_path.exists():
            return []

        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (json.JSONDecodeError, OSError):
            return []

    def _save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                ensure_ascii=False,
                indent=2
            )

        temp_path.replace(self.file_path)

    def _words(self, text):
        return set(re.findall(r"\w+", str(text).lower()))

    def add(self, title, content, category="general", source="user"):
        title = str(title).strip()
        content = str(content).strip()

        if not title or not content:
            raise ValueError("Title and content cannot be empty.")

        # Duplicate detection
        for entry in self.data:
            if (
                entry.get("title", "").lower() == title.lower()
                and entry.get("content", "").lower() == content.lower()
            ):
                return entry

        new_id = max(
            (item.get("id", 0) for item in self.data),
            default=0
        ) + 1

        entry = {
            "id": new_id,
            "title": title,
            "content": content,
            "category": category,
            "source": source,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": None
        }

        self.data.append(entry)
        self._save()

        return entry

    def search(self, keyword, category=None, limit=10):
        query_words = self._words(keyword)

        if not query_words:
            return []

        results = []

        for entry in self.data:

            if category and entry.get("category") != category:
                continue

            title_words = self._words(entry.get("title", ""))
            content_words = self._words(entry.get("content", ""))
            category_words = self._words(entry.get("category", ""))

            title_score = len(query_words & title_words) * 3
            content_score = len(query_words & content_words)
            category_score = len(query_words & category_words)

            score = title_score + content_score + category_score

            if str(keyword).strip().lower() == entry.get(
                "title", ""
            ).lower():
                score += 10

            if score > 0:
                results.append((score, entry))

        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            entry for score, entry in results[:max(0, limit)]
        ]

    def update(self, knowledge_id, title=None, content=None,
               category=None, source=None):

        for entry in self.data:
            if entry.get("id") == knowledge_id:

                if title is not None:
                    entry["title"] = str(title).strip()

                if content is not None:
                    entry["content"] = str(content).strip()

                if category is not None:
                    entry["category"] = category

                if source is not None:
                    entry["source"] = source

                entry["updated_at"] = datetime.now(
                    timezone.utc
                ).isoformat()

                self._save()
                return entry

        return None

    def delete(self, knowledge_id):
        original_count = len(self.data)

        self.data = [
            entry for entry in self.data
            if entry.get("id") != knowledge_id
        ]

        if len(self.data) == original_count:
            return False

        self._save()
        return True

    def get(self, knowledge_id):
        for entry in self.data:
            if entry.get("id") == knowledge_id:
                return entry

        return None

    def get_all(self, category=None):
        if category is None:
            return list(self.data)

        return [
            entry for entry in self.data
            if entry.get("category") == category
        ]

    def count(self):
        return len(self.data)

    def save(self):
        self._save()


if __name__ == "__main__":
    brain = BHKnowledge()

    brain.add(
        "Earth",
        "Earth is the third planet from the Sun.",
        "science",
        "starter"
    )

    print("Search:", brain.search("what is Earth"))
    print("Knowledge count:", brain.count())
    print("BH-OMNI CORE Knowledge Engine ready!")
