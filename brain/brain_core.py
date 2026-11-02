
from pathlib import Path
import hashlib
import math
import re

from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.memory_engine import BHMemory
from brain.text_network import BHTextNetwork
from brain.multilingual_pipeline import BHMultilingualPipeline


class BlackHoleBrain:

    _STOP_WORDS = {
        "a", "an", "the", "is", "am", "are", "was", "were",
        "be", "been", "being", "what", "which", "who", "whom",
        "whose", "when", "where", "why", "how", "do", "does",
        "did", "can", "could", "would", "should", "will",
        "shall", "may", "might", "must", "have", "has", "had",
        "having", "to", "of", "in", "on", "at", "by", "for",
        "from", "with", "about", "into", "onto", "over", "under",
        "and", "or", "but", "if", "then", "than", "that",
        "this", "these", "those", "it", "its", "i", "you",
        "he", "she", "we", "they", "me", "my", "your", "his",
        "her", "our", "their", "tell", "explain", "describe",
        "please"
    }

    def __init__(
        self,
        knowledge_engine,
        user_memory_dir="database/users"
    ):
        if knowledge_engine is None:
            raise ValueError("A knowledge_engine is required.")

        self.knowledge_engine = knowledge_engine
        self.user_memory_dir = Path(user_memory_dir)

        self.network_manager = BHNetworkManager()
        self.predictive_engine = PredictiveEngine(
            knowledge_engine
        )

        self.text_network = BHTextNetwork()
        self.multilingual_pipeline = BHMultilingualPipeline()

        self.network_manager.register(
            name="text",
            network=self.text_network.network,
            description="Text processing neural network",
            priority=10
        )

        self.user_memories = {}
        self.is_ready = True

    # User memory management
    def _get_user_memory(self, user_id):
        if user_id is None:
            raise ValueError("A valid user_id is required.")

        user_id = str(user_id).strip()

        if not user_id:
            raise ValueError("A valid user_id is required.")

        if user_id not in self.user_memories:
            safe_id = hashlib.sha256(
                user_id.encode("utf-8")
            ).hexdigest()

            memory_path = (
                self.user_memory_dir / f"{safe_id}.json"
            )

            self.user_memories[user_id] = BHMemory(
                file_path=memory_path
            )

        return self.user_memories[user_id]

    # Network management
    def register_network(
        self,
        name,
        network,
        description="",
        priority=5
    ):
        return self.network_manager.register(
            name,
            network,
            description,
            priority
        )

    def activate_network(self, name):
        return self.network_manager.activate(name)

    def deactivate_network(self, name):
        return self.network_manager.deactivate(name)

    def remove_network(self, name):
        return self.network_manager.remove(name)

    def get_network_status(self):
        return self.network_manager.list_networks()

    def connect_networks(self, source, target):
        return self.network_manager.connect(source, target)

    def disconnect_networks(self, source, target):
        return self.network_manager.disconnect(source, target)

    # Text network
    def train_text_network(
        self,
        text,
        targets,
        learning_rate=0.5
    ):
        return self.text_network.train_text(
            text,
            targets,
            learning_rate
        )

    def save_text_network(self):
        self.text_network.save()
        return True

    def think_ahead(self, typed_text):
        if not isinstance(typed_text, str):
            return None

        if not typed_text.strip():
            return None

        return self.predictive_engine.prepare(typed_text)

    # Multilingual processing
    def process_multilingual_text(self, text):
        return self.multilingual_pipeline.process(text)

    def reset_multilingual_pipeline(self):
        self.multilingual_pipeline.reset()
        return True

    # Memory operations
    def remember_for_user(
        self,
        user_id,
        text,
        category="general",
        memory_type="long_term",
        importance=5
    ):
        return self._get_user_memory(user_id).remember(
            text=text,
            category=category,
            memory_type=memory_type,
            importance=importance
        )

    def recall_for_user(
        self,
        user_id,
        keyword=None,
        category=None,
        memory_type=None,
        min_importance=None,
        limit=None
    ):
        return self._get_user_memory(user_id).recall(
            keyword=keyword,
            category=category,
            memory_type=memory_type,
            min_importance=min_importance,
            limit=limit
        )

    def update_user_memory(
        self,
        user_id,
        memory_id,
        text=None,
        category=None,
        memory_type=None,
        importance=None
    ):
        return self._get_user_memory(user_id).update(
            memory_id=memory_id,
            text=text,
            category=category,
            memory_type=memory_type,
            importance=importance
        )

    def forget_user_memory(self, user_id, memory_id):
        return self._get_user_memory(user_id).forget(memory_id)

    def clear_user_short_term_memory(self, user_id):
        return self._get_user_memory(user_id).clear_short_term()

    def get_user_memory_count(self, user_id, memory_type=None):
        return self._get_user_memory(user_id).count(memory_type)

    # Meaningful word extraction
    @classmethod
    def _meaningful_words(cls, text):
        if not isinstance(text, str):
            return set()

        words = re.findall(
            r"[^\W_]+",
            text.casefold(),
            flags=re.UNICODE
        )

        return {
            word
            for word in words
            if len(word) > 1 and word not in cls._STOP_WORDS
        }

    # Knowledge relevance filter
    @classmethod
    def _filter_relevant_knowledge(
        cls,
        question,
        results
    ):
        question_words = cls._meaningful_words(question)

        if not question_words or not isinstance(results, list):
            return []

        minimum_overlap = max(
            1,
            math.ceil(len(question_words) * 0.25)
        )

        scored_results = []

        for index, item in enumerate(results):
            if not isinstance(item, dict):
                continue

            searchable_text = " ".join((
                str(item.get("title", "")),
                str(item.get("content", "")),
                str(item.get("category", ""))
            ))

            entry_words = cls._meaningful_words(
                searchable_text
            )

            overlap = len(
                question_words.intersection(entry_words)
            )

            if overlap >= minimum_overlap:
                scored_results.append(
                    (overlap, index, item)
                )

        scored_results.sort(
            key=lambda result: (-result[0], result[1])
        )

        return [
            item
            for _, _, item in scored_results
        ]

    # Build extractive answer
    @staticmethod
    def _build_answer(question, knowledge_results):
        if not knowledge_results:
            return (
                "I don't have enough information in my "
                "knowledge database to answer that yet."
            )

        best = knowledge_results[0]

        title = str(best.get("title", "")).strip()
        content = str(best.get("content", "")).strip()

        if not content:
            return (
                "I found a knowledge entry, but it does "
                "not contain an answer."
            )

        if title:
            return f"{title}: {content}"

        return content

    # Complete question-answer pipeline
    def answer_request(
        self,
        user_id,
        question,
        network_inputs=None
    ):
        if not isinstance(question, str):
            return {
                "status": "error",
                "message": "Question must be text."
            }

        question = question.strip()

        if not question:
            return {
                "status": "error",
                "message": "Question is empty."
            }

        try:
            user_memory = self._get_user_memory(user_id)
        except ValueError as error:
            return {
                "status": "error",
                "message": str(error)
            }

        # Multilingual processing
        try:
            multilingual_result = (
                self.multilingual_pipeline.process(question)
            )
        except (TypeError, ValueError) as error:
            return {
                "status": "error",
                "message": f"Multilingual processing failed: {error}"
            }

        # Shared knowledge retrieval
        prediction = self.predictive_engine.get_on_send(
            question
        )

        raw_knowledge_results = (
            prediction.get("results", [])
            if isinstance(prediction, dict)
            else []
        )

        knowledge_results = self._filter_relevant_knowledge(
            question,
            raw_knowledge_results
        )

        # Personal memory retrieval
        relevant_memories = user_memory.recall(
            keyword=question,
            limit=10
        )

        # Neural network execution
        if network_inputs is not None:
            network_results = (
                self.network_manager.run_active_networks(
                    network_inputs
                )
            )
        else:
            network_results = {}

            if "text" in self.network_manager.networks:
                features = (
                    self.text_network.feature_engine.text_to_features(
                        question
                    )
                )

                network_results["text"] = (
                    self.network_manager.run_network(
                        "text",
                        features
                    )
                )

        # Grounded answer generation
        answer = self._build_answer(
            question,
            knowledge_results
        )

        status = (
            "answered"
            if knowledge_results
            else "insufficient_context"
        )

        return {
            "status": status,
            "question": question,
            "answer": answer,
            "knowledge_results": knowledge_results,
            "relevant_user_memories": relevant_memories,
            "network_results": network_results,
            "multilingual_analysis": (
                multilingual_result["script_analysis"]
            ),
            "numeric_features": (
                multilingual_result["numeric_features"]
            ),
            "numeric_feature_count": (
                multilingual_result["feature_count"]
            ),
            "answer_type": "extractive"
        }

    def clear_prediction_cache(self):
        self.predictive_engine.clear_cache()

    # System health check
    def health_check(self):
        return {
            "ready": self.is_ready,
            "knowledge_count": self.knowledge_engine.count(),
            "registered_networks": len(
                self.network_manager.networks
            ),
            "active_networks": len(
                self.network_manager.get_active_networks()
            ),
            "users_with_memory": len(
                self.user_memories
            ),
            "multilingual_pipeline": (
                self.multilingual_pipeline is not None
            )
        }
