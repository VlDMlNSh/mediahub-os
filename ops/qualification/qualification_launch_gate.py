#!/usr/bin/env python3
"""Deterministic fail-closed evaluator for the ASTRA GOLD qualification/launch contract."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import yaml

from ops.qualification.current_qualification_state import build as reduce_current_state

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
    for key in ("fresh_evidence_bundle","A3_verification_record","soak_record"):
        if launch.get(key) is not True:
            missing_launch.append(key + ":explicit_confirmation_required")
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
