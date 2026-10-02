#!/usr/bin/env python3
"""Render the single current-truth artifact for ASTRA GOLD.

The reference-scheme review found the current status (NOT_PROVEN / BLOCKED)
restated as prose across several documents, which can drift. This generator
produces one deterministic artifact from the governance contract and an optional
gate-evidence file, so "current truth" is read from a generated file instead of
prose. With no evidence supplied every gate is BLOCKED (fail-closed).
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
GOVERNANCE = ROOT / "architecture" / "ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml"

BLOCKED = "BLOCKED"


def render(governance: dict, evidence: dict | None) -> str:
    gates = governance["gate_registry"]["gates"]
    results = (evidence or {}).get("gate_results", evidence or {}) if evidence else {}

    lines = [
        "<!-- GENERATED FILE — do not edit by hand.",
        "     Regenerate with: python ops/qualification/render_current_truth.py --out docs/qualification/CURRENT-TRUTH.generated.md",
        "     Source: architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml -->",
        "",
        "# ASTRA GOLD — Current Truth (generated)",
        "",
        "This file is generated from the governance contract and, when present, a",
        "gate-evidence file. It is the single readable source of current gate state.",
        "No gate is promoted by this document.",
        "",
        "## Gates",
        "",
        "| Gate | Name | Status |",
        "|---|---|---|",
    ]

    for gate in gates:
        status = results.get(gate["id"], BLOCKED)
        lines.append(f"| {gate['id']} | {gate['name']} | {status} |")

    qualified = [gate["id"] for gate in gates if results.get(gate["id"]) == "PASS"]
    if qualified:
        truth = "PARTIAL — some gates have fresh PASS evidence"
    else:
        truth = "NOT_PROVEN / BLOCKED — no gate has fresh PASS evidence"

    lines += [
        "",
        "## Truth status",
        "",
        f"- Overall: {truth}",
        "- `ASTRA_GOLD_ELIGIBLE` is not asserted unless every mandatory gate has fresh PASS evidence at one frozen SHA.",
        "- `LAUNCH_READY` requires fresh PASS of G0–G9 and a complete launch-input bundle.",
        "- G11 is HUMAN_ONLY.",
        "",
        "## Promotion ladder",
        "",
        "`REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS →",
        "PROBE_PASS → EXECUTION_PASS → RESULT_VALIDATION_PASS → A3_VERIFIED →",
        "ASTRA_GOLD_ELIGIBLE → LAUNCH_READY → LAUNCHED` — no implicit transitions.",
        "",
    ]

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, default=None)
    args = parser.parse_args()

    governance = yaml.safe_load(GOVERNANCE.read_text(encoding="utf-8"))
    evidence = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else None

    args.out.write_text(render(governance, evidence), encoding="utf-8")
    print(f"CURRENT_TRUTH_WRITTEN={args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
