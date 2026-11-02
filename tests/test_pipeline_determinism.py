import unittest

from brain.multilingual_pipeline import BHMultilingualPipeline


class TestPipelineDeterminism(unittest.TestCase):

    def setUp(self):
        self.pipeline = BHMultilingualPipeline()

    def tearDown(self):
        self.pipeline.reset()

    def test_same_input_produces_same_output(self):
        first = self.pipeline.process("I am happy")
        self.pipeline.reset()
        second = self.pipeline.process("I am happy")

        self.assertEqual(first, second)

    def test_tamil_input_is_deterministic(self):
        text = "எனக்கு இது பிடிக்கவில்லை"

        first = self.pipeline.process(text)
        self.pipeline.reset()
        second = self.pipeline.process(text)

        self.assertEqual(first, second)

    def test_mixed_language_input_is_deterministic(self):
        text = "Hello நண்பா, I am happy"

        first = self.pipeline.process(text)
        self.pipeline.reset()
        second = self.pipeline.process(text)

        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()#
