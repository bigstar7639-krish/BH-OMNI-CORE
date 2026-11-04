
import base64
import hashlib
import json
import os
from pathlib import Path
from typing import List, Optional

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    AESGCM = None
    InvalidTag = Exception

class VaultError(Exception):
    pass

class VaultManager:
    """
    Secure Vault - Phase 1 Step 5
    - Master password -> PBKDF2-HMAC-SHA256, 600k iterations, 32-byte key, 16-byte salt
    - Each secret: AES-256-GCM, 12-byte nonce, unique per secret
    - File: JSON {salt, entries: {key: {n, c}}, version}
    - Lock: clears in-memory key, unlock requires password
    - Never log secrets or master password
    - Change password: re-encrypt all entries with new key
    """
    def __init__(self, vault_path=None, master_password: Optional[str] = None):
        if not CRYPTO_AVAILABLE:
            raise VaultError("cryptography not available - BLOCKED")
        self.vault_path = Path(vault_path) if vault_path else Path(__file__).parent / "vault_data.json"
        self._key = None
        self._salt = None
        self._locked = True
        self._entries = {}
        # Load existing vault file if exists, else create empty
        if self.vault_path.exists():
            try:
                data = json.loads(self.vault_path.read_text(encoding="utf-8"))
                self._salt = base64.b64decode(data.get("salt", ""))
                self._entries = data.get("entries", {})
                if not isinstance(self._entries, dict):
                    raise VaultError("Corrupted vault - entries not dict")
                if len(self._salt) != 16:
                    raise VaultError("Corrupted vault - invalid salt")
            except VaultError:
                raise
            except Exception as e:
                raise VaultError(f"Corrupted vault file - Cannot load: {type(e).__name__}") from e
        else:
            # New vault - generate salt
            self._salt = os.urandom(16)
            self._entries = {}
            self._save_file()  # Save empty vault with salt
        if master_password is not None:
            self.unlock(master_password)

    def _validate_password(self, password):
        if password is None:
            raise VaultError("Master password cannot be None")
        if not isinstance(password, str):
            raise VaultError("Master password must be str")
        if len(password) == 0:
            raise VaultError("Master password cannot be empty")
        if len(password) < 8:
            raise VaultError("Master password too short - Min 8 chars")
        if len(password) > 1024:
            raise VaultError("Master password too long")
        return True

    def _validate_key_name(self, key):
        if key is None:
            raise VaultError("Key cannot be None")
        if not isinstance(key, str):
            raise VaultError("Key must be str")
        if len(key.strip()) == 0:
            raise VaultError("Key cannot be empty")
        if len(key) > 128:
            raise VaultError("Key too long - Max 128")
        # No path traversal, no null bytes
        if "/" in key or "\\" in key or "\x00" in key or ".." in key:
            raise VaultError("Invalid key - No path characters")
        return key.strip()

    def _validate_value(self, value):
        if value is None:
            raise VaultError("Value cannot be None")
        if not isinstance(value, str):
            raise VaultError("Value must be str")
        if len(value) == 0:
            raise VaultError("Value cannot be empty")
        if len(value) > 100000:
            raise VaultError("Value too long - Max 100k")
        return True

    def _derive_key(self, password: str, salt: bytes) -> bytes:
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 600000, dklen=32)

    def _save_file(self):
        data = {"version": "v1", "salt": base64.b64encode(self._salt).decode(), "entries": self._entries}
        # Atomic write via temp
        tmp = self.vault_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.rename(self.vault_path)

    def _require_unlocked(self):
        if self._locked or self._key is None:
            raise VaultError("Vault is locked - Unlock first")

    def unlock(self, password: str) -> bool:
        self._validate_password(password)
        derived = self._derive_key(password, self._salt)
        # Verify by trying to decrypt one entry if exists, else store verification token
        # For empty vault, we store a verification entry on first unlock? Instead, check via test decrypt of verification
        # Simpler: If vault has verification entry, verify it. If not, create it on first store.
        # For now, set key and try to decrypt all entries to verify - if any fails, wrong password
        self._key = derived
        self._locked = False
        # Verify: try decrypt all entries - if any fails, wrong password
        try:
            for k in list(self._entries.keys()):
                if k == "__verify__":
                    continue
                self._decrypt_entry(k)
            # Also verify __verify__ if exists
            if "__verify__" in self._entries:
                self._decrypt_entry("__verify__")
            else:
                # First time: create verification entry so future wrong passwords are detected
                # Only if vault is empty or no verify yet - create it now
                if len(self._entries) == 0:
                    self._encrypt_and_store("__verify__", "BH-OMNI-CORE-VAULT-VERIFY")
                    self._save_file()
                else:
                    # Vault has entries but no verify - create verify for future
                    self._encrypt_and_store("__verify__", "BH-OMNI-CORE-VAULT-VERIFY")
                    self._save_file()
            return True
        except VaultError:
            # Wrong password - lock again
            self._key = None
            self._locked = True
            raise VaultError("Wrong master password - Cannot unlock") from None

    def lock(self):
        self._key = None
        self._locked = True

    def is_locked(self) -> bool:
        return self._locked

    def _encrypt_and_store(self, key: str, value: str):
        nonce = os.urandom(12)
        aesgcm = AESGCM(self._key)
        ct = aesgcm.encrypt(nonce, value.encode("utf-8"), None)
        self._entries[key] = {"n": base64.b64encode(nonce).decode(), "c": base64.b64encode(ct).decode()}

    def _decrypt_entry(self, key: str) -> str:
        rec = self._entries.get(key)
        if rec is None:
            raise VaultError(f"Key not found: {key}")
        try:
            nonce = base64.b64decode(rec["n"])
            ct = base64.b64decode(rec["c"])
        except Exception:
            raise VaultError("Corrupted entry - Invalid base64") from None
        if len(nonce) != 12:
            raise VaultError("Corrupted entry - Invalid nonce")
        try:
            aesgcm = AESGCM(self._key)
            pt = aesgcm.decrypt(nonce, ct, None)
            return pt.decode("utf-8")
        except InvalidTag:
            raise VaultError("Decryption failed - Wrong password or tampered") from None
        except Exception as e:
            raise VaultError(f"Decryption failed: {type(e).__name__}") from e

    def store(self, key: str, value: str) -> bool:
        self._require_unlocked()
        key = self._validate_key_name(key)
        self._validate_value(value)
        if key == "__verify__":
            raise VaultError("Reserved key")
        try:
            self._encrypt_and_store(key, value)
            self._save_file()
            return True
        except VaultError:
            raise
        except Exception as e:
            raise VaultError(f"Store failed: {type(e).__name__}") from e

    def retrieve(self, key: str) -> str:
        self._require_unlocked()
        key = self._validate_key_name(key)
        if key == "__verify__":
            raise VaultError("Reserved key")
        return self._decrypt_entry(key)

    def delete(self, key: str) -> bool:
        self._require_unlocked()
        key = self._validate_key_name(key)
        if key not in self._entries:
            raise VaultError(f"Key not found: {key}")
        del self._entries[key]
        self._save_file()
        return True

    def list_keys(self) -> List[str]:
        self._require_unlocked()
        # Never return values, only key names, exclude __verify__
        return sorted([k for k in self._entries.keys() if k != "__verify__"])

    def has_key(self, key: str) -> bool:
        self._require_unlocked()
        key = self._validate_key_name(key)
        return key in self._entries

    def change_password(self, old_password: str, new_password: str) -> bool:
        self._validate_password(old_password)
        self._validate_password(new_password)
        if old_password == new_password:
            raise VaultError("New password must differ from old")
        # Verify old password by unlocking
        # Save current state
        if not self._locked:
            # Already unlocked - verify old password matches current key
            old_key = self._derive_key(old_password, self._salt)
            if old_key != self._key:
                raise VaultError("Wrong old password")
        else:
            self.unlock(old_password)
        # Decrypt all entries with old key
        plain = {}
        for k in list(self._entries.keys()):
            if k == "__verify__":
                continue
            plain[k] = self._decrypt_entry(k)
        # Generate new salt + key, re-encrypt
        new_salt = os.urandom(16)
        new_key = self._derive_key(new_password, new_salt)
        self._salt = new_salt
        self._key = new_key
        self._entries = {}
        for k, v in plain.items():
            self._encrypt_and_store(k, v)
        # Recreate verify
        self._encrypt_and_store("__verify__", "BH-OMNI-CORE-VAULT-VERIFY")
        self._save_file()
        self._locked = False
        return True

    def get_info(self) -> dict:
        return {"locked": self._locked, "entries_count": len([k for k in self._entries if k != "__verify__"]), "version": "v1", "kdf": "PBKDF2-HMAC-SHA256-600k", "cipher": "AES-256-GCM"}
