# Sessions + Rate Limit - Limitations - Phase 1 Step 6
- Access JWT: HS256, 15 min, PyJWT, secret >=32 chars
- Refresh: Opaque random token, 7 days, rotation on every refresh, reuse detection revokes ALL sessions
- Rate Limit: Sliding window, in-memory only - Resets on restart (production needs Redis / persistent store)
- Brute-force: 5 fails -> 15 min lockout, in-memory only
- Limitations:
  1. No persistent session store - Sessions lost on restart (demo)
  2. No device fingerprint / IP binding in demo
  3. No persistent TOTP replay - Step 6 does NOT claim persistent replay protection (needs DB - future)
  4. Secret must be stored in Vault (Step 5), not hardcoded - Demo test uses test secret only
  5. No production claim without real assessment
  6. Never log tokens
