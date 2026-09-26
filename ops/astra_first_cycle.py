#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import time
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

os.environ.setdefault("MEDIAHUB_AI_URL", "http://127.0.0.1:11434/v1/chat/completions")
os.environ.setdefault("MEDIAHUB_LOCAL_MODEL_NAME", "qwen2.5-coder:3b")

from ops.astra_coordinator_lease import CoordinatorLease, CoordinatorLeaseError
from ops.astra_patch_admission import PatchAdmissionError, StructuredPatch, admit_patch
from ops.mediahub_task_lifecycle import *  # noqa: F401,F403
from runtime.mediahub_control_plane.model import Task, TaskStatus
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.sqlite_repository import SQLiteControlPlaneRepository
from ops.local_autonomous_agent import _generate_endpoint

STATE = ROOT / ".autonomous"
DB = STATE / "control-plane.sqlite3"
LOCK = STATE / "coordinator.lock"
BRANCH = "engineering/mh21-sandbox-lifecycle-20260910"
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"
AGENT = "astra-local-qwen"

TASKS = (
    {
        "id": "ASTRA-FIRST-001",
        "path": "tests/ops/test_patch_admission.py",
        "instruction": "Add one regression test named test_admission_limits_patch_size. The test must construct a StructuredPatch containing a small valid unified diff and assert admit_patch(..., max_patch_bytes=10) raises PatchAdmissionError. Do not modify imports or existing tests.",
        "test": "pytest -q tests/ops/test_patch_admission.py",
    },
    {
        "id": "ASTRA-FIRST-002",
        "path": "tests/ops/test_coordinator_lease.py",
        "instruction": "Add one regression test named test_heartbeat_requires_current_owner. Acquire a CoordinatorLease as coord-a, release it, then create coord-b and acquire it. Assert that calling heartbeat on the released coord-a raises CoordinatorLeaseError. Keep all existing tests unchanged.",
        "test": "pytest -q tests/ops/test_coordinator_lease.py",
    },
)


