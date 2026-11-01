
import json
import re
from copy import deepcopy
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

        except json.JSONDecodeError as error:
            raise ValueError(
                f"Knowledge database contains invalid JSON: {self.file_path}"
            ) from error

        except OSError as error:
            raise OSError(
                f"Unable to read knowledge database: {self.file_path}"
            ) from error

        if not isinstance(data, list):
            raise ValueError("Knowledge database must contain a JSON list.")

        valid_entries = []

        for entry in data:
            if not isinstance(entry, dict):
                continue

            if (
                not isinstance(entry.get("id"), int)
                or isinstance(entry.get("id"), bool)
                or not isinstance(entry.get("title"), str)
                or not isinstance(entry.get("content"), str)
            ):
                continue

            valid_entries.append(entry)

        return valid_entries

    def _save(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        temp_path = self.file_path.with_suffix(
            self.file_path.suffix + ".tmp"
        )

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(
                    self.data,
                    file,
                    ensure_ascii=False,
                    indent=2
                )
                file.flush()

            temp_path.replace(self.file_path)

        except OSError:
            try:
                if temp_path.exists():
                    temp_path.unlink()
            except OSError:
                pass

            raise

        return True

    @staticmethod
    def _validate_text(value, field_name):
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")

        value = value.strip()

        if not value:
            raise ValueError(f"{field_name} cannot be empty.")

        return value

    @staticmethod
    def _validate_id(knowledge_id):
        if not isinstance(knowledge_id, int) or isinstance(
            knowledge_id, bool
        ):
            raise TypeError("Knowledge ID must be an integer.")

    @staticmethod
    def _validate_limit(limit):
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise TypeError("Limit must be an integer.")

        if limit < 0:
            raise ValueError("Limit cannot be negative.")

    @staticmethod
    def _words(text):
        if not isinstance(text, str):
            return set()

        return set(re.findall(r"\w+", text.lower()))

    def _next_id(self):
        valid_ids = [
            entry["id"]
            for entry in self.data
            if isinstance(entry.get("id"), int)
            and not isinstance(entry.get("id"), bool)
        ]

        return max(valid_ids, default=0) + 1

    def add(self, title, content, category="general", source="user"):
        title = self._validate_text(title, "Title")
        content = self._validate_text(content, "Content")

        category = self._validate_text(category, "Category")
        source = self._validate_text(source, "Source")

        for entry in self.data:
            if (
                entry.get("title", "").casefold() == title.casefold()
                and entry.get("content", "").casefold()
                == content.casefold()
            ):
                return deepcopy(entry)

        entry = {
            "id": self._next_id(),
            "title": title,
            "content": content,
            "category": category,
            "source": source,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": None
        }

        self.data.append(entry)
        self._save()

        return deepcopy(entry)

    def search(self, keyword, category=None, limit=10):
        if not isinstance(keyword, str):
            raise TypeError("Keyword must be a string.")

        self._validate_limit(limit)

        if category is not None:
            category = self._validate_text(category, "Category")

        query_words = self._words(keyword)

        if not query_words or limit == 0:
            return []

        results = []

        for entry in self.data:
            if category is not None:
                if entry.get("category") != category:
                    continue

            title_words = self._words(entry.get("title", ""))
            content_words = self._words(entry.get("content", ""))
            category_words = self._words(entry.get("category", ""))

            title_score = len(query_words & title_words) * 3
            content_score = len(query_words & content_words)
            category_score = len(query_words & category_words)

            score = title_score + content_score + category_score

            if keyword.strip().casefold() == entry.get(
                "title", ""
            ).casefold():
                score += 10

            if score > 0:
                results.append((score, entry))

        results.sort(
            key=lambda item: item[0],
            reverse=True
        )

        return [
            deepcopy(entry)
            for score, entry in results[:limit]
        ]

    def update(
        self,
        knowledge_id,
        title=None,
        content=None,
        category=None,
        source=None
    ):
        self._validate_id(knowledge_id)

        for entry in self.data:
            if entry.get("id") != knowledge_id:
                continue

            if title is not None:
                entry["title"] = self._validate_text(title, "Title")

            if content is not None:
                entry["content"] = self._validate_text(content, "Content")

            if category is not None:
                entry["category"] = self._validate_text(
                    category, "Category"
                )

            if source is not None:
                entry["source"] = self._validate_text(source, "Source")

            entry["updated_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            self._save()
            return deepcopy(entry)

        return None

    def delete(self, knowledge_id):
        self._validate_id(knowledge_id)

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
        self._validate_id(knowledge_id)

        for entry in self.data:
            if entry.get("id") == knowledge_id:
                return deepcopy(entry)

        return None

    def get_all(self, category=None):
        if category is None:
            return deepcopy(self.data)

        category = self._validate_text(category, "Category")

        return [
            deepcopy(entry)
            for entry in self.data
            if entry.get("category") == category
        ]

    def count(self):
        return len(self.data)

    def save(self):
        return self._save()


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
