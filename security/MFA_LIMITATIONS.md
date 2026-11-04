# MFA - TOTP Limitations - Phase 1 Step 4
- TOTP: 6 digits, 30 sec, SHA1, RFC 6238, valid_window=1 (+-30 sec)
- Secret: Base32 32 chars, 160-bit, random via pyotp
- Backup codes: 10 codes, 8 chars, SHA256 hashed, single-use (single-use enforcement needs DB - not in this demo)
- Provisioning URI: otpauth://totp/ for Google Authenticator / Authy
- Limitations:
  1. No server storage - Secrets must be in secure DB, not plaintext
  2. No rate limiting - Need Step 6 Guardian for brute-force on 6-digit codes
  3. No backup code single-use enforcement without DB - Demo returns bool only
  4. Clock sync required - User phone time must be correct
  5. DO NOT CLAIM production-grade without real security assessment
  6. Never log secret or codes
