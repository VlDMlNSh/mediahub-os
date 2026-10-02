#!/usr/bin/env python3
"""Build a deterministic current qualification state from fresh evidence."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path

GATES=("G0_IDENTITY","G1_BOUNDARY","G2_CONTROL_PLANE","G3_EXECUTION_PATH",
       "G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY",
       "G7_INTEGRATED_A3","G8_PRE_SOAK","G9_24H_SOAK","G10_LAUNCH_READY","G11_LAUNCH")
FRESH=("G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY","G7_INTEGRATED_A3","G8_PRE_SOAK","G9_24H_SOAK")

def build(source: dict) -> dict:
    gates=dict(source.get("gates",{}))
    evidence=dict(source.get("gate_evidence",{}))
    failures=[]
    effective=dict(gates)
    prerequisites = {
        "G5_CONCURRENCY": ("G4_23_WAVE_QUALIFICATION",),
        "G6_RECOVERY": ("G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY"),
        "G7_INTEGRATED_A3": ("G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY"),
        "G8_PRE_SOAK": ("G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY","G7_INTEGRATED_A3"),
        "G9_24H_SOAK": ("G8_PRE_SOAK",),
        "G10_LAUNCH_READY": ("G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY","G7_INTEGRATED_A3","G8_PRE_SOAK","G9_24H_SOAK"),
    }
    for gate, required_gates in prerequisites.items():
        if gates.get(gate) == "PASS" and any(effective.get(dep) != "PASS" for dep in required_gates):
            effective[gate] = "BLOCKED"
    for gate in GATES:
        if gate=="G11_LAUNCH":
            if gates.get(gate)!="HUMAN_AUTHORIZED": failures.append(gate)
            continue
        status=gates.get(gate,"MISSING")
        if gate in FRESH:
            e=evidence.get(gate,{})
            if status=="PASS" and e.get("fresh") is not True: status="BLOCKED"
            if gate=="G7_INTEGRATED_A3" and e.get("independence_attested") is not True: status="BLOCKED"
        effective[gate]=status
        if status!="PASS": failures.append(gate)
    return {"schema":"mediahub.astra-gold.current-qualification-state.v1",
            "status":"LAUNCH_READY" if not failures else "BLOCKED",
            "gates":gates,"effective_gates":effective,"failed_gates":failures,
            "fresh_evidence_gates":[g for g in FRESH if evidence.get(g,{}).get("fresh") is True],
            "physical_blockers":[g for g in FRESH if evidence.get(g,{}).get("fresh") is not True],
            "source_sha":source.get("source_sha","")}

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument("input",type=Path); p.add_argument("--output",type=Path)
    a=p.parse_args()
    raw=a.input.read_bytes(); state=build(json.loads(raw))
    state["input_sha256"]=hashlib.sha256(raw).hexdigest()
    out=json.dumps(state,indent=2,sort_keys=True)
    if a.output: a.output.write_text(out+"\n",encoding="utf-8")
    else: print(out)
    return 0 if state["status"]=="LAUNCH_READY" else 2

if __name__=="__main__": sys.exit(main())
