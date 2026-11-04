
from typing import List, Dict, Set, Optional

class PermissionError(Exception):
    pass

# Role -> Permissions - Least Privilege by design
# guest: minimal read-only, user: own data, moderator: moderate + user, admin: all
ROLE_PERMISSIONS = {
    "guest": {"read_public"},
    "user": {"read_public", "read_own", "write_own", "use_ai", "use_voice", "use_vault"},
    "moderator": {"read_public", "read_own", "write_own", "use_ai", "use_voice", "use_vault", "moderate_content", "read_reports"},
    "admin": {"read_public", "read_own", "write_own", "use_ai", "use_voice", "use_vault", "moderate_content", "read_reports", "manage_users", "manage_system", "read_all", "write_all", "delete_all", "manage_security"},
}

ALL_PERMISSIONS = set().union(*ROLE_PERMISSIONS.values())

# Admin-only permissions - Never granted to non-admin via role escalation
ADMIN_ONLY = {"manage_users", "manage_system", "manage_security", "delete_all", "read_all", "write_all"}

class PermissionManager:
    """
    Phase 1 Step 7 - Permission Enforcement
    - Deny by default - No permission unless explicitly granted via role
    - Least privilege - guest minimal, user own-data only
    - Role assignment only via admin (enforced by caller - check_admin method)
    - Resource ownership: read_own/write_own only for owner, read_all/write_all only admin
    - Never grant ADMIN_ONLY to non-admin
    """
    def __init__(self):
        # user_id -> set of roles
        self._user_roles: Dict[str, Set[str]] = {}
        # user_id -> set of extra direct permissions (rare, explicit grant)
        self._direct_perms: Dict[str, Set[str]] = {}

    def _validate_user_id(self, user_id):
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise PermissionError("Invalid user_id")
        if len(user_id) > 128:
            raise PermissionError("user_id too long")
        return user_id.strip()

    def _validate_role(self, role):
        if role is None or not isinstance(role, str) or role not in ROLE_PERMISSIONS:
            raise PermissionError(f"Invalid role: {role} - Valid: {sorted(ROLE_PERMISSIONS.keys())}")
        return role

    def _validate_permission(self, perm):
        if perm is None or not isinstance(perm, str) or perm not in ALL_PERMISSIONS:
            raise PermissionError(f"Invalid permission: {perm}")
        return perm

    def assign_role(self, user_id: str, role: str, granted_by_is_admin: bool = False) -> bool:
        user_id = self._validate_user_id(user_id)
        role = self._validate_role(role)
        # Admin role can only be assigned by admin - prevents privilege escalation
        if role == "admin" and not granted_by_is_admin:
            raise PermissionError("Admin role can only be assigned by admin - Privilege escalation blocked")
        if user_id not in self._user_roles:
            self._user_roles[user_id] = set()
        self._user_roles[user_id].add(role)
        return True

    def revoke_role(self, user_id: str, role: str) -> bool:
        user_id = self._validate_user_id(user_id)
        role = self._validate_role(role)
        if user_id not in self._user_roles or role not in self._user_roles[user_id]:
            raise PermissionError(f"User does not have role: {role}")
        self._user_roles[user_id].discard(role)
        return True

    def get_roles(self, user_id: str) -> List[str]:
        user_id = self._validate_user_id(user_id)
        return sorted(list(self._user_roles.get(user_id, set())))

    def get_permissions(self, user_id: str) -> List[str]:
        user_id = self._validate_user_id(user_id)
        perms = set()
        for r in self._user_roles.get(user_id, set()):
            perms.update(ROLE_PERMISSIONS.get(r, set()))
        perms.update(self._direct_perms.get(user_id, set()))
        return sorted(list(perms))

    def has_permission(self, user_id: str, permission: str) -> bool:
        user_id = self._validate_user_id(user_id)
        permission = self._validate_permission(permission)
        # Deny by default
        perms = set(self.get_permissions(user_id))
        return permission in perms

    def require_permission(self, user_id: str, permission: str):
        if not self.has_permission(user_id, permission):
            raise PermissionError(f"Access denied - User {user_id} lacks permission: {permission}")

    def grant_direct_permission(self, user_id: str, permission: str, granted_by_is_admin: bool = False) -> bool:
        user_id = self._validate_user_id(user_id)
        permission = self._validate_permission(permission)
        # ADMIN_ONLY direct grant needs admin
        if permission in ADMIN_ONLY and not granted_by_is_admin:
            raise PermissionError("Admin-only permission can only be granted by admin")
        if user_id not in self._direct_perms:
            self._direct_perms[user_id] = set()
        self._direct_perms[user_id].add(permission)
        return True

    def revoke_direct_permission(self, user_id: str, permission: str) -> bool:
        user_id = self._validate_user_id(user_id)
        permission = self._validate_permission(permission)
        if user_id not in self._direct_perms or permission not in self._direct_perms[user_id]:
            raise PermissionError(f"User does not have direct permission: {permission}")
        self._direct_perms[user_id].discard(permission)
        return True

    def can_access_resource(self, user_id: str, action: str, resource_owner_id: str) -> bool:
        """
        Resource ownership check:
        - action: read / write / delete
        - If user is owner: need read_own/write_own
        - If user is NOT owner: need read_all/write_all/delete_all (admin only)
        - delete_own not exist - delete requires admin delete_all (safe default)
        """
        user_id = self._validate_user_id(user_id)
        resource_owner_id = self._validate_user_id(resource_owner_id)
        if action not in ("read", "write", "delete"):
            raise PermissionError(f"Invalid action: {action}")
        is_owner = (user_id == resource_owner_id)
        if action == "read":
            if is_owner:
                return self.has_permission(user_id, "read_own")
            else:
                return self.has_permission(user_id, "read_all")
        elif action == "write":
            if is_owner:
                return self.has_permission(user_id, "write_own")
            else:
                return self.has_permission(user_id, "write_all")
        elif action == "delete":
            # Delete always requires admin delete_all - even owner cannot delete via own perms
            return self.has_permission(user_id, "delete_all")
        return False

    def is_admin(self, user_id: str) -> bool:
        user_id = self._validate_user_id(user_id)
        return "admin" in self._user_roles.get(user_id, set())

    def get_info(self) -> dict:
        return {"roles": sorted(ROLE_PERMISSIONS.keys()), "total_permissions": len(ALL_PERMISSIONS), "users_tracked": len(self._user_roles), "principle": "Deny-by-default + Least-privilege"}
