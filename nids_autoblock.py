 #!/usr/bin/env python3
# NIDS Auto-Blocker: reads Suricata eve.json from stdin and blocks offending src_ip via UFW.

import sys
import json
import subprocess

def block_ip(ip):
    """Block an IP address using UFW (Linux firewall)."""
    try:
        subprocess.run(["ufw", "deny", "from", ip], check=True)
        print(f"[BLOCKED] {ip}")
    except Exception as e:
        print(f"[ERROR] Could not block {ip}: {e}")

def main():
    """Read Suricata eve.json alerts from stdin and block offending IPs."""
    for line in sys.stdin:
        try:
            event = json.loads(line)
            if event.get("event_type") == "alert":
                src_ip = event.get("src_ip")
                if src_ip:
                    print(f"[ALERT] Blocking IP: {src_ip}")
                    block_ip(src_ip)
        except json.JSONDecodeError:
            continue  # skip invalid JSON lines

if __name__ == "__main__":
    main()
