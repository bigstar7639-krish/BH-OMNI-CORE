
from typing import Dict

class SecureIntegrationError(Exception):
    pass

class SecureGateway:
    """
    Phase 4 Step 2 - Security + Core Integration
    - Wires PermissionManager (Phase 1 Step 7) + SecureAPIGateway (Phase 2 Step 3)
    - Request flow: user_id -> get permissions from PermissionManager -> gateway checks route permission -> handler
    - No direct gateway call without permission check - This class enforces it
    - Unknown user (no roles) -> 403, unknown route -> 404, handler crash -> 500 (no leak)
    - Wiring only - No new auth logic
    """
    def __init__(self, perm_manager, gateway):
        if perm_manager is None or gateway is None:
            raise SecureIntegrationError("PermissionManager + Gateway both required")
        self.perm = perm_manager
        self.gateway = gateway

    def register_route(self, path: str, method: str, required_permission: str, handler) -> bool:
        try:
            return self.gateway.register_route(path, method, required_permission, handler)
        except Exception as e:
            raise SecureIntegrationError(f"Route register failed: {e}") from e

    def request(self, user_id: str, path: str, method: str, payload: dict = None) -> dict:
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            return {"status": 403, "error": "Forbidden - Invalid user_id"}
        user_id = user_id.strip()
        try:
            perms = self.perm.get_permissions(user_id)
        except Exception:
            return {"status": 403, "error": "Forbidden - Cannot resolve permissions"}
        # Gateway does 404/403/200/500
        return self.gateway.handle_request(path, method, perms, payload or {})

    def get_info(self) -> dict:
        return {"principle": "PermissionManager -> Gateway - No bypass"}
