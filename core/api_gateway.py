
from typing import Dict, List, Callable, Optional

class GatewayError(Exception):
    pass

class SecureAPIGateway:
    """
    Phase 2 Step 3 - Secure API Gateway
    - Register route: {path, method, required_permission, handler}
    - Handle request: 404 if route missing, 403 if permission missing, 200 if ok, 500 if handler fails (no leak)
    - Path must start with /, method GET/POST/PUT/DELETE
    - Handler must be callable
    - Never expose internal error details - Generic 500 message only
    """
    def __init__(self):
        self._routes: Dict[str, dict] = {}  # "METHOD:/path" -> route

    def _validate_path(self, path):
        if path is None or not isinstance(path, str) or len(path.strip()) == 0:
            raise GatewayError("Invalid path")
        path = path.strip()
        if not path.startswith("/"):
            raise GatewayError("Path must start with /")
        if len(path) > 256:
            raise GatewayError("Path too long")
        if ".." in path or "\\" in path:
            raise GatewayError("Invalid path - No traversal")
        return path

    def _validate_method(self, method):
        if method is None or not isinstance(method, str):
            raise GatewayError("Invalid method")
        m = method.strip().upper()
        if m not in ("GET", "POST", "PUT", "DELETE"):
            raise GatewayError(f"Invalid method: {method} - Must be GET/POST/PUT/DELETE")
        return m

    def register_route(self, path: str, method: str, required_permission: str, handler: Callable) -> bool:
        path = self._validate_path(path)
        method = self._validate_method(method)
        if required_permission is None or not isinstance(required_permission, str) or len(required_permission.strip()) == 0:
            raise GatewayError("Invalid required_permission")
        if handler is None or not callable(handler):
            raise GatewayError("Handler must be callable")
        key = f"{method}:{path}"
        if key in self._routes:
            raise GatewayError(f"Duplicate route: {key}")
        self._routes[key] = {"path": path, "method": method, "required_permission": required_permission.strip(), "handler": handler}
        return True

    def handle_request(self, path: str, method: str, user_permissions: List[str], payload: dict = None) -> dict:
        try:
            path = self._validate_path(path)
            method = self._validate_method(method)
        except GatewayError:
            return {"status": 400, "error": "Bad Request - Invalid path/method"}
        if user_permissions is None or not isinstance(user_permissions, list):
            return {"status": 403, "error": "Forbidden - Invalid permissions"}
        key = f"{method}:{path}"
        route = self._routes.get(key)
        if route is None:
            return {"status": 404, "error": "Not Found - Route does not exist"}
        if route["required_permission"] not in user_permissions:
            return {"status": 403, "error": f"Forbidden - Missing permission: {route['required_permission']}"}
        try:
            result = route["handler"](payload or {})
            return {"status": 200, "data": result}
        except Exception:
            # Never leak internal error
            return {"status": 500, "error": "Internal Error - Handler failed"}

    def list_routes(self) -> List[dict]:
        out = []
        for k in sorted(self._routes.keys()):
            r = self._routes[k]
            out.append({"path": r["path"], "method": r["method"], "required_permission": r["required_permission"]})
        return out

    def get_info(self) -> dict:
        return {"routes": len(self._routes), "principle": "Deny by default + No error leak"}
