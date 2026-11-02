
from brain.language_analyzer import BHLanguageAnalyzer
from brain.multilingual_numeric_bridge import BHMultilingualNumericBridge
from brain.semantic_feature_engine import BHSemanticFeatureEngine


class BHMultilingualPipeline:
    """Combines script analysis, numeric encoding and semantic signals."""

    def __init__(self):
        self.bridge = BHMultilingualNumericBridge()
        self.semantic_engine = BHSemanticFeatureEngine()

    def process(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")

        if not text.strip():
            raise ValueError("Text cannot be empty")

        analysis = BHLanguageAnalyzer.analyze(text)
        numeric_features = self.bridge.encode_text(text)
        semantic_features = self.semantic_engine.extract(text)

        return {
            "original_text": text,
            "script_analysis": analysis,
            "numeric_features": numeric_features,
            "feature_count": len(numeric_features),
            "semantic_features": semantic_features,
        }

    def reset(self):
        self.bridge.reset()
        self.semantic_engine.reset()
