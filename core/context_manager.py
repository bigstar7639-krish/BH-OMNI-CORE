
from typing import List, Dict, Optional

class ContextError(Exception):
    pass

class ContextManager:
    """
    Phase 2 Step 4 - Context Manager
    - Messages: {role user/assistant/system, content}
    - Max tokens: estimate = len(content)//4 + 1 per message (approx, not exact tokenizer)
    - Trim: remove oldest user/assistant messages first, keep system messages
    - Clear, get_context, count
    - Invalid role/content -> FAIL
    """
    def __init__(self, max_tokens: int = 4000):
        if max_tokens is None or not isinstance(max_tokens, int) or max_tokens < 100 or max_tokens > 100000:
            raise ContextError("max_tokens must be 100-100000")
        self.max_tokens = max_tokens
        self._messages: List[dict] = []

    def _validate_role(self, role):
        if role not in ("user", "assistant", "system"):
            raise ContextError(f"Invalid role: {role} - Must be user/assistant/system")
        return role

    def _estimate_tokens(self, content: str) -> int:
        return max(1, len(content) // 4 + 1)

    def add(self, role: str, content: str) -> bool:
        role = self._validate_role(role)
        if content is None or not isinstance(content, str) or len(content.strip()) == 0:
            raise ContextError("Content cannot be empty")
        if len(content) > 50000:
            raise ContextError("Content too long - Max 50000 chars")
        self._messages.append({"role": role, "content": content, "tokens": self._estimate_tokens(content)})
        # Auto-trim if over limit
        self.trim()
        return True

    def total_tokens(self) -> int:
        return sum(m["tokens"] for m in self._messages)

    def trim(self) -> int:
        # Remove oldest non-system messages until under limit
        removed = 0
        while self.total_tokens() > self.max_tokens and len(self._messages) > 0:
            # Find first non-system index
            idx = None
            for i, m in enumerate(self._messages):
                if m["role"] != "system":
                    idx = i
                    break
            if idx is None:
                # Only system messages left - cannot trim further, break
                break
            self._messages.pop(idx)
            removed += 1
        return removed

    def get_context(self) -> List[dict]:
        return [{"role": m["role"], "content": m["content"]} for m in self._messages]

    def clear(self) -> bool:
        self._messages = []
        return True

    def count(self) -> int:
        return len(self._messages)

    def get_info(self) -> dict:
        return {"messages": len(self._messages), "tokens": self.total_tokens(), "max_tokens": self.max_tokens, "principle": "Keep system + Trim oldest first"}
