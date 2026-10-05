"""Bounded autonomous development queue for the Astra reference runtime.

Promotion-safe: workers create task branches and evidence, but never merge to main.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import re
import subprocess
import time
from pathlib import Path

from .agent_fabric import AgentClaim, ClaimStore

ROOT = Path(__file__).resolve().parents[2]
TASK_DIR = ROOT / "ops" / "agent-fabric" / "tasks"
STATE = Path(os.environ.get("ASTRA_QUEUE_STATE_DIR", "/var/lib/mediahub-astra/queue"))
CLAIMS = STATE / "claims"


def bounded_worker_count(requested: int) -> int:
    return max(1, min(int(requested), 3))


MAX_WORKERS = bounded_worker_count(int(os.environ.get("ASTRA_QUEUE_MAX_WORKERS", "3")))
CODEX = os.environ.get("ASTRA_CODEX_BIN", "/usr/local/bin/codex")
TASK_TIMEOUT = max(60, int(os.environ.get("ASTRA_QUEUE_TASK_TIMEOUT", "1800")))


def run(
    argv: list[str], timeout: int = 300, cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv, cwd=cwd or ROOT, text=True, capture_output=True, timeout=timeout, check=False
    )


def safe_task_id(task_id: str) -> str:
    value = str(task_id)
    if not value or not re.fullmatch(r"[A-Za-z0-9._-]+", value):
        raise ValueError("invalid_task_id")
    return value


def worktree_path(task_id: str) -> Path:
    return STATE / "worktrees" / safe_task_id(task_id)


def load_tasks() -> list[dict]:
    tasks = []
    for path in sorted(TASK_DIR.glob("*.json")):
        try:
            task = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if task.get("status") == "READY":
            task["_path"] = str(path)
            tasks.append(task)
    return sorted(tasks, key=lambda x: (x.get("priority", "Z"), x.get("task_id", "")))


def completed(task_id: str, base_sha: str | None = None) -> bool:
    path = STATE / "completed" / f"{safe_task_id(task_id)}.json"
    if not path.is_file():
        return False
    if base_sha is None:
        return True
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    return payload.get("status") == "VERIFIED" and payload.get("base_sha") == base_sha


def dependencies_satisfied(task: dict, base_sha: str | None = None) -> bool:
    return all(completed(str(dep), base_sha) for dep in task.get("dependencies", ()))


def evidence(task_id: str, payload: dict) -> None:
    target = STATE / "evidence"
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{safe_task_id(task_id)}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def claim_for(task: dict) -> AgentClaim:
    now = time.time()
    return AgentClaim(
        agent="A2-BUILDER",
        task_id=str(task["task_id"]),
        goal=str(task.get("mission", task["task_id"])),
        paths=tuple(task.get("boundary", [])),
        exclusive_actions=("implement", "commit"),
        dependencies=tuple(task.get("dependencies", [])),
        status="ACTIVE",
        started=now,
        updated=now,
        expiry=now + 900,
        base_sha=run(["git", "rev-parse", "HEAD"], 30).stdout.strip(),
    )


def builder_prompt(task: dict) -> str:
    forbidden = task.get("forbidden_surfaces", task.get("forbidden", []))
    return f"""You are A2 Builder in MediaHub Agent Fabric.
Task ID: {task["task_id"]}
Mission: {task.get("mission", "")}
Boundary: {json.dumps(task.get("boundary", []))}
Forbidden surfaces: {json.dumps(forbidden)}
Acceptance: {json.dumps(task.get("acceptance", []))}
Implement only this task. Do not touch forbidden surfaces, production infrastructure,
user data, credentials, or unrelated files. Work on the current task branch.
Run relevant tests. Do not merge to main. Report changes and verification."""


def verifier_prompt(task: dict) -> str:
    forbidden = task.get("forbidden_surfaces", task.get("forbidden", []))
    return f"""You are A3 Verifier, independent from the builder.
