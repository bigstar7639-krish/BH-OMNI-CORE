#!/bin/bash
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
