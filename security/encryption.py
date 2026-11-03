
import os
import json
import base64
import threading
from datetime import datetime, timedelta
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    AESGCM = None
    InvalidTag = Exception

class EncryptionError(Exception):
    pass

class KeyManager:
    def __init__(self, keys_file=None):
        self.keys_file = Path(keys_file) if keys_file else Path(__file__).parent / 'keys.json'
        self._keys = {}
        self._current_version = None
        self._load_keys()
    
    def _load_keys(self):
        if self.keys_file.exists():
            try:
                data = json.loads(self.keys_file.read_text(encoding='utf-8'))
                self._keys = data.get('keys', {})
                self._current_version = data.get('current_version')
            except:
                self._keys = {}
                self._current_version = None
        if not self._keys:
            self._generate_new_key("v1", True)
    
    def _save_keys(self):
        data = {"keys": self._keys, "current_version": self._current_version, "last_updated": datetime.now().isoformat()}
        temp = self.keys_file.with_suffix('.tmp')
        temp.write_text(json.dumps(data, indent=2), encoding='utf-8')
        temp.rename(self.keys_file)
    
    def _generate_new_key(self, version, is_initial=False):
        if not CRYPTO_AVAILABLE:
            raise EncryptionError("cryptography lib not available")
        key_bytes = os.urandom(32)
        key_b64 = base64.b64encode(key_bytes).decode()
        self._keys[version] = {"key_b64": key_b64, "created_at": datetime.now().isoformat(), "is_active": True}
        self._current_version = version
        self._save_keys()
        return version
    
    def get_current_key(self):
        if not self._current_version or self._current_version not in self._keys:
            raise EncryptionError("No current key")
        key_bytes = base64.b64decode(self._keys[self._current_version]["key_b64"])
        if len(key_bytes) != 32:
            raise EncryptionError("Invalid key length")
        return self._current_version, key_bytes
    
    def get_key_by_version(self, version):
        if version not in self._keys:
            raise EncryptionError(f"Unknown key version: {version}")
        key_bytes = base64.b64decode(self._keys[version]["key_b64"])
        if len(key_bytes) != 32:
            raise EncryptionError("Invalid key length")
        return key_bytes
    
    def rotate_key(self):
        if self._current_version and self._current_version.startswith('v'):
            try:
                num = int(self._current_version[1:])
                new_version = f"v{num+1}"
            except:
                new_version = f"v{len(self._keys)+1}"
        else:
            new_version = f"v{len(self._keys)+1}"
        self._generate_new_key(new_version, False)
        return new_version
    
    def list_versions(self):
        return {v: info.get("created_at") for v, info in self._keys.items()}

class NonceManager:
    def __init__(self):
        self._used_nonces = set()
        self._lock = threading.Lock()
    
    def generate_nonce(self):
        for _ in range(10):
            nonce = os.urandom(12)
            if len(nonce) != 12:
                raise EncryptionError("Invalid nonce length")
            nonce_b64 = base64.b64encode(nonce).decode()
            with self._lock:
                if nonce_b64 not in self._used_nonces:
                    self._used_nonces.add(nonce_b64)
                    if len(self._used_nonces) > 10000:
                        self._used_nonces.pop()
                    return nonce
        raise EncryptionError("Failed to generate unique nonce")

class AESGCMEncryption:
    def __init__(self, key_manager=None, nonce_manager=None):
        self.key_manager = key_manager or KeyManager()
        self.nonce_manager = nonce_manager or NonceManager()
        if not CRYPTO_AVAILABLE:
            raise EncryptionError("cryptography lib not available")
    
    def encrypt(self, plaintext, associated_data=None):
        if not isinstance(plaintext, bytes) or len(plaintext) == 0:
            raise EncryptionError("Invalid plaintext")
        version, key_bytes = self.key_manager.get_current_key()
        if len(key_bytes) != 32:
            raise EncryptionError("Invalid key length")
        nonce = self.nonce_manager.generate_nonce()
        if len(nonce) != 12:
            raise EncryptionError("Invalid nonce length")
        try:
            aesgcm = AESGCM(key_bytes)
            ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
            return {"v": version, "n": base64.b64encode(nonce).decode(), "c": base64.b64encode(ciphertext).decode()}
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {type(e).__name__}") from e
    
    def decrypt(self, encrypted_record, associated_data=None):
        if not isinstance(encrypted_record, dict) or "v" not in encrypted_record or "n" not in encrypted_record or "c" not in encrypted_record:
            raise EncryptionError("Invalid encrypted record")
        version = encrypted_record["v"]
        if not isinstance(version, str) or not version.startswith('v'):
            raise EncryptionError(f"Invalid version: {version}")
        try:
            nonce = base64.b64decode(encrypted_record["n"])
            ciphertext = base64.b64decode(encrypted_record["c"])
        except:
            raise EncryptionError("Invalid base64")
        if len(nonce) != 12:
            raise EncryptionError(f"Invalid nonce length: {len(nonce)}")
        if len(ciphertext) < 16:
            raise EncryptionError(f"Invalid ciphertext length")
        try:
            key_bytes = self.key_manager.get_key_by_version(version)
        except EncryptionError as e:
            raise EncryptionError(f"Unknown key version: {version}") from e
        if len(key_bytes) != 32:
            raise EncryptionError("Invalid key length")
        try:
            aesgcm = AESGCM(key_bytes)
            return aesgcm.decrypt(nonce, ciphertext, associated_data)
        except InvalidTag:
            raise EncryptionError("Decryption failed: Invalid tag - Wrong key or tampered") from None
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {type(e).__name__}") from e
