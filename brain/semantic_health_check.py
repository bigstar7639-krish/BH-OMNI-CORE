
"""BH-OMNI CORE semantic engine health check."""

from brain.semantic_feature_engine import BHSemanticFeatureEngine


def check_semantic_engine():
    engine = BHSemanticFeatureEngine()

    checks = {
        "positive sentiment": (
            engine.extract("I am happy")["sentiment_signal"] == 1.0
        ),
        "negative sentiment": (
            engine.extract("I am sad")["sentiment_signal"] == -1.0
        ),
        "negation handling": (
            engine.extract("I am not happy")["sentiment_signal"] == -1.0
        ),
        "Tamil negation": (
            engine.extract("எனக்கு இது பிடிக்கவில்லை")["sentiment_signal"] == -1.0
        ),
        "urgency detection": (
            engine.extract("This is an emergency")["urgency_signal"] == 1.0
        ),
        "question detection": (
            engine.extract("What is this?")["question_signal"] == 1.0
        ),
        "sentence boundary": (
            engine.extract("Not. Happy")["sentiment_signal"] == 1.0
        ),
    }

    for name, passed in checks.items():
        print(f"[{'PASS' if passed else 'FAIL'}] {name}")

    passed_count = sum(checks.values())
    total = len(checks)

    print(f"\nSemantic Health: {passed_count}/{total}")

    return passed_count == total


if __name__ == "__main__":
    if not check_semantic_engine():
        raise SystemExit(1)
