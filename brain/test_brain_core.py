
import tempfile
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


def test_brain_core():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        knowledge = BHKnowledge(root / "knowledge.json")

        knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun."
        )

        brain = BlackHoleBrain(
            knowledge,
            user_memory_dir=root / "users"
        )

        # Memory test
        brain.remember_for_user(
            "test_user",
            "My favourite subject is science."
        )

        memories = brain.recall_for_user(
            "test_user",
            keyword="science"
        )

        assert len(memories) > 0

        # Prediction test
        prediction = brain.think_ahead("What is Earth?")
        assert prediction is not None

        # Answer generation from stored knowledge
        result = brain.answer_request(
            "test_user",
            "What is Earth?"
        )

        assert result["status"] == "answered"
        assert "third planet" in result["answer"]
        assert result["answer_type"] == "extractive"

        # Unknown question must not invent an answer
        unknown = brain.answer_request(
            "test_user",
            "What is a black hole made of?"
        )

        assert unknown["status"] == "insufficient_context"
        assert "don't have enough information" in unknown["answer"]

        # Empty question
        empty = brain.answer_request("test_user", " ")
        assert empty["status"] == "error"

        # Invalid user
        invalid = brain.answer_request(None, "Hello")
        assert invalid["status"] == "error"

        print("BH-OMNI CORE answer pipeline tests passed!")


if __name__ == "__main__":
    test_brain_core()
