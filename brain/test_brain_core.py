
import tempfile
import unittest
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


class TestBrainCore(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.knowledge = BHKnowledge(
            self.root / "knowledge.json"
        )

        self.knowledge.add(
            "Earth",
            "Earth is the third planet from the Sun."
        )

        self.brain = BlackHoleBrain(
            self.knowledge,
            user_memory_dir=self.root / "users"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_memory_storage_and_recall(self):
        self.brain.remember_for_user(
            "test_user",
            "My favourite subject is science."
        )

        memories = self.brain.recall_for_user(
            "test_user",
            keyword="science"
        )

        self.assertGreater(len(memories), 0)

    def test_user_memory_isolation(self):
        self.brain.remember_for_user(
            "user_one",
            "My favourite subject is science."
        )

        user_one_memories = self.brain.recall_for_user(
            "user_one",
            keyword="science"
        )

        user_two_memories = self.brain.recall_for_user(
            "user_two",
            keyword="science"
        )

        self.assertGreater(len(user_one_memories), 0)
        self.assertEqual(len(user_two_memories), 0)

    def test_prediction(self):
        prediction = self.brain.think_ahead(
            "What is Earth?"
        )

        self.assertIsNotNone(prediction)

    def test_known_question_answer(self):
        result = self.brain.answer_request(
            "test_user",
            "What is Earth?"
        )

        self.assertEqual(result["status"], "answered")
        self.assertIn("third planet", result["answer"])
        self.assertEqual(
            result["answer_type"],
            "extractive"
        )

    def test_unknown_question(self):
        result = self.brain.answer_request(
            "test_user",
            "What is a black hole made of?"
        )

        self.assertEqual(
            result["status"],
            "insufficient_context"
        )

        self.assertIn(
            "don't have enough information",
            result["answer"]
        )

    def test_personal_memory_is_separate_from_answer(self):
        self.brain.remember_for_user(
            "test_user",
            "My favourite subject is science."
        )

        result = self.brain.answer_request(
            "test_user",
            "What is Earth?"
        )

        self.assertIn(
            "relevant_user_memories",
            result
        )

        self.assertNotIn(
            "favourite subject",
            result["answer"].lower()
        )

    def test_empty_question(self):
        result = self.brain.answer_request(
            "test_user",
            " "
        )

        self.assertEqual(result["status"], "error")

    def test_invalid_user(self):
        result = self.brain.answer_request(
            None,
            "Hello"
        )

        self.assertEqual(result["status"], "error")

    def test_invalid_question_type(self):
        result = self.brain.answer_request(
            "test_user",
            None
        )

        self.assertEqual(result["status"], "error")

    def test_unicode_meaningful_words(self):
        words = self.brain._meaningful_words(
            "தமிழ் அறிவியல் உலகம்"
        )

        self.assertIn("தமிழ்", words)
        self.assertIn("அறிவியல்", words)

    def test_network_registration(self):
        result = self.brain.register_network(
            "test_network",
            self.brain.text_network.network,
            "Test network",
            5
        )

        self.assertTrue(result)

        networks = self.brain.get_network_status()

        self.assertIn("test_network", networks)

    def test_network_activation_and_deactivation(self):
        self.brain.register_network(
            "test_network",
            self.brain.text_network.network
        )

        self.assertTrue(
            self.brain.deactivate_network("test_network")
        )

        self.assertTrue(
            self.brain.activate_network("test_network")
        )

    def test_health_check(self):
        result = self.brain.health_check()

        self.assertTrue(result["ready"])
        self.assertGreaterEqual(
            result["knowledge_count"],
            1
        )


if __name__ == "__main__":
    unittest.main()
