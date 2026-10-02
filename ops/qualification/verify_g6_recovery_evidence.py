#!/usr/bin/env python3
"""Fail-closed verifier for G6 publication-recovery evidence."""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime
from pathlib import Path

SCENARIOS=("timeout","executor_failure","transport_interruption","stale_claim",
           "worker_restart","duplicate_controller","replay_idempotency",
           "result_publication_recovery")
RECOVERY=("published_result_identity","source_sha","remote_branch_tip",
          "local_processed_state_reconciliation")

def verify(path: Path) -> dict:
    try:
        data=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status":"BLOCKED","reason":"invalid_recovery_evidence_json","detail":repr(exc)}
    if data.get("fresh") is not True:
        return {"status":"BLOCKED","reason":"fresh_recovery_evidence_required"}
    if data.get("secret_values") not in (None, "SUPPRESSED"):
        return {"status":"BLOCKED","reason":"secret_policy_violation"}
    scenarios=data.get("scenarios",{})
    source_shas=set()
    for name in SCENARIOS:
        item=scenarios.get(name,{})
        if not isinstance(item,dict):
            return {"status":"BLOCKED","reason":"scenario_record_invalid","scenario":name}
        if item.get("fresh") is not True:
            return {"status":"BLOCKED","reason":"scenario_not_fresh","scenario":name}
        sha=str(item.get("source_sha",""))
        if not re.fullmatch(r"[0-9a-fA-F]{40}",sha):
            return {"status":"BLOCKED","reason":"scenario_source_sha_invalid","scenario":name}
        for field in ("command_id","node_id"):
            value=item.get(field)
            if not isinstance(value,str) or not value.strip() or value.strip().lower() in {"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}:
                return {"status":"BLOCKED","reason":"scenario_identity_invalid","scenario":name,"field":field}
        for field in ("executor_id","provider_or_model_id","transport_id","workspace","verification_status"):
            value=item.get(field)
            if not isinstance(value,str) or not value.strip() or value.strip().lower() in {"unknown","undefined","none","null","n/a","na","tbd","todo","placeholder","unset"}:
                return {"status":"BLOCKED","reason":"scenario_metadata_invalid","scenario":name,"field":field}
        if item.get("status") != "PASS" or item.get("verification_status") != "PASS":
            return {"status":"BLOCKED","reason":"scenario_verification_not_pass","scenario":name}
        timestamp=item.get("timestamp")
        if not isinstance(timestamp,(int,float,str)) or (isinstance(timestamp,str) and not timestamp.strip()):
            return {"status":"BLOCKED","reason":"scenario_timestamp_missing","scenario":name}
        if isinstance(timestamp,str):
            try:
                datetime.fromisoformat(timestamp.replace("Z","+00:00"))
            except ValueError:
                return {"status":"BLOCKED","reason":"scenario_timestamp_invalid","scenario":name}
        elif not isinstance(timestamp,(int,float)):
            return {"status":"BLOCKED","reason":"scenario_timestamp_invalid","scenario":name}
        digest=str(item.get("evidence_digest","")).lower()
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            return {"status":"BLOCKED","reason":"scenario_evidence_digest_invalid","scenario":name}
        if item.get("secret_values") not in (None, "SUPPRESSED"):
            return {"status":"BLOCKED","reason":"scenario_secret_policy_violation","scenario":name}
        canonical=dict(item)
        canonical.pop("evidence_digest",None)
        actual=hashlib.sha256(
            json.dumps(canonical,sort_keys=True,separators=(",",":")).encode("utf-8")
        ).hexdigest()
        if actual != digest:
            return {"status":"BLOCKED","reason":"scenario_evidence_digest_mismatch","scenario":name}
        source_shas.add(sha.lower())
    if len(source_shas) != 1:
        return {"status":"BLOCKED","reason":"scenario_source_sha_mismatch"}

    missing=[s for s in SCENARIOS if scenarios.get(s,{}).get("status")!="PASS"]
    if missing:
        return {"status":"BLOCKED","reason":"required_recovery_scenarios_not_passed","missing":missing}
    pub=scenarios["result_publication_recovery"]
    missing_fields=[k for k in RECOVERY if not pub.get(k)]
    if missing_fields:
        return {"status":"BLOCKED","reason":"publication_recovery_fields_missing","missing":missing_fields}
    if not isinstance(pub["published_result_identity"],dict):
        return {"status":"BLOCKED","reason":"published_result_identity_not_structured"}
    if not pub["published_result_identity"]:
        return {"status":"BLOCKED","reason":"published_result_identity_empty"}
    if not re.fullmatch(r"[0-9a-fA-F]{40}",str(pub["source_sha"])):
        return {"status":"BLOCKED","reason":"publication_source_sha_invalid"}
    if str(pub["source_sha"]).lower() != next(iter(source_shas)):
        return {"status":"BLOCKED","reason":"publication_source_sha_mismatch"}
    if not re.fullmatch(r"[0-9a-fA-F]{40}",str(pub["remote_branch_tip"])):
        return {"status":"BLOCKED","reason":"remote_branch_tip_invalid"}
    reconciliation=pub["local_processed_state_reconciliation"]
    if not isinstance(reconciliation,dict) or not reconciliation:
        return {"status":"BLOCKED","reason":"processed_state_reconciliation_invalid"}
    if reconciliation.get("status")!="RECONCILED":
        return {"status":"BLOCKED","reason":"processed_state_not_reconciled"}
    if not reconciliation.get("processed_state_identity"):
        return {"status":"BLOCKED","reason":"processed_state_identity_missing"}
    if pub.get("duplicate_execution_detected") is not False:
        return {"status":"BLOCKED","reason":"duplicate_execution_not_suppressed"}
    if pub.get("evidence_rewritten") is not False:
        return {"status":"BLOCKED","reason":"evidence_rewrite_detected"}
    return {"status":"PASS","fresh":True,"scenarios_checked":len(SCENARIOS)}

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("evidence",type=Path)
    args=p.parse_args()
    result=verify(args.evidence)
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["status"]=="PASS" else 2

if __name__=="__main__":
    sys.exit(main())
