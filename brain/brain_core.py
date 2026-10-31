from brain.network_manager import NetworkManager
from brain.predictive_engine import PredictiveEngine


class BlackHoleBrain:

    def __init__(self, knowledge_engine):
        self.network_manager = NetworkManager()
        self.predictive_engine = PredictiveEngine(
            knowledge_engine
        )

        self.is_ready = True

    def think_ahead(self, typed_text):
        """
        Prepare matching knowledge while typing.
        """
        if not typed_text:
            return None

        return self.predictive_engine.prepare(
            typed_text
        )

    def answer_request(self, question):
        """
        Retrieve prepared knowledge when Send is pressed.
        This is retrieval, not full AI reasoning.
        """
        if not question:
            return {
                "status": "error",
                "message": "Question is empty."
            }

        result = self.predictive_engine.get_on_send(
            question
        )

        return {
            "status": "prepared",
            "question": question,
            "knowledge_results": (
                result["results"] if result else []
            )
        }

    def clear_memory_cache(self):
        self.predictive_engine.clear_cache()
