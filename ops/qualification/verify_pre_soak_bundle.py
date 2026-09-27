#!/usr/bin/env python3
"""Deterministic pre-soak qualification checklist.

This tool validates a supplied evidence directory. It deliberately does not
contact or modify live nodes. Each evidence item must be fresh and independently
captured by the deployment/operator layer.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

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
    args = parser.parse_args()

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
        if data.get("status") != "PASS":
            invalid.append(f"{name}: status={data.get('status')!r}")

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
