
import unittest

from brain.semantic_feature_engine import BHSemanticFeatureEngine
from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPublicAPIContracts(unittest.TestCase):

    def test_semantic_engine_has_extract_method(self):
        engine = BHSemanticFeatureEngine()
        self.assertTrue(callable(engine.extract))

    def test_semantic_engine_has_reset_method(self):
        engine = BHSemanticFeatureEngine()
        self.assertTrue(callable(engine.reset))

    def test_pipeline_has_process_method(self):
        pipeline = BHMultilingualPipeline()
        self.assertTrue(callable(pipeline.process))

    def test_pipeline_has_reset_method(self):
        pipeline = BHMultilingualPipeline()
        self.assertTrue(callable(pipeline.reset))

    def test_pipeline_returns_required_keys(self):
        pipeline = BHMultilingualPipeline()
        try:
            result = pipeline.process("I am happy")

            required = {
                "original_text",
                "script_analysis",
                "numeric_features",
                "feature_count",
                "semantic_features",
            }

            self.assertTrue(required.issubset(result.keys()))
        finally:
            pipeline.reset()


if __name__ == "__main__":
    unittest.main()
