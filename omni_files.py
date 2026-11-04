# OMNI FILES - Cat 09 - TXT/MD reader - Real file read
import pathlib
def read_file(path):
    try:
        p = pathlib.Path(path)
        if not p.exists():
            return f"📄 FILES: '{path}' - file illa da!"
        txt = p.read_text(errors="ignore")
        return f"📄 FILE: {path} ({len(txt)} chars):\n{txt[:1000]}"
    except Exception as e:
        return f"📄 FILES ERROR: {e}"
def handle_files(msg):
    s = msg.strip()
    m = s.lower()
    if m.startswith("read "):
        return read_file(s[5:].strip())
    if m in ["files", "file list"]:
        return "📄 FILES: 'read README.md' / 'read VERSION.txt' nu try pannu da!"
    return None
