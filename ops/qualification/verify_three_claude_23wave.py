#!/usr/bin/env python3
"""Fail-closed verifier for three independent Claude 23-wave lanes."""
import argparse,json
from pathlib import Path

def read(path: Path, marker: str, expected_sha: str):
    rows=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if len(rows)!=23 or [r.get("round") for r in rows]!=list(range(1,24)):
        raise SystemExit(f"{path}: invalid_23_round_sequence")
    for r in rows:
        if r.get("status")!="PASS" or r.get("returncode")!=0 or r.get("marker")!=marker:
            raise SystemExit(f"{path}: round_{r.get('round')}_not_PASS")
        if not isinstance(r.get("timestamp"),int) or r["timestamp"]<=0:
            raise SystemExit(f"{path}: invalid_timestamp")
        if r.get("target_sha", expected_sha) != expected_sha:
            raise SystemExit(f"{path}: target_sha_mismatch")
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--mh1",required=True); p.add_argument("--mac",required=True); p.add_argument("--mh2",required=True)
    p.add_argument("--expected-sha",required=True)
    a=p.parse_args()
    read(Path(a.mh1),"MEDIAHUB_CLAUDE_MH1_23WAVE_OK",a.expected_sha)
    read(Path(a.mac),"MEDIAHUB_CLAUDE_MAC_23WAVE_OK",a.expected_sha)
    read(Path(a.mh2),"MEDIAHUB_CLAUDE_MH2_23WAVE_OK",a.expected_sha)
    print(json.dumps({"schema":"mediahub.astra.three-claude-23wave-verification.v1","status":"PASS","expected_sha":a.expected_sha,"mh1_rounds":23,"mac_rounds":23,"mh2_rounds":23,"g5":3},sort_keys=True))
if __name__=="__main__":
    main()
