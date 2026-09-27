#!/usr/bin/env python3
import hashlib
import hmac
import json
import os
import sys
import time
import uuid

def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: sign_astra_command.py NODE_ID OPERATION")
    key = os.environ.get("ASTRA_COMMAND_HMAC_KEY")
    if not key:
        raise SystemExit("ASTRA_COMMAND_HMAC_KEY is required")
    command = {
        "schema": 1,
        "command_id": uuid.uuid4().hex,
        "node_id": sys.argv[1],
        "operation": sys.argv[2],
        "issued_at": int(time.time()),
    }
    body = json.dumps(command, sort_keys=True, separators=(",", ":")).encode()
    command["signature"] = hmac.new(key.encode(), body, hashlib.sha256).hexdigest()
    print(json.dumps(command, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
