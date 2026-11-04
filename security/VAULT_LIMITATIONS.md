# Vault - Limitations - Phase 1 Step 5
- KDF: PBKDF2-HMAC-SHA256, 600k iterations, 16-byte salt, 32-byte key
- Cipher: AES-256-GCM, 12-byte nonce per secret
- File: vault_data.json - JSON with salt + encrypted entries
- Lock: clears in-memory key
- Limitations:
  1. No hardware keystore - Key derived from password in memory, not Android Keystore (future)
  2. No auto-lock timer - Manual lock only (Step 6 can add)
  3. No backup encryption beyond file - File must be backed up securely, not in plaintext Git (vault_data.json contains encrypted data only, but do NOT commit real secrets file to public Git!)
  4. vault_data.json in this demo is for testing - Real vault file must NOT be committed to public repo with real secrets
  5. DO NOT CLAIM production-grade without real assessment
  6. Never log secrets or master password
