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
    gates = schema["gates"]
    statuses = evidence.get("gates", {})
    failures = []
    results = {}
    for gate_id in gates:
        if gate_id == "G11_LAUNCH":
            continue
        status = statuses.get(gate_id, "MISSING")
        gate_evidence = evidence.get("gate_evidence", {}).get(gate_id, {})
        if gate_id in {"G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY","G7_INTEGRATED_A3","G8_PRE_SOAK"}:
            if status == "PASS" and (gate_evidence.get("status") != "PASS" or gate_evidence.get("fresh") is not True):
                status = "BLOCKED"
            if gate_id == "G7_INTEGRATED_A3" and gate_evidence.get("independence_attested") is not True:
                status = "BLOCKED"
        results[gate_id] = status
        if status != "PASS":
            failures.append(gate_id)

    launch = evidence.get("launch", {})
    required = schema["launch_contract"]["required_inputs"]
    missing_launch = [key for key in required if not launch.get(key)]
    if statuses.get("G11_LAUNCH") != "HUMAN_AUTHORIZED":
        failures.append("G11_LAUNCH_HUMAN_AUTHORIZATION")
    if failures or missing_launch:
        reduced=reduce_current_state(evidence)
        return {
            "status": "BLOCKED",
            "launch_ready": False,
            "failed_gates": failures,
            "missing_launch_inputs": missing_launch,
            "gate_results": results,
            "next_blocker": reduced["failed_gates"][0] if reduced["failed_gates"] else "launch_inputs",
        }

    return {
        "status": "LAUNCH_READY",
        "launch_ready": True,
        "failed_gates": [],
        "missing_launch_inputs": [],
        "gate_results": results,
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
