
import hashlib
import hmac
import json
from pathlib import Path
from typing import Dict, List

class BackupError(Exception):
    pass

class BackupVerifier:
    """
    Phase 1 Step 8 - Backup Verify - Signed Manifest
    - Manifest: {files: {relative_path: sha256}, created_at, signature}
    - Signature: HMAC-SHA256(manifest_without_signature, secret) - Detects manifest tampering
    - Verify: recompute file hashes + verify signature
    - Never include secrets in manifest
    """
    def __init__(self, secret_key: str):
        if secret_key is None or not isinstance(secret_key, str) or len(secret_key) < 32:
            raise BackupError("Backup secret must be >=32 chars")
        self._secret = secret_key

    def _file_sha256(self, file_path: Path) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    def create_manifest(self, base_dir, file_list: List[str]) -> dict:
        base = Path(base_dir)
        if not base.exists() or not base.is_dir():
            raise BackupError("Invalid base_dir")
        files = {}
        for rel in file_list:
            if rel is None or not isinstance(rel, str) or len(rel.strip()) == 0:
                raise BackupError("Invalid file in list")
            # Block path traversal
            if ".." in rel or rel.startswith("/") or rel.startswith("\\"):
                raise BackupError(f"Invalid file path: {rel}")
            fp = base / rel
            if not fp.exists() or not fp.is_file():
                raise BackupError(f"File not found: {rel}")
            files[rel] = self._file_sha256(fp)
        import time
        manifest = {"files": files, "created_at": int(time.time()), "version": "v1"}
        canonical = json.dumps(manifest, sort_keys=True, separators=(",", ":"))
        sig = hmac.new(self._secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()
        manifest["signature"] = sig
        return manifest

    def verify_manifest(self, base_dir, manifest: dict) -> dict:
        base = Path(base_dir)
        if not isinstance(manifest, dict) or "files" not in manifest or "signature" not in manifest:
            return {"valid": False, "message": "Invalid manifest - Missing files/signature"}
        stored_sig = manifest["signature"]
        # Verify signature first
        unsigned = {k: v for k, v in manifest.items() if k != "signature"}
        canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
        expected = hmac.new(self._secret.encode(), canonical.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected, stored_sig):
            return {"valid": False, "message": "Manifest signature invalid - Manifest tampered"}
        # Verify each file
        for rel, expected_hash in manifest["files"].items():
            fp = base / rel
            if not fp.exists():
                return {"valid": False, "message": f"Missing file: {rel}"}
            actual = self._file_sha256(fp)
            if actual != expected_hash:
                return {"valid": False, "message": f"File modified: {rel} - Hash mismatch"}
        return {"valid": True, "message": f"Backup valid - {len(manifest['files'])} files verified", "files": len(manifest["files"])}

    def get_info(self) -> dict:
        return {"hash": "SHA256", "signature": "HMAC-SHA256", "version": "v1"}
