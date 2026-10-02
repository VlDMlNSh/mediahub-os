#!/usr/bin/env python3
"""Convert a dual-local-executor result into canonical G4 evidence, fail-closed."""
import argparse, hashlib, json
from pathlib import Path

PATHS = ["fcc_codex","fcc_claude","omni_claude","omni_codex","claude_code_direct"]

def digest(value):
    raw=json.dumps(value,sort_keys=True,separators=(",",":")).encode()
    return "sha256:"+hashlib.sha256(raw).hexdigest()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",type=Path)
    p.add_argument("output",type=Path)
    p.add_argument("--expected-sha",required=True)
    a=p.parse_args()
    raw=json.loads(a.input.read_text(encoding="utf-8"))
    rounds=raw.get("evidence_rounds",[])
    blocked=[]
    if raw.get("status")!="PASS": blocked.append("executor_result_not_PASS")
    if len(rounds)!=115: blocked.append(f"round_count={len(rounds)}_expected=115")
    for path in PATHS:
        count=sum(1 for x in rounds if x.get("path")==path.upper())
        if count!=23: blocked.append(f"{path}_round_count={count}_expected=23")
    for i,x in enumerate(rounds,1):
        if x.get("source_sha")!=a.expected_sha: blocked.append(f"round_{i}_source_sha_mismatch")
        if x.get("verification_status")!="PASS": blocked.append(f"round_{i}_verification_not_PASS")
    evidence={
      "schema":"mediahub.astra-gold.g4-115-evidence.v1",
      "status":"PASS" if not blocked else "BLOCKED",
      "source_sha":a.expected_sha,
      "rounds":rounds,
      "blocked_reasons":blocked,
      "secret_values":"SUPPRESSED",
    }
    evidence["evidence_digest"]=digest(evidence)
    a.output.write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":evidence["status"],"rounds":len(rounds),"blocked_reasons":blocked},sort_keys=True))
    return 0 if evidence["status"]=="PASS" else 2

if __name__=="__main__":
    raise SystemExit(main())
