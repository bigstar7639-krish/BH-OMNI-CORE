# build_350_v13.py - BH-OMNI-CORE V13 FINAL SAFETY CORRECTION - FIXES ONLY LISTED AUDIT FINDINGS
# DO NOT RUN IN REAL BH-OMNI-CORE PROJECT. Run ONLY in a newly created isolated temp project.
# KNOWN LIMITATIONS / THREAT MODEL:
# - 350 genuine features NOT achievable in one stdlib builder. V13 = 60 IMPLEMENTED, 0 PARTIAL, 290 NOT IMPLEMENTED. Never claims 350/350.
# - No voice/image/weather/web-AI claimed. Only text/math/validation/encoding/date/list/dict/file-helpers.
# - Assistant did NOT execute this file. Status is NOT EXECUTED. No PASS claimed until user runs it in Termux in isolated temp project and sees real output.
# - Regression: isolation cannot be enforced in Termux Python, so ALL existing regression scripts are SKIPPED (never counted as passed).
# - Exclusion: __pycache__/*.pyc/.git/backup-*/backup_* excluded from BOTH snapshot and recursive backup at ALL levels via ONE function.
# - THREAT MODEL for rollback: manifest_v13.json and backup/.backup_meta.json are PLAIN LOCAL JSON files in the SAME trust domain.
#   They are NOT cryptographically trusted, NOT signed, and do NOT prove authenticity. A local writer who can modify one can modify the other.
#   Therefore backup_meta is only a CONSISTENCY check (manifest vs backup_meta vs actual backup file must all agree + backup NAME must match + resolved path must equal expected), never sole authorization.
#   Real authorization is: (a) path in RESTORE_ALLOWLIST (V13-owned outputs only), (b) path NOT protected, (c) triple SHA agreement, (d) strict manifest structure.
#   Rollback is best-effort local recovery, NOT a security boundary against a local attacker with write access to manifest+backup.
# Run ONLY in isolated temp project: mkdir -p ~/v13-test && cp ~/build_350_v13.py ~/v13-test/ && cd ~/v13-test && python3 build_350_v13.py
import os, sys, json, shutil, hashlib, datetime, pathlib, subprocess, math, re, base64, urllib.parse, tempfile, calendar, time, signal, stat
ROOT = pathlib.Path(".").resolve()
STAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = ROOT / f"backup-350-v13-{STAMP}"
GEN = ["omni_350_v13.py","test_v13.py","report_v13.json","REPORT_V13.md","manifest_v13.json","rollback_v13.sh"]
ALLOWLIST = set(GEN)
RESTORE_ALLOWLIST = set(GEN)
EXCLUDE_DIRS = {"__pycache__",".git"}
PROTECTED_EXACT = {"own_ai_model.json","own_ai_backup.json","omni_memory.json"}
PROTECTED_V40_V41 = {"omni_brain_full.py","omni_chat_v41.py","omni_own_ai.py","omni_own_ai_v2.py","omni_own_ai_v3.py","omni_own_ai_auto.py","own_ai_seed.py","own_ai_seed2.py","VERSION.txt","README.md"}
PROTECTED_PREFIXES = {f"mod_{i:02d}" for i in range(1,33)}
MIN_FREE_BYTES = 10 * 1024 * 1024
def sha(p):
    try:
        h=hashlib.sha256()
        with open(p,"rb") as f:
            for c in iter(lambda:f.read(8192),b""): h.update(c)
        return h.hexdigest()
    except Exception: return ""
def log(m): print(m, flush=True)
def is_protected(rel):
    if not isinstance(rel, str): return True
    parts=pathlib.Path(rel).parts
    if not parts: return True
    name=parts[-1]
    if parts[0] in PROTECTED_EXACT: return True
    if name in PROTECTED_EXACT: return True
    if name in PROTECTED_V40_V41: return True
    if "v40" in name.lower() or "v41" in name.lower(): return True
    if parts[0] in PROTECTED_PREFIXES: return True
    for prefix in PROTECTED_PREFIXES:
        if parts[0]==prefix or parts[0].startswith(prefix+".") or parts[0].startswith(prefix+"_"): return True
    if rel in PROTECTED_EXACT: return True
    return False
def is_excluded_rel(rel_parts):
    for part in rel_parts:
        if part in EXCLUDE_DIRS: return True
        if part.startswith("backup-") or part.startswith("backup_"): return True
    if rel_parts and str(rel_parts[-1]).endswith(".pyc"): return True
    return False
def is_excluded(p, base=ROOT):
    try: rel=p.relative_to(base)
    except Exception: return False
    return is_excluded_rel(rel.parts)
def validate_rel(rel, base=ROOT):
    if not isinstance(rel, str) or not rel: return False
    if os.path.isabs(rel): return False
    parts=pathlib.Path(rel).parts
    if any(p==".." for p in parts): return False
    if any(p=="" for p in parts): return False
    if is_protected(rel): return False
    cur=pathlib.Path(base)
    for part in parts[:-1]:
        cur=cur/part
        try:
            if cur.is_symlink():
                tgt=(cur.parent/os.readlink(cur)).resolve()
                try: tgt.relative_to(pathlib.Path(base).resolve())
                except ValueError: return False
        except OSError: return False
    try:
        parent=(pathlib.Path(base)/rel).parent.resolve(); parent.relative_to(pathlib.Path(base).resolve())
    except (ValueError, OSError, RuntimeError): return False
    return True
def validate_backup_rel(rel, base=ROOT):
    if not isinstance(rel, str) or not rel: return False
    if rel==".": return False
    if os.path.isabs(rel): return False
    parts=pathlib.Path(rel).parts
    if len(parts)!=1: return False
    name=parts[0]
    if not re.match(r"^backup-350-v1[123]-[0-9_]+$", name): return False
    if any(p==".." for p in parts): return False
    bpath=pathlib.Path(base)/rel
    try:
        if bpath.is_symlink(): return False
        cur=pathlib.Path(base)
        for part in parts:
            cur=cur/part
            if cur.is_symlink(): return False
        resolved=bpath.resolve(); resolved.relative_to(pathlib.Path(base).resolve())
    except (ValueError, OSError, RuntimeError): return False
    return True
def check_free_space(required=MIN_FREE_BYTES, path=ROOT):
    try:
        usage=shutil.disk_usage(str(path))
        return usage.free >= required
    except Exception:
        return False
def ensure_backup_not_exists(backup_dir):
    p=pathlib.Path(backup_dir)
    if p.exists() or p.is_symlink():
        return False
    return True
def validate_manifest_structure(m):
    if not isinstance(m, dict): return False, "manifest is not a dict"
    if not isinstance(m.get("backup"), str) or not m.get("backup"): return False, "manifest.backup missing/not str"
    before=m.get("before")
    if not isinstance(before, dict): return False, "manifest.before missing/not dict"
    for k,v in before.items():
        if not isinstance(k, str): return False, "before key not str"
        if not isinstance(v, dict): return False, f"before[{k!r}] not dict"
        if v.get("kind") not in ("file","symlink"): return False, f"before[{k!r}].kind invalid"
        if v.get("kind")=="file" and not isinstance(v.get("sha"), str): return False, f"before[{k!r}].sha not str"
        if v.get("kind")=="symlink" and not isinstance(v.get("target"), str): return False, f"before[{k!r}].target not str"
    for field in ("modified","deleted","created","intended"):
        if field in m and not isinstance(m[field], list): return False, f"manifest.{field} not list"
        if field in m:
            for item in m[field]:
                if not isinstance(item, str): return False, f"manifest.{field} entry not str"
    return True, "ok"
def py_compile_file(path):
    r=subprocess.run([sys.executable,"-m","py_compile",str(path)], capture_output=True, text=True)
    return r.returncode==0, r.stdout+r.stderr
def atomic_write(path, text, _fail=False, _sleep_before_replace=0, _ready_path=None):
    path=pathlib.Path(path); tmp=path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        tmp.write_text(text, encoding="utf-8")
        if _fail: raise RuntimeError("INJECTED_ATOMIC_FAILURE")
        if _ready_path is not None:
            pathlib.Path(_ready_path).write_text("READY", encoding="utf-8")
        if _sleep_before_replace: time.sleep(_sleep_before_replace)
        os.replace(tmp, path)
    except Exception:
        try:
            if tmp.exists(): tmp.unlink()
        except Exception: pass
        raise
def save_manifest_to(path, m):
    atomic_write(pathlib.Path(path), json.dumps(m, indent=2, ensure_ascii=False))
def save_manifest(m):
    save_manifest_to(ROOT/"manifest_v13.json", m)
def list_leftover_tmp_only():
    found=[]
    for gen in GEN:
        for tmp in ROOT.glob(f".{gen}.tmp-*"):
            if tmp.is_file(): found.append(tmp.name)
    return found
def recursive_backup(src_dir, dest_dir, base_root):
    src_dir=pathlib.Path(src_dir); dest_dir=pathlib.Path(dest_dir); base_root=pathlib.Path(base_root)
    for p in sorted(src_dir.iterdir()):
        try: relp=p.relative_to(base_root)
        except ValueError: continue
        if is_excluded_rel(relp.parts): continue
        # FIX: do NOT skip protected files in backup - backup must be complete for SHA verification.
        # Protection is enforced at modify/restore time, not at backup time.
        d=dest_dir/p.name
        if p.is_symlink(): os.symlink(os.readlink(p), d)
        elif p.is_dir(): d.mkdir(exist_ok=True); recursive_backup(p, d, base_root)
        elif p.is_file(): shutil.copy2(p, d)
def validate_backup_dir(backup):
    b=pathlib.Path(backup)
    try:
        if b.is_symlink(): return False
        if not b.is_dir(): return False
    except OSError: return False
    return True
def manifest_lifecycle_test():
    tmp=tempfile.mkdtemp(prefix="v13-manifest-")
    try:
        p=pathlib.Path(tmp)/"manifest_v13.json"
        m={"backup":"backup-350-v13-00000000_000000","intended":["a.py"],"created":[],"status":"STARTED"}
        save_manifest_to(p, m)
        loaded=json.loads(p.read_text(encoding="utf-8"))
        assert loaded["status"]=="STARTED"
        assert loaded["backup"]=="backup-350-v13-00000000_000000"
        loaded["created"].append("a.py"); loaded["status"]="VERIFIED"
        save_manifest_to(p, loaded)
        loaded2=json.loads(p.read_text(encoding="utf-8"))
        assert loaded2["created"]==["a.py"] and loaded2["status"]=="VERIFIED"
        assert loaded2["intended"]==["a.py"]
        log("MANIFEST LIFECYCLE TEST: create->save->load->mutate->save->load verified ok=True")
        return True
    finally: shutil.rmtree(tmp, ignore_errors=True)
