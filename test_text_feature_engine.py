import unittest

from brain.text_feature_engine import BHTextFeatureEngine


class TestTextFeatureEngine(unittest.TestCase):
    def setUp(self):
        self.engine = BHTextFeatureEngine()

    def test_text_to_features_has_four_finite_values(self):
        result = self.engine.text_to_features("What is Earth?")
        self.assertEqual(len(result), 4)
        for value in result:
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 1.0)

    def test_empty_and_invalid_text(self):
        self.assertEqual(self.engine.text_to_features(""), [0.0] * 4)
        self.assertEqual(self.engine.text_to_features(None), [0.0] * 4)

    def test_same_text_always_has_same_features(self):
        first = self.engine.text_to_features("What is Earth?")
        self.engine.tokenizer.learn("unrelated new vocabulary tokens")
        second = self.engine.text_to_features("What is Earth?")
        self.assertEqual(first, second)

    def test_feature_engine_does_not_learn_words(self):
        before = dict(self.engine.tokenizer.vocab)
        self.engine.text_to_features("brand new words")
        self.assertEqual(before, self.engine.tokenizer.vocab)


if __name__ == "__main__":
    unittest.main()
