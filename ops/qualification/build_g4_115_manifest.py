#!/usr/bin/env python3
"""Build a deterministic G4 command manifest; execution remains external and fail-closed.

The default profile is the mandatory 5-path matrix (CODEX_FCC, CLAUDE_FCC,
CODEX_OMNIROUTE, CLAUDE_OMNIROUTE, CLAUDE_CODE_DIRECT) with 23 rounds each =
115 rounds.

Cloud executors are an admitted extension, not a new authority plane, so the
manifest can also be generated for a larger, explicitly named path set without
changing the mandatory default. Pass ``--paths`` (comma-separated) and/or
``--rounds`` to build an extended manifest for qualification planning.
"""
import argparse
import hashlib
import json
from pathlib import Path

PATHS = ["CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE", "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"]


def build(source_sha: str, paths, rounds: int) -> dict:
    commands = []
    for path in paths:
        for n in range(1, rounds + 1):
            raw = f"G4|{source_sha}|{path}|{n}".encode()
            cid = "g4-" + hashlib.sha256(raw).hexdigest()[:24]
            commands.append({"command_id": cid, "path": path, "round": n, "source_sha": source_sha})
    return {
        "schema": "mediahub.astra-gold.g4-115-manifest.v1",
        "status": "READY_FOR_EXECUTION",
        "source_sha": source_sha,
        "rounds": commands,
        "execution_policy": "external-only",
        "runner_creation": False,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source-sha", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--paths", default=",".join(PATHS), help="comma-separated executor paths")
    p.add_argument("--rounds", type=int, default=23, help="rounds per path (default 23)")
    a = p.parse_args()

    paths = [item.strip() for item in a.paths.split(",") if item.strip()]
    if not paths:
        raise SystemExit("no executor paths provided")
    if a.rounds < 1:
        raise SystemExit("rounds must be >= 1")

    manifest = build(a.source_sha, paths, a.rounds)
    manifest["paths"] = paths
    manifest["rounds_per_path"] = a.rounds
    a.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "source_sha": a.source_sha, "rounds": len(manifest["rounds"]), "paths": len(paths)}, sort_keys=True))


if __name__ == "__main__":
    main()
