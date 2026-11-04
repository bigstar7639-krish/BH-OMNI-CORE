# DEBUG P3H - Termux-la enna error nu full-a kaatum
from pathlib import Path
import sys, traceback
BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))
print("=== DEBUG P3H START ===")
try:
    from systems_fj.analytics import Analytics
    from systems_fj.insights import Insights
    print("Import OK")
    a = Analytics()
    print("Analytics() OK")
    a.track("u1", "app_open")
    print(f"track OK - total={a.total_events()}")
    ins = Insights()
    print("Insights() OK")
    r1 = ins.build(12, 2, {"app_open": 12}, {"u1": 6, "u2": 6})
    print(f"build HIGH: {r1}")
    r2 = ins.build(4, 2, {"app_open": 4}, {"u1": 2, "u2": 2})
    print(f"build MEDIUM: {r2}")
    print("DEBUG P3H: PASS - P3H logic works in Termux!")
except Exception as e:
    print(f"DEBUG P3H: FAIL - {type(e).__name__}: {e}")
    print("--- FULL TRACEBACK ---")
    traceback.print_exc()
    print("--- END TRACEBACK ---")
    # Also check file versions
    try:
        import systems_fj.analytics as am
        import systems_fj.insights as im
        print(f"analytics file: {am.__file__}")
        print(f"insights file: {im.__file__}")
    except Exception as e2:
        print(f"File check FAIL: {e2}")
print("=== DEBUG P3H END ===")
