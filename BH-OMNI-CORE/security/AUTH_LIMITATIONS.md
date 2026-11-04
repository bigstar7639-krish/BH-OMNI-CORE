# Auth - Argon2id Limitations - Phase 1 Step 3
Date: 2026-11-03

## Implementation
- Argon2id: time_cost=3, memory_cost=65536 (64MB), parallelism=4, hash_len=32, salt_len=16, type=ID
- PHC format: $argon2id$v=19$m=65536,t=3,p=4$salt$hash
- Random salt each hash - Same password -> different hashes
- Never log password or hash

## Limitations - NOT Production-Grade Without Verification
1. Rate limiting: NOT in auth.py - Need Step 6 Guardian - Brute-force protection required in production
2. MFA: NOT in auth.py - Need Step 4 TOTP - Password alone is not enough for production
3. Session: NOT in auth.py - Need Step 6 Sessions - After verify, need JWT session
4. Password policy: Min 8 chars, max 1024 - In production, need stronger policy + breach check (HaveIBeenPwned)
5. Storage: Hashes must be stored in secure DB, not in plaintext file - No DB in this demo
6. Timing: Argon2 verify is timing-safe for hash comparison, but overall flow needs constant-time handling
7. Production: DO NOT CLAIM production-grade without real security assessment, penetration test, OWASP, etc.
8. Android Keystore: Not used for password hashing - Password hashing is server-side, not keystore

## Input Validation
- Password: str, not None, not empty, 8-1024 chars
- Hash: str, not None, not empty, must start with $argon2id$
- Wrong password -> False, not exception
- Invalid hash format -> AuthError safely, no password exposure
- Corrupted hash -> False or AuthError safely

## Tests
- See test_phase1_step3.py - 8 tests
