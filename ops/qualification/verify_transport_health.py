#!/usr/bin/env python3
"""Validate a fresh Astra GitHub Transport health result.

This is a qualification gate, not a live deployment tool. It verifies the
identity contract emitted by the canonical transport agent.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REQUIRED = ("node_id", "transport_version", "agent_source_sha", "agent_path", "worktree")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("health_json", type=Path)
    parser.add_argument("--agent", type=Path, required=True)
    parser.add_argument("--worktree", type=Path, required=True)
    args = parser.parse_args()

    health = json.loads(args.health_json.read_text())
    missing = [key for key in REQUIRED if not health.get(key)]
    if missing:
        raise SystemExit("FAIL: missing health fields: " + ", ".join(missing))

    if health["transport_version"] != "self-reexec-v1":
        raise SystemExit(
            "FAIL: unexpected transport_version=" + repr(health["transport_version"])
        )

    expected_agent = args.agent.resolve()
    reported_agent = Path(health["agent_path"]).resolve()
    expected_worktree = args.worktree.resolve()
    reported_worktree = Path(health["worktree"]).resolve()

    if reported_worktree != expected_worktree:
        raise SystemExit(
            f"FAIL: worktree mismatch: reported={reported_worktree} expected={expected_worktree}"
        )

    try:
        reported_agent.relative_to(reported_worktree)
    except ValueError:
        raise SystemExit(
            f"FAIL: agent_path is outside worktree: {reported_agent}"
        )

    if reported_agent != expected_agent:
        raise SystemExit(
            f"FAIL: agent_path mismatch: reported={reported_agent} expected={expected_agent}"
        )

    actual_sha = hashlib.sha256(expected_agent.read_bytes()).hexdigest()
    if health["agent_source_sha"] != actual_sha:
        raise SystemExit(
            "FAIL: agent_source_sha mismatch: "
            f"reported={health['agent_source_sha']} actual={actual_sha}"
        )

    print("PASS: canonical Astra transport identity verified")
    print(f"node_id={health['node_id']}")
    print(f"transport_version={health['transport_version']}")
    print(f"agent_source_sha={actual_sha}")
    print(f"agent_path={reported_agent}")
    print(f"worktree={reported_worktree}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
