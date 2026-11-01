
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
        brain = BlackHoleBrain(knowledge)

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

        print("BH-OMNI CORE integration test passed!")


if __name__ == "__main__":
    test_brain_core()
