
import unittest

from brain.text_relevance_engine import BHTextRelevanceEngine


class TestBHTextRelevanceEngine(unittest.TestCase):

    def setUp(self):
        self.engine = BHTextRelevanceEngine()

    def test_identical_text(self):
        self.assertEqual(
            self.engine.score("hello world", "hello world"),
            1.0
        )

    def test_unrelated_text(self):
        self.assertEqual(
            self.engine.score("apple orange", "quantum physics"),
            0.0
        )

    def test_partial_match(self):
        score = self.engine.score("hello world", "hello there")
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_tamil_text(self):
        score = self.engine.score(
            "வணக்கம் உலகம்",
            "வணக்கம் நண்பா"
        )
        self.assertGreater(score, 0.0)

    def test_tamil_combining_marks_preserved(self):
        tokens = self.engine.tokenize("தமிழ் மொழி")
        self.assertEqual(tokens, ["தமிழ்", "மொழி"])

    def test_tamil_english_mixed_text(self):
        tokens = self.engine.tokenize("வணக்கம் hello நண்பா")
        self.assertEqual(tokens, ["வணக்கம்", "hello", "நண்பா"])

    def test_mixed_text_relevance(self):
        score = self.engine.score(
            "தமிழ் programming language",
            "தமிழ் programming"
        )
        self.assertGreater(score, 0.0)

    def test_case_insensitive(self):
        self.assertEqual(
            self.engine.score("Hello World", "hello world"),
            1.0
        )

    def test_unicode_normalization(self):
        first = self.engine.tokenize("ＡＢＣ")
        second = self.engine.tokenize("abc")
        self.assertEqual(first, second)

    def test_empty_text(self):
        self.assertEqual(self.engine.score("", "hello"), 0.0)

    def test_rank_order(self):
        results = self.engine.rank(
            "python programming",
            [
                "football match",
                "python programming language",
                "cooking recipes"
            ]
        )
        self.assertEqual(
            results[0]["text"],
            "python programming language"
        )

    def test_rank_limit(self):
        results = self.engine.rank(
            "hello",
            ["hello world", "hello friend", "goodbye"],
            limit=2
        )
        self.assertEqual(len(results), 2)

    def test_invalid_query(self):
        with self.assertRaises(TypeError):
            self.engine.score(123, "hello")

    def test_invalid_candidates(self):
        with self.assertRaises(TypeError):
            self.engine.rank("hello", "not a list")


if __name__ == "__main__":
    unittest.main()
