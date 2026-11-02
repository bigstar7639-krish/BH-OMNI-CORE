
import unittest

from brain.semantic_health_check import check_semantic_engine


class TestSemanticHealthCheck(unittest.TestCase):

    def test_health_check_returns_true(self):
        result = check_semantic_engine()
        self.assertIs(result, True)


if __name__ == "__main__":
    unittest.main()
