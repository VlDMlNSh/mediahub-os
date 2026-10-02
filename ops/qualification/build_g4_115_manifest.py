#!/usr/bin/env python3
"""Build a deterministic G4 command manifest; execution remains external and fail-closed."""
import argparse, hashlib, json
from pathlib import Path

PATHS = ["CODEX_FCC","CLAUDE_FCC","CODEX_OMNIROUTE","CLAUDE_OMNIROUTE","CLAUDE_CODE_DIRECT"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-sha", required=True)
    p.add_argument("--out", type=Path, required=True)
    a=p.parse_args()
    rounds=[]
    for path in PATHS:
        for n in range(1,24):
            raw=f"G4|{a.source_sha}|{path}|{n}".encode()
            cid="g4-"+hashlib.sha256(raw).hexdigest()[:24]
            rounds.append({"command_id":cid,"path":path,"round":n,"source_sha":a.source_sha})
    manifest={"schema":"mediahub.astra-gold.g4-115-manifest.v1","status":"READY_FOR_EXECUTION","source_sha":a.source_sha,"rounds":rounds,"execution_policy":"external-only","runner_creation":False}
    a.out.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":manifest["status"],"source_sha":a.source_sha,"rounds":len(rounds),"paths":len(PATHS)},sort_keys=True))
if __name__=="__main__":
    main()
