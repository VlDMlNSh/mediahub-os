#!/usr/bin/env python3
"""Fail-closed G8 pre-soak bundle verifier."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

REQUIRED=("g4_115","g5_coordination","g6_recovery","a3_independent","clean_worktree","fresh_bundle")

def verify(path: Path) -> dict:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: return {"status":"BLOCKED","reason":"invalid_g8_bundle","detail":repr(exc)}
    if data.get("fresh") is not True: return {"status":"BLOCKED","reason":"fresh_g8_bundle_required"}
    missing=[x for x in REQUIRED if data.get(x,{}).get("status")!="PASS"]
    if missing: return {"status":"BLOCKED","reason":"g8_prerequisites_not_passed","missing":missing}
    if data.get("g4_115",{}).get("observations") != 115: return {"status":"BLOCKED","reason":"g4_115_count_invalid"}
    if data.get("g4_115",{}).get("paths") != 5: return {"status":"BLOCKED","reason":"g4_path_count_invalid"}
    if data.get("g5_coordination",{}).get("max_parallel") != 2: return {"status":"BLOCKED","reason":"g5_parallelism_contract_invalid"}
    if data.get("a3_independent",{}).get("independence_attested") is not True: return {"status":"BLOCKED","reason":"a3_independence_missing"}
    if data.get("clean_worktree",{}).get("dirty") is not False: return {"status":"BLOCKED","reason":"worktree_not_clean"}
    if not data.get("bundle_sha256"): return {"status":"BLOCKED","reason":"bundle_integrity_missing"}
    if data.get("source_sha") and data.get("a3_independent",{}).get("source_sha") and data["source_sha"] != data["a3_independent"]["source_sha"]:
        return {"status":"BLOCKED","reason":"bundle_source_sha_mismatch"}
    return {"status":"PASS","prerequisites_verified":len(REQUIRED),"g4_observations":115}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("bundle",type=Path)
    args=p.parse_args()
    result=verify(args.bundle)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 2
if __name__=="__main__": sys.exit(main())
