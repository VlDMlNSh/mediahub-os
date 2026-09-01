#!/usr/bin/env python3
"""Unified MHX development execution pipeline.

This is execution infrastructure only. It delegates state-changing operations to
mhx.py and deliberately has no governance/baseline mutation capability.
"""
import argparse
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
MHX = ROOT / "tools" / "mhx.py"


def run_mhx(*args, allow=(0,)):
    cmd = [sys.executable, str(MHX), *map(str, args)]
    proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout, end="")
    if proc.stderr:
        print(proc.stderr, end="", file=sys.stderr)
    if proc.returncode not in allow:
        raise SystemExit(proc.returncode)
    return proc.returncode, proc.stdout


def pipeline(args):
    # Deterministic preparation. These operations never invoke an external worker.
    run_mhx("manifest", args.source)
    run_mhx("index")
    run_mhx("chunk", "--lines", args.lines)

    # Governance firewall is enforced by task creation before any routing/execution.
    task_args = [
        "task", "create", args.task_id, args.objective,
        "--task-class", args.task_class,
        "--base-revision", args.base_revision,
        "--context", args.context,
        "--expected-output", args.expected_output,
    ]
    if args.artifacts:
        task_args += ["--artifacts", *args.artifacts]
    if args.chunks:
        task_args += ["--chunks", *args.chunks]
    if args.constraints:
        task_args += ["--constraints", *args.constraints]
    if args.governance:
        task_args.append("--governance")
    if args.historical:
        task_args.append("--historical")
    if args.baseline:
        task_args.append("--baseline")

    code, output = run_mhx(*task_args, allow=(0, 3))
    if code == 3:
        print("PIPELINE_STOPPED: GOVERNANCE_FIREWALL")
        return 3

    task = json.loads(output)
    task_hash = task["task_hash"]

    # Cache resolution happens before worker invocation.
    code, cache_output = run_mhx("cache", task_hash, allow=(0, 1))
    cache = json.loads(cache_output)
    match = cache.get("match")
    if match == "EXACT":
        print("PIPELINE_CACHE_EXACT: REUSE")
        return 0
    if match == "RELATED":
        print("PIPELINE_CACHE_RELATED: DELTA_REQUIRED")
        return 0

    print("PIPELINE_EXECUTION_READY: MISS")
    print(f"TASK_ID={args.task_id}")
    print(f"TASK_HASH={task_hash}")
    print("NEXT=CLAIM_WORKER -> RESULT -> NORMALIZE -> REVIEW")
    return 0


def main():
    p = argparse.ArgumentParser(prog="mhx-pipeline")
    p.add_argument("source")
    p.add_argument("task_id")
    p.add_argument("objective")
    p.add_argument("--task-class", default="T1")
    p.add_argument("--base-revision", default="R0")
    p.add_argument("--context", default="CXT-1")
    p.add_argument("--lines", type=int, default=80)
    p.add_argument("--expected-output", default="result pack")
    p.add_argument("--artifacts", nargs="*", default=[])
    p.add_argument("--chunks", nargs="*", default=[])
    p.add_argument("--constraints", nargs="*", default=[])
    p.add_argument("--governance", action="store_true")
    p.add_argument("--historical", action="store_true")
    p.add_argument("--baseline", action="store_true")
    args = p.parse_args()
    try:
        return pipeline(args)
    except KeyboardInterrupt:
        print("PIPELINE_INTERRUPTED", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
