
import tempfile
from pathlib import Path

from brain.brain_core import BlackHoleBrain


def test_brain_core():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)

        brain = BlackHoleBrain()

        # Test user memory
        brain.remember_for_user(
            "test_user",
            "My favourite subject is science."
        )

        memories = brain.recall_for_user(
            "test_user",
            keyword="science"
        )

        assert len(memories) > 0

        # Test predictive preparation
        prediction = brain.think_ahead("What is Earth?")

        assert prediction is not None

        print("BH-OMNI CORE integration test passed!")


if __name__ == "__main__":
    test_brain_core()
