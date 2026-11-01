
from datetime import datetime, timezone


class BHNetworkManager:
    def __init__(self):
        self.networks = {}
        self.connections = {}
        self.activity_log = []

    # Register a network
    def register(self, name, network, description="", priority=5):
        name = str(name).strip()

        if not name or network is None:
            return False

        if name in self.networks:
            return False

        priority = max(1, min(10, int(priority)))

        self.networks[name] = {
            "network": network,
            "description": str(description),
            "active": True,
            "priority": priority,
            "registered_at": self._time(),
            "runs": 0
        }

        self.connections[name] = set()
        self.log(f"Registered: {name}")
        return True

    # Activate a network
    def activate(self, name):
        if name not in self.networks:
            return False

        self.networks[name]["active"] = True
        self.log(f"Activated: {name}")
        return True

    # Deactivate a network
    def deactivate(self, name):
        if name not in self.networks:
            return False

        self.networks[name]["active"] = False
        self.log(f"Deactivated: {name}")
        return True

    # Remove a network and its connections
    def remove(self, name):
        if name not in self.networks:
            return False

        del self.networks[name]
        self.connections.pop(name, None)

        for connected in self.connections.values():
            connected.discard(name)

        self.log(f"Removed: {name}")
        return True

    # Connect two registered networks
    def connect(self, source, target):
        if source not in self.networks:
            return False

        if target not in self.networks:
            return False

        if source == target:
            return False

        if target in self.connections[source]:
            return False

        self.connections[source].add(target)
        self.log(f"Connected: {source} -> {target}")
        return True

    # Disconnect two networks
    def disconnect(self, source, target):
        if source not in self.connections:
            return False

        if target not in self.connections[source]:
            return False

        self.connections[source].remove(target)
        self.log(f"Disconnected: {source} -> {target}")
        return True

    # Get a network object
    def get_network(self, name):
        details = self.networks.get(name)

        if details is None:
            return None

        return details["network"]

    # Get active networks
    def get_active_networks(self):
        return {
            name: details["network"]
            for name, details in self.networks.items()
            if details["active"]
        }

    # Get connected network names
    def get_connections(self, name):
        if name not in self.connections:
            return []

        return sorted(self.connections[name])

    # Run one active network
    def run_network(self, name, inputs):
        details = self.networks.get(name)

        if details is None or not details["active"]:
            self.log(f"Execution skipped: {name}")
            return None

        network = details["network"]

        if not hasattr(network, "forward"):
            self.log(f"Execution failed: {name} has no forward method")
            return None

        try:
            result = network.forward(inputs)
            details["runs"] += 1
            self.log(f"Executed: {name}")
            return result

        except Exception as error:
            self.log(f"Execution error in {name}: {error}")
            return None

    # Run all active networks by priority
    def run_active_networks(self, inputs):
        results = {}

        active = sorted(
            self.networks.items(),
            key=lambda item: item[1]["priority"],
            reverse=True
        )

        for name, details in active:
            if details["active"]:
                results[name] = self.run_network(name, inputs)

        return results

    # List network information
    def list_networks(self):
        return {
            name: {
                "description": details["description"],
                "active": details["active"],
                "priority": details["priority"],
                "runs": details["runs"],
                "connections": self.get_connections(name)
            }
            for name, details in self.networks.items()
        }

    # Activity log
    def log(self, message):
        self.activity_log.append({
            "message": str(message),
            "time": self._time()
        })

        # Keep the latest 1000 entries
        if len(self.activity_log) > 1000:
            self.activity_log = self.activity_log[-1000:]

    @staticmethod
    def _time():
        return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    manager = BHNetworkManager()

    manager.register("math", object(), "Mathematics specialist", 8)
    manager.register("language", object(), "Language specialist", 6)

    manager.connect("math", "language")

    print("Networks:", manager.list_networks())
    print("Connections:", manager.get_connections("math"))
    print("BH Network Manager ready!")
