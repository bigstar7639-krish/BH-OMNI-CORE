
from brain.multilingual_pipeline import BHMultilingualPipeline


class BHMultilingualBatchProcessor:
    """Processes multiple text inputs independently."""

    def __init__(self):
        self.pipeline = BHMultilingualPipeline()

    def process_batch(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("Texts must be a list or tuple")

        results = []

        for index, text in enumerate(texts):
            try:
                result = self.pipeline.process(text)

                results.append({
                    "index": index,
                    "success": True,
                    "result": result,
                    "error": None,
                })

            except (TypeError, ValueError) as error:
                results.append({
                    "index": index,
                    "success": False,
                    "result": None,
                    "error": str(error),
                })

        return {
            "total": len(texts),
            "successful": sum(
                1 for item in results if item["success"]
            ),
            "failed": sum(
                1 for item in results if not item["success"]
            ),
            "results": results,
        }