def run(*args: str, timeout: int = 120, check: bool = False, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run([*args], cwd=ROOT, text=True, input=input_text, capture_output=True, timeout=timeout, check=check)


def git(*args: str) -> str:
    result = run("/usr/bin/git", *args)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def verify_repo() -> None:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong engineering branch")
    if git("status", "--porcelain"):
        raise RuntimeError("worktree must be clean before autonomous cycle")
    if run("/usr/bin/git", "merge-base", "--is-ancestor", R4, "HEAD").returncode != 0:
        raise RuntimeError("immutable R4 ancestry invariant failed")


def clean_model_diff(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    marker = text.find("diff --git ")
    if marker < 0:
        raise PatchAdmissionError("local model did not return a unified git diff")
    return text[marker:] + "\n"


def generate_patch(task: dict) -> str:
    target = (ROOT / task["path"]).read_text(encoding="utf-8")
    prompt = f"""MediaHub Astra bounded coding task. Return ONLY a complete unified git diff for one file.\n\nTask: {task['instruction']}\n\nTarget file path: {task['path']}\nCurrent file contents:\n---\n{target}\n---\nConstraints: modify only this file; do not delete existing tests; do not add dependencies; produce a patch that applies cleanly to the exact current file.\n"""
    rc, content, status = _generate_endpoint(os.environ["MEDIAHUB_AI_URL"], prompt, os.environ["MEDIAHUB_LOCAL_MODEL_NAME"])
    if rc != 0:
        raise RuntimeError(f"local AI generation failed: {status}")
    return clean_model_diff(content)


def record_failure(repo: SQLiteControlPlaneRepository, service: ControlPlaneService, task_id: str, generation: int, reason: str) -> None:
    task = repo.get_task(task_id)
    if task and task.status is TaskStatus.RUNNING:
        try:
            service.fail(task_id, AGENT, generation, reason)
        except Exception:
            pass


def execute_task(repo: SQLiteControlPlaneRepository, service: ControlPlaneService, task: dict, epoch: int) -> dict:
    task_id = task["id"]
    existing = repo.get_task(task_id)
    if existing is None:
        repo.create_task(Task(task_id, "bounded_code_change", payload={"path": task["path"], "instruction": task["instruction"]}, priority=100, status=TaskStatus.READY, idempotency_key=task_id, max_attempts=3, required_capabilities=("code_generation",)))
    elif existing.status is TaskStatus.SUCCEEDED:
        return {"task_id": task_id, "status": "ALREADY_SUCCEEDED"}
    lease = service.claim(task_id, AGENT, epoch)
    generation = lease.generation
    base = git("rev-parse", "HEAD")
    patch = generate_patch(task)
    proposal = StructuredPatch.from_json(json.dumps({"files": [{"path": task["path"], "operation": "modify", "patch": patch}]}))
    try:
        admission = admit_patch(proposal, ROOT, allowed_paths=("tests/ops/**",), forbidden_paths=(".github/**", "credentials/**", ".autonomous/**"), max_patch_bytes=32_000)
    except Exception as exc:
        record_failure(repo, service, task_id, generation, f"PATCH_ADMISSION_FAILED:{exc}")
        raise
    test = run("/usr/bin/python3", "-m", "pytest", "-q", task["path"], timeout=180)
    if test.returncode:
        run("/usr/bin/git", "restore", "--staged", "--worktree", "--", *admission.changed_files)
        record_failure(repo, service, task_id, generation, f"VERIFY_FAILED:{test.stdout[-4000:]}{test.stderr[-2000:]}")
        raise RuntimeError(f"verification failed for {task_id}")
    diff_check = run("/usr/bin/git", "diff", "--check")
    if diff_check.returncode:
        run("/usr/bin/git", "restore", "--staged", "--worktree", "--", *admission.changed_files)
        record_failure(repo, service, task_id, generation, "DIFF_CHECK_FAILED")
        raise RuntimeError("git diff --check failed")
    run("/usr/bin/git", "add", "--", *admission.changed_files, check=True)
    staged = git("diff", "--cached", "--name-only").splitlines()
    if tuple(staged) != admission.changed_files:
        run("/usr/bin/git", "reset", "--", *admission.changed_files)
        run("/usr/bin/git", "restore", "--staged", "--worktree", "--", *admission.changed_files)
        record_failure(repo, service, task_id, generation, "STAGED_FILE_MANIFEST_MISMATCH")
        raise RuntimeError("staged file manifest mismatch")
    message = f"autonomy({task_id}): bounded verified change [generation={generation} epoch={epoch}]"
    commit = run("/usr/bin/git", "commit", "-m", message, check=True)
    commit_sha = git("rev-parse", "HEAD")
    if commit_sha == base or run("/usr/bin/git", "merge-base", "--is-ancestor", base, commit_sha).returncode != 0:
        raise RuntimeError("commit provenance/ancestry check failed")
    push = run("/usr/bin/git", "push", "--ff-only", "origin", f"{BRANCH}:{BRANCH}", timeout=180)
    if push.returncode:
        raise RuntimeError(push.stderr.strip() or "fast-forward push failed")
    remote = run("/usr/bin/git", "ls-remote", "origin", f"refs/heads/{BRANCH}", timeout=30)
    remote_sha = remote.stdout.split()[0] if remote.returncode == 0 and remote.stdout.split() else ""
    if remote_sha != commit_sha:
        raise RuntimeError(f"post-push reconciliation failed: local={commit_sha} remote={remote_sha}")
    result = {
        "task_id": task_id,
        "execution_id": f"{task_id}:{lease.lease_id}",
        "generation": generation,
        "coordinator_epoch": epoch,
        "worker": AGENT,
        "model": os.environ.get("MEDIAHUB_LOCAL_MODEL_NAME", "qwen2.5-coder:3b"),
        "patch": {"files": list(admission.changed_files), "bytes": admission.patch_bytes},
        "tests": {"command": task["test"], "returncode": test.returncode},
        "commit_sha": commit_sha,
        "push_sha": remote_sha,
        "base_sha": base,
        "timestamp": time.time(),
    }
    service.complete(task_id, AGENT, generation, result=result, lease_id=lease.lease_id)
    return result


def main() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    verify_repo()
    coordinator = CoordinatorLease(DB, LOCK, branch=BRANCH)
    coordinator.acquire(f"astra-{os.getpid()}", now=time.time())
    try:
        repo = SQLiteControlPlaneRepository(DB)
        service = ControlPlaneService(repo)
        coordinator.heartbeat(now=time.time())
        results = []
        for task in TASKS:
            coordinator.heartbeat(now=time.time())
            result = execute_task(repo, service, task, coordinator.record.epoch)
            results.append(result)
            if result.get("status") == "ALREADY_SUCCEEDED":
                continue
        checkpoint = {
            "kind": "FIRST_AUTONOMOUS_CYCLE_PROOF",
            "branch": BRANCH,
            "coordinator_epoch": coordinator.record.epoch,
            "tasks": results,
            "next_task_generation": True,
        }
        (STATE / "first-cycle-proof.json").write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return 0
    finally:
        coordinator.release(now=time.time())


if __name__ == "__main__":
    raise SystemExit(main())
