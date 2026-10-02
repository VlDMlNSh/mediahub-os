#!/usr/bin/env python3
"""Build G9 evidence from observed worker telemetry; fail closed."""

from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

REQUIRED=(
    "continuous_heartbeat",
    "no_unexplained_controller_restart",
    "no_duplicate_claim_corruption",
    "no_unresolved_execution_failure",
    "evidence_integrity",
    "no_authority_boundary_violation",
)
SHA40=re.compile(r"^[0-9a-fA-F]{40}$")

def write_blocked(path: Path, reason: str, **extra) -> int:
    result={"status":"BLOCKED","reason":reason,"secret_values":"SUPPRESSED",**extra}
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 2

def parse_ts(value):
    if not isinstance(value,(int,float)): return None
    return float(value)

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("--telemetry",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--source-sha",required=True)
    a=p.parse_args()

    if not SHA40.fullmatch(a.source_sha):
        return write_blocked(a.output,"source_sha_invalid")

    try:
        telemetry_bytes=a.telemetry.read_bytes()
        telemetry_sha256=hashlib.sha256(telemetry_bytes).hexdigest()
        lines=telemetry_bytes.decode("utf-8").splitlines()
    except OSError as exc:
        return write_blocked(a.output,"telemetry_unreadable",detail=type(exc).__name__)

    observations=[]
    for line_no,line in enumerate(lines,1):
        if not line.strip(): continue
        try:
            item=json.loads(line)
        except json.JSONDecodeError as exc:
            return write_blocked(a.output,"telemetry_json_corrupt",line=line_no,detail=str(exc))
        if not isinstance(item,dict) or not isinstance(parse_ts(item.get("timestamp")),float):
            return write_blocked(a.output,"telemetry_observation_invalid",line=line_no)
        if not item.get("event") or not item.get("node_id") or not item.get("worker_id"):
            return write_blocked(a.output,"telemetry_identity_missing",line=line_no)
        telemetry_sha=str(item.get("source_sha",""))
        if not SHA40.fullmatch(telemetry_sha):
            return write_blocked(a.output,"telemetry_source_sha_invalid",line=line_no)
        if telemetry_sha.lower() != a.source_sha.lower():
            return write_blocked(a.output,"telemetry_source_sha_mismatch",line=line_no,
                                 telemetry_source_sha=telemetry_sha.lower())
        observations.append(item)

    if not observations:
        return write_blocked(a.output,"telemetry_empty")

    observations.sort(key=lambda x: x["timestamp"])
    start=observations[0]["timestamp"]
    end=observations[-1]["timestamp"]
    duration=end-start
    if duration < 86400:
        return write_blocked(a.output,"g9_full_duration_not_observed",
                             observed_seconds=round(duration,3))

    heartbeats=[x["timestamp"] for x in observations if x["event"]=="heartbeat"]
    if len(heartbeats)<2:
        continuous=False
        max_gap=None
    else:
        gaps=[b-a for a,b in zip(heartbeats,heartbeats[1:])]
        max_gap=max(gaps)
        # Worker poll interval defaults to 30s; allow bounded scheduling jitter,
        # but never accept a gap greater than 5 minutes as continuous heartbeat.
        continuous=max_gap <= 300.0

    starts=[x for x in observations if x["event"]=="controller_started"]
    pids={x.get("pid") for x in starts}
    unexplained_restart=len(starts)>1 or len(pids)>1

    duplicate_claim=any(x["event"] in {
        "duplicate_controller_lock_failure","duplicate_controller_or_lock_failure","claim_collision","claim_exists",
        "claim_capacity_exceeded","claim_corruption"
    } for x in observations)
    execution_failure=any(x["event"] in {
        "execution_failed","controller_error","claim_heartbeat_error","claim_release_error"
    } for x in observations)
    authority_violation=any(x["event"] in {
        "authority_boundary_violation","unauthorized_publish","unauthorized_launch"
    } for x in observations)

    conditions={
        "continuous_heartbeat":continuous,
        "no_unexplained_controller_restart":not unexplained_restart,
        "no_duplicate_claim_corruption":not duplicate_claim,
        "no_unresolved_execution_failure":not execution_failure,
        "evidence_integrity":True,
        "no_authority_boundary_violation":not authority_violation,
    }
    missing=[k for k,v in conditions.items() if not v]
    if missing:
        return write_blocked(a.output,"g9_runtime_conditions_failed",
                             failed_conditions=missing,observation_count=len(observations),
                             heartbeat_count=len(heartbeats),max_heartbeat_gap_seconds=max_gap,
                             controller_start_count=len(starts))

    start_iso=datetime.fromtimestamp(start,tz=timezone.utc).isoformat().replace("+00:00","Z")
    end_iso=datetime.fromtimestamp(end,tz=timezone.utc).isoformat().replace("+00:00","Z")
    payload={
        "schema":"mediahub.astra-gold.g9-24h-soak.v1",
        "fresh":True,
        "duration_hours":24,
        "source_sha":a.source_sha,
        "telemetry_source_sha":a.source_sha.lower(),
        "telemetry_sha256":telemetry_sha256,
        "telemetry_path":str(a.telemetry),
        "started_at":start_iso,
        "ended_at":end_iso,
        "conditions":conditions,
        "observation_count":len(observations),
        "heartbeat_count":len(heartbeats),
        "max_heartbeat_gap_seconds":round(max_gap,3) if max_gap is not None else None,
        "controller_start_count":len(starts),
        "secret_values":"SUPPRESSED",
    }
    canonical=json.dumps(payload,sort_keys=True,separators=(",",":"))
    payload["evidence_digest"]=hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return 0

if __name__=="__main__":
    sys.exit(main())
