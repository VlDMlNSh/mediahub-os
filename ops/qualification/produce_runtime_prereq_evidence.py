#!/usr/bin/env python3
"""Deterministic, fail-closed producers for the pre-soak runtime gates.

These producers exercise the real MediaHub/Astra runtime modules present in this
checkout (autonomous queue, claim/lease fabric, generation fencing, in-memory
state authority, durable memory). They never fabricate PASS:

- every observation must be directly produced by running the module under test;
- the file-level ``status`` is PASS only when all observations hold *and* the
  producer is running in the canonical qualification context (node ``mh-dev-01``).

Live multi-node field evidence is still required by A3 and is not asserted here.
Secrets are never read or emitted.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import subprocess
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

CANONICAL_NODE = "mh-dev-01"
SECRETS = "SUPPRESSED"


def digest(payload: object) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _claim(task_id: str, paths, now: float = 100.0):
    from mediahub_runtime.agent_fabric import AgentClaim

    return AgentClaim(
        "A2-BUILDER", task_id, "qualification", tuple(paths), ("implement",), (),
        "ACTIVE", now, now, now + 900, "base",
    )


def check_scheduler() -> dict:
    """Deterministic task selection, ordering, gating and suppression."""
    from mediahub_runtime import autonomous_queue as q

    obs: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        tasks = root / "tasks"
        tasks.mkdir()
        state = root / "state"
        (state / "completed").mkdir(parents=True)
        (tasks / "b.json").write_text(json.dumps({"task_id": "B", "status": "WAIT", "priority": "P0"}))
        (tasks / "a.json").write_text(json.dumps({"task_id": "A", "status": "READY", "priority": "P1"}))
        (tasks / "c.json").write_text(json.dumps({"task_id": "C", "status": "READY", "priority": "P0", "dependencies": ["DEP"]}))
        old_tasks, old_state = q.TASK_DIR, q.STATE
        q.TASK_DIR, q.STATE = tasks, state
        try:
            ids = [t["task_id"] for t in q.load_tasks()]
            obs["non_ready_excluded"] = "B" not in ids
            obs["priority_then_id_order"] = ids == ["C", "A"]
            obs["ready_tasks_selected"] = set(ids) == {"A", "C"}
            obs["dependency_unsatisfied_gated"] = not q.dependencies_satisfied({"dependencies": ["DEP"]})
            (state / "completed" / "DEP.json").write_text(json.dumps({"status": "VERIFIED"}))
            obs["dependency_satisfied_after_completion"] = q.dependencies_satisfied({"dependencies": ["DEP"]})
            obs["completed_task_suppressed"] = q.completed("DEP")
            obs["selection_deterministic"] = [t["task_id"] for t in q.load_tasks()] == [t["task_id"] for t in q.load_tasks()]
        finally:
            q.TASK_DIR, q.STATE = old_tasks, old_state
    return obs


def check_fencing() -> dict:
    """Claim/lease fencing plus authoritative generation fencing."""
    import mediahub_runtime.agent_fabric as af

    from mediahub_runtime.agent_fabric import AgentFabricError, ClaimStore
    from mediahub_runtime.in_memory_state import InMemoryStateAuthority, StaleTransaction
    from mediahub_runtime.generation import Generation
    from mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy

    obs: dict[str, bool] = {}
    orig_time = af.time.time
    with tempfile.TemporaryDirectory() as tmp:
        store = ClaimStore(Path(tmp))
        af.time.time = lambda: 100.0
        try:
            store.acquire(_claim("A", ["src/a.py"]))
            try:
                store.acquire(_claim("B", ["src/a.py"]))
                obs["duplicate_overlap_rejected"] = False
            except AgentFabricError as exc:
                obs["duplicate_overlap_rejected"] = str(exc) == "claim_collision"
            try:
                store.acquire(_claim("A", ["other/x.py"]))
                obs["duplicate_controller_rejected"] = False
            except AgentFabricError as exc:
                obs["duplicate_controller_rejected"] = str(exc) == "claim_exists"
            store.acquire(_claim("C", ["docs/b.md"]))
            obs["disjoint_claims_admitted"] = len([c for c in store.list_claims() if c.status == "ACTIVE"]) == 2
        finally:
            af.time.time = orig_time
        af.time.time = lambda: 1000.0
        try:
            store.acquire(_claim("D", ["src/a.py"], now=1000.0))
            claims = {c.task_id: c for c in store.list_claims()}
            obs["stale_lease_expired"] = claims["A"].status == "EXPIRED"
            obs["stale_lease_reacquirable"] = claims["D"].status == "ACTIVE"
        finally:
            af.time.time = orig_time

    ops = ("begin", "commit", "abort", "snapshot", "restore")
    ctx = AuthorizationContext("A0", "state")
    policy = AuthorizationPolicy(grants={("A0", "state", op) for op in ops})
    authority = InMemoryStateAuthority(
        Generation("gen-1", "1.0.0", "1.0.0", "0", "ref"), {"value": 0}, policy
    )
    tx1 = authority.begin(ctx, {"value": 1})
    tx2 = authority.begin(ctx, {"value": 2})
    authority.commit(tx1)
    try:
        authority.commit(tx2)
        obs["stale_transaction_rejected"] = False
    except StaleTransaction:
        obs["stale_transaction_rejected"] = True
    return obs


def check_recovery() -> dict:
    """Bounded failure/timeout handling and state recovery after failure."""
    from mediahub_runtime.autonomous_task import AutonomousTaskPolicy, BoundedAutonomousTask
    from mediahub_runtime.in_memory_state import InMemoryStateAuthority
    from mediahub_runtime.generation import Generation
    from mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy

    obs: dict[str, bool] = {}

    def boom(_plan, _attempt):
        raise RuntimeError("executor_failure")

    failed = BoundedAutonomousTask(
        plan=lambda: {"phase": "plan"},
        execute=boom,
        verify=lambda _r, _a: (True, "unreachable"),
        policy=AutonomousTaskPolicy(max_attempts=2, max_repairs=0, max_duration_seconds=30.0),
    ).run()
    obs["executor_failure_bounded"] = failed.status == "FAILED"

    clock = [0.0]

    def advancing() -> float:
        if clock:
            return clock.pop(0)
        return 100.0

    timed_out = BoundedAutonomousTask(
        plan=lambda: {"phase": "plan"},
        execute=lambda _p, _a: {"ok": True},
        verify=lambda _r, _a: (True, "ok"),
        policy=AutonomousTaskPolicy(max_attempts=3, max_repairs=0, max_duration_seconds=0.5),
        clock=advancing,
    ).run()
    obs["timeout_enforced"] = timed_out.status == "REPAIR_EXHAUSTED" and timed_out.attempts == 0

    attempts = {"n": 0}

    def flaky(_plan, _attempt):
        attempts["n"] += 1
        if attempts["n"] == 1:
            raise RuntimeError("first_attempt")
        return {"ok": True}

    recovered = BoundedAutonomousTask(
        plan=lambda: {"phase": "plan"},
        execute=flaky,
        verify=lambda _r, _a: (True, "ok"),
        repair=lambda plan, _r, _a: plan,
        policy=AutonomousTaskPolicy(max_attempts=3, max_repairs=1, max_duration_seconds=30.0),
    ).run()
    obs["bounded_repair_recovers"] = recovered.status == "PASS" and recovered.repairs == 1

    ops = ("begin", "commit", "abort", "snapshot", "restore")
    ctx = AuthorizationContext("A0", "state")
    policy = AuthorizationPolicy(grants={("A0", "state", op) for op in ops})
    authority = InMemoryStateAuthority(
        Generation("gen-1", "1.0.0", "1.0.0", "0", "ref"), {"value": 0}, policy
    )
    checkpoint = authority.snapshot(ctx)
    mutated = authority.commit(authority.begin(ctx, {"value": 9}))
    restored = authority.restore(checkpoint, ctx)
    obs["state_recovers_after_failure"] = restored.payload["value"] == 0 and mutated.payload["value"] == 9
    return obs


def check_backup_restore() -> dict:
    """Snapshot/restore ownership, state round-trip and durable memory round-trip."""
    from mediahub_runtime.astra_memory import AstraMemory, MEMORY_CLASSES
    from mediahub_runtime.in_memory_state import (
        InMemoryStateAuthority,
        InvalidCheckpoint,
    )
    from mediahub_runtime.generation import Generation
    from mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy

    obs: dict[str, bool] = {}
    ops = ("begin", "commit", "abort", "snapshot", "restore")
    ctx = AuthorizationContext("A0", "state")
    policy = AuthorizationPolicy(grants={("A0", "state", op) for op in ops})
    first = InMemoryStateAuthority(
        Generation("gen-1", "1.0.0", "1.0.0", "0", "ref"), {"value": "before"}, policy
    )
    second = InMemoryStateAuthority(
        Generation("gen-1", "1.0.0", "1.0.0", "0", "ref"), {"value": "other"}, policy
    )
    checkpoint = first.snapshot(ctx)
    first.commit(first.begin(ctx, {"value": "after"}))
    restored = first.restore(checkpoint, ctx)
    obs["snapshot_restore_roundtrip"] = restored.payload["value"] == "before"
    try:
        second.restore(checkpoint, ctx)
        obs["foreign_checkpoint_rejected"] = False
    except InvalidCheckpoint:
        obs["foreign_checkpoint_rejected"] = True

    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "memory.jsonl"
        memory = AstraMemory(path)
        for memory_class in MEMORY_CLASSES:
            memory.remember(memory_class, f"{memory_class} backup evidence", project_id="p1")
        reloaded = AstraMemory(path)
        obs["durable_memory_roundtrip"] = {r.memory_class for r in reloaded.records()} == set(MEMORY_CLASSES)
        obs["memory_scope_isolated"] = len(reloaded.select("backup", project_id="other")) == 0
    return obs


CHECKS = {
    "scheduler-e2e.json": ("scheduler_live_e2e", check_scheduler),
    "fencing.json": ("multi_node_fencing", check_fencing),
    "recovery.json": ("runtime_recovery", check_recovery),
    "backup-restore.json": ("backup_restore", check_backup_restore),
}


def build(out_dir: Path, *, node: str | None = None) -> dict:
    node = node or platform.node()
    canonical = node == CANONICAL_NODE
    out_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict] = {}
    target_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not target_sha:
        raise RuntimeError("target_sha_unavailable")
    for name, (check, producer) in CHECKS.items():
        observations = producer()
        passed = all(observations.values()) if observations else False
        status = "PASS" if passed and canonical else "BLOCKED"
        if not passed:
            reason = "observation_failed"
        elif not canonical:
            reason = "non_canonical_context"
        else:
            reason = ""
        payload = {
            "schema": "mediahub.pre-soak-evidence.v1",
            "status": status,
            "captured_at": int(time.time()),
            "target_sha": target_sha,
            "node_id": node,
            "canonical_node": canonical,
            "scope": "single_node_deterministic_module_exercise",
            "requires_live_integration": True,
            "check": check,
            "reason": reason,
            "observations": observations,
            "secret_values": SECRETS,
        }
        payload["evidence_digest"] = digest({k: v for k, v in payload.items() if k != "evidence_digest"})
        (out_dir / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        summary[name] = {"status": status, "reason": reason, "observations": observations}
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=ROOT / "evidence")
    parser.add_argument("--node", default=None, help="override node identity (tests/lab only)")
    args = parser.parse_args()
    summary = build(args.out, node=args.node)
    blocked = sorted(name for name, item in summary.items() if item["status"] != "PASS")
    print(json.dumps({
        "schema": "mediahub.astra-gold.runtime-prereq-producer.v1",
        "status": "PASS" if not blocked else "BLOCKED",
        "out_dir": str(args.out),
        "artifacts": summary,
        "blocked": blocked,
        "secret_values": SECRETS,
    }, indent=2, sort_keys=True))
    return 0 if not blocked else 2


if __name__ == "__main__":
    raise SystemExit(main())
