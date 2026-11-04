
from typing import List, Dict, Optional

class StoryError(Exception):
    pass

class StoryEngine:
    """
    Phase 3 Step 1 - System F - Story Engine
    - Create story: title, genre, language
    - Genres: fantasy, thriller, romance, comedy, horror, devotional
    - Add chapters, get story, list stories
    - Duplicate title -> FAIL
    - This is structure engine - NOT LLM story generation
    """
    VALID_GENRES = ["fantasy", "thriller", "romance", "comedy", "horror", "devotional", "sci-fi", "drama"]
    def __init__(self):
        self._stories: Dict[str, dict] = {}

    def _validate_title(self, title):
        if title is None or not isinstance(title, str) or len(title.strip()) == 0:
            raise StoryError("Title cannot be empty")
        if len(title) > 200:
            raise StoryError("Title too long")
        return title.strip()

    def create(self, title: str, genre: str, language: str = "tanglish") -> bool:
        title = self._validate_title(title)
        if genre not in self.VALID_GENRES:
            raise StoryError(f"Invalid genre: {genre} - Must be {self.VALID_GENRES}")
        if language not in ("tanglish", "tamil", "english", "hindi"):
            raise StoryError("Language must be tanglish/tamil/english/hindi")
        if title in self._stories:
            raise StoryError(f"Duplicate story: {title}")
        self._stories[title] = {"title": title, "genre": genre, "language": language, "chapters": []}
        return True

    def add_chapter(self, title: str, chapter_title: str, content: str) -> bool:
        title = self._validate_title(title)
        if title not in self._stories:
            raise StoryError(f"Story not found: {title}")
        if chapter_title is None or not isinstance(chapter_title, str) or len(chapter_title.strip()) == 0:
            raise StoryError("Chapter title cannot be empty")
        if content is None or not isinstance(content, str) or len(content.strip()) == 0:
            raise StoryError("Chapter content cannot be empty")
        if len(content) > 20000:
            raise StoryError("Chapter too long - Max 20000 chars")
        self._stories[title]["chapters"].append({"title": chapter_title.strip(), "content": content, "chars": len(content)})
        return True

    def get_story(self, title: str) -> dict:
        title = self._validate_title(title)
        if title not in self._stories:
            raise StoryError(f"Story not found: {title}")
        s = self._stories[title]
        return {"title": s["title"], "genre": s["genre"], "language": s["language"], "chapters": len(s["chapters"]), "total_chars": sum(c["chars"] for c in s["chapters"]), "chapter_titles": [c["title"] for c in s["chapters"]]}

    def list_stories(self) -> List[str]:
        return sorted(list(self._stories.keys()))

    def get_info(self) -> dict:
        return {"stories": len(self._stories), "genres": len(self.VALID_GENRES), "principle": "Structure only - No LLM generation claim"}
