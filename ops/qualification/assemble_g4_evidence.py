#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

def digest(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

target=sys.argv[1]; output=Path(sys.argv[-1]); files=sys.argv[2:-1]
required=["CODEX_FCC","CLAUDE_FCC","CODEX_OMNIROUTE","CLAUDE_OMNIROUTE","CLAUDE_CODE_DIRECT"]
rounds=[]; blocked=[]
seen=set()
for f in files:
    d=json.loads(Path(f).read_text(encoding="utf-8"))
    if d.get("status")!="PASS": blocked.append(f"{f}:path_not_PASS")
    rounds.extend(d.get("rounds",[]))
if len(rounds)!=115: blocked.append(f"round_count={len(rounds)}")
counts={p:0 for p in required}
for r in rounds:
    p=r.get("path")
    if p not in counts: blocked.append("unknown_path:"+str(p)); continue
    counts[p]+=1
    key=(p,r.get("round"))
    if key in seen: blocked.append("duplicate_path_round:"+repr(key))
    seen.add(key)
    if r.get("source_sha")!=target: blocked.append("round_source_sha_mismatch")
    if r.get("verification_status")!="PASS": blocked.append("round_not_PASS")
for p,n in counts.items():
    if n!=23: blocked.append(f"{p}_round_count={n}")
result={"schema":"mediahub.astra-gold.g4-115-evidence.v1","status":"PASS" if not blocked else "BLOCKED","source_sha":target,"rounds":rounds,"path_counts":counts,"blocked_reasons":blocked,"secret_values":"SUPPRESSED"}
result["evidence_digest"]=digest(result)
output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps({"status":result["status"],"path_counts":counts,"blocked_reasons":blocked},sort_keys=True))
raise SystemExit(0 if result["status"]=="PASS" else 2)
