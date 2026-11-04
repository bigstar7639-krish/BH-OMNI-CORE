# OMNI NETWORK - Cat 13 - Real Termux network check - NO unauthorized scan
import subprocess, socket
def network_status():
    try:
        ip = socket.gethostbyname(socket.gethostname())
        return f"📶 NETWORK STATUS:\nLocal IP: {ip}\nHost: {socket.gethostname()}\nNote: Unauthorized device scan PANNAMATTOM - un network mattum paakkurom!"
    except Exception as e:
        return f"📶 NETWORK ERROR: {e}"
def handle_network(msg):
    m = msg.strip().lower()
    if m in ["network", "network status", "wifi"]:
        return network_status()
    return None
