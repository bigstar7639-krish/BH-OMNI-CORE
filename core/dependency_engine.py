
from typing import Dict, List, Set

class DependencyError(Exception):
    pass

class DependencyEngine:
    """
    Phase 2 Step 1 - Dependency Engine
    - Register modules with dependencies
    - Topological sort for load order
    - Missing dependency -> FAIL (not silent)
    - Circular dependency -> FAIL with cycle path
    - Duplicate registration -> FAIL
    - Never auto-skip missing modules
    """
    def __init__(self):
        self._modules: Dict[str, List[str]] = {}

    def _validate_name(self, name):
        if name is None or not isinstance(name, str) or len(name.strip()) == 0:
            raise DependencyError("Invalid module name")
        if len(name) > 128:
            raise DependencyError("Module name too long")
        if "/" in name or "\\" in name or ".." in name:
            raise DependencyError("Invalid module name - No path chars")
        return name.strip()

    def register(self, name: str, dependencies: List[str] = None) -> bool:
        name = self._validate_name(name)
        deps = dependencies or []
        if not isinstance(deps, list):
            raise DependencyError("dependencies must be list")
        for d in deps:
            self._validate_name(d)
            if d == name:
                raise DependencyError(f"Module cannot depend on itself: {name}")
        if name in self._modules:
            raise DependencyError(f"Duplicate module: {name} - Already registered")
        self._modules[name] = list(deps)
        return True

    def unregister(self, name: str) -> bool:
        name = self._validate_name(name)
        if name not in self._modules:
            raise DependencyError(f"Module not found: {name}")
        del self._modules[name]
        return True

    def list_modules(self) -> List[str]:
        return sorted(list(self._modules.keys()))

    def get_dependencies(self, name: str) -> List[str]:
        name = self._validate_name(name)
        if name not in self._modules:
            raise DependencyError(f"Module not found: {name}")
        return list(self._modules[name])

    def resolve_order(self) -> List[str]:
        # Check missing dependencies first
        all_deps = set()
        for deps in self._modules.values():
            all_deps.update(deps)
        missing = sorted([d for d in all_deps if d not in self._modules])
        if missing:
            raise DependencyError(f"Missing dependencies: {missing} - Register them first")
        # Topological sort - DFS with cycle detection
        visited: Set[str] = set()
        visiting: Set[str] = set()
        order: List[str] = []
        path: List[str] = []
        def dfs(node: str):
            if node in visited:
                return
            if node in visiting:
                # Cycle found - build cycle path
                idx = path.index(node) if node in path else 0
                cycle = path[idx:] + [node]
                raise DependencyError(f"Circular dependency detected: {' -> '.join(cycle)}")
            visiting.add(node)
            path.append(node)
            for dep in self._modules.get(node, []):
                dfs(dep)
            path.pop()
            visiting.discard(node)
            visited.add(node)
            order.append(node)
        for mod in sorted(self._modules.keys()):
            dfs(mod)
        return order

    def get_info(self) -> dict:
        return {"modules": len(self._modules), "principle": "Explicit deps + Fail on missing/circular"}
