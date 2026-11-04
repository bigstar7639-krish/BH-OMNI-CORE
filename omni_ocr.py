# OMNI OCR - Cat 08 - Interface + pytesseract check - NO fake OCR
import shutil
def ocr_status():
    if shutil.which("tesseract"):
        return "📷 OCR READY - tesseract irukku!\nUse: tesseract photo.jpg out - Pydroid3/Termux-la photo-a text aakkalam!"
    return "📷 OCR SETUP:\n pkg install tesseract\nAppuram photo-a text aakkalam da!\nNote: Camera permission venum, photo file venum."
def handle_ocr(msg):
    m = msg.strip().lower()
    if m in ["ocr", "ocr status", "scan"]:
        return ocr_status()
    if m.startswith("ocr file "):
        return f"📷 OCR FILE: {msg.strip()[9:].strip()}\nCommand: tesseract {msg.strip()[9:].strip()} out\nAdha run panna text kedaikkum da!"
    return None
