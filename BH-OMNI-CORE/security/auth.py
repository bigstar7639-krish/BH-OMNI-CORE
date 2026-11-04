
import os
import re
from typing import Optional

try:
    from argon2 import PasswordHasher
    from argon2.low_level import Type
    from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError
    ARGON2_AVAILABLE = True
except ImportError:
    ARGON2_AVAILABLE = False
    PasswordHasher = None
    VerifyMismatchError = Exception
    VerificationError = Exception
    InvalidHashError = Exception

class AuthError(Exception):
    pass

class AuthManager:
    """
    Argon2id Authentication - Phase 1 Step 3
    Parameters: time_cost=3, memory_cost=65536 (64MB), parallelism=4, hash_len=32, salt_len=16, type=ID
    - Never log password or hash in production logs
    - Validate inputs, handle wrong password, corrupted hash, invalid format safely
    - Limitations: No rate limiting here (Step 6 Guardian), no MFA here (Step 4), no session here (Step 6)
    """
    def __init__(self, time_cost=3, memory_cost=65536, parallelism=4, hash_len=32, salt_len=16):
        if not ARGON2_AVAILABLE:
            raise AuthError("argon2-cffi not available - BLOCKED for production")
        self.time_cost = time_cost
        self.memory_cost = memory_cost
        self.parallelism = parallelism
        self.hash_len = hash_len
        self.salt_len = salt_len
        self.hasher = PasswordHasher(
            time_cost=time_cost,
            memory_cost=memory_cost,
            parallelism=parallelism,
            hash_len=hash_len,
            salt_len=salt_len,
            type=Type.ID,
        )
        # Argon2id PHC format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash

    def _validate_password(self, password):
        if password is None:
            raise AuthError("Password cannot be None")
        if not isinstance(password, str):
            raise AuthError("Password must be str")
        if len(password) == 0:
            raise AuthError("Password cannot be empty")
        if len(password) < 8:
            raise AuthError("Password too short - Must be at least 8 chars")
        if len(password) > 1024:
            raise AuthError("Password too long - Max 1024 chars")
        return True

    def _validate_hash_format(self, password_hash):
        if password_hash is None:
            raise AuthError("Hash cannot be None")
        if not isinstance(password_hash, str):
            raise AuthError("Hash must be str")
        if len(password_hash) == 0:
            raise AuthError("Hash cannot be empty")
        # Must start with $argon2id$
        if not password_hash.startswith("$argon2id$"):
            raise AuthError("Invalid hash format - Must start with $argon2id$")
        return True

    def hash_password(self, password: str) -> str:
        """Hash password with Argon2id - Generates random salt each time"""
        self._validate_password(password)
        try:
            # Never log password!
            password_hash = self.hasher.hash(password)
            # Validate generated hash format
            if not password_hash.startswith("$argon2id$"):
                raise AuthError("Generated hash has invalid format")
            return password_hash
        except AuthError:
            raise
        except Exception as e:
            raise AuthError(f"Hashing failed: {type(e).__name__}") from e

    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify password against hash - Returns True/False, never raises for wrong password
        - Wrong password -> False (not exception)
        - Invalid hash format -> Raises AuthError safely (no password exposure)
        - Corrupted hash -> False or AuthError safely
        """
        # Validate password (but for verify, if password invalid, return False safely? For security, raise for None/empty)
        try:
            self._validate_password(password)
        except AuthError:
            # For verify, invalid password format -> return False, don't leak details
            return False
        try:
            self._validate_hash_format(password_hash)
        except AuthError as e:
            # Invalid hash format - Raise safely, don't expose password
            raise AuthError(f"Invalid hash format - Cannot verify") from e
        try:
            self.hasher.verify(password_hash, password)
            return True
        except VerifyMismatchError:
            # Wrong password - Expected, return False safely
            return False
        except VerificationError:
            # Verification error - Could be corrupted hash - Return False safely
            return False
        except InvalidHashError:
            # Invalid hash - Raise safely
            raise AuthError("Invalid hash - Corrupted or malformed") from None
        except Exception as e:
            # Other errors - Return False safely, don't expose password
            return False

    def needs_rehash(self, password_hash: str) -> bool:
        """Check if hash needs rehash due to parameter change - For migration"""
        try:
            self._validate_hash_format(password_hash)
            return self.hasher.check_needs_rehash(password_hash)
        except AuthError:
            raise
        except Exception:
            return True

    def get_params(self) -> dict:
        """Return params without secrets - For audit, no password/hash"""
        return {
            "time_cost": self.time_cost,
            "memory_cost": self.memory_cost,
            "parallelism": self.parallelism,
            "hash_len": self.hash_len,
            "salt_len": self.salt_len,
            "type": "Argon2id",
        }
