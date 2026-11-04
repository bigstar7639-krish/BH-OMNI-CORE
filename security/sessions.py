
import base64
import hashlib
import hmac
import json
import time
import secrets
from typing import Dict, List, Optional

class SessionError(Exception):
    pass

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")

def _b64url_decode(s: str) -> bytes:
    # Add padding
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def _jwt_encode(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h = _b64url_encode(json.dumps(header, separators=(",", ":")).encode())
    p = _b64url_encode(json.dumps(payload, separators=(",", ":")).encode())
    signing_input = f"{h}.{p}".encode()
    sig = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    return f"{h}.{p}.{_b64url_encode(sig)}"

def _jwt_decode(token: str, secret: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise SessionError("Invalid access token")
    h_b64, p_b64, sig_b64 = parts
    signing_input = f"{h_b64}.{p_b64}".encode()
    expected = hmac.new(secret.encode(), signing_input, hashlib.sha256).digest()
    try:
        given = _b64url_decode(sig_b64)
    except Exception:
        raise SessionError("Invalid access token") from None
    if not hmac.compare_digest(expected, given):
        raise SessionError("Invalid access token - Bad signature")
    try:
        payload = json.loads(_b64url_decode(p_b64).decode())
    except Exception:
        raise SessionError("Invalid access token - Bad payload") from None
    # Check header alg
    try:
        header = json.loads(_b64url_decode(h_b64).decode())
        if header.get("alg") != "HS256":
            raise SessionError("Invalid access token - Bad alg")
    except SessionError:
        raise
    except Exception:
        raise SessionError("Invalid access token - Bad header") from None
    return payload

class SessionManager:
    """
    Phase 1 Step 6 - Sessions - Manual JWT (no PyJWT dependency, avoids jwt module conflict)
    - Access Token: JWT HS256 manual, 15 min expiry
    - Refresh Token: Random opaque token (32 bytes), 7 days, rotation on every refresh
    - Reuse Detection: If old refresh token reused -> revoke ALL sessions for that user (breach)
    - Revocation: revoke_session + revoke_all_for_user
    - Never log tokens
    """
    def __init__(self, secret_key: Optional[str] = None, access_expiry_seconds: int = 900, refresh_expiry_seconds: int = 604800):
        if secret_key is None or not isinstance(secret_key, str) or len(secret_key) < 32:
            raise SessionError("Secret key must be >=32 chars - Use strong secret")
        self._secret = secret_key
        self._access_expiry = access_expiry_seconds
        self._refresh_expiry = refresh_expiry_seconds
        self._sessions: Dict[str, dict] = {}
        self._used_refresh: Dict[str, str] = {}

    def _hash_token(self, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _validate_user_id(self, user_id):
        if user_id is None or not isinstance(user_id, str) or len(user_id.strip()) == 0:
            raise SessionError("Invalid user_id")
        if len(user_id) > 128:
            raise SessionError("user_id too long")
        return user_id.strip()

    def create_session(self, user_id: str, roles: Optional[List[str]] = None) -> dict:
        user_id = self._validate_user_id(user_id)
        roles = roles or ["user"]
        if not isinstance(roles, list):
            raise SessionError("roles must be list")
        now = int(time.time())
        access_payload = {"sub": user_id, "roles": roles, "iat": now, "exp": now + self._access_expiry, "type": "access"}
        try:
            access_token = _jwt_encode(access_payload, self._secret)
        except Exception as e:
            raise SessionError(f"Access token creation failed: {type(e).__name__}") from e
        refresh_token = secrets.token_urlsafe(32)
        rh = self._hash_token(refresh_token)
        self._sessions[rh] = {"user_id": user_id, "roles": roles, "created_at": now, "expires_at": now + self._refresh_expiry, "revoked": False, "rotated": False}
        return {"access_token": access_token, "refresh_token": refresh_token, "user_id": user_id, "roles": roles, "access_expires_in": self._access_expiry}

    def validate_access_token(self, token: str) -> dict:
        if token is None or not isinstance(token, str) or len(token) == 0:
            raise SessionError("Invalid access token")
        payload = _jwt_decode(token, self._secret)
        # Check required fields
        if "exp" not in payload or "iat" not in payload or "sub" not in payload:
            raise SessionError("Invalid access token - Missing fields")
        if int(time.time()) > int(payload["exp"]):
            raise SessionError("Access token expired")
        if payload.get("type") != "access":
            raise SessionError("Not an access token - Refresh token cannot be used as access")
        return {"user_id": payload["sub"], "roles": payload.get("roles", []), "exp": payload["exp"]}

    def refresh_session(self, refresh_token: str) -> dict:
        if refresh_token is None or not isinstance(refresh_token, str) or len(refresh_token) == 0:
            raise SessionError("Invalid refresh token")
        rh = self._hash_token(refresh_token)
        if rh in self._used_refresh:
            victim_user = self._used_refresh[rh]
            self.revoke_all_for_user(victim_user)
            raise SessionError("Refresh token reuse detected - All sessions revoked for user")
        sess = self._sessions.get(rh)
        if sess is None:
            raise SessionError("Refresh token not found - Invalid or revoked")
        if sess.get("revoked"):
            raise SessionError("Refresh token revoked")
        if sess.get("rotated"):
            raise SessionError("Refresh token already rotated")
        if int(time.time()) > sess["expires_at"]:
            del self._sessions[rh]
            raise SessionError("Refresh token expired")
        user_id = sess["user_id"]
        roles = sess["roles"]
        self._used_refresh[rh] = user_id
        del self._sessions[rh]
        new_sess = self.create_session(user_id, roles)
        return new_sess

    def revoke_session(self, refresh_token: str) -> bool:
        if refresh_token is None or not isinstance(refresh_token, str):
            raise SessionError("Invalid refresh token")
        rh = self._hash_token(refresh_token)
        if rh in self._sessions:
            del self._sessions[rh]
            return True
        if rh in self._used_refresh:
            return True
        raise SessionError("Session not found")

    def revoke_all_for_user(self, user_id: str) -> int:
        user_id = self._validate_user_id(user_id)
        count = 0
        for rh in list(self._sessions.keys()):
            if self._sessions[rh].get("user_id") == user_id:
                del self._sessions[rh]
                count += 1
        return count

    def list_active_sessions(self, user_id: str) -> List[dict]:
        user_id = self._validate_user_id(user_id)
        out = []
        now = int(time.time())
        for rh, s in self._sessions.items():
            if s.get("user_id") == user_id and not s.get("revoked") and s["expires_at"] > now:
                out.append({"user_id": s["user_id"], "roles": s["roles"], "created_at": s["created_at"], "expires_at": s["expires_at"]})
        return out

    def get_info(self) -> dict:
        return {"active_sessions": len(self._sessions), "used_refresh_tracked": len(self._used_refresh), "access_expiry": self._access_expiry, "refresh_expiry": self._refresh_expiry, "alg": "HS256-manual-no-PyJWT"}
