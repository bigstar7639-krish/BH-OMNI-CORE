# Core Architecture - Limitations - Phase 2 Step 1
- DependencyEngine: Topological sort, missing/circular detection, duplicate rejection
- EventBus: Safe delivery, error isolation, depth guard, delivery report
- Limitations:
  1. In-memory only - No persistent module registry in demo
  2. No async event delivery - Sync only (future)
  3. No event persistence / replay - Future Step
  4. No production claim without real assessment
  5. Preserve mod_01-mod_32 - This core does NOT modify them, only orders them
