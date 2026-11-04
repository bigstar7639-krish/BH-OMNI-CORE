
import time
from typing import Dict, List, Optional

class HealthError(Exception):
    pass

VALID_STATUS = {"HEALTHY", "DEGRADED", "DOWN", "UNKNOWN"}

class ModuleHealthMonitor:
    """
    Phase 2 Step 2 - Module Health Monitor
    - Register module -> UNKNOWN initially
    - Report: HEALTHY / DEGRADED / DOWN
    - List unhealthy (DEGRADED + DOWN)
    - Uptime tracking per module
    - Unknown module -> FAIL (not silent)
    """
    def __init__(self):
        self._modules: Dict[str, dict] = {}

    def _validate_name(self, name):
        if name is None or not isinstance(name, str) or len(name.strip()) == 0:
            raise HealthError("Invalid module name")
        if len(name) > 128:
            raise HealthError("Module name too long")
        return name.strip()

    def register(self, name: str) -> bool:
        name = self._validate_name(name)
        if name in self._modules:
            raise HealthError(f"Duplicate module: {name}")
        self._modules[name] = {"status": "UNKNOWN", "last_check": int(time.time()), "registered_at": int(time.time()), "message": "Registered - Not checked yet", "checks": 0}
        return True

    def report(self, name: str, status: str, message: str = "") -> bool:
        name = self._validate_name(name)
        if name not in self._modules:
            raise HealthError(f"Module not found: {name} - Register first")
        if status not in VALID_STATUS:
            raise HealthError(f"Invalid status: {status} - Must be {sorted(VALID_STATUS)}")
        if message is None or not isinstance(message, str):
            raise HealthError("Message must be str")
        if len(message) > 500:
            raise HealthError("Message too long")
        self._modules[name]["status"] = status
        self._modules[name]["last_check"] = int(time.time())
        self._modules[name]["message"] = message or status
        self._modules[name]["checks"] += 1
        return True

    def get_status(self, name: str) -> dict:
        name = self._validate_name(name)
        if name not in self._modules:
            raise HealthError(f"Module not found: {name}")
        m = self._modules[name]
        return {"name": name, "status": m["status"], "last_check": m["last_check"], "message": m["message"], "checks": m["checks"], "uptime_seconds": int(time.time()) - m["registered_at"]}

    def list_unhealthy(self) -> List[dict]:
        out = []
        for name in sorted(self._modules.keys()):
            if self._modules[name]["status"] in ("DEGRADED", "DOWN"):
                out.append(self.get_status(name))
        return out

    def list_all(self) -> List[dict]:
        return [self.get_status(n) for n in sorted(self._modules.keys())]

    def is_healthy(self, name: str) -> bool:
        return self.get_status(name)["status"] == "HEALTHY"

    def get_info(self) -> dict:
        total = len(self._modules)
        healthy = sum(1 for m in self._modules.values() if m["status"] == "HEALTHY")
        return {"total": total, "healthy": healthy, "unhealthy": total - healthy, "principle": "Explicit status + No silent healthy"}
