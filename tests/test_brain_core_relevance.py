
import tempfile
import unittest
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


class TestBrainCoreRelevance(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)

        knowledge = BHKnowledge(root / "knowledge.json")
        self.brain = BlackHoleBrain(
            knowledge,
            user_memory_dir=root / "users"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_relevant_result_is_ranked_first(self):
        results = [
            {"title": "Football", "content": "Sports match"},
            {"title": "Python", "content": "Python programming language"},
            {"title": "Cooking", "content": "Food recipes"}
        ]

        ranked = self.brain._filter_relevant_knowledge(
            "Python programming",
            results
        )

        self.assertGreater(len(ranked), 0)
        self.assertEqual(ranked[0]["title"], "Python")

    def test_unrelated_results_are_removed(self):
        results = [
            {"title": "Football", "content": "Sports match"},
            {"title": "Cooking", "content": "Food recipes"}
        ]

        ranked = self.brain._filter_relevant_knowledge(
            "Quantum physics",
            results
        )

        self.assertEqual(ranked, [])

    def test_empty_results(self):
        ranked = self.brain._filter_relevant_knowledge(
            "Python programming",
            []
        )

        self.assertEqual(ranked, [])

    def test_invalid_result_entries_are_skipped(self):
        results = [
            None,
            "invalid",
            {"title": "Python", "content": "Python programming"}
        ]

        ranked = self.brain._filter_relevant_knowledge(
            "Python programming",
            results
        )

        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0]["title"], "Python")

    def test_invalid_question_returns_empty_list(self):
        ranked = self.brain._filter_relevant_knowledge(
            None,
            [{"title": "Python", "content": "Programming"}]
        )

        self.assertEqual(ranked, [])


if __name__ == "__main__":
    unittest.main()
