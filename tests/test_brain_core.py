
import tempfile
import unittest
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


class TestBrainCorePipeline(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)

        self.knowledge = BHKnowledge(root / "knowledge.json")
        self.knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun."
        )

        self.brain = BlackHoleBrain(
            self.knowledge,
            user_memory_dir=root / "users"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_grounded_answer(self):
        result = self.brain.answer_request(
            "user1", "What is Earth?"
        )

        self.assertEqual(result["status"], "answered")
        self.assertIn("third planet", result["answer"])

    def test_unknown_question(self):
        result = self.brain.answer_request(
            "user1", "Explain quantum computers"
        )

        self.assertEqual(
            result["status"], "insufficient_context"
        )

    def test_empty_question(self):
        result = self.brain.answer_request("user1", " ")

        self.assertEqual(result["status"], "error")

    def test_invalid_user(self):
        result = self.brain.answer_request(None, "Hello")

        self.assertEqual(result["status"], "error")

    def test_network_output_is_returned(self):
        result = self.brain.answer_request(
            "user1", "What is Earth?"
        )

        self.assertIn("text", result["network_results"])
        self.assertEqual(len(result["network_results"]["text"]), 2)


if __name__ == "__main__":
    unittest.main()
