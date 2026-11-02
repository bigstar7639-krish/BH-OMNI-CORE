
import tempfile
import unittest
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


class TestMemoryIsolation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.knowledge = BHKnowledge(
            self.root / "knowledge.json"
        )

        self.brain = BlackHoleBrain(
            self.knowledge,
            user_memory_dir=self.root / "users"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_none_user_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.brain.remember_for_user(None, "Hello")

    def test_empty_user_id_is_rejected(self):
        with self.assertRaises(ValueError):
            self.brain.remember_for_user("   ", "Hello")

    def test_users_get_separate_memory_files(self):
        self.brain.remember_for_user("alice", "Alice memory")
        self.brain.remember_for_user("bob", "Bob memory")

        alice_files = list(
            (self.root / "users").glob("*.json")
        )

        self.assertEqual(len(alice_files), 2)

        alice = self.brain.recall_for_user(
            "alice",
            keyword="Alice"
        )
        bob = self.brain.recall_for_user(
            "bob",
            keyword="Bob"
        )

        self.assertEqual(len(alice), 1)
        self.assertEqual(len(bob), 1)

        self.assertEqual(alice[0]["text"], "Alice memory")
        self.assertEqual(bob[0]["text"], "Bob memory")

    def test_user_memory_is_not_visible_to_another_user(self):
        self.brain.remember_for_user(
            "alice",
            "Private Alice project"
        )

        bob_memories = self.brain.recall_for_user(
            "bob",
            keyword="Private"
        )

        self.assertEqual(bob_memories, [])


if __name__ == "__main__":
    unittest.main()
