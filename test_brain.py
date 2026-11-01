
import tempfile
from pathlib import Path

from brain.knowledge_engine import BHKnowledge
from brain.memory_engine import BHMemory
from brain.neural_network import BHNeuralNetwork
from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.tokenizer import BHTokenizer


def run_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)

        # 1. Knowledge test
        knowledge = BHKnowledge(root / "knowledge.json")
        knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun.",
            "science"
        )
        assert knowledge.search("Earth")

        # 2. Memory test
        memory = BHMemory(root / "memory.json")
        memory.remember("BH OMNI CORE project", "project")
        assert memory.recall("BH OMNI")

        # 3. Neural network test
        network = BHNeuralNetwork(2, 4, 1)
        output = network.forward([0.5, 0.2])
        assert len(output) == 1

        # 4. Network manager test
        manager = BHNetworkManager()
        assert manager.register("math", network)
        assert not manager.register("math", network)
        assert "math" in manager.get_active_networks()

        # 5. Predictive engine test
        predictor = PredictiveEngine(knowledge)
        candidate = predictor.prepare("What is Earth?")
        assert candidate is not None
        assert candidate["results"]

        # 6. Tokenizer test
        tokenizer = BHTokenizer()
        tokenizer.learn("Hello BH OMNI")
        encoded = tokenizer.encode("Hello BH OMNI")
        assert encoded
        assert tokenizer.decode(encoded)

    print("ALL BASIC MODULE TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
