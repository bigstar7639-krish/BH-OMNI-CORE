
from pathlib import Path
import hashlib

from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.memory_engine import BHMemory
from brain.text_network import BHTextNetwork


class BlackHoleBrain:

    def __init__(self, knowledge_engine):

        self.knowledge_engine = knowledge_engine

        self.network_manager = BHNetworkManager()

        self.predictive_engine = PredictiveEngine(
            knowledge_engine
        )

        self.text_network = BHTextNetwork()

        self.network_manager.register(
            name="text",
            network=self.text_network.network,
            description="Text processing neural network",
            priority=10
        )

        self.user_memories = {}

        self.is_ready = True

    # Get or create isolated user memory
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

    # Train text neural network
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

    # Save neural network weights
    def save_text_network(self):
        self.text_network.save()
        return True

    # Prediction while typing
    def think_ahead(self, typed_text):

        if not isinstance(typed_text, str):
            return None

        if not typed_text.strip():
            return None

        return self.predictive_engine.prepare(typed_text)

    # Store user memory
    def remember_for_user(
        self,
        user_id,
        text,
        category="general",
        memory_type="long_term",
        importance=5
    ):

        memory = self._get_user_memory(user_id)

        return memory.remember(
            text=text,
            category=category,
            memory_type=memory_type,
            importance=importance
        )

    # Retrieve user memories
    def recall_for_user(
        self,
        user_id,
        keyword=None,
        category=None,
        memory_type=None,
        min_importance=None,
        limit=None
    ):

        memory = self._get_user_memory(user_id)

        return memory.recall(
            keyword=keyword,
            category=category,
            memory_type=memory_type,
            min_importance=min_importance,
            limit=limit
        )

    # Update existing memory
    def update_user_memory(
        self,
        user_id,
        memory_id,
        text=None,
        category=None,
        memory_type=None,
        importance=None
    ):

        memory = self._get_user_memory(user_id)

        return memory.update(
            memory_id=memory_id,
            text=text,
            category=category,
            memory_type=memory_type,
            importance=importance
        )

    # Forget a memory
    def forget_user_memory(self, user_id, memory_id):

        memory = self._get_user_memory(user_id)

        return memory.forget(memory_id)

    # Clear short-term memories
    def clear_user_short_term_memory(self, user_id):

        memory = self._get_user_memory(user_id)

        return memory.clear_short_term()

    # Count user memories
    def get_user_memory_count(
        self,
        user_id,
        memory_type=None
    ):

        memory = self._get_user_memory(user_id)

        return memory.count(memory_type)

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

        # Retrieve this user's isolated memory
        user_memory = self._get_user_memory(user_id)

        knowledge_results = (
            result["results"]
            if result else []
        )

        relevant_memories = user_memory.recall(
            keyword=question,
            limit=10
        )

        # Run neural networks
        network_results = {}

        if network_inputs is not None:

            network_results = (
                self.network_manager.run_active_networks(
                    network_inputs
                )
            )

        elif "text" in self.network_manager.networks:

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
