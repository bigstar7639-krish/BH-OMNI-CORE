import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineInputValidation(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_none_input_is_rejected(self):
        with self.assertRaises(TypeError):
            self.pipeline.process(None)

    def test_integer_input_is_rejected(self):
        with self.assertRaises(TypeError):
            self.pipeline.process(123)

    def test_list_input_is_rejected(self):
        with self.assertRaises(TypeError):
            self.pipeline.process(["hello"])

    def test_empty_string_is_rejected(self):
        with self.assertRaises(ValueError):
            self.pipeline.process("")

    def test_whitespace_input_is_rejected(self):
        with self.assertRaises(ValueError):
            self.pipeline.process("   ")


if __name__ == "__main__":
    unittest.main()
