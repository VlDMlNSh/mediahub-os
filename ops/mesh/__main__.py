from __future__ import annotations
import os
import time

def main() -> int:
    # Runtime placeholder: intentionally non-authoritative until node-side
    # transport integration and signed heartbeat publication are installed.
    if os.environ.get("MEDIAHUB_MESH_FAIL_CLOSED", "1") != "1":
        raise SystemExit("MEDIAHUB_MESH_FAIL_CLOSED must remain 1")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()
