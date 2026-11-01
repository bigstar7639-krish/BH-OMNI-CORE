
from brain.network_manager import BHNetworkManager
from brain.tokenizer import BHTokenizer
from brain.knowledge_engine import BHKnowledge
from brain.memory_engine import BHMemory
from brain.text_network import BHTextNetwork


def _run_check(name, check_function, results):
    try:
        check_function()
        results[name] = {
            "status": True,
            "error": None
        }
    except Exception as error:
        results[name] = {
            "status": False,
            "error": f"{type(error).__name__}: {error}"
        }


def _check_network_manager():
    manager = BHNetworkManager()

    if not isinstance(manager.networks, dict):
        raise RuntimeError("Network registry is invalid.")

    if not isinstance(manager.connections, dict):
        raise RuntimeError("Network connections are invalid.")


def _check_tokenizer():
    tokenizer = BHTokenizer()

    if tokenizer is None:
        raise RuntimeError("Tokenizer initialization failed.")


def _check_knowledge_engine():
    engine = BHKnowledge()

    if engine is None:
        raise RuntimeError("Knowledge engine initialization failed.")


def _check_memory_engine():
    memory = BHMemory()

    if memory is None:
        raise RuntimeError("Memory engine initialization failed.")


def _check_text_network():
    text_network = BHTextNetwork()

    result = text_network.forward_text(
        "BH OMNI CORE health check"
    )

    if not isinstance(result, dict):
        raise RuntimeError("Text network returned an invalid result.")

    if "features" not in result or "output" not in result:
        raise RuntimeError("Text network result is incomplete.")

    if len(result["features"]) != 4:
        raise RuntimeError("Text network feature count must be 4.")


def check_brain():
    results = {}

    checks = [
        ("network_manager", _check_network_manager),
        ("tokenizer", _check_tokenizer),
        ("knowledge_engine", _check_knowledge_engine),
        ("memory_engine", _check_memory_engine),
        ("text_network", _check_text_network),
    ]

    for name, check_function in checks:
        _run_check(name, check_function, results)

    for module, result in results.items():
        if result["status"]:
            print(f"{module}: OK")
        else:
            print(
                f"{module}: FAILED - {result['error']}"
            )

    passed = sum(
        1 for result in results.values()
        if result["status"]
    )

    total = len(results)

    print(f"\nHealth checks: {passed}/{total} passed")

    return passed == total


if __name__ == "__main__":
    if check_brain():
        print("BH-OMNI CORE: ALL CHECKS PASSED")
    else:
        print("BH-OMNI CORE: CHECK FAILED")
