
import math
import tempfile
from pathlib import Path

from brain.knowledge_engine import BHKnowledge
from brain.memory_engine import BHMemory
from brain.neural_network import BHNeuralNetwork
from brain.network_manager import BHNetworkManager
from brain.predictive_engine import PredictiveEngine
from brain.tokenizer import BHTokenizer


def _check(condition, message):
    if not condition:
        raise AssertionError(message)


def run_tests():
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)

        # 1. Knowledge engine test
        knowledge = BHKnowledge(root / "knowledge.json")

        knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun.",
            "science"
        )

        knowledge_results = knowledge.search("Earth")

        _check(
            bool(knowledge_results),
            "Knowledge search failed."
        )

        # 2. Memory engine test
        memory = BHMemory(root / "memory.json")

        memory.remember(
            "BH OMNI CORE project",
            "project"
        )

        memory_results = memory.recall("BH OMNI")

        _check(
            bool(memory_results),
            "Memory recall failed."
        )

        # 3. Neural network test
        network = BHNeuralNetwork(2, 4, 1)

        output = network.forward([0.5, 0.2])

        _check(
            isinstance(output, (list, tuple)),
            "Neural network output must be a list or tuple."
        )

        _check(
            len(output) == 1,
            "Neural network output size is incorrect."
        )

        _check(
            all(
                isinstance(value, (int, float))
                and math.isfinite(value)
                for value in output
            ),
            "Neural network produced an invalid numeric output."
        )

        # 4. Network manager test
        manager = BHNetworkManager()

        registered = manager.register("math", network)

        _check(
            registered is True,
            "Network registration failed."
        )

        duplicate_registered = manager.register("math", network)

        _check(
            duplicate_registered is False,
            "Duplicate network registration should fail."
        )

        active_networks = manager.get_active_networks()

        _check(
            "math" in active_networks,
            "Registered network is missing from active networks."
        )

        # 5. Predictive engine test
        predictor = PredictiveEngine(knowledge)

        candidate = predictor.prepare("What is Earth?")

        _check(
            isinstance(candidate, dict),
            "Predictive engine did not return a valid candidate."
        )

        _check(
            bool(candidate.get("results")),
            "Predictive engine returned no knowledge results."
        )

        # 6. Tokenizer test
        tokenizer = BHTokenizer()

        tokenizer.learn("Hello BH OMNI")

        encoded = tokenizer.encode("Hello BH OMNI")

        _check(
            isinstance(encoded, (list, tuple)) and bool(encoded),
            "Tokenizer encoding failed."
        )

        decoded = tokenizer.decode(encoded)

        _check(
            isinstance(decoded, str) and bool(decoded.strip()),
            "Tokenizer decoding failed."
        )

    print("ALL BASIC MODULE TESTS PASSED!")


if __name__ == "__main__":
    run_tests()
