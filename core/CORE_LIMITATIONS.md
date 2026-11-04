# Core Architecture - Limitations - Phase 2 Step 1
- DependencyEngine: Topological sort, missing/circular detection, duplicate rejection
- EventBus: Safe delivery, error isolation, depth guard, delivery report
- Limitations:
  1. In-memory only - No persistent module registry in demo
  2. No async event delivery - Sync only (future)
  3. No event persistence / replay - Future Step
  4. No production claim without real assessment
  5. Preserve mod_01-mod_32 - This core does NOT modify them, only orders them

## Step 3 - Gateway + Registry
- Gateway: 404/403/200/500, no internal error leak, permission check per route
- Registry: F-XXX IDs, duplicate ID/name blocked
- Limitations: In-memory only, no JWT validation in gateway (Step 6 Session must be checked by caller), no persistent registry
