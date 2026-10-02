#!/usr/bin/env python3
"""Fail-closed verifier for ASTRA-GOLD G9 24h soak evidence."""

from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED = (
    "continuous_heartbeat",
    "no_unexplained_controller_restart",
    "no_duplicate_claim_corruption",
    "no_unresolved_execution_failure",
    "evidence_integrity",
    "no_authority_boundary_violation",
)

def verify(path: Path, telemetry_path: Path) -> dict:
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status":"BLOCKED","reason":"invalid_g9_evidence_json","detail":repr(exc)}
    if not isinstance(data.get("workflow_run_id"), int) or data.get("workflow_run_id") <= 0:
        return {"status":"BLOCKED","reason":"workflow_run_id_invalid"}
    if not isinstance(data.get("workflow_run_url"), str) or not data.get("workflow_run_url").startswith("https://github.com/"):
        return {"status":"BLOCKED","reason":"workflow_run_url_invalid"}
    if data.get("fresh") is not True:
        return {"status":"BLOCKED","reason":"fresh_g9_evidence_required"}
    if data.get("duration_hours") != 24:
        return {"status":"BLOCKED","reason":"g9_duration_must_be_24_hours"}
    sha=str(data.get("source_sha",""))
    if not re.fullmatch(r"[0-9a-fA-F]{40}", sha):
        return {"status":"BLOCKED","reason":"g9_source_sha_invalid"}
    if data.get("secret_values") != "SUPPRESSED":
        return {"status":"BLOCKED","reason":"secret_policy_invalid"}
    telemetry_sha=str(data.get("telemetry_sha256","")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", telemetry_sha):
        return {"status":"BLOCKED","reason":"g9_telemetry_sha256_invalid"}
    try:
        actual_telemetry_sha=hashlib.sha256(telemetry_path.read_bytes()).hexdigest()
    except OSError as exc:
        return {"status":"BLOCKED","reason":"g9_telemetry_unreadable","detail":type(exc).__name__}
    if actual_telemetry_sha != telemetry_sha:
        return {"status":"BLOCKED","reason":"g9_telemetry_sha256_mismatch"}
    conditions=data.get("conditions",{})
    missing=[x for x in REQUIRED if conditions.get(x) is not True]
    if missing:
        return {"status":"BLOCKED","reason":"g9_required_conditions_not_proven","missing":missing}
    if not data.get("started_at") or not data.get("ended_at"):
        return {"status":"BLOCKED","reason":"g9_interval_metadata_missing"}
    digest=str(data.get("evidence_digest","")).lower()
    if not re.fullmatch(r"[0-9a-f]{64}", digest):
        return {"status":"BLOCKED","reason":"g9_evidence_digest_invalid"}
    canonical=dict(data)
    canonical.pop("evidence_digest",None)
    actual=hashlib.sha256(json.dumps(canonical,sort_keys=True,separators=(",",":")).encode("utf-8")).hexdigest()
    if actual != digest:
        return {"status":"BLOCKED","reason":"g9_evidence_digest_mismatch"}
    return {"status":"PASS","fresh":True,"duration_hours":24,"conditions_verified":len(REQUIRED)}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("evidence",type=Path)
    p.add_argument("--telemetry",type=Path,required=True)
    args=p.parse_args()
    result=verify(args.evidence,args.telemetry)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 2

if __name__=="__main__":
    sys.exit(main())
