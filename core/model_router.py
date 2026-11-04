
from typing import Dict, List, Optional

class RouterError(Exception):
    pass

class ModelRouter:
    """
    Phase 2 Step 4 - Model Router
    - Register model: {name, capabilities [chat, voice, image, code], cost_level 1-5, available bool}
    - Route: pick available model with capability + lowest cost
    - No capable model -> FAIL (not silent fallback to wrong model)
    - Fallback: explicit default model only if requested
    - Duplicate -> FAIL
    """
    def __init__(self):
        self._models: Dict[str, dict] = {}
        self._default: Optional[str] = None

    def _validate_name(self, name):
        if name is None or not isinstance(name, str) or len(name.strip()) == 0:
            raise RouterError("Invalid model name")
        if len(name) > 128:
            raise RouterError("Model name too long")
        return name.strip()

    def register(self, name: str, capabilities: List[str], cost_level: int = 3, available: bool = True, is_default: bool = False) -> bool:
        name = self._validate_name(name)
        if capabilities is None or not isinstance(capabilities, list) or len(capabilities) == 0:
            raise RouterError("Capabilities must be non-empty list")
        valid_caps = {"chat", "voice", "image", "code", "search", "story"}
        for c in capabilities:
            if c not in valid_caps:
                raise RouterError(f"Invalid capability: {c} - Must be {sorted(valid_caps)}")
        if cost_level is None or not isinstance(cost_level, int) or cost_level < 1 or cost_level > 5:
            raise RouterError("cost_level must be 1-5")
        if available is None or not isinstance(available, bool):
            raise RouterError("available must be bool")
        if name in self._models:
            raise RouterError(f"Duplicate model: {name}")
        self._models[name] = {"name": name, "capabilities": list(capabilities), "cost_level": cost_level, "available": available}
        if is_default:
            self._default = name
        return True

    def set_default(self, name: str) -> bool:
        name = self._validate_name(name)
        if name not in self._models:
            raise RouterError(f"Model not found: {name}")
        self._default = name
        return True

    def route(self, capability: str, prefer_low_cost: bool = True) -> dict:
        if capability is None or not isinstance(capability, str) or len(capability.strip()) == 0:
            raise RouterError("Invalid capability")
        cap = capability.strip()
        candidates = [m for m in self._models.values() if cap in m["capabilities"] and m["available"]]
        if not candidates:
            raise RouterError(f"No available model for capability: {cap}")
        # Sort by cost, then name for determinism
        candidates.sort(key=lambda m: (m["cost_level"], m["name"]) if prefer_low_cost else (m["name"],))
        chosen = candidates[0]
        return {"model": chosen["name"], "capability": cap, "cost_level": chosen["cost_level"]}

    def route_with_fallback(self, capability: str) -> dict:
        try:
            return self.route(capability)
        except RouterError:
            if self._default is None:
                raise RouterError(f"No model for {capability} and no default set") from None
            dm = self._models.get(self._default)
            if dm is None or not dm["available"]:
                raise RouterError(f"Default model unavailable: {self._default}") from None
            return {"model": self._default, "capability": capability, "cost_level": dm["cost_level"], "fallback": True}

    def list_models(self) -> List[dict]:
        return [dict(self._models[n]) for n in sorted(self._models.keys())]

    def get_info(self) -> dict:
        return {"models": len(self._models), "default": self._default, "principle": "Capability match + Lowest cost + Explicit fallback"}
