#!/usr/bin/env python3
"""Fail-closed verifier for independent A3 evidence."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED=("focused_tests","regression","contracts","architecture_conformance",
          "security","concurrency","failure","recovery","exact_sha_evidence")

def verify(path: Path) -> dict:
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc: return {"status":"BLOCKED","reason":"invalid_a3_evidence_json","detail":repr(exc)}
    if data.get("fresh") is not True: return {"status":"BLOCKED","reason":"fresh_a3_evidence_required"}
    if data.get("verifier_role") != "A3": return {"status":"BLOCKED","reason":"independent_a3_verifier_required"}
    if data.get("independence_attested") is not True: return {"status":"BLOCKED","reason":"a3_independence_not_attested"}
    if data.get("source_evidence_path") == data.get("a3_evidence_path"): return {"status":"BLOCKED","reason":"self_verification_surface"}
    missing=[x for x in REQUIRED if data.get(x,{}).get("status")!="PASS"]
    if missing: return {"status":"BLOCKED","reason":"a3_required_checks_not_passed","missing":missing}
    source_sha=str(data.get("source_sha",""))
    verified_sha=str(data.get("verified_sha",""))
    if not re.fullmatch(r"[0-9a-fA-F]{40}", source_sha) or not re.fullmatch(r"[0-9a-fA-F]{40}", verified_sha) or source_sha.lower() != verified_sha.lower():
        return {"status":"BLOCKED","reason":"a3_exact_sha_mismatch"}
    if data.get("secret_values") not in (None, "SUPPRESSED"):
        return {"status":"BLOCKED","reason":"secret_policy_violation"}
    digest = str(data.get("evidence_sha256","")).lower()
    if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        return {"status":"BLOCKED","reason":"a3_evidence_integrity_invalid"}
    evidence_path = Path(str(data.get("source_evidence_path","")))
    if not evidence_path.is_file():
        return {"status":"BLOCKED","reason":"a3_source_evidence_missing"}
    actual = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    if actual != digest:
        return {"status":"BLOCKED","reason":"a3_evidence_digest_mismatch"}
    return {"status":"PASS","verifier_role":"A3","source_sha":data["source_sha"],
            "evidence_sha256":data["evidence_sha256"],"checks_verified":len(REQUIRED)}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("evidence",type=Path)
    args=p.parse_args()
    result=verify(args.evidence)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 2

if __name__=="__main__": sys.exit(main())
