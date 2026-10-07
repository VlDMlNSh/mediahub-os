#!/usr/bin/env python3
"""Fail-closed verifier for the real dual Codex/Claude 23-round wave."""
from __future__ import annotations
import argparse,json
from pathlib import Path

def read(path: Path, marker: str) -> list[dict]:
    rows=[]
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    if len(rows)!=23:
        raise SystemExit(f"{path}: round_count={len(rows)} expected=23")
    if [r.get("round") for r in rows] != list(range(1,24)):
        raise SystemExit(f"{path}: noncanonical_round_sequence")
    for r in rows:
        if r.get("status")!="PASS" or r.get("returncode")!=0 or r.get("marker")!=marker:
            raise SystemExit(f"{path}: round_{r.get('round')}_not_PASS")
        if not isinstance(r.get("timestamp"),int) or r["timestamp"]<=0:
            raise SystemExit(f"{path}: invalid_timestamp")
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--codex",required=True)
    p.add_argument("--claude",required=True)
    p.add_argument("--expected-sha",required=True)
    a=p.parse_args()
    read(Path(a.codex),"MEDIAHUB_LOCAL_CODEX_23WAVE_OK")
    read(Path(a.claude),"MEDIAHUB_LOCAL_CLAUDE_23WAVE_OK")
    print(json.dumps({"schema":"mediahub.astra.dual-local-23wave-verification.v1","status":"PASS","expected_sha":a.expected_sha,"codex_rounds":23,"claude_rounds":23,"secret_values":"SUPPRESSED"},sort_keys=True))
if __name__=="__main__":
    main()
