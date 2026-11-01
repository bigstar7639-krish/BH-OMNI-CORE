
import tempfile
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


def test_brain_core():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        # Create knowledge engine
        knowledge = BHKnowledge(root / "knowledge.json")

        # Add sample knowledge
        knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun."
        )

        # Create brain
        brain = BlackHoleBrain(knowledge, user_memory_dir=root / "users")

        # Test user memory
        brain.remember_for_user(
            "test_user",
            "My favourite subject is science."
        )

        memories = brain.recall_for_user(
            "test_user",
            keyword="science"
        )

        assert len(memories) > 0, "Memory test failed"

        # Test predictive engine
        prediction = brain.think_ahead("What is Earth?")

        assert prediction is not None, "Prediction test failed"

        # Short questions must not crash when prediction has no candidate.
        short_result = brain.answer_request("test_user", "Hi")
        assert short_result["status"] == "retrieved"
        assert short_result["knowledge_results"] == []

        # A normal question returns retrieved context, not a generated answer.
        answer_result = brain.answer_request("test_user", "What is Earth?")
        assert answer_result["status"] == "retrieved"
        assert isinstance(answer_result["knowledge_results"], list)

        print("BH-OMNI CORE integration test passed!")


if __name__ == "__main__":
    test_brain_core()
