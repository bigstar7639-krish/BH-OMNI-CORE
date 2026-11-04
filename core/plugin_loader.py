
from typing import Dict, List, Callable, Optional

class PluginError(Exception):
    pass

class PluginLoader:
    """
    Phase 2 Step 2 - Plugin Loader
    - Manifest: {name, version, description, entry} - All required
    - Version format: X.Y.Z (e.g. 1.0.0)
    - Entry must be callable
    - Duplicate -> FAIL, Invalid manifest -> FAIL
    - Load / Unload with state tracking
    - Never auto-load unvalidated plugin
    """
    def __init__(self):
        self._plugins: Dict[str, dict] = {}
        self._loaded: Dict[str, bool] = {}

    def _validate_name(self, name):
        if name is None or not isinstance(name, str) or len(name.strip()) == 0:
            raise PluginError("Invalid plugin name")
        if len(name) > 128:
            raise PluginError("Plugin name too long")
        if "/" in name or "\\" in name or ".." in name:
            raise PluginError("Invalid plugin name - No path chars")
        return name.strip()

    def _validate_version(self, version):
        if version is None or not isinstance(version, str):
            raise PluginError("Invalid version - Must be str X.Y.Z")
        parts = version.strip().split(".")
        if len(parts) != 3:
            raise PluginError(f"Invalid version: {version} - Must be X.Y.Z")
        for p in parts:
            if not p.isdigit():
                raise PluginError(f"Invalid version: {version} - Parts must be numbers")
        return version.strip()

    def register(self, manifest: dict) -> bool:
        if manifest is None or not isinstance(manifest, dict):
            raise PluginError("Manifest must be dict")
        for field in ["name", "version", "description", "entry"]:
            if field not in manifest:
                raise PluginError(f"Manifest missing field: {field}")
        name = self._validate_name(manifest["name"])
        version = self._validate_version(manifest["version"])
        desc = manifest["description"]
        entry = manifest["entry"]
        if desc is None or not isinstance(desc, str) or len(desc.strip()) == 0:
            raise PluginError("Invalid description")
        if len(desc) > 500:
            raise PluginError("Description too long")
        if entry is None or not callable(entry):
            raise PluginError("Entry must be callable")
        if name in self._plugins:
            raise PluginError(f"Duplicate plugin: {name}")
        self._plugins[name] = {"name": name, "version": version, "description": desc.strip(), "entry": entry}
        self._loaded[name] = False
        return True

    def unregister(self, name: str) -> bool:
        name = self._validate_name(name)
        if name not in self._plugins:
            raise PluginError(f"Plugin not found: {name}")
        if self._loaded.get(name):
            raise PluginError(f"Cannot unregister loaded plugin: {name} - Unload first")
        del self._plugins[name]
        del self._loaded[name]
        return True

    def load(self, name: str):
        name = self._validate_name(name)
        if name not in self._plugins:
            raise PluginError(f"Plugin not found: {name}")
        if self._loaded.get(name):
            raise PluginError(f"Plugin already loaded: {name}")
        try:
            result = self._plugins[name]["entry"]()
        except Exception as e:
            raise PluginError(f"Plugin entry failed: {name} - {type(e).__name__}: {str(e)[:200]}") from e
        self._loaded[name] = True
        return result

    def unload(self, name: str) -> bool:
        name = self._validate_name(name)
        if name not in self._plugins:
            raise PluginError(f"Plugin not found: {name}")
        if not self._loaded.get(name):
            raise PluginError(f"Plugin not loaded: {name}")
        self._loaded[name] = False
        return True

    def is_loaded(self, name: str) -> bool:
        name = self._validate_name(name)
        if name not in self._plugins:
            raise PluginError(f"Plugin not found: {name}")
        return self._loaded.get(name, False)

    def list_plugins(self) -> List[dict]:
        out = []
        for name in sorted(self._plugins.keys()):
            p = self._plugins[name]
            out.append({"name": p["name"], "version": p["version"], "description": p["description"], "loaded": self._loaded.get(name, False)})
        return out

    def get_info(self) -> dict:
        loaded = sum(1 for v in self._loaded.values() if v)
        return {"total": len(self._plugins), "loaded": loaded, "principle": "Validate manifest + No auto-load"}
