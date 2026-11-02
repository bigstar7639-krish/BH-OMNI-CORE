
import tempfile
import unittest
from pathlib import Path

from brain.memory_engine import BHMemory


class TestMemoryStaleInstance(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_second_instance_does_not_overwrite_first_instance_data(self):
        first = BHMemory(self.memory_file)
        second = BHMemory(self.memory_file)

        first.remember("Memory saved by first instance")
        second.remember("Memory saved by second instance")

        latest = BHMemory(self.memory_file)
        texts = [item["text"] for item in latest.get_all()]

        self.assertIn("Memory saved by first instance", texts)
        self.assertIn("Memory saved by second instance", texts)


if __name__ == "__main__":
    unittest.main()
