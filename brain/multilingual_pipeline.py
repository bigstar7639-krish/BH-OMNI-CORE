
from brain.language_analyzer import BHLanguageAnalyzer
from brain.multilingual_numeric_bridge import BHMultilingualNumericBridge


class BHMultilingualPipeline:
    """Combines script analysis and numerical text encoding."""

    def __init__(self):
        self.bridge = BHMultilingualNumericBridge()

    def process(self, text):
        if not isinstance(text, str):
            raise TypeError("Text must be a string")

        if not text.strip():
            raise ValueError("Text cannot be empty")

        analysis = BHLanguageAnalyzer.analyze(text)
        numeric_features = self.bridge.encode_text(text)

        return {
            "original_text": text,
            "script_analysis": analysis,
            "numeric_features": numeric_features,
            "feature_count": len(numeric_features),
        }

    def reset(self):
        self.bridge.reset()