Review task {task["task_id"]} against acceptance criteria:
{json.dumps(task.get("acceptance", []))}
Boundary: {json.dumps(task.get("boundary", []))}
Forbidden surfaces: {json.dumps(forbidden)}
Inspect the actual git diff and run appropriate tests. Do not modify source files.
Return exactly one verdict line: ASTRA_VERDICT: PASS or ASTRA_VERDICT: BLOCKED.
Use ASTRA_VERDICT: PASS only if acceptance is directly evidenced; otherwise return BLOCKED."""


def _path_in_scope(path: str, boundary: tuple[str, ...]) -> bool:
    normalized = path.lstrip("./")
    return any(
        normalized == root or normalized.startswith(root.rstrip("/") + "/")
        for root in boundary
    )


def _diff_outside_scope(task: dict, worktree: Path, base_sha: str) -> list[str]:
    result = run(["git", "diff", "--name-only", base_sha, "HEAD"], 60, worktree)
    if result.returncode != 0:
        raise RuntimeError("diff_listing_failed")
    boundary = tuple(str(item) for item in task.get("boundary", []))
    forbidden = tuple(str(item) for item in task.get("forbidden_surfaces", task.get("forbidden", [])))
    bad: list[str] = []
    for path in (line.strip() for line in result.stdout.splitlines()):
        if not path:
            continue
        if forbidden and any(
            path == root or path.startswith(root.rstrip("/") + "/") for root in forbidden
        ):
            bad.append(path)
        elif boundary and not _path_in_scope(path, boundary):
            bad.append(path)
    status = run(["git", "status", "--porcelain", "--untracked-files=all"], 60, worktree)
    if status.returncode != 0:
        raise RuntimeError("status_listing_failed")
    for line in status.stdout.splitlines():
        if not line:
            continue
        path = line[3:].strip() if len(line) >= 3 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path and (forbidden and any(path == root or path.startswith(root.rstrip("/") + "/") for root in forbidden)
                      or (boundary and not _path_in_scope(path, boundary))):
            bad.append(path)
    return sorted(set(bad))


def _verifier_passed(stdout: str) -> bool:
    verdicts = re.findall(r"(?m)^ASTRA_VERDICT:\s*(PASS|BLOCKED)\s*$", stdout)
    return verdicts == ["PASS"]


def prepare_worktree(worktree: Path) -> None:
    if not worktree.exists():
        return
    status = run(["git", "status", "--porcelain", "--untracked-files=all"], 60, worktree)
    if status.returncode != 0:
        raise RuntimeError("stale_worktree_status_failed")
    if status.stdout.strip():
        raise RuntimeError("stale_worktree_dirty")
    cleanup = run(["git", "worktree", "remove", "--force", str(worktree)], 120)
    if cleanup.returncode:
        raise RuntimeError("worktree_cleanup_failed")


def process_task(task: dict) -> dict:
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "completed").mkdir(parents=True, exist_ok=True)
    store = ClaimStore(CLAIMS)
    claim = claim_for(task)
    started = time.time()
    task_key = safe_task_id(str(task["task_id"]))
    branch = f"astra/auto/{task_key}-{claim.base_sha[:12]}-{int(started)}"
    worktree = worktree_path(str(task["task_id"]))
    record = {
        "task_id": task["task_id"],
        "started_at": int(started),
        "base_sha": claim.base_sha,
        "branch": branch,
        "status": "BLOCKED",
    }
    try:
        store.acquire(claim)
        worktree.parent.mkdir(parents=True, exist_ok=True)
        prepare_worktree(worktree)
        fetch_main = run(["git", "fetch", "--prune", "origin", "main"], 120)
        if fetch_main.returncode != 0:
            raise RuntimeError("queue_main_fetch_failed")
        remote_main = run(["git", "rev-parse", "origin/main"], 30)
        if remote_main.returncode != 0 or remote_main.stdout.strip() != claim.base_sha:
            raise RuntimeError("queue_base_sha_drift")
        existing_branch = run(["git", "ls-remote", "--exit-code", "--heads", "origin", f"refs/heads/{branch}"], 60)
        if existing_branch.returncode == 0:
            raise RuntimeError("queue_branch_already_exists")
        if existing_branch.returncode != 2:
            raise RuntimeError("queue_branch_probe_failed")
        checkout = run(["git", "worktree", "add", "-b", branch, str(worktree), claim.base_sha], 120)
        if checkout.returncode:
            raise RuntimeError("worktree_create_failed")
        build = run(
            [CODEX, "exec", "--full-auto", "--skip-git-repo-check", builder_prompt(task)],
            TASK_TIMEOUT,
            worktree,
        )
        record["builder"] = {
            "returncode": build.returncode,
            "stdout": build.stdout[-12000:],
            "stderr": build.stderr[-8000:],
        }
        if build.returncode != 0:
            raise RuntimeError("builder_failed")
        outside_scope = _diff_outside_scope(task, worktree, claim.base_sha)
        record["scope"] = {
            "status": "PASS" if not outside_scope else "BLOCKED",
            "outside_scope": outside_scope,
        }
        if outside_scope:
            raise RuntimeError("task_boundary_violation")
        test = run(
            ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            900,
            worktree,
        )
        record["tests"] = {
            "returncode": test.returncode,
            "stdout": test.stdout[-8000:],
            "stderr": test.stderr[-6000:],
        }
        if test.returncode != 0:
            raise RuntimeError("tests_failed")
        diff = run(["git", "diff", "--check"], 60, worktree)
        if diff.returncode:
            raise RuntimeError("diff_check_failed")
        verifier = run(
            [CODEX, "exec", "--sandbox", "read-only", "--skip-git-repo-check", verifier_prompt(task)],
            TASK_TIMEOUT,
            worktree,
        )
        record["verifier"] = {
            "returncode": verifier.returncode,
            "stdout": verifier.stdout[-12000:],
            "stderr": verifier.stderr[-8000:],
        }
        if verifier.returncode != 0 or not _verifier_passed(verifier.stdout):
            raise RuntimeError("verifier_failed")
        status = run(["git", "status", "--porcelain"], 60, worktree)
        if not status.stdout.strip():
            raise RuntimeError("no_changes")
        if run(["git", "add", "-A"], 60, worktree).returncode:
            raise RuntimeError("git_add_failed")
        commit = run(
            ["git", "commit", "-m", f"astra: complete {task['task_id']}"], 120, worktree
        )
        if commit.returncode:
            raise RuntimeError("git_commit_failed")
        push = run(
            ["git", "push", "origin", f"HEAD:refs/heads/{branch}"], 180, worktree
        )
        record["push"] = {
            "returncode": push.returncode,
            "stdout": push.stdout[-4000:],
            "stderr": push.stderr[-4000:],
        }
        if push.returncode:
            raise RuntimeError("git_push_failed")
        record["head_sha"] = run(["git", "rev-parse", "HEAD"], 30, worktree).stdout.strip()
        remote_head = run(
            ["git", "ls-remote", "origin", f"refs/heads/{branch}"], 60, worktree
        )
        if remote_head.returncode != 0:
            raise RuntimeError("git_push_verification_failed")
        remote_sha = remote_head.stdout.split()[0] if remote_head.stdout.split() else ""
        if remote_sha != record["head_sha"]:
            raise RuntimeError("git_push_sha_mismatch")
        record["push_verification"] = {
            "status": "PASS",
            "remote_sha": remote_sha,
            "branch": branch,
        }
        record["status"] = "VERIFIED"
        (STATE / "completed" / f"{task_key}.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    except Exception as exc:
        record["error"] = type(exc).__name__ + ":" + str(exc)
    finally:
        try:
            store.release(
                claim.task_id, "VERIFIED" if record["status"] == "VERIFIED" else "REJECTED"
            )
        except Exception as exc:
            record["claim_release_error"] = repr(exc)
        try:
            if worktree.exists():
                run(["git", "worktree", "remove", "--force", str(worktree)], 120)
        except Exception:
            record["worktree_cleanup_error"] = True
        record["elapsed_seconds"] = round(time.time() - started, 3)
        evidence(task["task_id"], record)
    return record


def main() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    base_sha = run(["git", "rev-parse", "HEAD"], 30).stdout.strip()
    if not base_sha:
        print(json.dumps({"status": "BLOCKED", "reason": "queue_base_sha_unavailable"}, sort_keys=True))
        return 2
    tasks = [
        t
        for t in load_tasks()
        if not completed(str(t["task_id"]), base_sha) and dependencies_satisfied(t, base_sha)
    ]
    if not tasks:
        print(json.dumps({"status": "IDLE", "reason": "no_ready_tasks"}, sort_keys=True))
        return 0
    selected = tasks[:MAX_WORKERS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected)) as pool:
        results = list(pool.map(process_task, selected))
    all_verified = all(r["status"] == "VERIFIED" for r in results)
    print(
        json.dumps(
            {
                "status": "PASS" if all_verified else "BLOCKED",
                "workers": len(selected),
                "selected_tasks": [str(t["task_id"]) for t in selected],
                "results": results,
            },
            sort_keys=True,
        )
    )
    return 0 if all_verified else 2


if __name__ == "__main__":
    raise SystemExit(main())
