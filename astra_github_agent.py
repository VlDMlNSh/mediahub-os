#!/usr/bin/env python3
"""Astra GitHub transport worker.

The worker uses GitHub as a durable desired-state bus and delegates only to the
existing Astra application runtime. It does not accept arbitrary shell text.
"""
from __future__ import annotations
import hashlib
import hmac
import json
import os
import platform
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = os.environ.get("ASTRA_GITHUB_REPO", "VlDMlNSh/mediahub-os")
NODE_ID = os.environ.get("ASTRA_NODE_ID", platform.node())
TOKEN = os.environ.get("GITHUB_TOKEN", "")
POLL = max(15, int(os.environ.get("ASTRA_POLL_SECONDS", "30")))
KEY = os.environ.get("ASTRA_COMMAND_HMAC_KEY", "")
API = f"https://api.github.com/repos/{REPO}"
STATE = Path(os.environ.get("ASTRA_STATE_DIR", "/var/lib/mediahub-astra"))
OPERATIONS = {"health", "research", "architecture", "review", "documents", "coding"}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def request(path, method="GET", body=None):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "MediaHub-Astra"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def command():
    path = f"/contents/control/commands/{NODE_ID}.json?ref=main"
    try:
        item = request(path)
        import base64
        raw = base64.b64decode(item["content"]).decode()
        return json.loads(raw)
    except (urllib.error.URLError, KeyError, ValueError, TimeoutError):
        return None

def verify(cmd):
    if not KEY or cmd.get("node_id") != NODE_ID:
        return False
    supplied = str(cmd.get("signature", ""))
    unsigned = {k: v for k, v in cmd.items() if k != "signature"}
    expected = hmac.new(KEY.encode(), canonical(unsigned), hashlib.sha256).hexdigest()
    return hmac.compare_digest(supplied, expected)

def publish(result):
    import base64
    path = f"/contents/control/results/{NODE_ID}.json"
    body = json.dumps(result, indent=2, sort_keys=True) + "\n"
    payload = {
        "message": f"astra: result {NODE_ID}",
        "content": base64.b64encode(body.encode()).decode(),
        "branch": f"astra-node/{NODE_ID}",
    }
    try:
        current = request(path + f"?ref=astra-node/{NODE_ID}")
        payload["sha"] = current["sha"]
    except Exception:
        pass
    return request(path, method="PUT", body=payload)

def execute(cmd):
    operation = cmd.get("operation")
    if operation == "health":
        return {"status": "ready", "platform": platform.platform(), "python": platform.python_version()}
    if operation not in OPERATIONS:
        return {"error": "unsupported_operation", "operation": operation}
    from mediahub_runtime.astra_gateway import AstraGatewayRuntime
    runtime = AstraGatewayRuntime()
    result = runtime.run_bounded({
        "task_id": cmd.get("command_id", "github-task"),
        "title": cmd.get("title", operation),
        "description": cmd.get("description", ""),
        "capability": operation,
    })
    return result

def main():
    STATE.mkdir(parents=True, exist_ok=True)
    last_id = ""
    while True:
        try:
            cmd = command()
            if cmd and verify(cmd) and cmd.get("command_id") != last_id:
                started = time.time()
                try:
                    value = execute(cmd)
                    rc = 0
                except Exception as exc:
                    value = {"error": repr(exc)}
                    rc = 1
                publish({
                    "schema": 1,
                    "node_id": NODE_ID,
                    "command_id": cmd.get("command_id"),
                    "returncode": rc,
                    "duration_seconds": round(time.time() - started, 3),
                    "result": value,
                    "completed_at": int(time.time()),
                })
                last_id = str(cmd.get("command_id"))
        except Exception as exc:
            (STATE / "last_error.json").write_text(json.dumps({"error": repr(exc), "time": int(time.time())}))
        time.sleep(POLL)

if __name__ == "__main__":
    main()
