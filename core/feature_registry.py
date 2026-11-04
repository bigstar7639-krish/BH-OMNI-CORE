
from typing import Dict, List, Optional

class RegistryError(Exception):
    pass

class FeatureRegistry:
    """
    Phase 2 Step 3 - Unique Feature Registry
    - Feature: {id F-001, name, category, module}
    - ID must be F-XXX format (F-001 to F-999)
    - Duplicate ID -> FAIL, Duplicate name (same category) -> FAIL
    - List by category, search by module
    - Preserves Phase 0 baseline: 350 features concept - This registry prevents duplicates going forward
    """
    def __init__(self):
        self._features: Dict[str, dict] = {}  # id -> feature
        self._names: Dict[str, str] = {}  # "category::name_lower" -> id

    def _validate_id(self, fid):
        if fid is None or not isinstance(fid, str):
            raise RegistryError("Invalid feature ID")
        fid = fid.strip().upper()
        if not fid.startswith("F-"):
            raise RegistryError(f"Invalid feature ID: {fid} - Must be F-XXX")
        num = fid[2:]
        if not num.isdigit() or len(num) != 3:
            raise RegistryError(f"Invalid feature ID: {fid} - Must be F-001 to F-999")
        if int(num) < 1 or int(num) > 999:
            raise RegistryError(f"Invalid feature ID: {fid} - Out of range")
        return fid

    def _validate_str(self, val, field, max_len=128):
        if val is None or not isinstance(val, str) or len(val.strip()) == 0:
            raise RegistryError(f"Invalid {field}")
        if len(val.strip()) > max_len:
            raise RegistryError(f"{field} too long")
        return val.strip()

    def register(self, fid: str, name: str, category: str, module: str) -> bool:
        fid = self._validate_id(fid)
        name = self._validate_str(name, "name")
        category = self._validate_str(category, "category")
        module = self._validate_str(module, "module")
        if fid in self._features:
            raise RegistryError(f"Duplicate feature ID: {fid}")
        name_key = f"{category.lower()}::{name.lower()}"
        if name_key in self._names:
            raise RegistryError(f"Duplicate feature name in category: {name} in {category} - Already {self._names[name_key]}")
        self._features[fid] = {"id": fid, "name": name, "category": category, "module": module}
        self._names[name_key] = fid
        return True

    def get(self, fid: str) -> dict:
        fid = self._validate_id(fid)
        if fid not in self._features:
            raise RegistryError(f"Feature not found: {fid}")
        return dict(self._features[fid])

    def list_by_category(self, category: str) -> List[dict]:
        category = self._validate_str(category, "category")
        return [dict(f) for f in self._features.values() if f["category"].lower() == category.lower()]

    def list_by_module(self, module: str) -> List[dict]:
        module = self._validate_str(module, "module")
        return [dict(f) for f in self._features.values() if f["module"].lower() == module.lower()]

    def list_all(self) -> List[dict]:
        return [dict(self._features[fid]) for fid in sorted(self._features.keys())]

    def count(self) -> int:
        return len(self._features)

    def get_info(self) -> dict:
        cats = len(set(f["category"] for f in self._features.values()))
        return {"total": len(self._features), "categories": cats, "principle": "Unique ID + Unique name per category"}
