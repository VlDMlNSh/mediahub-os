#!/usr/bin/env python3
"""Deterministic fail-closed evaluator for the ASTRA GOLD qualification/launch contract."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
import yaml

from ops.qualification.current_qualification_state import build as reduce_current_state
from ops.qualification.verify_g9_24h_soak import verify as verify_g9_evidence

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "architecture" / "ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml"


def load_schema() -> dict:
    return yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))


def evaluate(evidence: dict, schema: dict) -> dict:
    state=reduce_current_state(evidence)
    results=state["effective_gates"]
    failures=list(state["failed_gates"])
    launch=evidence.get("launch",{})
    required=schema["launch_contract"]["required_inputs"]
    missing_launch=[key for key in required if not launch.get(key)]
    approved_sha = str(launch.get("approved_source_sha",""))
    if launch.get("approved_source_sha") and (len(approved_sha) != 40 or any(ch not in "0123456789abcdefABCDEF" for ch in approved_sha)):
        missing_launch.append("approved_source_sha:invalid")
    for key in ("launch_target","rollback_target"):
        value=launch.get(key)
        if not isinstance(value,str) or not value.strip():
            missing_launch.append(key + ":nonempty_string_required")
    def record_ok(key: str) -> bool:
        value = launch.get(key)
        if not isinstance(value, dict):
            return False
        if value.get("status") not in ("PASS", "LAUNCH_READY"):
            return False
        if value.get("fresh") is not True:
            return False
        record_sha = str(value.get("source_sha", ""))
        if not re.fullmatch(r"[0-9a-fA-F]{40}", record_sha):
            return False
        if record_sha.lower() != approved_sha.lower():
            return False
        return True
    for key in ("fresh_evidence_bundle","A3_verification_record","soak_record"):
        if not record_ok(key):
            missing_launch.append(key + ":validated_evidence_record_required")
    soak_record=launch.get("soak_record")
    if isinstance(soak_record,dict) and record_ok("soak_record"):
        # Validate the launch-carried G9 record itself, without trusting only its
        # status/fresh/source_sha fields. The verifier normally reads a file, so
        # perform the same canonical contract checks inline here.
        conditions=soak_record.get("conditions",{})
        required_conditions=(
            "continuous_heartbeat",
            "no_unexplained_controller_restart",
            "no_duplicate_claim_corruption",
            "no_unresolved_execution_failure",
            "evidence_integrity",
            "no_authority_boundary_violation",
        )
        digest=str(soak_record.get("evidence_digest","")).lower()
        canonical=dict(soak_record)
        canonical.pop("evidence_digest",None)
        actual=__import__("hashlib").sha256(
            json.dumps(canonical,sort_keys=True,separators=(",",":")).encode("utf-8")
        ).hexdigest()
        telemetry_source_sha=str(soak_record.get("telemetry_source_sha","")).lower()
        telemetry_sha256=str(soak_record.get("telemetry_sha256","")).lower()
        if (
            soak_record.get("duration_hours") != 24
            or soak_record.get("secret_values") != "SUPPRESSED"
            or telemetry_source_sha != approved_sha.lower()
            or not re.fullmatch(r"[0-9a-f]{64}",telemetry_sha256)
            or any(conditions.get(k) is not True for k in required_conditions)
            or not re.fullmatch(r"[0-9a-f]{64}",digest)
            or actual != digest
        ):
            missing_launch.append("soak_record:g9_evidence_contract_invalid")
    if failures or missing_launch:
        return {
            "status":"BLOCKED",
            "launch_ready":False,
            "failed_gates":failures,
            "missing_launch_inputs":missing_launch,
            "gate_results":results,
            "next_blocker":failures[0] if failures else "launch_inputs",
        }
    return {
        "status":"LAUNCH_READY",
        "launch_ready":True,
        "failed_gates":[],
        "missing_launch_inputs":[],
        "gate_results":results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    evidence = json.loads(args.evidence.read_text(encoding="utf-8"))
    result = evaluate(evidence, load_schema())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "LAUNCH_READY" else 2


if __name__ == "__main__":
    sys.exit(main())
