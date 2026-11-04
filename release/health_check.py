
"""
Phase 5 Step 1 - Release Health Check
- Tries to import every module - Reports MISSING / OK per module
- Never crashes on missing module - Reports it
"""
IMPORTS = [
    ("security.permissions", "PermissionManager"),
    ("core.feature_registry", "FeatureRegistry"),
    ("core.api_gateway", "SecureAPIGateway"),
    ("systems_fj.voice_engine", "VoiceEngine"),
    ("systems_fj.story_engine", "StoryEngine"),
    ("systems_fj.ads_engine", "AdsEngine"),
    ("systems_fj.monetization", "Monetization"),
    ("systems_fj.analytics", "Analytics"),
    ("systems_fj.insights", "Insights"),
    ("systems_fj.sync_engine", "SyncEngine"),
    ("systems_fj.backup_manager", "BackupManager"),
    ("systems_fj.marketplace", "Marketplace"),
    ("systems_fj.creator_hub", "CreatorHub"),
    ("integration.app_orchestrator", "AppOrchestrator"),
    ("integration.secure_gateway", "SecureGateway"),
    ("integration.full_regression", "run_regression"),
]

def health_check():
    results = []
    for mod_name, attr in IMPORTS:
        try:
            mod = __import__(mod_name, fromlist=[attr])
            obj = getattr(mod, attr)
            assert obj is not None
            results.append({"module": mod_name, "status": "OK"})
        except Exception as e:
            results.append({"module": mod_name, "status": "MISSING", "error": f"{type(e).__name__}: {str(e)[:80]}"})
    ok = sum(1 for r in results if r["status"] == "OK")
    missing = [r for r in results if r["status"] == "MISSING"]
    return {"total": len(results), "ok": ok, "missing": len(missing), "overall": "PASS" if len(missing) == 0 else "FAIL", "details": results, "missing_modules": [m["module"] for m in missing]}
