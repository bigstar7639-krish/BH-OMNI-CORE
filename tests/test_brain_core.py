
import math
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
            "user1",
            "What is Earth?"
        )

        self.assertEqual(result["status"], "answered")
        self.assertIn("third planet", result["answer"])

    def test_unknown_question(self):
        result = self.brain.answer_request(
            "user1",
            "Explain quantum computers"
        )

        self.assertEqual(
            result["status"],
            "insufficient_context"
        )

    def test_empty_question(self):
        result = self.brain.answer_request("user1", " ")

        self.assertEqual(result["status"], "error")

    def test_invalid_user(self):
        result = self.brain.answer_request(None, "Hello")

        self.assertEqual(result["status"], "error")

    def test_invalid_question_type(self):
        result = self.brain.answer_request("user1", 123)

        self.assertEqual(result["status"], "error")

    def test_response_structure(self):
        result = self.brain.answer_request(
            "user1",
            "What is Earth?"
        )

        expected_keys = {
            "status",
            "question",
            "answer",
            "knowledge_results",
            "relevant_user_memories",
            "network_results",
            "answer_type"
        }

        self.assertTrue(expected_keys.issubset(result.keys()))

        self.assertIsInstance(result["answer"], str)
        self.assertIsInstance(result["knowledge_results"], list)
        self.assertIsInstance(
            result["relevant_user_memories"],
            list
        )
        self.assertIsInstance(result["network_results"], dict)

    def test_network_output_is_returned(self):
        result = self.brain.answer_request(
            "user1",
            "What is Earth?"
        )

        self.assertIn("text", result["network_results"])

        output = result["network_results"]["text"]

        self.assertEqual(len(output), 2)

        for value in output:
            self.assertIsInstance(value, (int, float))
            self.assertTrue(math.isfinite(value))

    def test_unicode_question(self):
        result = self.brain.answer_request(
            "user1",
            "தமிழ் மொழி என்றால் என்ன?"
        )

        self.assertIn(
            result["status"],
            {"answered", "insufficient_context"}
        )

    def test_repeated_request(self):
        first = self.brain.answer_request(
            "user1",
            "What is Earth?"
        )

        second = self.brain.answer_request(
            "user1",
            "What is Earth?"
        )

        self.assertEqual(first["status"], second["status"])
        self.assertEqual(first["answer"], second["answer"])

    def test_different_users_have_separate_memory_results(self):
        first = self.brain.answer_request(
            "user1",
            "What is Earth?"
        )

        second = self.brain.answer_request(
            "user2",
            "What is Earth?"
        )

        self.assertIsInstance(
            first["relevant_user_memories"],
            list
        )
        self.assertIsInstance(
            second["relevant_user_memories"],
            list
        )


if __name__ == "__main__":
    unittest.main()
