
from brain.network_manager import BHNetworkManager
from brain.tokenizer import BHTokenizer
from brain.knowledge_engine import BHKnowledge
from brain.memory_engine import BHMemory


def check_brain():
    checks = {}

    try:
        checks["network_manager"] = BHNetworkManager() is not None
        checks["tokenizer"] = BHTokenizer() is not None
        checks["knowledge_engine"] = BHKnowledge() is not None
        checks["memory_engine"] = BHMemory() is not None
    except Exception as error:
        print("Brain health check failed:", error)
        return False

    for module, status in checks.items():
        print(f"{module}: {'OK' if status else 'FAILED'}")

    return all(checks.values())


if __name__ == "__main__":
    if check_brain():
        print("BH-OMNI CORE: ALL CHECKS PASSED")
    else:
        print("BH-OMNI CORE: CHECK FAILED")
