
from brain.multilingual_pipeline import BHMultilingualPipeline


class BHMultilingualBatchProcessor:
    """Processes batches with configurable memory safety limits."""

    def __init__(self, max_batch_size=100, max_text_length=10000):
        if not isinstance(max_batch_size, int) or isinstance(max_batch_size, bool):
            raise ValueError("max_batch_size must be an integer")

        if not isinstance(max_text_length, int) or isinstance(max_text_length, bool):
            raise ValueError("max_text_length must be an integer")

        if max_batch_size < 1 or max_text_length < 1:
            raise ValueError("Limits must be greater than zero")

        self.max_batch_size = max_batch_size
        self.max_text_length = max_text_length
        self.pipeline = BHMultilingualPipeline()

    def process_batch(self, texts):
        if not isinstance(texts, (list, tuple)):
            raise TypeError("Texts must be a list or tuple")

        if len(texts) > self.max_batch_size:
            raise ValueError(
                f"Batch exceeds maximum size of {self.max_batch_size}"
            )

        results = []

        for index, text in enumerate(texts):
            try:
                if not isinstance(text, str):
                    raise TypeError("Text must be a string")

                if len(text) > self.max_text_length:
                    raise ValueError(
                        f"Text exceeds maximum length of {self.max_text_length}"
                    )

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
