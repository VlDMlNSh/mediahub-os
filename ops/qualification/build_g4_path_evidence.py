#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,sys
from pathlib import Path

def digest(v):
    return "sha256:"+hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()

path,src,target=sys.argv[1:4]
lines=[json.loads(x) for x in Path(src).read_text(encoding="utf-8").splitlines() if x.strip()]
blocked=[]
if len(lines)!=23: blocked.append(f"round_count={len(lines)}")
if any(x.get("source_sha")!=target for x in lines): blocked.append("source_sha_mismatch")
if any(x.get("path")!=path for x in lines): blocked.append("path_mismatch")
if {x.get("round") for x in lines}!={*range(1,24)}: blocked.append("round_set_invalid")
if any(x.get("verification_status")!="PASS" for x in lines): blocked.append("round_not_PASS")
result={"schema":"mediahub.astra-gold.g4-115-evidence.v1","status":"PASS" if not blocked else "BLOCKED","source_sha":target,"path":path,"rounds":lines,"blocked_reasons":blocked,"secret_values":"SUPPRESSED"}
result["evidence_digest"]=digest(result)
Path(src.replace(".jsonl",".json")).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(result,sort_keys=True))
raise SystemExit(0 if result["status"]=="PASS" else 2)
