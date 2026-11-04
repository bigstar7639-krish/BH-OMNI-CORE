
from typing import Dict, List

class CreatorError(Exception):
    pass

class CreatorHub:
    """
    Phase 3 Step 5 - System J - Creator Hub
    - Register creator: {creator_id, name}
    - Publish: creator publishes content {content_id, title, type}
    - Types: story, voice, theme
    - Follow: user follows creator, unfollow, follower count
    - Duplicate creator/content -> FAIL, self-follow -> FAIL
    - Local simulation - No real social network
    """
    VALID_TYPES = ["story", "voice", "theme"]
    def __init__(self):
        self._creators: Dict[str, dict] = {}
        self._content: Dict[str, dict] = {}
        self._follows: Dict[str, set] = {}  # creator_id -> set of followers

    def register(self, creator_id: str, name: str) -> bool:
        if creator_id is None or not isinstance(creator_id, str) or len(creator_id.strip()) == 0:
            raise CreatorError("creator_id cannot be empty")
        creator_id = creator_id.strip()
        if name is None or not isinstance(name, str) or len(name.strip()) == 0:
            raise CreatorError("name cannot be empty")
        if creator_id in self._creators:
            raise CreatorError(f"Duplicate creator: {creator_id}")
        self._creators[creator_id] = {"creator_id": creator_id, "name": name.strip(), "content_count": 0}
        self._follows[creator_id] = set()
        return True

    def publish(self, creator_id: str, content_id: str, title: str, ctype: str) -> bool:
        if creator_id not in self._creators:
            raise CreatorError(f"Creator not found: {creator_id}")
        if content_id is None or not isinstance(content_id, str) or len(content_id.strip()) == 0:
            raise CreatorError("content_id cannot be empty")
        content_id = content_id.strip()
        if title is None or not isinstance(title, str) or len(title.strip()) == 0:
            raise CreatorError("title cannot be empty")
        if ctype not in self.VALID_TYPES:
            raise CreatorError(f"Invalid type: {ctype} - Must be {self.VALID_TYPES}")
        if content_id in self._content:
            raise CreatorError(f"Duplicate content: {content_id}")
        self._content[content_id] = {"content_id": content_id, "title": title.strip(), "type": ctype, "creator_id": creator_id}
        self._creators[creator_id]["content_count"] += 1
        return True

    def follow(self, creator_id: str, follower_id: str) -> bool:
        if creator_id not in self._creators:
            raise CreatorError(f"Creator not found: {creator_id}")
        if follower_id is None or not isinstance(follower_id, str) or len(follower_id.strip()) == 0:
            raise CreatorError("follower_id cannot be empty")
        follower_id = follower_id.strip()
        if follower_id == creator_id:
            raise CreatorError("Cannot follow yourself")
        if follower_id in self._follows[creator_id]:
            raise CreatorError(f"Already following: {creator_id}")
        self._follows[creator_id].add(follower_id)
        return True

    def unfollow(self, creator_id: str, follower_id: str) -> bool:
        if creator_id not in self._creators:
            raise CreatorError(f"Creator not found: {creator_id}")
        if follower_id not in self._follows[creator_id]:
            raise CreatorError(f"Not following: {creator_id}")
        self._follows[creator_id].remove(follower_id)
        return True

    def follower_count(self, creator_id: str) -> int:
        if creator_id not in self._creators:
            raise CreatorError(f"Creator not found: {creator_id}")
        return len(self._follows[creator_id])

    def get_creator(self, creator_id: str) -> dict:
        if creator_id not in self._creators:
            raise CreatorError(f"Creator not found: {creator_id}")
        c = self._creators[creator_id]
        return {"creator_id": c["creator_id"], "name": c["name"], "content_count": c["content_count"], "followers": len(self._follows[creator_id])}

    def get_info(self) -> dict:
        return {"creators": len(self._creators), "content": len(self._content), "principle": "Local simulation - No real social network"}
