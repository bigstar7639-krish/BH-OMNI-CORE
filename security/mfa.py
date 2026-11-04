
import base64
import hashlib
import os
import secrets
import time
from typing import List, Optional

try:
    import pyotp
    PYOTP_AVAILABLE = True
except ImportError:
    PYOTP_AVAILABLE = False
    pyotp = None


# Fallback TOTP using stdlib only - Used when pyotp not available (e.g. container test)
# RFC 6238: HMAC-SHA1, 30 sec, 6 digits
import hmac as _hmac
import hashlib as _hashlib
import struct as _struct
import base64 as _b64

def _fallback_random_base32():
    raw = secrets.token_bytes(20)  # 160-bit
    return _b64.b32encode(raw).decode().rstrip("=")

def _fallback_totp_at(secret, for_time, interval=30, digits=6):
    key = _b64.b32decode(secret.upper() + "=" * ((8 - len(secret) % 8) % 8))
    counter = int(for_time // interval)
    msg = _struct.pack(">Q", counter)
    h = _hmac.new(key, msg, _hashlib.sha1).digest()
    o = h[-1] & 0x0F
    code_int = (_struct.unpack(">I", h[o:o+4])[0] & 0x7FFFFFFF) % (10 ** digits)
    return f"{code_int:0{digits}d}"

def _fallback_totp_verify(secret, code, for_time, valid_window=1, interval=30, digits=6):
    for offset in range(-valid_window, valid_window + 1):
        t = for_time + offset * interval
        if _fallback_totp_at(secret, t, interval, digits) == code:
            return True
    return False


class MFAError(Exception):
    pass

class MFAManager:
    """
    TOTP MFA - Phase 1 Step 4
    - Secret: Base32, 32 chars (160-bit) via pyotp.random_base32()
    - Code: 6 digits, 30 sec window, SHA1 (RFC 6238 default)
    - Verify with valid_window=1 (allows +-30 sec clock skew)
    - Backup codes: 10 codes, 8 chars each, stored as SHA256 hashes, single-use
    - Provisioning URI: otpauth://totp/...
    - Never log secret or codes
    """
    def __init__(self, issuer="BH-OMNI-CORE"):
        # pyotp preferred, fallback to stdlib if missing - Both RFC 6238 compatible
        self.use_pyotp = PYOTP_AVAILABLE
        self.issuer = issuer

    def _validate_secret(self, secret):
        if secret is None:
            raise MFAError("Secret cannot be None")
        if not isinstance(secret, str):
            raise MFAError("Secret must be str")
        if len(secret) == 0:
            raise MFAError("Secret cannot be empty")
        # Must be Base32 chars A-Z2-7
        allowed = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        if any(c not in allowed for c in secret.upper()):
            raise MFAError("Invalid secret - Must be Base32 A-Z2-7")
        if len(secret) < 16:
            raise MFAError("Secret too short - Min 16 chars")
        return True

    def _validate_code(self, code):
        if code is None:
            raise MFAError("Code cannot be None")
        if not isinstance(code, str):
            # Allow int? Convert to str with leading zeros
            if isinstance(code, int):
                code = f"{code:06d}"
            else:
                raise MFAError("Code must be str")
        if len(code) != 6:
            raise MFAError("Code must be 6 digits")
        if not code.isdigit():
            raise MFAError("Code must be digits only")
        return code

    def generate_secret(self) -> str:
        try:
            secret = pyotp.random_base32() if self.use_pyotp else _fallback_random_base32()
            # Ensure 32 chars
            if len(secret) != 32:
                # pyotp returns 32 by default, but enforce
                secret = secret[:32] if len(secret) > 32 else secret
            self._validate_secret(secret)
            return secret
        except MFAError:
            raise
        except Exception as e:
            raise MFAError(f"Secret generation failed: {type(e).__name__}") from e

    def get_totp(self, secret: str):
        self._validate_secret(secret)
        if self.use_pyotp:
            return pyotp.TOTP(secret, interval=30, digits=6)
        return None

    def generate_code(self, secret: str, for_time: Optional[int] = None) -> str:
        self._validate_secret(secret)
        try:
            if self.use_pyotp:
                totp = self.get_totp(secret)
                if for_time is not None:
                    return totp.at(for_time)
                return totp.now()
            else:
                t = for_time if for_time is not None else int(time.time())
                return _fallback_totp_at(secret, t)
        except MFAError:
            raise
        except Exception as e:
            raise MFAError(f"Code generation failed: {type(e).__name__}") from e

    def verify_code(self, secret: str, code: str, valid_window: int = 1, for_time: Optional[int] = None) -> bool:
        try:
            code = self._validate_code(code)
        except MFAError:
            return False
        try:
            self._validate_secret(secret)
        except MFAError:
            raise MFAError("Invalid secret - Cannot verify") from None
        try:
            if self.use_pyotp:
                totp = self.get_totp(secret)
                if for_time is not None:
                    return totp.verify(code, for_time=for_time, valid_window=valid_window)
                return totp.verify(code, valid_window=valid_window)
            else:
                t = for_time if for_time is not None else int(time.time())
                return _fallback_totp_verify(secret, code, t, valid_window)
        except Exception:
            return False

    def get_provisioning_uri(self, secret: str, username: str) -> str:
        self._validate_secret(secret)
        if not username or not isinstance(username, str):
            raise MFAError("Username must be non-empty str")
        if len(username) > 64:
            raise MFAError("Username too long")
        try:
            if self.use_pyotp:
                totp = self.get_totp(secret)
                uri = totp.provisioning_uri(name=username, issuer_name=self.issuer)
            else:
                # Manual otpauth URI - RFC 6238 compatible with Google Authenticator
                from urllib.parse import quote
                label = f"{self.issuer}:{username}"
                uri = f"otpauth://totp/{quote(label)}?secret={secret}&issuer={quote(self.issuer)}&algorithm=SHA1&digits=6&period=30"
            if not uri.startswith("otpauth://totp/"):
                raise MFAError("Invalid provisioning URI")
            return uri
        except MFAError:
            raise
        except Exception as e:
            raise MFAError(f"URI generation failed: {type(e).__name__}") from e

    def generate_backup_codes(self, count: int = 10) -> List[str]:
        if count < 1 or count > 20:
            raise MFAError("Backup code count must be 1-20")
        codes = []
        for _ in range(count):
            # 8 chars, alphanumeric without confusing chars (no 0/O, 1/I)
            alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
            code = "".join(secrets.choice(alphabet) for _ in range(8))
            # Format XXXX-XXXX for readability
            code = f"{code[:4]}-{code[4:]}"
            codes.append(code)
        # Must be unique
        if len(set(codes)) != len(codes):
            return self.generate_backup_codes(count)
        return codes

    def hash_backup_code(self, code: str) -> str:
        if not code or not isinstance(code, str):
            raise MFAError("Backup code must be non-empty str")
        # Normalize: remove hyphen, uppercase
        norm = code.replace("-", "").upper()
        return hashlib.sha256(norm.encode()).hexdigest()

    def verify_backup_code(self, code: str, stored_hashes: List[str]) -> bool:
        if not code or not isinstance(code, str):
            return False
        if not stored_hashes or not isinstance(stored_hashes, list):
            return False
        try:
            h = self.hash_backup_code(code)
            return h in stored_hashes
        except Exception:
            return False

    def get_params(self) -> dict:
        return {"issuer": self.issuer, "digits": 6, "interval": 30, "algorithm": "SHA1", "type": "TOTP"}
