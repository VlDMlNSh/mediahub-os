#!/usr/bin/env python3
"""Deterministic planner that minimizes active work before ASTRA GOLD test authorization.

This does not shorten mandatory qualification durations (notably G9=24h) and never
changes authority or gate requirements. It only selects the next highest-leverage
unblocked action and uses a geometric active-work budget target.
"""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

from ops.qualification.current_qualification_state import build as reduce_current_state

ORDER=(
    ("G0_IDENTITY","close identity/source gaps"),
    ("G1_BOUNDARY","close authority/transport/workspace boundaries"),
    ("G2_CONTROL_PLANE","close queue/claim/publication/heartbeat gaps"),
    ("G3_EXECUTION_PATH","close executor/runtime/result-validation gaps"),
    ("G4_23_WAVE_QUALIFICATION","execute fresh 115-round qualification"),
    ("G5_CONCURRENCY","collect fresh shared coordination attestation"),
    ("G6_RECOVERY","execute all fresh recovery scenarios"),
    ("G7_INTEGRATED_A3","run independent A3 verification"),
    ("G8_PRE_SOAK","assemble and verify fresh pre-soak bundle"),
    ("G9_24H_SOAK","complete mandatory 24h soak"),
    ("G10_LAUNCH_READY","reconcile launch-ready evidence"),
    ("G11_LAUNCH","human authorization and launch"),
)

def reduce_state(evidence: dict) -> dict:
    state=reduce_current_state(evidence)
    physical={"G4_23_WAVE_QUALIFICATION","G5_CONCURRENCY","G6_RECOVERY",
              "G7_INTEGRATED_A3","G8_PRE_SOAK","G9_24H_SOAK"}
    actions=dict(ORDER)
    blockers=[]
    for gate in state["failed_gates"]:
        if gate=="G11_LAUNCH":
            kind="HUMAN"; reason="explicit human authorization required"
        elif gate in physical:
            kind="PHYSICAL"; reason="fresh physical or integrated evidence missing"
        else:
            kind="ENGINEERING"; reason="gate not passed"
        blockers.append({"gate":gate,"action":actions.get(gate,"human authorization"),
                         "kind":kind,"reason":reason})
    return {"blockers":blockers,"next":blockers[0] if blockers else None,
            "remaining_count":len(blockers),
            "physical_blockers":sum(x["kind"]=="PHYSICAL" for x in blockers)}

def plan(evidence: dict, interaction: int = 1, initial_active_hours: float = 8.0) -> dict:
    state=reduce_state(evidence)
    target=max(0.25, initial_active_hours/(2**max(0,interaction-1)))
    nxt=state["next"]
    return {
        "status":"BLOCKED" if nxt else "READY_FOR_HUMAN_REVIEW",
        "next_gate":nxt["gate"] if nxt else "NONE",
        "next_action":nxt["action"] if nxt else "no_remaining_action",
        "next_kind":nxt["kind"] if nxt else "NONE",
        "next_reason":nxt["reason"] if nxt else "none",
        "interaction":interaction,
        "active_work_budget_target_hours":round(target,3),
        "geometric_factor":0.5,
        "remaining_blockers":state["remaining_count"],
        "physical_blockers":state["physical_blockers"],
        "mandatory_wall_clock_hours":24 if nxt and nxt["gate"]=="G9_24H_SOAK" else 0,
        "note":"Budget target is planning only; it cannot override fresh evidence, gate semantics, or mandatory duration."
    }

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument("evidence",type=Path)
    p.add_argument("--interaction",type=int,default=1)
    p.add_argument("--initial-active-hours",type=float,default=8.0)
    args=p.parse_args()
    print(json.dumps(plan(json.loads(args.evidence.read_text(encoding="utf-8")),
                          args.interaction,args.initial_active_hours),indent=2,sort_keys=True))
    return 0

if __name__=="__main__": sys.exit(main())
