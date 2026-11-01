
from brain.language_analyzer import BHLanguageAnalyzer
from brain.multilingual_pipeline import BHMultilingualPipeline
from brain.numeric_brain import BHNumericBrain
from brain.sparse_numeric_ops import BHSparseNumericOps


def run_health_check():
    results = {}

    # 1. Script detection
    try:
        result = BHLanguageAnalyzer.analyze("வணக்கம்")
        results["tamil_script_detection"] = (
            result["primary_script"] == "Tamil"
        )
    except Exception:
        results["tamil_script_detection"] = False

    # 2. English processing
    try:
        pipeline = BHMultilingualPipeline()
        result = pipeline.process("Hello world")
        results["english_pipeline"] = result["feature_count"] == 4
    except Exception:
        results["english_pipeline"] = False

    # 3. Tamil processing
    try:
        result = pipeline.process("வணக்கம் உலகம்")
        results["tamil_pipeline"] = (
            result["script_analysis"]["primary_script"] == "Tamil"
        )
    except Exception:
        results["tamil_pipeline"] = False

    # 4. Dynamic numerical features
    try:
        brain = BHNumericBrain()
        for value in range(100):
            brain.add_feature(value)

        results["dynamic_numeric_features"] = (
            brain.get_feature_count() == 100
        )
    except Exception:
        results["dynamic_numeric_features"] = False

    # 5. Sparse mathematical operations
    try:
        result = BHSparseNumericOps.dot_product(
            {0: 2, 100: 3},
            {0: 4, 100: 5}
        )
        results["sparse_math"] = result == 23
    except Exception:
        results["sparse_math"] = False

    passed = sum(results.values())
    total = len(results)

    print("\nBH-OMNI MULTILINGUAL HEALTH CHECK")
    print("-" * 40)

    for name, status in results.items():
        print(f"{name}: {'PASS' if status else 'FAIL'}")

    print("-" * 40)
    print(f"RESULT: {passed}/{total} checks passed")

    return passed == total


if __name__ == "__main__":
    success = run_health_check()
    raise SystemExit(0 if success else 1)
