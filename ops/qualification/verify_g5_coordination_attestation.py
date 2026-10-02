#!/usr/bin/env python3
"""Fail-closed verifier for fresh G5 shared-coordination attestations."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED = ("node_id","running_agent_source_sha","coordination_authority_id",
            "coordination_state","coordination_transport","active_claim_count",
            "reservation_result")

def verify(path: Path) -> dict:
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status":"BLOCKED","reason":"invalid_attestation_json","detail":repr(exc)}
    missing=[k for k in REQUIRED if k not in data]
    if missing:
        return {"status":"BLOCKED","reason":"missing_attestation_fields","missing":missing}
    if not data.get("fresh",False):
        return {"status":"BLOCKED","reason":"fresh_attestation_required"}
    source_sha=str(data.get("running_agent_source_sha",""))
    if not re.fullmatch(r"[0-9a-fA-F]{40}", source_sha):
        return {"status":"BLOCKED","reason":"running_agent_source_sha_invalid"}
    if data.get("secret_values") != "SUPPRESSED":
        return {"status":"BLOCKED","reason":"secret_policy_violation"}
    for field in ("node_id","coordination_authority_id","coordination_state","coordination_transport"):
        value=data.get(field)
        if not isinstance(value,str) or not value.strip() or value.strip().lower() in {"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}:
            return {"status":"BLOCKED","reason":"coordination_identity_invalid","field":field}
    timestamp=data.get("timestamp")
    if not isinstance(timestamp,(int,float)) and not isinstance(timestamp,str):
        return {"status":"BLOCKED","reason":"timestamp_missing"}
    digest=str(data.get("evidence_digest","")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}",digest):
        return {"status":"BLOCKED","reason":"evidence_digest_invalid"}
    canonical=dict(data)
    canonical.pop("evidence_digest",None)
    actual=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
    if actual != digest:
        return {"status":"BLOCKED","reason":"evidence_digest_mismatch"}
    if data.get("reservation_result") != "PASS":
        return {"status":"BLOCKED","reason":"reservation_not_pass"}
    if not isinstance(data.get("active_claim_count"), int) or not 0 <= data["active_claim_count"] <= 2:
        return {"status":"BLOCKED","reason":"active_claim_count_invalid"}
    if data.get("duplicate_controller_detected") is not False:
        return {"status":"BLOCKED","reason":"duplicate_controller_not_proven_absent"}
    if data.get("shared_surface_serialization") is not True:
        return {"status":"BLOCKED","reason":"shared_surface_serialization_not_attested"}
    if data.get("disjoint_claims_attested") is not True:
        return {"status":"BLOCKED","reason":"disjoint_claims_not_attested"}
    if not data["coordination_authority_id"] or not data["coordination_state"] or not data["coordination_transport"]:
        return {"status":"BLOCKED","reason":"shared_coordination_domain_unresolved"}
    return {"status":"PASS","node_id":data["node_id"],
            "coordination_authority_id":data["coordination_authority_id"],
            "running_agent_source_sha":data["running_agent_source_sha"]}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("attestation",type=Path)
    args=p.parse_args()
    result=verify(args.attestation)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 2

if __name__=="__main__":
    sys.exit(main())
