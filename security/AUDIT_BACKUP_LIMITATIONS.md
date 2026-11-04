# Audit + Backup - Limitations - Phase 1 Step 8
- Audit: Append-only JSONL, SHA256 hash chain, prev_hash linkage, verify_chain detects tamper/reorder
- Backup: SHA256 per file + HMAC-SHA256 signed manifest
- Limitations:
  1. Audit log file can be deleted if attacker has file access - Hash chain detects tampering, not deletion (production needs remote / immutable log store)
  2. No log rotation in demo - File grows (production needs rotation)
  3. Backup verifier checks files in base_dir only - Does not check ZIP integrity beyond manifest
  4. Secrets must NEVER be logged - Basic blocklist check in audit.log(), not exhaustive
  5. No production claim without real assessment
  6. Phase 1 COMPLETE after this step - 8/8 steps!
