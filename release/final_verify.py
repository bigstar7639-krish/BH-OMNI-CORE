
from pathlib import Path

def final_verify(base_path: str = "."):
    """
    Phase 5 Step 2 - Final Verify (Local)
    - Checks: .gitignore blocks secrets, no vault_data.json, VERSION + README exist,
      all 4 phase folders exist, test files count
    - Returns report, never crashes
    - This is LOCAL check only - GitHub verify needs `git log` in Termux
    """
    base = Path(base_path)
    checks = []
    def add(name, ok, detail=""):
        checks.append({"name": name, "status": "PASS" if ok else "FAIL", "detail": detail})

    # 1. .gitignore
    gi = base / ".gitignore"
    if gi.exists():
        txt = gi.read_text(errors="ignore")
        add("gitignore_exists", True, "Found")
        add("gitignore_blocks_vault", "vault_data.json" in txt, "vault_data.json blocked" if "vault_data.json" in txt else "NOT blocked!")
        add("gitignore_blocks_pycache", "__pycache__" in txt, "pycache blocked" if "__pycache__" in txt else "NOT blocked")
    else:
        add("gitignore_exists", False, "Missing .gitignore!")
        add("gitignore_blocks_vault", False, "No .gitignore")
        add("gitignore_blocks_pycache", False, "No .gitignore")

    # 2. No secrets in repo (local)
    vault = list(base.rglob("vault_data.json"))
    add("no_vault_data", len(vault) == 0, f"Found {len(vault)} vault files!" if vault else "Clean - No vault_data.json")

    # 3. VERSION + README
    add("version_exists", (base / "VERSION.txt").exists(), "VERSION.txt found" if (base / "VERSION.txt").exists() else "Missing!")
    add("readme_exists", (base / "README-BH-OMNI.md").exists(), "README found" if (base / "README-BH-OMNI.md").exists() else "Missing!")

    # 4. Phase folders
    for folder in ["security", "core", "systems_fj", "integration", "release"]:
        add(f"folder_{folder}", (base / folder).is_dir(), f"{folder}/ found" if (base / folder).is_dir() else f"{folder}/ MISSING!")

    # 5. Test files count - Should be 8+5+5+3+2 = 23 test files (Phase1 8 + Phase2 5 + Phase3 5 + Phase4 3 + Phase5 2)
    tests = list(base.glob("test_phase*.py"))
    add("test_files_count", len(tests) >= 20, f"Found {len(tests)} test files (expect >=20)")

    passed = sum(1 for c in checks if c["status"] == "PASS")
    failed = sum(1 for c in checks if c["status"] == "FAIL")
    return {"total": len(checks), "passed": passed, "failed": failed, "overall": "PASS" if failed == 0 else "FAIL", "checks": checks}
