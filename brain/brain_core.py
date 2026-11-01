
from pathlib import Path
import hashlib

from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.memory_engine import BHMemory


class BlackHoleBrain:

    def __init__(self, knowledge_engine):
        # Shared knowledge for all users
        self.knowledge_engine = knowledge_engine

        # Shared specialist network registry
        self.network_manager = BHNetworkManager()

        # Predictive search cache
        self.predictive_engine = PredictiveEngine(
            knowledge_engine
        )

        # Separate memory instance for each user
        self.user_memories = {}

        self.is_ready = True

    def _get_user_memory(self, user_id):
        if not user_id:
            raise ValueError("A valid user_id is required.")

        user_id = str(user_id).strip()

        if not user_id:
            raise ValueError("A valid user_id is required.")

        if user_id not in self.user_memories:
            safe_id = hashlib.sha256(
                user_id.encode("utf-8")
            ).hexdigest()

            memory_path = (
                Path("database")
                / "users"
                / f"{safe_id}.json"
            )

            self.user_memories[user_id] = BHMemory(
                file_path=memory_path
            )

        return self.user_memories[user_id]

    def think_ahead(self, typed_text):
        if not typed_text:
            return None

        return self.predictive_engine.prepare(
            typed_text
        )

    def remember_for_user(
        self, user_id, text, category="general"
    ):
        memory = self._get_user_memory(user_id)

        return memory.remember(
            text,
            category,
            "long_term"
        )

    def recall_for_user(
        self, user_id, keyword=None, category=None
    ):
        memory = self._get_user_memory(user_id)

        return memory.recall(
            keyword=keyword,
            category=category
        )

    def answer_request(self, user_id, question):
        if not question or not question.strip():
            return {
                "status": "error",
                "message": "Question is empty."
            }

        result = self.predictive_engine.get_on_send(
            question
        )

        user_memory = self._get_user_memory(user_id)

        return {
            "status": "retrieved",
            "question": question,
            "knowledge_results": (
                result["results"] if result else []
            ),
            "relevant_user_memories": user_memory.recall(
                keyword=question
            )
        }

    def clear_prediction_cache(self):
        self.predictive_engine.clear_cache()
