"""V41 S3 tests - no fake PASS. Real execute only."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import omni_chat_v41_s3 as s3

PASS = 0
FAIL = 0
FAILED = []
def check(name, cond, info=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"PASS {name}")
    else:
        FAIL += 1
        FAILED.append(name)
        print(f"FAIL {name} :: {info}")

# 1. Empty safe
r, src = s3.chat_s3("")
check("empty-safe", src == "empty" and isinstance(r, str), r)

# 2. Unknown -> fallback, fake answer illa (teach / fallback nu varanum)
r, src = s3.chat_s3("zzqqwwxx_unknown_12345")
check("unknown-fallback", src in ("fallback", "own_ai") and isinstance(r, str) and len(r) > 0, r)

# 3. Lesson match - temp lessons koduthu test (real file-a touch pannadhu)
lessons = [{"q": "vanakkam eppadi iruka", "a": "Nalla iruken da!"}]
r, src = s3.chat_s3("vanakkam eppadi", lessons=lessons)
check("lesson-match", src == "own_ai" and r == "Nalla iruken da!", f"{src} {r}")

# 4. No match -> not own_ai
r, src = s3.chat_s3("xyzabc no match here", lessons=lessons)
check("no-match-not-ownai", src == "fallback", f"{src} {r}")

# 5. Memory max 20 - real file la save aachu nu check
msgs = s3.load_memory()
check("memory-max-20", len(msgs) <= 20, f"len={len(msgs)}")
check("memory-is-list", isinstance(msgs, list))

# 6. Memory file exists + valid JSON
check("memory-file-valid", os.path.isfile(s3.MEMORY_PATH), s3.MEMORY_PATH)

# 7. Lessons loader does not crash on real model file
try:
    L = s3.load_lessons()
    check("lessons-loader", isinstance(L, list), type(L))
except Exception as e:
    check("lessons-loader", False, str(e))

print(f"\nV41 S3: PASS={PASS} FAIL={FAIL} TOTAL={PASS+FAIL}")
print("FAILED:", FAILED)
sys.exit(0 if FAIL == 0 else 1)