def main():
    if (ROOT/"omni_memory.json").exists() and (ROOT/"own_ai_model.json").exists() and os.environ.get("BH_OMNI_ALLOW_REAL")!="1":
        log("FAIL: Refusing to run in real BH-OMNI-CORE project (omni_memory.json + own_ai_model.json present). Run ONLY in a newly created isolated temp project. Set BH_OMNI_ALLOW_REAL=1 only if you explicitly intend this."); sys.exit(11)
    ok, out = py_compile_file(pathlib.Path(__file__).resolve())
    if not ok:
        log(f"FAIL: python3 -m py_compile build_350_v13.py failed:\n{out}"); sys.exit(2)
    log("PY_COMPILE build_350_v13.py OK")
    if not check_free_space(MIN_FREE_BYTES, ROOT):
        log(f"FAIL: insufficient disk space - need >= {MIN_FREE_BYTES} bytes free before backup. Stopping safely, no files deleted."); sys.exit(5)
    log(f"DISK SPACE CHECK OK: >= {MIN_FREE_BYTES} bytes free")
    if not ensure_backup_not_exists(BACKUP_DIR):
        log(f"FAIL: backup path already exists: {BACKUP_DIR.name} - will NOT overwrite existing backup. Stopping safely."); sys.exit(6)
    log(f"BACKUP COLLISION CHECK OK: {BACKUP_DIR.name} does not exist")
    for g in GEN:
        p=ROOT/g
        if p.exists() or p.is_symlink():
            log(f"STOP: V13 output exists/symlink: {g} - will NOT overwrite."); sys.exit(10)
    leftover=list_leftover_tmp_only()
    log(f"LEFTOVER_TMP_PRESERVED (NOT deleted, V13 pattern only): {leftover}")
    log("=== V13 BUILDER (FINAL SAFETY CORRECTION) ==="); log("NO-OVERWRITE CHECK PASS"); log("EXCLUSION: __pycache__/*.pyc/.git/backup-*/backup_* excluded BOTH snapshot+recursive backup ALL levels")
    log("THREAT MODEL: manifest + backup_meta are plain local JSON in same trust domain, NOT cryptographically trusted. Restore requires allowlist + protected block + backup-name match + resolved-path match + triple SHA agreement + strict manifest structure.")
    if not manifest_lifecycle_test():
        log("FAIL manifest lifecycle"); sys.exit(3)
    before={}
    for p in ROOT.rglob("*"):
        if is_excluded(p, ROOT): continue
        if p.is_symlink(): before[str(p.relative_to(ROOT))]={"kind":"symlink","target":os.readlink(p)}
        elif p.is_file(): before[str(p.relative_to(ROOT))]={"kind":"file","sha":sha(p),"size":p.stat().st_size}
    log(f"SNAPSHOT BEFORE: {len(before)} entries")
    if BACKUP_DIR.is_symlink():
        log("FAIL: backup dir is symlink - STOP"); sys.exit(1)
    if not validate_backup_rel(BACKUP_DIR.name, ROOT):
        log("FAIL: backup path validation failed"); sys.exit(1)
    if not ensure_backup_not_exists(BACKUP_DIR):
        log(f"FAIL: backup path already exists (re-checked): {BACKUP_DIR.name} - will NOT overwrite."); sys.exit(6)
    BACKUP_DIR.mkdir(exist_ok=False)
    recursive_backup(ROOT, BACKUP_DIR, ROOT)
    backup_meta={"backup":BACKUP_DIR.name,"before":before,"note":"NOT cryptographically trusted. Plain local JSON consistency check only. backup name must equal manifest backup. See threat model."}
    save_manifest_to(BACKUP_DIR/".backup_meta.json", backup_meta)
    if not validate_backup_dir(BACKUP_DIR):
        log("FAIL: backup dir validation failed"); sys.exit(1)
    verify_fail=[]
    for rel,info in before.items():
        bp=BACKUP_DIR/rel
        if info["kind"]=="symlink":
            if not bp.is_symlink() or os.readlink(bp)!=info["target"]: verify_fail.append(rel)
        else:
            if not bp.is_file() or sha(bp)!=info["sha"]: verify_fail.append(rel)
    nested_leak=[]
    for p in BACKUP_DIR.rglob("*"):
        if p.name==".backup_meta.json": continue
        parts=pathlib.Path(str(p.relative_to(BACKUP_DIR))).parts
        if is_excluded_rel(parts): nested_leak.append(str(p.relative_to(BACKUP_DIR)))
    log(f"BACKUP {BACKUP_DIR.name} verify_fail={verify_fail} nested_leak={nested_leak}")
    if verify_fail or nested_leak: log("FAIL backup verification - STOP"); sys.exit(1)
    log("BACKUP VERIFIED SHA-256 + symlinks + nested exclusions + backup_meta consistency OK (not cryptographic trust)")
    manifest={"backup":BACKUP_DIR.name,"stamp":STAMP,"before":before,"intended":list(GEN),"created":[],"modified":[],"deleted":[],"status":"STARTED","exclusion":"__pycache__/*.pyc/.git/backup-*/backup_* excluded both, all levels","leftover_tmp_preserved":leftover,"allowlist":sorted(ALLOWLIST),"restore_allowlist":sorted(RESTORE_ALLOWLIST),"protected":["own_ai_model.json","own_ai_backup.json","omni_memory.json","mod_01..mod_32","V40/V41 files"],"threat_model":"manifest + backup_meta are plain local JSON in same trust domain, NOT cryptographically trusted. Restore requires allowlist + protected block + backup-name match + resolved-path match + triple SHA agreement + strict manifest structure."}
    save_manifest(manifest)
    RB = """#!/bin/bash
# rollback_v13.sh - SAFE: relative backup-350-v13-* only, RESTORE ALLOWLIST only, protected never restored/deleted.
# THREAT MODEL: manifest_v13.json and backup/.backup_meta.json are PLAIN LOCAL JSON in SAME trust domain, NOT cryptographically trusted.
# Restore requires: strict manifest structure + backup_meta.backup == manifest.backup + both point to same expected backup dir + NOT protected + validate_rel + manifest SHA == backup_meta SHA == actual backup file SHA.
# Defensive: never follow directory symlinks, never overwrite a directory or symlink path with a file, never delete a directory. No partial restoration: all validation happens before any restore/deletion.
set -e
if [ ! -f manifest_v13.json ]; then echo "FAIL manifest missing"; exit 1; fi
python3 - << 'PY'
import json, pathlib, shutil, hashlib, os, re, stat
try:
    m=json.load(open("manifest_v13.json"))
except Exception as e:
    print(f"FAIL malformed manifest JSON: {e} - refusing to restore"); raise SystemExit(1)
ROOT=pathlib.Path(".").resolve()
ALLOWLIST={"omni_350_v13.py","test_v13.py","report_v13.json","REPORT_V13.md","manifest_v13.json","rollback_v13.sh"}
RESTORE_ALLOWLIST={"omni_350_v13.py","test_v13.py","report_v13.json","REPORT_V13.md","manifest_v13.json","rollback_v13.sh"}
PROTECTED_EXACT={"own_ai_model.json","own_ai_backup.json","omni_memory.json"}
PROTECTED_V40_V41={"omni_brain_full.py","omni_chat_v41.py","omni_own_ai.py","omni_own_ai_v2.py","omni_own_ai_v3.py","omni_own_ai_auto.py","own_ai_seed.py","own_ai_seed2.py","VERSION.txt","README.md"}
PROTECTED_PREFIXES={f"mod_{i:02d}" for i in range(1,33)}
def fail(msg):
    print(f"FAIL {msg} - refusing to restore or delete anything"); raise SystemExit(1)
if not isinstance(m, dict): fail("manifest is not a dict")
if not isinstance(m.get("backup"), str) or not m.get("backup"): fail("manifest.backup missing/not str")
before=m.get("before")
if not isinstance(before, dict): fail("manifest.before missing/not dict")
for k,v in before.items():
    if not isinstance(k, str): fail("before key not str")
    if not isinstance(v, dict): fail(f"before[{k!r}] not dict")
    if v.get("kind") not in ("file","symlink"): fail(f"before[{k!r}].kind invalid")
    if v.get("kind")=="file" and not isinstance(v.get("sha"), str): fail(f"before[{k!r}].sha not str")
    if v.get("kind")=="symlink" and not isinstance(v.get("target"), str): fail(f"before[{k!r}].target not str")
for field in ("modified","deleted","created","intended"):
    if field in m:
        if not isinstance(m[field], list): fail(f"manifest.{field} not list")
        for item in m[field]:
            if not isinstance(item, str): fail(f"manifest.{field} entry not str")
    else:
        m[field]=[]
def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda: f.read(8192), b""): h.update(c)
    return h.hexdigest()
def is_protected(rel):
    if not isinstance(rel, str): return True
    parts=pathlib.Path(rel).parts
    if not parts: return True
    name=parts[-1]
    if parts[0] in PROTECTED_EXACT: return True
    if name in PROTECTED_EXACT: return True
    if name in PROTECTED_V40_V41: return True
    if "v40" in name.lower() or "v41" in name.lower(): return True
    if parts[0] in PROTECTED_PREFIXES: return True
    for prefix in PROTECTED_PREFIXES:
        if parts[0]==prefix or parts[0].startswith(prefix+".") or parts[0].startswith(prefix+"_"): return True
    return False
def validate_rel(rel, base=ROOT):
    if not isinstance(rel, str) or not rel: return False
    if os.path.isabs(rel): return False
    parts=pathlib.Path(rel).parts
    if any(p==".." for p in parts): return False
    if any(p=="" for p in parts): return False
    if is_protected(rel): return False
    cur=pathlib.Path(base)
    for part in parts[:-1]:
        cur=cur/part
        try:
            if cur.is_symlink():
                tgt=(cur.parent/os.readlink(cur)).resolve()
                try: tgt.relative_to(pathlib.Path(base).resolve())
                except ValueError: return False
        except OSError: return False
    try:
        parent=(pathlib.Path(base)/rel).parent.resolve(); parent.relative_to(pathlib.Path(base).resolve())
    except (ValueError, OSError, RuntimeError): return False
    return True
def validate_backup_rel(rel, base=ROOT):
    if not isinstance(rel, str) or not rel: return False
    if rel==".": return False
    if os.path.isabs(rel): return False
    parts=pathlib.Path(rel).parts
    if len(parts)!=1: return False
    if not re.match(r"^backup-350-v1[123]-[0-9_]+$", parts[0]): return False
    bpath=pathlib.Path(base)/rel
    try:
        if bpath.is_symlink(): return False
        cur=pathlib.Path(base)
        for part in parts:
            cur=cur/part
            if cur.is_symlink(): return False
        resolved=bpath.resolve(); resolved.relative_to(pathlib.Path(base).resolve())
    except (ValueError, OSError, RuntimeError): return False
    return True
def validate_symlink_target(rel, target):
    if os.path.isabs(target): return False
    try:
        resolved=((ROOT/rel).parent/target).resolve(); resolved.relative_to(ROOT.resolve()); return True
    except (ValueError, OSError, RuntimeError): return False
def parent_has_symlink(rel):
    cur=pathlib.Path(ROOT)
    for part in pathlib.Path(rel).parts[:-1]:
        cur=cur/part
        try:
            if cur.is_symlink(): return True
        except OSError: return True
    return False
def is_dir_or_symlink_to_dir(p):
    try:
        st=os.lstat(p)
    except OSError: return False
    if stat.S_ISDIR(st.st_mode): return True
    if stat.S_ISLNK(st.st_mode):
        try: return pathlib.Path(p).resolve().is_dir()
        except OSError: return True
    return False
def safe_unlink_file_only(p):
    try: st=os.lstat(p)
    except OSError: return False
    if stat.S_ISDIR(st.st_mode): return False
    if stat.S_ISLNK(st.st_mode):
        try:
            if pathlib.Path(p).resolve().is_dir(): return False
        except OSError: return False
    p.unlink(); return True
brel=m.get("backup","")
if not validate_backup_rel(brel, ROOT):
    print(f"FAIL backup path rejected: {brel} - refusing to restore"); raise SystemExit(1)
backup=ROOT/brel
if backup.is_symlink() or not backup.is_dir():
    print("FAIL backup dir is symlink or not a dir - refusing to restore"); raise SystemExit(1)
meta_path=backup/".backup_meta.json"
if not meta_path.is_file():
    print("FAIL backup_meta missing - refusing to restore"); raise SystemExit(1)
try: backup_meta=json.loads(meta_path.read_text(encoding="utf-8"))
except Exception as e:
    print(f"FAIL backup_meta unreadable: {e} - refusing"); raise SystemExit(1)
if not isinstance(backup_meta, dict): fail("backup_meta is not a dict")
if not isinstance(backup_meta.get("backup"), str): fail("backup_meta.backup missing/not str")
if not isinstance(backup_meta.get("before"), dict): fail("backup_meta.before missing/not dict")
if backup_meta.get("backup") != m.get("backup"):
    print(f"FAIL backup name mismatch: backup_meta.backup={backup_meta.get('backup')!r} != manifest.backup={m.get('backup')!r} - refusing to restore or delete anything"); raise SystemExit(1)
if not validate_backup_rel(backup_meta.get("backup"), ROOT):
    print("FAIL backup_meta.backup is not a valid backup dir name - refusing"); raise SystemExit(1)
try:
    if (ROOT / backup_meta.get("backup")).resolve() != backup.resolve():
        print("FAIL backup_meta and manifest do not point to same expected backup directory - refusing"); raise SystemExit(1)
except OSError as e:
    print(f"FAIL backup path resolution failed: {e} - refusing"); raise SystemExit(1)
trusted=backup_meta.get("before",{})
for rel in list(m.get("modified", [])) + list(m.get("deleted", [])):
    if is_protected(rel):
        print(f"SKIP protected {rel}: never overwrite protected file"); continue
    if rel not in RESTORE_ALLOWLIST:
        print(f"SKIP restore {rel}: not in RESTORE_ALLOWLIST (V13-owned outputs only)"); continue
    if not validate_rel(rel, ROOT):
        print(f"SKIP unsafe path {rel}"); continue
    if parent_has_symlink(rel):
        print(f"SKIP {rel}: parent path contains symlink - never follow unexpected directory/symlink"); continue
    orig=before.get(rel); trusted_orig=trusted.get(rel); src=backup/rel
    if orig is None or trusted_orig is None:
        print(f"SKIP {rel}: not in both manifest.before and backup_meta"); continue
    if orig!=trusted_orig:
        print(f"SKIP {rel}: manifest.before != backup_meta - tampered manifest or tampered backup_meta suspected"); continue
    if not validate_rel(rel, ROOT):
        print(f"SKIP unsafe path on re-check {rel}"); continue
    try:
        src_resolved=src.resolve(); src_resolved.relative_to(backup.resolve())
    except (ValueError, OSError, RuntimeError):
        if orig.get("kind")!="symlink":
            print(f"SKIP {rel}: backup source escapes backup root"); continue
    _target=pathlib.Path(rel)
    if is_dir_or_symlink_to_dir(_target):
        print(f"SKIP {rel}: target is directory or symlink to directory - never overwrite directory path"); continue
    if orig.get("kind")=="symlink":
        if not validate_symlink_target(rel, orig["target"]):
            print(f"SKIP symlink {rel}: target escapes project"); continue
        if src.is_symlink() and os.readlink(src)==orig["target"]:
            p=pathlib.Path(rel); p.parent.mkdir(parents=True, exist_ok=True)
            if parent_has_symlink(rel): print(f"SKIP {rel}: parent symlink on re-check"); continue
            if not validate_rel(rel, ROOT): print(f"SKIP {rel} re-check"); continue
            if not safe_unlink_file_only(p) and p.exists(): print(f"SKIP {rel}: cannot safely unlink target"); continue
            os.symlink(orig["target"], p); print(f"restored symlink {rel}")
        else: print(f"SKIP symlink {rel}: backup target mismatch vs manifest")
    else:
        actual_sha=sha(src) if src.is_file() else ""
        if src.is_file() and actual_sha==orig["sha"] and actual_sha==trusted_orig["sha"]:
            p=pathlib.Path(rel); p.parent.mkdir(parents=True, exist_ok=True)
            if parent_has_symlink(rel): print(f"SKIP {rel}: parent symlink on re-check"); continue
            if not validate_rel(rel, ROOT): print(f"SKIP {rel} re-check"); continue
            if is_dir_or_symlink_to_dir(p): print(f"SKIP {rel}: target became directory"); continue
            if not safe_unlink_file_only(p) and p.exists(): print(f"SKIP {rel}: cannot safely unlink target"); continue
            shutil.copy2(src, p); print(f"restored {rel} sha OK (triple agreement + backup-name match)")
        else: print(f"SKIP restore {rel}: SHA mismatch - manifest vs backup_meta vs actual backup file disagree (tamper suspected)")
for rel in list(m.get("created", [])) + list(m.get("intended", [])):
    if rel in ("manifest_v13.json","rollback_v13.sh"): continue
    if is_protected(rel):
        print(f"SKIP delete {rel}: protected"); continue
    if rel not in ALLOWLIST:
        print(f"SKIP delete {rel}: not in V13 allowlist"); continue
    if not validate_rel(rel, ROOT):
        print(f"SKIP unsafe path {rel}"); continue
    if parent_has_symlink(rel):
        print(f"SKIP delete {rel}: parent path contains symlink - never follow"); continue
    if rel in before:
        print(f"SKIP delete {rel}: pre-existing in before, never delete"); continue
    p=pathlib.Path(rel)
    try: os.lstat(p)
    except OSError: continue
    if is_dir_or_symlink_to_dir(p):
        print(f"SKIP delete {rel}: target is directory or symlink to directory - never delete directories"); continue
    if not validate_rel(rel, ROOT): print(f"SKIP {rel} re-check"); continue
    p.unlink(); print(f"deleted created/intended {rel}")
for gen in ["omni_350_v13.py","test_v13.py","report_v13.json","REPORT_V13.md","manifest_v13.json","rollback_v13.sh"]:
    for tmp in pathlib.Path(".").glob(f".{gen}.tmp-*"):
        print(f"preserved leftover tmp {tmp} - not auto-deleted (manual review)")
print("ROLLBACK DONE - only allowlisted genuinely-new V13 files removed, protected never touched, restores require allowlist + backup-name match + triple SHA agreement + strict manifest structure.")
PY
"""
    manifest["intended"].append("rollback_v13.sh"); save_manifest(manifest)
    atomic_write(ROOT/"rollback_v13.sh", RB); os.chmod("rollback_v13.sh", 0o755)
    manifest["created"].append("rollback_v13.sh"); save_manifest(manifest)
    log("RECOVERY MANIFEST + ROLLBACK CREATED BEFORE GENERATING")
    def track_created(name):
        if name not in manifest["created"]: manifest["created"].append(name)
        save_manifest(manifest)
    def pre_register(name):
        if name not in manifest["intended"]: manifest["intended"].append(name)
        save_manifest(manifest)
    pre_register("report_v13.json")
    if not check_free_space(MIN_FREE_BYTES, ROOT):
        log(f"FAIL: insufficient disk space before generation - need >= {MIN_FREE_BYTES} bytes free. Stopping safely, no files deleted."); manifest["status"]="FAILED_DISK_SPACE"; save_manifest(manifest); sys.exit(5)
    TODAY=datetime.date.today().isoformat(); YEAR=datetime.date.today().year
    FEATURES=[
     ("V13-001","Text Uppercase","Text Processing","upper","hello","HELLO",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","A"),("Ab C","AB C")]),
     ("V13-002","Text Lowercase","Text Processing","lower","HELLO","hello",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("A","a"),("Ab C","ab c")]),
     ("V13-003","Text Reverse","Text Processing","reverse","hello","olleh",123,"321","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","a"),("ab","ba")]),
     ("V13-004","Text Title Case","Text Processing","title","hello world","Hello World",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","A"),("hi there","Hi There")]),
     ("V13-005","Word Count","Text Processing","word_count","hello world test",3,123,1,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a",1),("a b",2)]),
     ("V13-006","Character Count","Text Processing","char_count","hello",5,123,3,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a",1),("ab",2)]),
     ("V13-007","Palindrome Check","Text Processing","is_palindrome","Madam",True,"hello",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a",True),("ab",False)]),
     ("V13-008","Vowel Count","Text Processing","vowel_count","hello",2,123,0,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a",1),("bc",0)]),
     ("V13-009","Slugify","Text Processing","slugify","Hello World!","hello-world",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("A B","a-b"),("Hi!","hi")]),
     ("V13-010","Strip Whitespace","Text Processing","strip_spaces","  hello  ","hello",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("  a  ","a"),("x","x")]),
     ("V13-011","First Word","Text Processing","first_word","hello world","hello",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a b","a"),("x","x")]),
     ("V13-012","Last Word","Text Processing","last_word","hello world","world",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a b","b"),("x","x")]),
     ("V13-013","Sorted Characters","Text Processing","sorted_chars","cba","abc",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("b","b"),("ba","ab")]),
     ("V13-014","Deduplicate Characters","Text Processing","unique_chars","hello","helo",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","a"),("aaab","ab")]),
     ("V13-015","Has Digit Check","Text Processing","has_digit","abc1",True,"abc",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("1",True),("a",False)]),
     ("V13-016","Email Pattern Check","Validation","is_email_like","a@b.com",True,"not-an-email",False,False,"ERROR_EMPTY_INPUT",[("user.name@example.org",True),("a@",False),("a@b",False),("@b.com",False),("   ",False),("invalid-email",False)]),
     ("V13-017","URL Encode","Encoding","url_encode","hello world","hello%20world",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a b","a%20b"),("x","x")]),
     ("V13-018","Base64 Encode","Encoding","b64_encode","hello","aGVsbG8=",123,"MTIz","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","YQ=="),("hi","aGk=")]),
     ("V13-019","Base64 Decode","Encoding","b64_decode","aGVsbG8=","hello","!!!not-b64!!!","ERROR_INVALID_BASE64","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("YQ==","a"),("aGk=","hi")]),
     ("V13-020","MD5 Hex","Encoding","md5_hex","hello","5d41402abc4b2a76b9719d911017c592",123,"202cb962ac59075b964b07152d234b70","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","0cc175b9c0f1b6a831c399e269772661")]),
     ("V13-021","SHA256 Hex","Encoding","sha256_hex","hello","2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",123,"a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb")]),
     ("V13-022","Add 10","Mathematics","add_10","5",15.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-5",5.0),("0",10.0),("2.5",12.5),("nan","ERROR_NON_FINITE"),("inf","ERROR_NON_FINITE")]),
     ("V13-023","Multiply by 3","Mathematics","mul_3","4",12.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-2",-6.0),("0",0.0),("2.5",7.5),("nan","ERROR_NON_FINITE"),("-inf","ERROR_NON_FINITE")]),
     ("V13-024","Square","Mathematics","square","4",16.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-3",9.0),("0",0.0),("2.5",6.25),("nan","ERROR_NON_FINITE")]),
     ("V13-025","Square Root Absolute","Mathematics","sqrt_abs","16",4.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-9",3.0),("0",0.0),("2.25",1.5),("nan","ERROR_NON_FINITE")]),
     ("V13-026","Percentage To Fraction","Mathematics","percent","50",0.5,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-50",-0.5),("0",0.0),("12.5",0.125),("inf","ERROR_NON_FINITE")]),
     ("V13-027","Celsius To Fahrenheit","Mathematics","c_to_f","0",32.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-40",-40.0),("100",212.0),("37",98.6),("nan","ERROR_NON_FINITE")]),
     ("V13-028","Fahrenheit To Celsius","Mathematics","f_to_c","32",0.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-40",-40.0),("212",100.0),("98.6",37.0),("inf","ERROR_NON_FINITE")]),
     ("V13-029","Prime Check (reject fractions)","Mathematics","is_prime","7",True,"8",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("2",True),("1",False),("0",False),("2.5","ERROR_FRACTIONAL_NOT_ALLOWED"),("-3",False),("nan","ERROR_NON_FINITE")]),
     ("V13-030","Factorial 0-10 (reject fractions)","Mathematics","factorial_small","5",120,"11","ERROR_OUT_OF_RANGE_0_10","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("0",1),("1",1),("10",3628800),("2.5","ERROR_FRACTIONAL_NOT_ALLOWED"),("nan","ERROR_NON_FINITE")]),
     ("V13-031","Even Check (reject fractions)","Mathematics","is_even","4",True,"3",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-2",True),("0",True),("5",False),("2.5","ERROR_FRACTIONAL_NOT_ALLOWED"),("nan","ERROR_NON_FINITE")]),
     ("V13-032","Absolute Value","Mathematics","abs_val","-5",5.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-0.5",0.5),("0",0.0),("3",3.0),("nan","ERROR_NON_FINITE")]),
     ("V13-033","Kilometres To Metres","Mathematics","km_to_m","1",1000.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-1",-1000.0),("0",0.0),("0.5",500.0),("inf","ERROR_NON_FINITE")]),
     ("V13-034","Hours To Minutes","Mathematics","hours_to_min","2",120.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-1",-60.0),("0",0.0),("0.5",30.0),("nan","ERROR_NON_FINITE")]),
     ("V13-035","Average Of Two","Mathematics","avg_two","10,20",15.0,"10,abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("10","ERROR_INVALID_INPUT"),("-10,10",0.0),("1.5,2.5",2.0),("nan,1","ERROR_NON_FINITE"),("a,b","ERROR_INVALID_NUMBER")]),
     ("V13-036","Max Of Two","Mathematics","max_two","10,20",20.0,"10,abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("10","ERROR_INVALID_INPUT"),("-5,5",5.0),("2.5,2.0",2.5),("inf,1","ERROR_NON_FINITE")]),
     ("V13-037","Min Of Two","Mathematics","min_two","10,20",10.0,"10,abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("10","ERROR_INVALID_INPUT"),("-5,5",-5.0),("2.5,2.0",2.0),("1,nan","ERROR_NON_FINITE")]),
     ("V13-038","Is Positive","Mathematics","is_positive","5",True,"-1",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("0",False),("-0.5",False),("0.1",True),("nan","ERROR_NON_FINITE")]),
     ("V13-039","Round To 2 Decimals","Mathematics","round2","3.14159",3.14,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-1.234",-1.23),("0",0.0),("2.5",2.5),("nan","ERROR_NON_FINITE")]),
     ("V13-040","Clamp 0-100","Mathematics","clamp_100","150",100.0,"abc","ERROR_INVALID_NUMBER","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("-10",0.0),("0",0.0),("50.5",50.5),("nan","ERROR_NON_FINITE")]),
     ("V13-041","Today Date ISO","Date/Time","today_iso","",TODAY,"",TODAY,TODAY,"ERROR_EMPTY_INPUT",[(TODAY,TODAY)]),
     ("V13-042","Year Of Today","Date/Time","year_today","",YEAR,"",YEAR,YEAR,"ERROR_EMPTY_INPUT",[(YEAR,YEAR)]),
     ("V13-043","Days In Month Feb 2024","Date/Time","days_feb_2024","",29,"",29,29,"ERROR_EMPTY_INPUT",[(29,29)]),
     ("V13-044","List Length","List Processing","list_len","a,b,c",3,123,1,0,"ERROR_EMPTY_INPUT",[("a",1),("a,b",2),("a,,b",2)]),
     ("V13-045","List First","List Processing","list_first","a,b,c","a",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("x","x"),("x,y","x")]),
     ("V13-046","List Last","List Processing","list_last","a,b,c","c",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("x","x"),("x,y","y")]),
     ("V13-047","List Sorted","List Processing","list_sorted","c,a,b","a,b,c",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("b,a","a,b"),("x","x")]),
     ("V13-048","List Unique","List Processing","list_unique","a,a,b","a,b",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a,a","a"),("b,b,a","b,a")]),
     ("V13-049","Dict Keys Count","Dict Processing","dict_keys_count","a=1,b=2",2,123,0,0,"ERROR_EMPTY_INPUT",[("a=1",1),("a=1,b=2,c=3",3)]),
     ("V13-050","JSON Validate","Validation","json_validate",'{"a":1}',True,"{bad",False,False,"ERROR_EMPTY_INPUT",[('{"x":[]}',True),("[1,2]",True),("notjson",False)]),
     ("V13-051","Safe Filename (dotfiles + ../)","File Helpers","safe_filename","My File!.txt","My_File_.txt",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a b","a_b"),("../etc/passwd",".._etc_passwd"),(".hidden",".hidden"),("a/b","a_b")]),
     ("V13-052","File Extension","File Helpers","file_ext","photo.jpg","jpg","noext","","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a.tar.gz","gz"),("a",""),(".hidden","hidden")]),
     ("V13-053","Contains Tamil Range","Text Processing","has_tamil","vanakkam",False,"தமிழ்",True,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a",False),("த",True)]),
     ("V13-054","Repeat Twice","Text Processing","repeat_twice","hi","hihi",123,"123123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","aa"),("ab","abab")]),
     ("V13-055","Swap Case","Text Processing","swap_case","Hello","hELLO",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a","A"),("Ab","aB")]),
     ("V13-056","Remove Digits","Text Processing","remove_digits","abc123","abc",123,"","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("a1","a"),("123","")]),
     ("V13-057","Count Sentences","Text Processing","count_sentences","Hi. Bye.",2,123,0,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("Hi",0),("Hi! Bye?",2)]),
     ("V13-058","PIN 4-Digit Check","Validation","is_pin4","1234",True,"12",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("0000",True),("12345",False),("abcd",False)]),
     ("V13-059","Password Length Check","Validation","pwd_len_ok","abcdefgh",True,"abc",False,"ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("12345678",True),("1234567",False)]),
     ("V13-060","Trim And Lower","Text Processing","trim_lower","  HELLO  ","hello",123,"123","ERROR_EMPTY_INPUT","ERROR_EMPTY_INPUT",[("  A  ","a"),("X","x")]),
    ]
    IMPLEMENTED=len(FEATURES); PARTIAL=0; NOT_IMPL=350-IMPLEMENTED
    log(f"GENUINE: IMPLEMENTED={IMPLEMENTED} PARTIAL={PARTIAL} NOT_IMPLEMENTED={NOT_IMPL}")
    INT_CHECK=["if not str(inp).strip(): return 'ERROR_EMPTY_INPUT'","try: _v=float(inp)","except Exception: return 'ERROR_INVALID_NUMBER'","import math","if not math.isfinite(_v): return 'ERROR_NON_FINITE'","if _v!=int(_v): return 'ERROR_FRACTIONAL_NOT_ALLOWED'","n=int(_v)"]
    NUM_CHECK=["if not str(inp).strip(): return 'ERROR_EMPTY_INPUT'","try: v=float(inp)","except Exception: return 'ERROR_INVALID_NUMBER'","import math","if not math.isfinite(v): return 'ERROR_NON_FINITE'"]
    PAIR_PREFIX=["if not str(inp).strip(): return 'ERROR_EMPTY_INPUT'","parts=str(inp).split(',')","if len(parts)!=2: return 'ERROR_INVALID_INPUT'"]
    BS=chr(92)
    EMAIL_LINE="return bool(re.match(r'^[^@"+BS+"s]+@[^@"+BS+"s]+"+BS+".[^@"+BS+"s]+$', s))"
    IMPLS={
     "upper": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.upper()"],
     "lower": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.lower()"],
     "reverse": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s[::-1]"],
     "title": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.title()"],
     "word_count": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return len(s.split())"],
     "char_count": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return len(s)"],
     "is_palindrome": ["s=''.join(c.lower() for c in str(inp) if c.isalnum())","if not s: return 'ERROR_EMPTY_INPUT'","return s==s[::-1]"],
     "vowel_count": ["s=str(inp).lower()","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return sum(1 for c in s if c in 'aeiou')"],
     "slugify": ["s=str(inp).lower()","import re","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return re.sub(r'[^a-z0-9]+','-',s).strip('-')"],
     "strip_spaces": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.strip()"],
     "first_word": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.split()[0]"],
     "last_word": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.split()[-1]"],
     "sorted_chars": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return ''.join(sorted(s))"],
     "unique_chars": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return ''.join(dict.fromkeys(s))"],
     "has_digit": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return any(c.isdigit() for c in s)"],
     "is_email_like": ["s=str(inp).strip()","import re","if not s: return False",EMAIL_LINE],
     "url_encode": ["s=str(inp)","import urllib.parse","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return urllib.parse.quote(s)"],
     "b64_encode": ["s=str(inp)","import base64","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return base64.b64encode(s.encode()).decode()"],
     "b64_decode": ["s=str(inp).strip()","import base64","if not s.strip(): return 'ERROR_EMPTY_INPUT'","try: return base64.b64decode(s, validate=True).decode()","except Exception: return 'ERROR_INVALID_BASE64'"],
     "md5_hex": ["s=str(inp)","import hashlib","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return hashlib.md5(s.encode()).hexdigest()"],
     "sha256_hex": ["s=str(inp)","import hashlib","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return hashlib.sha256(s.encode()).hexdigest()"],
     "add_10": NUM_CHECK+["return v+10"],
     "mul_3": NUM_CHECK+["return v*3"],
     "square": NUM_CHECK+["return v*v"],
     "sqrt_abs": NUM_CHECK+["return round(math.sqrt(abs(v)),4)"],
     "percent": NUM_CHECK+["return round(v/100.0,4)"],
     "c_to_f": NUM_CHECK+["return round(v*9/5+32,2)"],
     "f_to_c": NUM_CHECK+["return round((v-32)*5/9,2)"],
     "is_prime": INT_CHECK+["return n>1 and all(n%i!=0 for i in range(2,int(math.sqrt(n))+1))"],
     "factorial_small": INT_CHECK+["return math.factorial(n) if 0<=n<=10 else 'ERROR_OUT_OF_RANGE_0_10'"],
     "is_even": INT_CHECK+["return n%2==0"],
     "abs_val": NUM_CHECK+["return abs(v)"],
     "km_to_m": NUM_CHECK+["return round(v*1000,2)"],
     "hours_to_min": NUM_CHECK+["return round(v*60,2)"],
     "avg_two": PAIR_PREFIX+["try: a=float(parts[0]); b=float(parts[1])","except Exception: return 'ERROR_INVALID_NUMBER'","import math","if not math.isfinite(a) or not math.isfinite(b): return 'ERROR_NON_FINITE'","return round((a+b)/2,2)"],
     "max_two": PAIR_PREFIX+["try: a=float(parts[0]); b=float(parts[1])","except Exception: return 'ERROR_INVALID_NUMBER'","import math","if not math.isfinite(a) or not math.isfinite(b): return 'ERROR_NON_FINITE'","return max(a,b)"],
     "min_two": PAIR_PREFIX+["try: a=float(parts[0]); b=float(parts[1])","except Exception: return 'ERROR_INVALID_NUMBER'","import math","if not math.isfinite(a) or not math.isfinite(b): return 'ERROR_NON_FINITE'","return min(a,b)"],
     "is_positive": NUM_CHECK+["return v>0"],
     "round2": NUM_CHECK+["return round(v,2)"],
     "clamp_100": NUM_CHECK+["return max(0.0,min(100.0,v))"],
     "today_iso": ["import datetime","return datetime.date.today().isoformat()"],
     "year_today": ["import datetime","return datetime.date.today().year"],
     "days_feb_2024": ["import calendar","return calendar.monthrange(2024,2)[1]"],
     "list_len": ["s=str(inp)","if not s.strip(): return 0","return len([x for x in s.split(',') if x.strip()])"],
     "list_first": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.split(',')[0].strip()"],
     "list_last": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.split(',')[-1].strip()"],
     "list_sorted": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return ','.join(sorted([x.strip() for x in s.split(',')]))"],
     "list_unique": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return ','.join(dict.fromkeys([x.strip() for x in s.split(',')]))"],
     "dict_keys_count": ["s=str(inp)","if not s.strip(): return 0","return len([p for p in s.split(',') if '=' in p])"],
     "json_validate": ["import json","try: json.loads(str(inp)); return True","except Exception: return False"],
     "safe_filename": ["s=str(inp)","import re","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return re.sub(r'[^A-Za-z0-9._-]','_',s)"],
     "file_ext": ["s=str(inp).strip()","if not s: return 'ERROR_EMPTY_INPUT'","return s.rsplit('.',1)[-1] if '.' in s else ''"],
     "has_tamil": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return any(0x0B80<=ord(c)<=0x0BFF for c in s)"],
     "repeat_twice": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s*2"],
     "swap_case": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.swapcase()"],
     "remove_digits": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return ''.join(c for c in s if not c.isdigit())"],
     "count_sentences": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return sum(1 for c in s if c in '.!?')"],
     "is_pin4": ["s=str(inp).strip()","if not s: return 'ERROR_EMPTY_INPUT'","return len(s)==4 and s.isdigit()"],
     "pwd_len_ok": ["s=str(inp)","if not s: return 'ERROR_EMPTY_INPUT'","return len(s)>=8"],
     "trim_lower": ["s=str(inp)","if not s.strip(): return 'ERROR_EMPTY_INPUT'","return s.strip().lower()"],
    }
    pre_register("omni_350_v13.py")
    out=["# omni_350_v13.py - Generated by build_350_v13.py - Genuine stdlib features only. 60 IMPLEMENTED, 0 PARTIAL, 290 NOT IMPLEMENTED.","FEATURES={}"]
    for fid,name,cat,fn,ni,ne,ii,ie,ee,ne2,edges in FEATURES:
        out.append(f"def {fn}(inp=None):")
        out.append(f'    """{name} | {cat} | normal {ni!r}->{ne!r} | invalid {ii!r}->{ie!r} | empty->{ee!r} | none->{ne2!r} """')
        for ln in IMPLS[fn]: out.append(f"    {ln}")
        out.append(f'FEATURES["{fid}"]={{"id":"{fid}","name":{name!r},"category":{cat!r},"func":{fn},"status":"IMPLEMENTED"}}')
    out.append('def execute(fid, inp="test"):')
    out.append('    f=FEATURES.get(fid)')
    out.append('    if not f: return "ERROR_FEATURE_NOT_FOUND"')
    out.append('    if inp is None: return "ERROR_EMPTY_INPUT"')
    out.append('    try: return f["func"](inp)')
    out.append('    except Exception as e: return f"ERROR_{type(e).__name__}:{e}"')
    out.append('def list_by_category(cat): return [f for f in FEATURES.values() if f["category"]==cat]')
    omni_src="\n".join(out)+"\n"
    try: compile(omni_src, "omni_350_v13.py", "exec")
    except SyntaxError as e: log(f"FAIL: generated omni_350_v13.py has invalid Python syntax: {e}"); manifest["status"]="FAILED_GENERATED_SYNTAX"; save_manifest(manifest); sys.exit(2)
    log("COMPILE-CHECK generated omni_350_v13.py string OK")
    try:
        atomic_write(ROOT/"omni_350_v13.py", omni_src); track_created("omni_350_v13.py"); log("GENERATED omni_350_v13.py")
    except Exception as e: log(f"FAIL generate features: {e} - Recovery: bash rollback_v13.sh"); manifest["status"]="FAILED_GENERATE"; save_manifest(manifest); sys.exit(2)
    ok2, out2 = py_compile_file(ROOT/"omni_350_v13.py")
    if not ok2: log(f"FAIL: python3 -m py_compile omni_350_v13.py failed:\n{out2}"); manifest["status"]="FAILED_PYCOMPILE"; save_manifest(manifest); sys.exit(2)
    log("PY_COMPILE omni_350_v13.py OK")
    _email_code="import sys; sys.path.insert(0,'.'); from omni_350_v13 import execute; cases=[('a@b.com',True),('user.name@example.org',True),('invalid-email',False),('a@b',False),('a@',False),('@b.com',False),('',False),('   ',False)]; bad=[(c,execute('V13-016',c),exp) for c,exp in cases if execute('V13-016',c)!=exp]; print('EMAIL_BAD='+str(bad)); assert not bad, bad; print('EMAIL_REGEX_EXECUTED_OK')"
    _email_check=subprocess.run([sys.executable,"-c",_email_code], capture_output=True, text=True)
    print(_email_check.stdout); print(_email_check.stderr)
    if _email_check.returncode!=0: log("FAIL: Generated email regex execution check failed"); manifest["status"]="FAILED_REGEX_VERIFY"; save_manifest(manifest); sys.exit(2)
    log("EMAIL REGEX VERIFIED by actual execution of generated omni_350_v13.py")
    pre_register("test_v13.py")
    t=["# test_v13.py - Independent tests - ALL expected are LITERALS. Imports ONLY omni_350_v13 (production module).","from omni_350_v13 import FEATURES, execute","passed=0; failed=[]","def check(fid,cond,info=''):","    global passed","    passed+=1 if cond else 0","    failed.append((fid,info)) if not cond else None"]
    t.append('check("REG1", len(FEATURES)==60, "total 60")')
    t.append('check("REG2", len(set(f["name"] for f in FEATURES.values()))==60, "unique")')
    t.append('check("REG3", execute("NOPE","x")=="ERROR_FEATURE_NOT_FOUND", "invalid id")')
    t.append('check("V13-016-EMPTY", execute("V13-016","")==False, "email empty False documented")')
    t.append('check("V13-016-WHITESPACE", execute("V13-016","   ")==False, "email whitespace False")')
    t.append('check("REG-EMAIL", execute("V13-016","a@b.com")==True and execute("V13-016","user.name@example.org")==True and execute("V13-016","invalid-email")==False and execute("V13-016","a@b")==False and execute("V13-016","a@")==False and execute("V13-016","@b.com")==False and execute("V13-016","")==False, "email regex literals")')
    t.append('check("REG-NAN", execute("V13-022","nan")=="ERROR_NON_FINITE" and execute("V13-022","inf")=="ERROR_NON_FINITE", "nan/inf")')
    t.append('check("REG-DOTFILE", execute("V13-051",".hidden")==".hidden" and execute("V13-051","../etc/passwd")==".._etc_passwd", "dotfiles + ../ ")')
    t.append('check("REG-NUM-EMPTY", execute("V13-022","")== "ERROR_EMPTY_INPUT" and execute("V13-029","")== "ERROR_EMPTY_INPUT" and execute("V13-040","")== "ERROR_EMPTY_INPUT", "numeric empty")')
    t.append('check("REG-PAIR-EMPTY", execute("V13-035","")== "ERROR_EMPTY_INPUT" and execute("V13-036","")== "ERROR_EMPTY_INPUT" and execute("V13-037","")== "ERROR_EMPTY_INPUT", "pair empty")')
    t.append('check("REG-PAIR-MALFORMED", execute("V13-035","10")== "ERROR_INVALID_INPUT" and execute("V13-035","a,b")== "ERROR_INVALID_NUMBER", "pair malformed")')
    for fid,name,cat,fn,ni,ne,ii,ie,ee,ne2,edges in FEATURES:
        t.append(f'check("{fid}", execute("{fid}", {ni!r})=={ne!r}, "normal literal")')
        t.append(f'check("{fid}-INVALID", execute("{fid}", {ii!r})=={ie!r}, "invalid literal")')
        t.append(f'check("{fid}-EMPTY", execute("{fid}", "")=={ee!r}, "empty specific")')
        t.append(f'check("{fid}-NONE", execute("{fid}", None)=={ne2!r}, "none specific")')
        for _ei_idx, (ei,ee2) in enumerate(edges): t.append(f'check("{fid}-EDGE-{_ei_idx}", execute("{fid}", {ei!r})=={ee2!r}, "edge literal")')
    t.append('total=passed+len(failed)')
    t.append('print(f"=== V13 FEATURE TESTS ===\\nPASS={passed} FAIL={len(failed)} TOTAL={total}")')
    t.append('if failed: print("FAILED:", failed[:40])')
    t.append('import json,sys; json.dump({"pass":passed,"fail":len(failed),"failed":failed[:50]}, open("report_v13.json","w"), indent=2); sys.exit(0 if not failed else 1)')
    test_src="\n".join(t)+"\n"
    try: compile(test_src, "test_v13.py", "exec")
    except SyntaxError as e: log(f"FAIL: generated test_v13.py has invalid Python syntax: {e}"); manifest["status"]="FAILED_GENERATED_SYNTAX"; save_manifest(manifest); sys.exit(2)
    log("COMPILE-CHECK generated test_v13.py string OK")
    try: atomic_write(ROOT/"test_v13.py", test_src); track_created("test_v13.py"); log("GENERATED test_v13.py")
    except Exception as e: log(f"FAIL generate test: {e} - Recovery: bash rollback_v13.sh"); manifest["status"]="FAILED_GENERATE"; save_manifest(manifest); sys.exit(2)
    ok3, out3 = py_compile_file(ROOT/"test_v13.py")
    if not ok3: log(f"FAIL: python3 -m py_compile test_v13.py failed:\n{out3}"); manifest["status"]="FAILED_PYCOMPILE"; save_manifest(manifest); sys.exit(2)
    log("PY_COMPILE test_v13.py OK")
    r=subprocess.run([sys.executable,"test_v13.py"], capture_output=True, text=True)
    print(r.stdout); print(r.stderr); log(f"test_v13 exit={r.returncode}")
    track_created("report_v13.json")
    if r.returncode!=0:
        log("FAIL V13 feature tests - STATUS FAILED - Recovery: bash rollback_v13.sh"); manifest["status"]="FAILED_TESTS"; save_manifest(manifest)
        pre_register("REPORT_V13.md"); atomic_write(ROOT/"REPORT_V13.md", f"# V13 REPORT - FAILED\n- test exit {r.returncode}\n- {r.stdout}\n- Recovery: bash rollback_v13.sh\n"); track_created("REPORT_V13.md"); sys.exit(r.returncode)
    regression={}; skipped=[]
    for tf in ["test_full_regression.py","test_own_ai_full.py","test_v41_s2.py","test_final_all.py","test_350.py","test_v4.py","test_v5.py","test_v6.py","test_v7.py","test_v8.py","test_v9.py","test_v10.py","test_v11.py","test_v12.py"]:
        if not pathlib.Path(tf).exists(): regression[tf]={"result":"SKIPPED","reason":"NOT FOUND"}
        else: regression[tf]={"result":"SKIPPED","reason":"Isolation unavailable in Termux - cannot guarantee no project write, skipped per spec. NOT counted as passed."}
        skipped.append(tf)
    log(f"REGRESSION: ALL SKIPPED - {skipped}")
    nested_ok=False
    try:
        ntmp=tempfile.mkdtemp(prefix="v13-nested-"); nproj=pathlib.Path(ntmp)/"proj"; nproj.mkdir()
        (nproj/"keep.txt").write_text("keep",encoding="utf-8")
        (nproj/"sub").mkdir(); (nproj/"sub"/"deep").mkdir(); (nproj/"sub"/"deep"/"file.txt").write_text("deep",encoding="utf-8")
        for rel in ["__pycache__/a.pyc",".git/config","backup-old/x.txt","backup_new/y.txt","sub/__pycache__/b.pyc","sub/.git/c","sub/backup-foo/z.txt","sub/backup_bar/w.txt","sub/deep/backup-deep/v.txt","sub/deep/__pycache__/d.pyc","sub/deep/file.pyc"]:
            p=nproj/rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(b"excluded")
        (nproj/"sub"/"deep"/"good.txt").write_text("good",encoding="utf-8")
        (nproj/"link.txt").symlink_to("keep.txt")
        nback=pathlib.Path(ntmp)/"back"; nback.mkdir()
        recursive_backup(nproj, nback, nproj)
        excluded_present=[str(p.relative_to(nback)) for p in nback.rglob("*") if is_excluded_rel(p.relative_to(nback).parts)]
        nested_ok=(len(excluded_present)==0 and (nback/"keep.txt").exists() and (nback/"sub"/"deep"/"good.txt").exists() and (nback/"link.txt").is_symlink())
        log(f"NESTED EXCLUSION TEST (production recursive_backup): excluded_present={excluded_present} ok={nested_ok}")
        if not nested_ok: log("FAIL nested exclusion test"); manifest["status"]="FAILED_NESTED"; save_manifest(manifest); sys.exit(3)
    finally: shutil.rmtree(ntmp, ignore_errors=True)
    disk_test_ok=(check_free_space(10**18, ROOT)==False)
    log(f"DISK SPACE LOGIC TEST: huge requirement rejected={disk_test_ok}")
    try:
        from unittest.mock import patch
        from collections import namedtuple
        FakeUsage=namedtuple("FakeUsage", ["total","used","free"])
        with patch("shutil.disk_usage", return_value=FakeUsage(total=100*1024*1024, used=99*1024*1024, free=1024)):
            mocked_ok=(check_free_space(MIN_FREE_BYTES, ROOT)==False)
        log(f"DISK SPACE MOCKED TEST: mocked 1KB free correctly rejected={mocked_ok}")
        disk_test_ok=disk_test_ok and mocked_ok
    except Exception as e:
        log(f"FAIL mocked disk-space test: {e}"); disk_test_ok=False
    if not disk_test_ok: log("FAIL disk-space logic test"); manifest["status"]="FAILED_DISK_TEST"; save_manifest(manifest); sys.exit(3)
    collision_test_ok=False
    try:
        ctmp=tempfile.mkdtemp(prefix="v13-collision-")
        cpath=pathlib.Path(ctmp)/"backup-350-v13-20240101_000000"; cpath.mkdir()
        collision_test_ok=(ensure_backup_not_exists(cpath)==False and ensure_backup_not_exists(pathlib.Path(ctmp)/"backup-350-v13-20990101_000000")==True)
        log(f"BACKUP COLLISION LOGIC TEST: existing rejected + missing accepted ok={collision_test_ok}")
    finally: shutil.rmtree(ctmp, ignore_errors=True)
    if not collision_test_ok: log("FAIL backup collision logic test"); manifest["status"]="FAILED_COLLISION_TEST"; save_manifest(manifest); sys.exit(3)
    atomic_ok=False
    try:
        atmp=tempfile.mkdtemp(prefix="v13-atomic-"); aproj=pathlib.Path(atmp)/"proj"; aproj.mkdir()
        builder_path=pathlib.Path(__file__).resolve()
        code1=f"import sys; sys.path.insert(0, {str(builder_path.parent)!r}); import build_350_v13 as B; p={str(aproj/'target.txt')!r}; open(p,'w').write('ORIGINAL'); ok=False\ntry:\n B.atomic_write(p, 'SHOULD-NOT-APPEAR', _fail=True)\nexcept RuntimeError:\n ok=True\nassert ok, 'injected failure did not raise'\nassert open(p).read()=='ORIGINAL', 'original changed'\nimport pathlib; assert len(list(pathlib.Path({str(aproj)!r}).glob('.target.txt.tmp-*')))==0, 'tmp not cleaned'\nB.atomic_write(p, 'NEW'); assert open(p).read()=='NEW'\nprint('ATOMIC_SUBPROCESS_INJECTED_OK')"
        s1=subprocess.run([sys.executable,"-c",code1], capture_output=True, text=True)
        print(s1.stdout); print(s1.stderr)
        assert s1.returncode==0, "atomic subprocess injected test failed"
        target2=aproj/"target2.txt"; target2.write_text("ORIGINAL2",encoding="utf-8")
        ready_file=aproj/"ready.txt"
        code2=f"import sys; sys.path.insert(0, {str(builder_path.parent)!r}); import build_350_v13 as B; B.atomic_write({str(target2)!r}, 'X'*200000, _sleep_before_replace=5, _ready_path={str(ready_file)!r})"
        proc=subprocess.Popen([sys.executable,"-c",code2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        handshake=False
        for _ in range(50):
            if ready_file.exists(): handshake=True; break
            time.sleep(0.1)
        assert handshake, "child never reached pre-replace wait state (no ready handshake)"
        tmps=list(aproj.glob(".target2.txt.tmp-*"))
        assert len(tmps)==1, f"expected 1 tmp after handshake, got {tmps}"
        assert target2.read_text(encoding="utf-8")=="ORIGINAL2", "target changed before replace - atomicity broken"
        proc.kill(); proc.wait()
        assert target2.read_text(encoding="utf-8")=="ORIGINAL2", "target changed after kill"
        for t in tmps:
            if t.is_file(): t.unlink()
        assert len(list(aproj.glob(".target2.txt.tmp-*")))==0
        atomic_ok=True; log("ATOMIC TEST (real atomic_write in subprocess, ready handshake, interruption BEFORE REPLACE): ok=True")
    finally: shutil.rmtree(atmp, ignore_errors=True)
    backup_path_ok=True
    for bad in [".","./","..","../evil","/tmp/evil","backup-350-v13","backup-350-v13-","backup-350-v14-123","backup-350-v13-123/extra","evil","backup-350-v11-123/extra"]:
        if validate_backup_rel(bad, ROOT): backup_path_ok=False; log(f"FAIL backup path should reject {bad!r}")
    for good in ["backup-350-v13-20240101_000000","backup-350-v12-20240101_000000","backup-350-v11-20240101_000000"]:
        if not validate_backup_rel(good, ROOT): backup_path_ok=False; log(f"FAIL backup path should accept {good!r}")
    log(f"BACKUP PATH VALIDATION: ok={backup_path_ok} (rejects '.' and all non-valid names)")
    if not backup_path_ok: manifest["status"]="FAILED_BACKUP_PATH"; save_manifest(manifest); sys.exit(3)
    tmpdir=tempfile.mkdtemp(prefix="v13-rollback-test-")
    rollback_ok=False
    try:
        proj=pathlib.Path(tmpdir)/"proj"; proj.mkdir()
        outside=pathlib.Path(tmpdir)/"outside"; outside.mkdir(); (outside/"secret.txt").write_text("SECRET-OUTSIDE",encoding="utf-8")
        (proj/"keep.txt").write_text("keep-me-original",encoding="utf-8")
        (proj/"unrelated.txt").write_text("UNRELATED-ORIGINAL",encoding="utf-8")
        (proj/"preexisting.txt").write_text("do-not-delete",encoding="utf-8")
        (proj/"user.txt").write_text("USER-FILE-MUST-NOT-BE-DELETED",encoding="utf-8")
        (proj/"own_ai_model.json").write_text("ORIGINAL-MODEL",encoding="utf-8")
        (proj/"own_ai_backup.json").write_text("ORIGINAL-BACKUP",encoding="utf-8")
        (proj/"omni_memory.json").write_text("ORIGINAL-MEMORY",encoding="utf-8")
        (proj/"mod_01.py").write_text("ORIGINAL-MOD01",encoding="utf-8")
        (proj/"mod_32.py").write_text("ORIGINAL-MOD32",encoding="utf-8")
        (proj/"target.txt").write_text("target-content",encoding="utf-8")
        (proj/"link.txt").symlink_to("target.txt")
        (proj/"evil_link").symlink_to(outside)
        tbackup=proj/"backup-350-v13-20240101_000000"; tbackup.mkdir()
        (tbackup/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
        (tbackup/"unrelated.txt").write_text("UNRELATED-ORIGINAL",encoding="utf-8")
        (tbackup/"keep.txt").write_text("keep-me-original",encoding="utf-8")
        (tbackup/"link.txt").symlink_to("target.txt")
        (tbackup/"target.txt").write_text("target-content",encoding="utf-8")
        before_temp={
         "omni_350_v13.py":{"kind":"file","sha":sha(tbackup/"omni_350_v13.py")},
         "unrelated.txt":{"kind":"file","sha":sha(tbackup/"unrelated.txt")},
         "keep.txt":{"kind":"file","sha":sha(tbackup/"keep.txt")},
         "link.txt":{"kind":"symlink","target":"target.txt"},
         "preexisting.txt":{"kind":"file","sha":sha(proj/"preexisting.txt")},
         "target.txt":{"kind":"file","sha":sha(proj/"target.txt")},
         "user.txt":{"kind":"file","sha":sha(proj/"user.txt")},
         "own_ai_model.json":{"kind":"file","sha":sha(proj/"own_ai_model.json")},
         "own_ai_backup.json":{"kind":"file","sha":sha(proj/"own_ai_backup.json")},
         "omni_memory.json":{"kind":"file","sha":sha(proj/"omni_memory.json")},
         "mod_01.py":{"kind":"file","sha":sha(proj/"mod_01.py")},
         "mod_32.py":{"kind":"file","sha":sha(proj/"mod_32.py")},
        }
        trusted_meta={"backup":"backup-350-v13-20240101_000000","before":dict(before_temp)}
        (tbackup/".backup_meta.json").write_text(json.dumps(trusted_meta),encoding="utf-8")
        tmanifest={"backup":"backup-350-v13-20240101_000000","intended":["omni_350_v13.py","partial.txt","manifest_v13.json","rollback_v13.sh"],"created":["omni_350_v13.py","partial.txt","user.txt","../../evil.txt","/tmp/evil.txt","own_ai_model.json"],"modified":["omni_350_v13.py","unrelated.txt","link.txt","/tmp/evil.txt","../evil.txt","evil_link/escape.txt","own_ai_model.json","own_ai_backup.json","omni_memory.json","mod_01.py","mod_32.py"],"deleted":["user.txt"],"before":dict(before_temp)}
        (proj/"manifest_v13.json").write_text(json.dumps(tmanifest),encoding="utf-8")
        (proj/"omni_350_v13.py").write_text("OMNI-BAD",encoding="utf-8")
        (proj/"unrelated.txt").write_text("UNRELATED-BAD-ATTEMPT",encoding="utf-8")
        (proj/"partial.txt").write_text("PARTIAL-CRASH-WRITE",encoding="utf-8")
        if (proj/"link.txt").is_symlink(): (proj/"link.txt").unlink()
        (proj/"link.txt").write_text("BAD-REGULAR-FILE-INSTEAD-OF-SYMLINK",encoding="utf-8")
        shutil.copy2(ROOT/"rollback_v13.sh", proj/"rollback_v13.sh")
        rr=subprocess.run(["bash","rollback_v13.sh"], cwd=str(proj), capture_output=True, text=True)
        print(rr.stdout); print(rr.stderr)
        omni_ok=(proj/"omni_350_v13.py").read_text(encoding="utf-8")=="OMNI-ORIGINAL"
        unrelated_preserved_bad=(proj/"unrelated.txt").read_text(encoding="utf-8")=="UNRELATED-BAD-ATTEMPT"
        model_ok=(proj/"own_ai_model.json").read_text(encoding="utf-8")=="ORIGINAL-MODEL"
        backup_ok=(proj/"own_ai_backup.json").read_text(encoding="utf-8")=="ORIGINAL-BACKUP"
        memory_ok=(proj/"omni_memory.json").read_text(encoding="utf-8")=="ORIGINAL-MEMORY"
        mod01_ok=(proj/"mod_01.py").read_text(encoding="utf-8")=="ORIGINAL-MOD01"
        mod32_ok=(proj/"mod_32.py").read_text(encoding="utf-8")=="ORIGINAL-MOD32"
        user_ok=(proj/"user.txt").read_text(encoding="utf-8")=="USER-FILE-MUST-NOT-BE-DELETED"
        partial_preserved=(proj/"partial.txt").exists()
        link_not_restored=(proj/"link.txt").is_file() and not (proj/"link.txt").is_symlink()
        outside_ok=(outside/"secret.txt").read_text(encoding="utf-8")=="SECRET-OUTSIDE"
        allowlist_skip=("SKIP restore unrelated.txt: not in RESTORE_ALLOWLIST" in rr.stdout)
        btmp_mismatch=tempfile.mkdtemp(prefix="v13-mismatch-")
        try:
            bproj=pathlib.Path(btmp_mismatch)/"proj"; bproj.mkdir()
            bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
            (bback/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
            orig_sha=sha(bback/"omni_350_v13.py")
            (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-99999999_999999","before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}),encoding="utf-8")
            mism={"backup":"backup-350-v13-20240101_000000","intended":[],"created":[],"modified":["omni_350_v13.py"],"deleted":[],"before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}
            (bproj/"manifest_v13.json").write_text(json.dumps(mism),encoding="utf-8")
            (bproj/"omni_350_v13.py").write_text("OMNI-BAD",encoding="utf-8")
            shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
            brm=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
            mismatch_ok=(bproj/"omni_350_v13.py").read_text(encoding="utf-8")=="OMNI-BAD" and "backup name mismatch" in brm.stdout.lower() and brm.returncode!=0
        finally: shutil.rmtree(btmp_mismatch, ignore_errors=True)
        malformed_cases=[
         {"backup":123,"before":{},"modified":[],"deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":[],"modified":[],"deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":{"omni_350_v13.py":"not-a-dict"},"modified":[],"deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":{"omni_350_v13.py":{"kind":"weird"}},"modified":[],"deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":{},"modified":"not-a-list","deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":{},"modified":[123],"deleted":[],"created":[],"intended":[]},
         {"backup":"backup-350-v13-20240101_000000","before":{},"modified":[],"deleted":[],"created":[],"intended":[]},
        ]
        malformed_ok=True
        for idx, bad_manifest in enumerate(malformed_cases):
            btmp=tempfile.mkdtemp(prefix="v13-malformed-")
            try:
                bproj=pathlib.Path(btmp)/"proj"; bproj.mkdir()
                bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
                (bback/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
                (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-20240101_000000","before":{}}),encoding="utf-8")
                (bproj/"manifest_v13.json").write_text(json.dumps(bad_manifest),encoding="utf-8")
                (bproj/"omni_350_v13.py").write_text("OMNI-BAD",encoding="utf-8")
                shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
                br=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
                if idx==len(malformed_cases)-1:
                    if br.returncode!=0: malformed_ok=False
                else:
                    if br.returncode==0 or (bproj/"omni_350_v13.py").read_text(encoding="utf-8")!="OMNI-BAD": malformed_ok=False
            finally: shutil.rmtree(btmp, ignore_errors=True)
        symlink_dir_ok=True
        try:
            btmp=tempfile.mkdtemp(prefix="v13-symlinkdir-")
            bproj=pathlib.Path(btmp)/"proj"; bproj.mkdir()
            outside2=pathlib.Path(btmp)/"outside2"; outside2.mkdir(); (outside2/"victim.txt").write_text("VICTIM-ORIGINAL",encoding="utf-8")
            (bproj/"linkdir").symlink_to(outside2, target_is_directory=True)
            bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
            (bback/"linkdir").mkdir(exist_ok=True); (bback/"linkdir"/"victim.txt").write_text("BACKUP-VICTIM",encoding="utf-8")
            victim_sha=sha(bback/"linkdir"/"victim.txt")
            (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-20240101_000000","before":{"linkdir/victim.txt":{"kind":"file","sha":victim_sha}}}),encoding="utf-8")
            sym_manifest={"backup":"backup-350-v13-20240101_000000","intended":[],"created":[],"modified":["linkdir/victim.txt"],"deleted":[],"before":{"linkdir/victim.txt":{"kind":"file","sha":victim_sha}}}
            (bproj/"manifest_v13.json").write_text(json.dumps(sym_manifest),encoding="utf-8")
            shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
            brs=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
            symlink_dir_ok=((outside2/"victim.txt").read_text(encoding="utf-8")=="VICTIM-ORIGINAL" and (bproj/"linkdir").is_symlink())
        finally: shutil.rmtree(btmp, ignore_errors=True)
        dir_target_ok=True
        try:
            btmp=tempfile.mkdtemp(prefix="v13-dirtarget-")
            bproj=pathlib.Path(btmp)/"proj"; bproj.mkdir()
            bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
            (bback/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
            orig_sha=sha(bback/"omni_350_v13.py")
            (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-20240101_000000","before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}),encoding="utf-8")
            (bproj/"omni_350_v13.py").mkdir(exist_ok=True); (bproj/"omni_350_v13.py"/"inner.txt").write_text("INNER",encoding="utf-8")
            dir_manifest={"backup":"backup-350-v13-20240101_000000","intended":[],"created":[],"modified":["omni_350_v13.py"],"deleted":[],"before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}
            (bproj/"manifest_v13.json").write_text(json.dumps(dir_manifest),encoding="utf-8")
            shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
            brd=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
            dir_target_ok=((bproj/"omni_350_v13.py").is_dir() and (bproj/"omni_350_v13.py"/"inner.txt").read_text(encoding="utf-8")=="INNER")
        finally: shutil.rmtree(btmp, ignore_errors=True)
        btmp2=tempfile.mkdtemp(prefix="v13-tamper-manifest-")
        try:
            bproj=pathlib.Path(btmp2)/"proj"; bproj.mkdir()
            bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
            (bback/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
            orig_sha=sha(bback/"omni_350_v13.py")
            (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-20240101_000000","before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}),encoding="utf-8")
            tampered={"backup":"backup-350-v13-20240101_000000","intended":[],"created":[],"modified":["omni_350_v13.py"],"deleted":[],"before":{"omni_350_v13.py":{"kind":"file","sha":"0"*64}}}
            (bproj/"manifest_v13.json").write_text(json.dumps(tampered),encoding="utf-8")
            (bproj/"omni_350_v13.py").write_text("OMNI-BAD",encoding="utf-8")
            shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
            br=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
            tampered_manifest_ok=(bproj/"omni_350_v13.py").read_text(encoding="utf-8")=="OMNI-BAD"
        finally: shutil.rmtree(btmp2, ignore_errors=True)
        btmp3=tempfile.mkdtemp(prefix="v13-tamper-meta-")
        try:
            bproj=pathlib.Path(btmp3)/"proj"; bproj.mkdir()
            bback=bproj/"backup-350-v13-20240101_000000"; bback.mkdir()
            (bback/"omni_350_v13.py").write_text("OMNI-ORIGINAL",encoding="utf-8")
            orig_sha=sha(bback/"omni_350_v13.py")
            (bback/".backup_meta.json").write_text(json.dumps({"backup":"backup-350-v13-20240101_000000","before":{"omni_350_v13.py":{"kind":"file","sha":"f"*64}}}),encoding="utf-8")
            good={"backup":"backup-350-v13-20240101_000000","intended":[],"created":[],"modified":["omni_350_v13.py"],"deleted":[],"before":{"omni_350_v13.py":{"kind":"file","sha":orig_sha}}}
            (bproj/"manifest_v13.json").write_text(json.dumps(good),encoding="utf-8")
            (bproj/"omni_350_v13.py").write_text("OMNI-BAD",encoding="utf-8")
            shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
            br3=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
            tampered_meta_ok=(bproj/"omni_350_v13.py").read_text(encoding="utf-8")=="OMNI-BAD"
        finally: shutil.rmtree(btmp3, ignore_errors=True)
        ext_ok=True
        for bad_backup in [".","/tmp/evil-backup","../evil-backup","backup-350-v14-123","evil"]:
            btmp=tempfile.mkdtemp(prefix="v13-ext-")
            try:
                bproj=pathlib.Path(btmp)/"proj"; bproj.mkdir()
                bman={"backup":bad_backup,"intended":[],"created":[],"modified":[],"deleted":[],"before":{}}
                (bproj/"manifest_v13.json").write_text(json.dumps(bman),encoding="utf-8")
                shutil.copy2(ROOT/"rollback_v13.sh", bproj/"rollback_v13.sh")
                br=subprocess.run(["bash","rollback_v13.sh"], cwd=str(bproj), capture_output=True, text=True)
                if "FAIL backup path rejected" not in br.stdout and br.returncode==0: ext_ok=False
            finally: shutil.rmtree(btmp, ignore_errors=True)
        rollback_ok=omni_ok and unrelated_preserved_bad and model_ok and backup_ok and memory_ok and mod01_ok and mod32_ok and user_ok and partial_preserved and link_not_restored and outside_ok and allowlist_skip and mismatch_ok and malformed_ok and symlink_dir_ok and dir_target_ok and tampered_manifest_ok and tampered_meta_ok and ext_ok and rr.returncode==0
        log(f"ROLLBACK/MALICIOUS TEST: omni_restored={omni_ok} unrelated_NOT_restored={unrelated_preserved_bad} model={model_ok} backup_json={backup_ok} memory={memory_ok} mod01={mod01_ok} mod32={mod32_ok} user={user_ok} partial_preserved={partial_preserved} link_not_restored={link_not_restored} outside={outside_ok} allowlist_skip={allowlist_skip} backup_name_mismatch_rejected={mismatch_ok} malformed_rejected={malformed_ok} symlink_dir_not_followed={symlink_dir_ok} dir_target_not_overwritten={dir_target_ok} tampered_manifest_skipped={tampered_manifest_ok} tampered_meta_skipped={tampered_meta_ok} ext_backup_rejected={ext_ok} exit={rr.returncode} ok={rollback_ok}")
        if not rollback_ok: log("FAIL rollback/malicious test"); manifest["status"]="FAILED_ROLLBACK"; save_manifest(manifest); sys.exit(3)
    finally: shutil.rmtree(tmpdir, ignore_errors=True)
    isolated_ok=False
    if os.environ.get("V13_ISOLATED_RUN")!="1":
        iso_tmp=tempfile.mkdtemp(prefix="v13-isolated-builder-")
        try:
            iso_proj=pathlib.Path(iso_tmp)/"proj"; iso_proj.mkdir()
            (iso_proj/"keep.txt").write_text("keep",encoding="utf-8")
            (iso_proj/"own_ai_model.json").write_text("ORIGINAL-MODEL",encoding="utf-8")
            (iso_proj/"own_ai_backup.json").write_text("ORIGINAL-BACKUP",encoding="utf-8")
            (iso_proj/"mod_01.py").write_text("ORIGINAL-MOD01",encoding="utf-8")
            before_hashes={n:sha(iso_proj/n) for n in ["keep.txt","own_ai_model.json","own_ai_backup.json","mod_01.py"]}
            shutil.copy2(pathlib.Path(__file__).resolve(), iso_proj/"build_350_v13.py")
            env=dict(os.environ); env["V13_ISOLATED_RUN"]="1"
            ir=subprocess.run([sys.executable,"build_350_v13.py"], cwd=str(iso_proj), capture_output=True, text=True, env=env)
            print(ir.stdout[-3000:]); print(ir.stderr[-2000:])
            ver=subprocess.run([sys.executable,"-c","import sys; sys.path.insert(0,'.'); from omni_350_v13 import execute; assert execute('V13-016','a@b.com')==True; assert execute('V13-016','user.name@example.org')==True; assert execute('V13-016','invalid-email')==False; assert execute('V13-016','a@b')==False; print('ISOLATED_GENERATED_MODULE_OK')"], cwd=str(iso_proj), capture_output=True, text=True)
            print(ver.stdout); print(ver.stderr)
            after_hashes={n:sha(iso_proj/n) for n in ["keep.txt","own_ai_model.json","own_ai_backup.json","mod_01.py"]}
            protected_unchanged=(before_hashes==after_hashes)
            iso_manifest = {}
            _iso_manifest_path = iso_proj/"manifest_v13.json"
            if not _iso_manifest_path.is_file():
                log(f"ISOLATED COMPLETE BUILDER RUN: FAILED - isolated manifest missing, isolated exit={ir.returncode}")
                isolated_ok=False
            else:
                iso_manifest=json.loads(_iso_manifest_path.read_text(encoding="utf-8"))
            before_after_ok=(iso_manifest.get("modified")==[] and iso_manifest.get("deleted")==[])
            isolated_ok=(ir.returncode==0 and ver.returncode==0 and (iso_proj/"omni_350_v13.py").exists() and (iso_proj/"test_v13.py").exists() and (iso_proj/"REPORT_V13.md").exists() and (iso_proj/"report_v13.json").exists() and (iso_proj/"rollback_v13.sh").exists() and protected_unchanged and before_after_ok)
            log(f"ISOLATED COMPLETE BUILDER RUN: exit={ir.returncode} generated_module={ver.returncode==0} protected_unchanged={protected_unchanged} before_after={before_after_ok} ok={isolated_ok}")
            log(f"ISOLATED PROTECTED HASHES BEFORE: {before_hashes}")
            log(f"ISOLATED PROTECTED HASHES AFTER: {after_hashes}")
            if not isolated_ok: log("FAIL isolated complete builder run"); manifest["status"]="FAILED_ISOLATED"; save_manifest(manifest); sys.exit(3)
        finally: shutil.rmtree(iso_tmp, ignore_errors=True)
    else:
        isolated_ok=True; log("ISOLATED COMPLETE BUILDER RUN: skipped (already inside isolated run, guard active)")
    after={}
    for p in ROOT.rglob("*"):
        if is_excluded(p, ROOT): continue
        if p.is_symlink(): after[str(p.relative_to(ROOT))]={"kind":"symlink","target":os.readlink(p)}
        elif p.is_file(): after[str(p.relative_to(ROOT))]={"kind":"file","sha":sha(p),"size":p.stat().st_size}
    created=[k for k in after if k not in before]
    modified=[k for k in after if k in before and after[k]!=before[k]]
    deleted=[k for k in before if k not in after]
    log(f"AFTER: created={created} modified={modified} deleted={deleted}")
    if modified: log(f"FAIL unexpected modification {modified} - Recovery: bash rollback_v13.sh"); manifest["status"]="FAILED_MODIFIED"; save_manifest(manifest); sys.exit(4)
    if deleted: log(f"FAIL unexpected deletion {deleted} - Recovery: bash rollback_v13.sh"); manifest["status"]="FAILED_DELETED"; manifest["deleted"]=deleted; save_manifest(manifest); sys.exit(4)
    for c in list(created): track_created(c)
    try: rep=json.loads(pathlib.Path("report_v13.json").read_text())
    except Exception: rep={"pass":0,"fail":999}
    LIMITATIONS=["350 genuine features not achievable in one stdlib builder - V13 implements 60 genuine, 290 NOT IMPLEMENTED","No voice/image/weather/web-AI claimed","Regression ALL SKIPPED (isolation unavailable) - never counted as passed","Assistant did NOT execute this file - status NOT EXECUTED","Rollback requires manifest_v13.json + relative backup-350-v13-* dir + backup_meta consistency + backup-name match + resolved-path match together; backup_meta is NOT cryptographically trusted (see threat model)","Rollback restores ONLY V13-owned outputs (RESTORE_ALLOWLIST). Unrelated pre-existing files are NEVER restored, even with valid backup_meta entries."]
    manifest.update({"created":sorted(set(manifest["created"])|set(created)),"modified":modified,"deleted":deleted,"implemented":IMPLEMENTED,"partial":PARTIAL,"not_implemented":NOT_IMPL,"test_pass":rep.get("pass"),"test_fail":rep.get("fail"),"regression":regression,"nested_test":"PASS isolated - production recursive_backup","atomic_test":"PASS - real atomic_write in subprocess, ready handshake, interruption BEFORE REPLACE","rollback_test":"PASS isolated - real rollback_v13.sh, backup-name mismatch, malformed manifest, symlink-dir, dir-target, tampered manifest/meta, protected, backup-path rejected","isolated_builder_test":"PASS - complete builder run in separate temp project, generated module + protected hashes + before/after verified" if isolated_ok else "SKIPPED - already isolated","limitations":LIMITATIONS,"status":"VERIFIED" if rep.get("fail")==0 else "FAILED"})
    save_manifest(manifest)
    md=[f"# BH-OMNI-CORE V13 HONEST REPORT - {STAMP}",f"- Backup: {BACKUP_DIR.name} - SHA-256 verified, symlinks verified, ONE exclusion function, recursive backup (production helper), all levels, nested leak check, backup dir validated (relative backup-350-v13-* only, not symlink, inside ROOT), backup collision checked (never overwrite existing), disk-space >=10 MB checked, backup_meta consistency + backup-name match + resolved-path match (NOT cryptographic trust)",f"- Implemented (genuine): {IMPLEMENTED}",f"- Partial: {PARTIAL}",f"- NOT Implemented (of 350): {NOT_IMPL}",f"- Tests: PASS={rep.get('pass')} FAIL={rep.get('fail')} - test_v13 exit 0, literals only, normal/invalid/empty/None/edge incl numeric empty, pair empty/malformed, NaN/Infinity, dotfiles/../, email executed check on generated module",f"- Regression: PASS=0 SKIPPED={len(skipped)} - {skipped} - skipped (isolation unavailable), NEVER counted as passed",f"- Created: {created}",f"- Modified: {modified} (must be [] - additive only)",f"- Deleted: {deleted} (must be [] - unexpected deletion = FAILED)",f"- Leftover tmp PRESERVED at start (never deleted): {leftover}",f"- Nested exclusion test: PASS - production recursive_backup",f"- Disk-space test: PASS - >=10 MB required, huge + mocked insufficient-space rejected, never deletes files to make space",f"- Backup collision test: PASS - existing backup path rejected, never overwritten",f"- Python validation: PASS - py_compile build_350_v13.py + py_compile omni_350_v13.py + py_compile test_v13.py + compile() on generated strings before writing",f"- Atomic test: PASS - real atomic_write in subprocess, ready handshake, interruption BEFORE REPLACE, target unchanged",f"- Rollback: PASS - real rollback_v13.sh, backup-name mismatch rejected, malformed manifest rejected, symlink-dir not followed, dir-target not overwritten, RESTORE_ALLOWLIST only, tampered manifest/meta skipped, protected never touched - Run: bash rollback_v13.sh",f"- Isolated complete builder: PASS - builder run in separate temp project, generated module + protected hashes + before/after verified" if isolated_ok else "- Isolated complete builder: SKIPPED (already isolated)",f"- Protected (never modified): own_ai_model.json, own_ai_backup.json, omni_memory.json, mod_01..mod_32, V40/V41 files, all pre-existing files (verified via before/after)",f"- Threat model: manifest + backup_meta are plain local JSON in same trust domain, NOT cryptographically trusted. Restore requires allowlist + protected block + backup-name match + resolved-path match + triple SHA agreement + strict manifest structure.",f"- Limitations: {LIMITATIONS}",f"- Status: {'VERIFIED - 60/60 genuine features pass' if rep.get('fail')==0 else 'FAILED'}",f"- DO NOT CLAIM 350/350 - Actual genuine count is 60."]
    pre_register("REPORT_V13.md"); atomic_write(ROOT/"REPORT_V13.md", "\n".join(md)+"\n"); track_created("REPORT_V13.md")
    log("\n".join(md)); log("=== V13 DONE ===")
if __name__=="__main__":
    main()
