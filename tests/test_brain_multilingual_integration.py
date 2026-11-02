
import tempfile
import unittest
from pathlib import Path

from brain.brain_core import BlackHoleBrain
from brain.knowledge_engine import BHKnowledge


class TestBrainMultilingualIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)

        self.knowledge = BHKnowledge(root / "knowledge.json")

        self.knowledge.add(
            "Tamil",
            "Tamil is a classical language."
        )

        self.brain = BlackHoleBrain(
            self.knowledge,
            user_memory_dir=root / "users"
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_multilingual_pipeline_is_connected(self):
        self.assertIsNotNone(
            self.brain.multilingual_pipeline
        )

    def test_process_multilingual_text(self):
        result = self.brain.process_multilingual_text(
            "Vanakkam"
        )

        self.assertEqual(
            result["original_text"],
            "Vanakkam"
        )
        self.assertIn("script_analysis", result)
        self.assertIn("numeric_features", result)
        self.assertEqual(
            result["feature_count"],
            len(result["numeric_features"])
        )

    def test_answer_contains_multilingual_data(self):
        result = self.brain.answer_request(
            "user1",
            "Tamil"
        )

        self.assertIn("multilingual_analysis", result)
        self.assertIn("numeric_features", result)
        self.assertIn("numeric_feature_count", result)

    def test_multilingual_pipeline_reset(self):
        self.assertTrue(
            self.brain.reset_multilingual_pipeline()
        )

    def test_health_check_reports_pipeline(self):
        result = self.brain.health_check()

        self.assertTrue(
            result["multilingual_pipeline"]
        )


if __name__ == "__main__":
    unittest.main()
