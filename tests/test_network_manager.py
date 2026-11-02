
import unittest

from brain.network_manager import BHNetworkManager


class DummyNetwork:
    def forward(self, values):
        return [sum(values)]


class TestNetworkManager(unittest.TestCase):
    def setUp(self):
        self.manager = BHNetworkManager()
        self.manager.register("a", DummyNetwork(), priority=8)
        self.manager.register("b", DummyNetwork(), priority=3)

    def test_register_and_duplicate(self):
        self.assertFalse(self.manager.register("a", DummyNetwork()))

    def test_connect_disconnect(self):
        self.assertTrue(self.manager.connect("a", "b"))
        self.assertEqual(self.manager.get_connections("a"), ["b"])
        self.assertTrue(self.manager.disconnect("a", "b"))
        self.assertEqual(self.manager.get_connections("a"), [])

    def test_remove_cleans_connections(self):
        self.manager.connect("a", "b")
        self.assertTrue(self.manager.remove("b"))
        self.assertEqual(self.manager.get_connections("a"), [])

    def test_inactive_network_is_not_run(self):
        self.manager.deactivate("a")
        self.assertIsNone(self.manager.run_network("a", [1, 2]))

    def test_active_network_execution(self):
        self.assertEqual(self.manager.run_network("a", [1, 2]), [3])
        self.assertEqual(self.manager.list_networks()["a"]["runs"], 1)


if __name__ == "__main__":
    unittest.main()
