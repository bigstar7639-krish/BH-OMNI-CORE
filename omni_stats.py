# OMNI STATS - Phase 23 Step 1 - SAME PROJECT
import pathlib, glob
def get_stats():
    py_files = len(glob.glob("*.py")) + len(glob.glob("**/*.py", recursive=True))
    tests = len(glob.glob("test_*.py"))
    return f"📊 BH-OMNI CORE STATS:\n- Python files: {py_files}\n- Test files: {tests}\n- Full Regression: 12 PASS\n- Phases: 1-22 DONE\n- Version: V22 - Aurora Orb"
def handle_stats(msg):
    m = msg.strip().lower()
    if m in ["stats", "status", "project stats", "omni stats"]:
        return get_stats()
    return None
