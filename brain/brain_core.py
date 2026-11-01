from pathlib import Path
import hashlib

from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.memory_engine import BHMemory


class BlackHoleBrain:

    def __init__(self, knowledge_engine):

        # Shared knowledge
        self.knowledge_engine = knowledge_engine

        # Specialist network manager
        self.network_manager = BHNetworkManager()

        # Prediction engine
        self.predictive_engine = PredictiveEngine(
            knowledge_engine
        )

        # Separate memory for each user
        self.user_memories = {}

        self.is_ready = True

    # Get or create user memory
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
                Path("database")
                / "users"
                / f"{safe_id}.json"
            )

            self.user_memories[user_id] = BHMemory(
                file_path=memory_path
            )

        return self.user_memories[user_id]

    # Register a specialist network
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

    # Activate network
    def activate_network(self, name):
        return self.network_manager.activate(name)

    # Deactivate network
    def deactivate_network(self, name):
        return self.network_manager.deactivate(name)

    # Remove network
    def remove_network(self, name):
        return self.network_manager.remove(name)

    # View registered networks
    def get_network_status(self):
        return self.network_manager.list_networks()

    # Connect specialist networks
    def connect_networks(self, source, target):
        return self.network_manager.connect(
            source,
            target
        )

    # Prepare prediction while typing
    def think_ahead(self, typed_text):

        if not isinstance(typed_text, str):
            return None

        if not typed_text.strip():
            return None

        return self.predictive_engine.prepare(
            typed_text
        )

    # Remember information for a user
    def remember_for_user(
        self,
        user_id,
        text,
        category="general"
    ):

        memory = self._get_user_memory(user_id)

        return memory.remember(
            text,
            category,
            "long_term"
        )

    # Recall user memories
    def recall_for_user(
        self,
        user_id,
        keyword=None,
        category=None
    ):

        memory = self._get_user_memory(user_id)

        return memory.recall(
            keyword=keyword,
            category=category
        )

    # Process a user question
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

        # Search shared knowledge
        result = self.predictive_engine.get_on_send(
            question
        )

        # Get separate user memory
        user_memory = self._get_user_memory(user_id)

        knowledge_results = (
            result["results"]
            if result else []
        )

        relevant_memories = user_memory.recall(
            keyword=question
        )

        # Run specialist networks only when
        # correctly formatted numeric inputs are supplied.
        network_results = {}

        if network_inputs is not None:
            network_results = (
                self.network_manager.run_active_networks(
                    network_inputs
                )
            )

        return {
            "status": "retrieved",
            "question": question,
            "knowledge_results": knowledge_results,
            "relevant_user_memories": relevant_memories,
            "network_results": network_results
        }

    # Clear prediction cache
    def clear_prediction_cache(self):
        self.predictive_engine.clear_cache()

    # Brain health status
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
            "users_with_memory": len(self.user_memories)
        }
