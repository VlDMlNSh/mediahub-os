#!/usr/bin/env python3
"""Build G9 evidence from observed soak telemetry; never synthesizes PASS."""

from __future__ import annotations
import argparse, hashlib, json, re, sys
from pathlib import Path

REQUIRED=(
    "continuous_heartbeat",
    "no_unexplained_controller_restart",
    "no_duplicate_claim_corruption",
    "no_unresolved_execution_failure",
    "evidence_integrity",
    "no_authority_boundary_violation",
)

def sha(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--telemetry",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--source-sha",required=True)
    a=p.parse_args()

    raw=a.telemetry.read_text(encoding="utf-8")
    try: data=json.loads(raw)
    except Exception as exc:
        result={"status":"BLOCKED","reason":"invalid_g9_telemetry","detail":repr(exc)}
        a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return 2

    observations=data.get("observations")
    conditions=data.get("conditions")
    required_meta=("started_at","ended_at","duration_hours")
    missing=[x for x in required_meta if not data.get(x)]
    if not isinstance(observations,list) or not isinstance(conditions,dict) or missing:
        result={"status":"BLOCKED","reason":"incomplete_g9_runtime_telemetry",
                "missing":missing,"secret_values":"SUPPRESSED"}
        a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return 2

    # PASS is allowed only when telemetry explicitly attests every required condition.
    absent=[x for x in REQUIRED if conditions.get(x) is not True]
    if data.get("duration_hours") != 24 or absent:
        result={"status":"BLOCKED","reason":"g9_conditions_not_proven",
                "duration_hours":data.get("duration_hours"),
                "missing_conditions":absent,"observation_count":len(observations),
                "source_sha":a.source_sha,"secret_values":"SUPPRESSED"}
        a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        return 2

    payload={
        "schema":"mediahub.astra-gold.g9-24h-soak.v1",
        "fresh":True,"duration_hours":24,"source_sha":a.source_sha,
        "started_at":data["started_at"],"ended_at":data["ended_at"],
        "conditions":{k:conditions[k] for k in REQUIRED},
        "observation_count":len(observations),
        "secret_values":"SUPPRESSED",
    }
    payload["evidence_digest"]=sha(json.dumps(payload,sort_keys=True,separators=(",",":")))
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0

if __name__=="__main__":
    sys.exit(main())
