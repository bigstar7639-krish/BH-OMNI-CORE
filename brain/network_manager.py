
from datetime import datetime, timezone


class BHNetworkManager:
    def __init__(self):
        self.networks = {}
        self.activity_log = []

    def register(self, name, network, description=""):
        name = str(name).strip()

        if not name or network is None:
            return False

        if name in self.networks:
            return False

        self.networks[name] = {
            "network": network,
            "description": description,
            "active": True
        }

        self.log(f"Registered: {name}")
        return True

    def activate(self, name):
        if name not in self.networks:
            return False

        self.networks[name]["active"] = True
        self.log(f"Activated: {name}")
        return True

    def deactivate(self, name):
        if name not in self.networks:
            return False

        self.networks[name]["active"] = False
        self.log(f"Deactivated: {name}")
        return True

    def remove(self, name):
        if name not in self.networks:
            return False

        del self.networks[name]
        self.log(f"Removed: {name}")
        return True

    def get_network(self, name):
        details = self.networks.get(name)

        if details is None:
            return None

        return details["network"]

    def get_active_networks(self):
        return {
            name: details["network"]
            for name, details in self.networks.items()
            if details["active"]
        }

    def list_networks(self):
        return {
            name: {
                "description": details["description"],
                "active": details["active"]
            }
            for name, details in self.networks.items()
        }

    def log(self, message):
        self.activity_log.append({
            "message": message,
            "time": datetime.now(timezone.utc).isoformat()
        })


if __name__ == "__main__":
    manager = BHNetworkManager()

    manager.register("math", object(), "Mathematics specialist")
    manager.register("language", object(), "Language specialist")

    print(manager.list_networks())
    print("BH Network Manager ready!")
