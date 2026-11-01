
from collections.abc import Iterable

from brain.multilingual_pipeline import BHMultilingualPipeline


class BHMultilingualBatchProcessor:
    """Processes text batches with limits and streaming support."""

    def __init__(self, max_batch_size=100, max_text_length=10000):
        if (
            not isinstance(max_batch_size, int)
            or isinstance(max_batch_size, bool)
            or max_batch_size < 1
        ):
            raise ValueError("max_batch_size must be a positive integer")

        if (
            not isinstance(max_text_length, int)
            or isinstance(max_text_length, bool)
            or max_text_length < 1
        ):
            raise ValueError("max_text_length must be a positive integer")

        self.max_batch_size = max_batch_size
        self.max_text_length = max_text_length
        self.pipeline = BHMultilingualPipeline()

    def process_iter(self, texts):
        """Yield individual results without storing the entire batch."""

        if isinstance(texts, (str, bytes)) or not isinstance(texts, Iterable):
            raise TypeError("Texts must be an iterable of strings")

        for index, text in enumerate(texts):
            if index >= self.max_batch_size:
                raise ValueError(
                    f"Batch exceeds maximum size of {self.max_batch_size}"
                )

            try:
                if not isinstance(text, str):
                    raise TypeError("Text must be a string")

                if len(text) > self.max_text_length:
                    raise ValueError(
                        f"Text exceeds maximum length of {self.max_text_length}"
                    )

                result = self.pipeline.process(text)

                yield {
                    "index": index,
                    "success": True,
                    "result": result,
                    "error": None,
                }

            except (TypeError, ValueError) as error:
                yield {
                    "index": index,
                    "success": False,
                    "result": None,
                    "error": str(error),
                }

    def process_batch(self, texts):
        """Compatibility method that returns a complete batch report."""

        results = list(self.process_iter(texts))

        successful = sum(1 for item in results if item["success"])

        return {
            "total": len(results),
            "successful": successful,
            "failed": len(results) - successful,
            "results": results,
        }
