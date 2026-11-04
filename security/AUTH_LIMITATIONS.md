# Auth - Argon2id Limitations - Phase 1 Step 3
Date: 2026-11-03

## Implementation
- Argon2id: time_cost=3, memory_cost=65536 (64MB), parallelism=4, hash_len=32, salt_len=16, type=ID
- PHC format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
- Random salt each time - Same password -> different hashes
- Never log password or hash

## Limitations - NOT Production-Grade Without Verification
1. Rate limiting: NOT in auth.py - Need Step 6 Guardian
2. MFA: NOT in auth.py - Need Step 4 TOTP
3. Session: NOT in auth.py - Need Step 6 Sessions
4. Password policy: Min 8 chars, max 1024 - Production needs stronger + breach check
5. Storage: Hashes must be in secure DB, not plaintext file
6. Production: DO NOT CLAIM production-grade without real security assessment
