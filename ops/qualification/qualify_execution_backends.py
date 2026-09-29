#!/usr/bin/env python3
"""Capture bounded, sanitized runtime evidence for local engineering backends.

This probe runs only on the node where the Astra worker executes. It never
prints command configuration or command output. The output is digest-only.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
import time

BACKENDS = {
    "codex": "MEDIAHUB_CODEX_COMMAND",
    "cursor": "MEDIAHUB_CURSOR_COMMAND",
}
FORBIDDEN = (";", "&&", "||", "|", ">", "<", "\n", "\r")
PROMPT = "MEDIAHUB_EXECUTION_BACKEND_QUALIFICATION"
TIMEOUT = 30


def digest(data: str) -> str:
    return "sha256:" + hashlib.sha256(data.encode("utf-8", "replace")).hexdigest()


def qualify(backend_id: str) -> dict:
    env_name = BACKENDS[backend_id]
    raw = os.environ.get(env_name, "").strip()
    result = {
        "node_id": platform.node(),
        "verification_state": "UNVERIFIED",
        "checks": {
            "node_identity": "PASS" if platform.node() == "mh-dev-01" else "FAIL",
            "binary_identity": "FAIL",
            "bounded_execution": "FAIL",
        },
        "secret_values": "SUPPRESSED",
    }
    if not raw:
        result["reason"] = "command_not_configured"
        return result
    if any(token in raw for token in FORBIDDEN):
        result["reason"] = "unsafe_command_syntax"
        return result
    try:
        argv = shlex.split(raw)
    except ValueError:
        result["reason"] = "invalid_command_syntax"
        return result
    if not argv:
        result["reason"] = "empty_command"
        return result
    # Normalize legacy node configuration that points directly to the Codex
    # binary: the bounded qualification contract requires non-interactive exec.
    if backend_id == "codex" and Path(argv[0]).name == "codex" and (len(argv) == 1 or argv[1] != "exec"):
        argv.insert(1, "exec")
    executable = shutil.which(argv[0])
    if not executable:
        result["reason"] = "executable_not_found"
        return result
    result["checks"]["binary_identity"] = "PASS"
    started = time.monotonic()
    try:
        proc = subprocess.run(
            [*argv, PROMPT],
            text=True,
            capture_output=True,
            timeout=TIMEOUT,
            check=False,
            env={"PATH": os.environ.get("PATH", "")},
        )
    except (OSError, subprocess.TimeoutExpired):
        result["reason"] = "bounded_execution_failed"
        return result
    duration = round(time.monotonic() - started, 3)
    combined = (proc.stdout or "") + (proc.stderr or "")
    result["duration_seconds"] = duration
    result["returncode"] = proc.returncode
    result["output_bytes"] = len(combined.encode("utf-8", "replace"))
    result["output_sha256"] = digest(combined)
    if proc.returncode != 0:
        result["reason"] = "nonzero_exit"
        return result
    if not combined.strip():
        result["reason"] = "empty_output"
        return result
    result["checks"]["bounded_execution"] = "PASS"
    result["verification_state"] = "VERIFIED"
    return result


def main() -> int:
    node_id = platform.node()
    try:
        repo_revision = subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True, timeout=10, check=False).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        repo_revision = ""
    payload = {
        "schema": "mediahub.execution-backends.v1",
        "status": "PASS",
        "captured_at": int(time.time()),
        "node_id": node_id,
        "repo_revision": repo_revision,
        "backends": {backend_id: qualify(backend_id) for backend_id in BACKENDS},
        "secret_values": "SUPPRESSED",
    }
    if not repo_revision:
        payload["status"] = "BLOCKED"
    if any(item["verification_state"] != "VERIFIED" for item in payload["backends"].values()):
        payload["status"] = "BLOCKED"
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["evidence_digest"] = digest(canonical)
    print(json.dumps(payload, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
