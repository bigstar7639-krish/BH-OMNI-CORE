# Permissions - Limitations - Phase 1 Step 7
- Roles: guest, user, moderator, admin - Deny-by-default, Least-privilege
- Resource ownership: read_own/write_own for owner, read_all/write_all for admin only, delete always admin
- Admin assignment needs admin - Blocks privilege escalation
- Limitations:
  1. In-memory only - Roles lost on restart (production needs DB)
  2. No ABAC / fine-grained per-resource ACL in demo - Only owner vs admin
  3. No audit log of role changes in this file - Step 8 Audit Logs covers it
  4. Caller must enforce granted_by_is_admin correctly - This file checks flag, not caller identity
  5. No production claim without real assessment
