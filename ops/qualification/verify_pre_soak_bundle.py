#!/usr/bin/env python3
"""Deterministic pre-soak qualification checklist.

This tool validates a supplied evidence directory. It deliberately does not
contact or modify live nodes. Each evidence item must be fresh and independently
captured by the deployment/operator layer.
"""
from __future__ import annotations

import argparse
import json
import re
import socket
import subprocess
import time
from pathlib import Path

SHA_RE = re.compile(r"^[0-9a-f]{40}$")

REQUIRED = (
    "transport-health.json",
    "runtime-e2e.json",
    "scheduler-e2e.json",
    "fencing.json",
    "recovery.json",
    "backup-restore.json",
    "provider-model.json",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence_dir", type=Path)
    parser.add_argument("--allow-missing", action="store_true")
    parser.add_argument("--target-sha", default=None)
    parser.add_argument("--node-id", default=None)
    parser.add_argument("--max-age-seconds", type=int, default=900)
    args = parser.parse_args()

    if args.max_age_seconds < 0:
        raise SystemExit("--max-age-seconds must be non-negative")

    expected_sha = args.target_sha
    if expected_sha is None:
        try:
            expected_sha = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=Path(__file__).resolve().parents[2],
                text=True,
            ).strip()
        except Exception as exc:
            raise SystemExit(f"BLOCK: cannot determine current target SHA: {exc}")
    expected_node = args.node_id or socket.gethostname()
    now = int(time.time())

    missing = [name for name in REQUIRED if not (args.evidence_dir / name).is_file()]
    if missing and not args.allow_missing:
        raise SystemExit("BLOCK: missing fresh evidence: " + ", ".join(missing))

    invalid = []
    for name in REQUIRED:
        path = args.evidence_dir / name
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text())
        except Exception as exc:
            invalid.append(f"{name}: invalid JSON ({exc})")
            continue
        if data.get("schema") != "mediahub.pre-soak-evidence.v1":
            invalid.append(f"{name}: schema={data.get('schema')!r}")
            continue
        if data.get("status") != "PASS":
            invalid.append(f"{name}: status={data.get('status')!r}")
            continue
        captured_at = data.get("captured_at")
        if not isinstance(captured_at, int):
            invalid.append(f"{name}: captured_at is not an integer")
        elif now - captured_at < 0 or now - captured_at > args.max_age_seconds:
            invalid.append(f"{name}: stale or future evidence (age={now - captured_at}s)")
        target_sha = data.get("target_sha")
        if not isinstance(target_sha, str) or not SHA_RE.fullmatch(target_sha):
            invalid.append(f"{name}: invalid target_sha")
        elif target_sha != expected_sha:
            invalid.append(f"{name}: target_sha mismatch")
        if data.get("node_id") != expected_node:
            invalid.append(f"{name}: node_id mismatch")

    if invalid:
        raise SystemExit("BLOCK: " + "; ".join(invalid))

    if missing:
        print("PARTIAL: required evidence set is incomplete")
        for name in missing:
            print(f"MISSING {name}")
        return 2

    print("PRE-SOAK PASS: all required evidence files report PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
