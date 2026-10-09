"""Bounded autonomous development queue for the Astra reference runtime.

Promotion-safe: workers create task branches and evidence, but never merge to main.
"""
from __future__ import annotations

import concurrent.futures
import json
import os
import re
import subprocess
import tempfile
import time
from pathlib import Path

from .agent_fabric import AgentClaim, ClaimStore

ROOT = Path(__file__).resolve().parents[2]
TASK_DIR = ROOT / "ops" / "agent-fabric" / "tasks"
STATE = Path(os.environ.get("ASTRA_QUEUE_STATE_DIR", "/var/lib/mediahub-astra/queue"))
CLAIMS = STATE / "claims"

# Three permanent executor lanes; Astra Gold permits up to three active claims.
PERMANENT_EXECUTOR_POOL = {
    "mh-dev-01": "claude",
    "mh-dev-02": "claude",
    "Voktors-Mac-mini.local": "claude",
}


def worker_artifact_name(run_id: int | str, node_id: str) -> str:
    """Return the exact artifact name emitted by the worker workflow for a node."""
    run = str(run_id)
    if not run.isdigit():
        raise ValueError("invalid_worker_run_id")
    if node_id in {"mh-dev-01", "mh-dev-02"}:
        return f"astra-distributed-worker-{node_id}-claude-{run}"
    if node_id in {"Voktors-Mac-mini.local", "Voktors-Mini.Dlink"}:
        return f"astra-distributed-worker-{run}"
    raise ValueError("unsupported_worker_node")


def bounded_worker_count(requested: int) -> int:
    return max(1, min(int(requested), len(PERMANENT_EXECUTOR_POOL)))


MAX_WORKERS = bounded_worker_count(int(os.environ.get("ASTRA_QUEUE_MAX_WORKERS", "3")))

def run(
    argv: list[str], timeout: int = 300, cwd: Path | None = None, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
        env=env,
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


def select_distributed_tasks(tasks: list[dict], max_workers: int = MAX_WORKERS) -> list[dict]:
    """Select at most one active claim per permanent executor lane/node."""
    selected: list[dict] = []
    used_nodes: set[str] = set()
    for task in tasks:
        node_id = str(task.get("node_id", "")).strip()
        executor = str(task.get("executor", "")).strip()
        if node_id in used_nodes:
            continue
        if node_id not in PERMANENT_EXECUTOR_POOL or PERMANENT_EXECUTOR_POOL[node_id] != executor:
            continue
        selected.append(task)
        used_nodes.add(node_id)
        if len(selected) >= bounded_worker_count(max_workers):
            break
    return selected


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


def claim_for(task: dict, base_sha: str) -> AgentClaim:
    """Claim both the task's edit boundary and its single permanent executor lane.

    Lane sentinels are coordination paths, not repository files. Because ClaimStore
    atomically rejects overlapping active paths, separate queue processes cannot
    dispatch two different tasks to the same physical Claude executor at once.
    This enforces the global G-5 limit even when controller invocations overlap.
    """
    node_id = str(task.get("node_id", "")).strip()
    executor = str(task.get("executor", "")).strip()
    expected = PERMANENT_EXECUTOR_POOL.get(node_id)
    if expected is None or executor != expected:
        raise ValueError("invalid_executor_lane_binding")
    boundary = tuple(str(path) for path in task.get("boundary", []) if str(path).strip())
    lane_path = f"__astra_executor_lanes__/{node_id}"
    paths = tuple(dict.fromkeys((*boundary, lane_path)))
    now = time.time()
    return AgentClaim(
        agent="A2-BUILDER",
        task_id=str(task["task_id"]),
        goal=str(task.get("mission", task["task_id"])),
        paths=paths,
        exclusive_actions=("implement", "commit"),
        dependencies=tuple(task.get("dependencies", [])),
        status="ACTIVE",
        started=now,
        updated=now,
        expiry=now + max(60.0, min(float(os.environ.get("ASTRA_CLAIM_LEASE_SECONDS", "600")), 21600.0)),
        base_sha=base_sha,
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


def verifier_prompt(task: dict, diff_text: str, test_text: str) -> str:
    forbidden = task.get("forbidden_surfaces", task.get("forbidden", []))
    return f"""You are A3 Verifier, independent from the builder.
Review task {task["task_id"]} against acceptance criteria:
{json.dumps(task.get("acceptance", []))}
Boundary: {json.dumps(task.get("boundary", []))}
Forbidden surfaces: {json.dumps(forbidden)}
The following evidence was collected by the controller:
--- GIT DIFF ---
{diff_text[-30000:]}
--- TEST OUTPUT ---
{test_text[-12000:]}
Do not call tools, do not modify files, and do not emit JSON or tool-call syntax.
Return exactly one line: ASTRA_VERDICT: PASS or ASTRA_VERDICT: BLOCKED.
Use PASS only when the supplied diff and tests directly evidence every acceptance criterion."""


def _path_in_scope(path: str, boundary: tuple[str, ...]) -> bool:
    normalized = path.lstrip("./")
    return any(
        normalized == root or normalized.startswith(root.rstrip("/") + "/")
        for root in boundary
    )


def _diff_outside_scope(task: dict, worktree: Path, base_sha: str) -> list[str]:
    # Inspect both committed and uncommitted tracked changes. A builder must not
    # hide a forbidden edit merely by leaving it unstaged.
    diff_specs = [
        ["git", "diff", "--name-only", base_sha],
        ["git", "diff", "--name-only", base_sha, "HEAD"],
        ["git", "diff", "--cached", "--name-only", base_sha],
    ]
    changed: set[str] = set()
    for argv in diff_specs:
        result = run(argv, 60, worktree)
        if result.returncode != 0:
            raise RuntimeError("diff_listing_failed")
        changed.update(line.strip() for line in result.stdout.splitlines() if line.strip())

    boundary = tuple(str(item) for item in task.get("boundary", []))
    forbidden = tuple(str(item) for item in task.get("forbidden_surfaces", task.get("forbidden", [])))
    bad: list[str] = []
    for path in sorted(changed):
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
        if path and (
            (forbidden and any(path == root or path.startswith(root.rstrip("/") + "/") for root in forbidden))
            or (boundary and not _path_in_scope(path, boundary))
        ):
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


def github_auth_env() -> dict[str, str] | None:
    """Use the node's authenticated gh CLI session when no token env is exported."""
    env = os.environ.copy()
    if env.get("GH_TOKEN") or env.get("GITHUB_TOKEN"):
        if env.get("GITHUB_TOKEN") and not env.get("GH_TOKEN"):
            env["GH_TOKEN"] = env["GITHUB_TOKEN"]
        return env
    try:
        token = subprocess.run(
            ["gh", "auth", "token"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            stdin=subprocess.DEVNULL,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    value = token.stdout.strip()
    if token.returncode != 0 or not value:
        return None
    env["GH_TOKEN"] = value
    return env


def process_task_remote(task: dict, expected_base_sha: str) -> dict:
    """Dispatch one queue task to its explicitly assigned local-executor node via GitHub."""
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "completed").mkdir(parents=True, exist_ok=True)
    store = ClaimStore(CLAIMS)
    claim = claim_for(task, expected_base_sha)
    started = time.time()
    task_key = safe_task_id(str(task["task_id"]))
    node_id = str(task.get("node_id", "")).strip()
    executor = str(task.get("executor", "")).strip()
    verifier = str(task.get("verifier", "")).strip()
    if node_id not in PERMANENT_EXECUTOR_POOL:
        return {"task_id": task_key, "status": "BLOCKED", "error": "unsupported_remote_node"}
    if executor != PERMANENT_EXECUTOR_POOL[node_id]:
        return {
            "task_id": task_key,
            "status": "BLOCKED",
            "error": "permanent_executor_binding_mismatch",
            "expected_executor": PERMANENT_EXECUTOR_POOL[node_id],
            "executor": executor,
        }
    if executor != "claude" or verifier != "claude":
        return {
            "task_id": task_key,
            "status": "BLOCKED",
            "error": "permanent_pool_requires_claude",
            "executor": executor,
            "verifier": verifier,
        }
    if executor == verifier and not bool(task.get("independent_verifier_process", False)):
        return {"task_id": task_key, "status": "BLOCKED", "error": "verifier_must_be_independent_process"}
    gh_env = github_auth_env()
    if gh_env is None:
        return {"task_id": task_key, "status": "BLOCKED", "error": "remote_transport_auth_missing"}
    record = {
        "task_id": task_key,
        "started_at": int(started),
        "base_sha": expected_base_sha,
        "node_id": node_id,
        "executor": executor,
        "verifier": verifier,
        "status": "BLOCKED",
    }
    task_payload = dict(task)
    task_payload["node_id"] = node_id
    task_payload["executor"] = executor
    task_payload["verifier"] = verifier
    try:
        store.acquire(claim)
        task_json = json.dumps(task_payload, sort_keys=True, separators=(",", ":"))
        dispatch = run([
            "gh", "workflow", "run", ".github/workflows/astra-distributed-local-worker.yml",
            "--ref", "main",
            "-f", f"command_id={os.environ.get('ASTRA_COMMAND_ID', '')}",
            "-f", f"target_sha={expected_base_sha}",
            "-f", f"task_id={task_key}",
            "-f", f"node_id={node_id}",
            "-f", f"executor={executor}",
            "-f", f"task_json={task_json}",
        ], 60, env=gh_env)
        if dispatch.returncode != 0:
            record["error"] = "remote_dispatch_failed:" + (dispatch.stderr or dispatch.stdout)[-2000:]
            return record

        run_id = None
        deadline = time.time() + max(300, int(os.environ.get("ASTRA_REMOTE_WORKER_WAIT_SECONDS", "2400")))
        run_title_bits = [os.environ.get("ASTRA_COMMAND_ID", ""), task_key, node_id, executor]
        while time.time() < deadline:
            listed = run([
                "gh", "run", "list", "--workflow", "astra-distributed-local-worker.yml",
                "--limit", "30", "--json", "databaseId,displayTitle,status,conclusion,createdAt"
            ], 30, env=gh_env)
            if listed.returncode == 0:
                try:
                    rows = json.loads(listed.stdout or "[]")
                except Exception:
                    rows = []
                matches = [
                    row for row in rows
                    if all(bit in str(row.get("displayTitle", "")) for bit in run_title_bits)
                ]
                if matches:
                    matches.sort(key=lambda row: row.get("createdAt", ""), reverse=True)
                    run_id = int(matches[0]["databaseId"])
                    break
            time.sleep(5)
        if not run_id:
            raise RuntimeError("remote_run_not_found")

        record["worker_run_id"] = run_id
        while time.time() < deadline:
            view = run(["gh", "run", "view", str(run_id), "--json", "status,conclusion"], 30, env=gh_env)
            if view.returncode == 0:
                data = json.loads(view.stdout or "{}")
                status = data.get("status")
                if status == "completed":
                    record["worker_run_status"] = status
                    record["worker_conclusion"] = data.get("conclusion")
                    break
            if time.time() - started > 60:
                try:
                    store.heartbeat(task_key, lease_seconds=max(60, min(int(os.environ.get("ASTRA_CLAIM_LEASE_SECONDS", "600")), 21600)))
                except Exception:
                    pass
            time.sleep(10)
        if record.get("worker_run_status") != "completed":
            raise RuntimeError("remote_worker_timeout")

        temp = tempfile.TemporaryDirectory(prefix="astra-remote-worker-")
        download = run([
            "gh", "run", "download", str(run_id), "-n", worker_artifact_name(run_id, node_id), "-D", temp.name
        ], 120, env=gh_env)
        if download.returncode != 0:
            raise RuntimeError("remote_evidence_download_failed")
        result_file = Path(temp.name) / "astra-distributed-worker-result.json"
        if not result_file.is_file():
            candidates = list(Path(temp.name).rglob("astra-distributed-worker-result.json"))
            if candidates:
                result_file = candidates[0]
        if not result_file.is_file():
            raise RuntimeError("remote_evidence_missing")
        remote = json.loads(result_file.read_text(encoding="utf-8"))
        required = {
            "schema": "mediahub.astra.distributed-local-worker.v1",
            "status": "PASS",
            "command_id": os.environ.get("ASTRA_COMMAND_ID", ""),
            "target_sha": expected_base_sha,
            "node_id": node_id,
            "task_id": task_key,
            "executor_identity": executor,
            "verifier_identity": verifier,
        }
        for key, value in required.items():
            if remote.get(key) != value:
                raise RuntimeError(f"remote_evidence_{key}_mismatch")
        branch = str(remote.get("branch", ""))
        head_sha = str(remote.get("head_sha", ""))
        remote_sha = str(remote.get("remote_head", ""))
        if not re.fullmatch(r"[0-9a-f]{40}", head_sha):
            raise RuntimeError("remote_head_sha_invalid")
        push_status = remote.get("push_verification", {}).get("status")
        if push_status == "NOT_REQUIRED" and bool(task.get("allow_no_changes", False)):
            if head_sha != expected_base_sha:
                raise RuntimeError("remote_nochange_sha_mismatch")
        else:
            if push_status != "PASS":
                raise RuntimeError("remote_push_verification_not_PASS")
            if remote_sha != head_sha:
                raise RuntimeError("remote_push_sha_mismatch")
            branch_probe = run(["git", "ls-remote", "origin", f"refs/heads/{branch}"], 60)
            actual_remote = branch_probe.stdout.split()[0] if branch_probe.returncode == 0 and branch_probe.stdout.split() else ""
            if actual_remote != head_sha:
                raise RuntimeError("controller_remote_branch_sha_mismatch")
        record.update(remote)
        if record.get("error"):
            raise RuntimeError("remote_evidence_error_present")
        if record.get("claim_release_error"):
            raise RuntimeError("remote_evidence_claim_release_error")
        record["status"] = "VERIFIED"
        record["elapsed_seconds"] = round(time.time() - started, 3)
        (STATE / "completed" / f"{task_key}.json").write_text(
            json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return record
    except Exception as exc:
        record["status"] = "BLOCKED"
        record["error"] = type(exc).__name__ + ":" + str(exc)
        return record
    finally:
        try:
            store.release(task_key, "VERIFIED" if record["status"] == "VERIFIED" else "REJECTED")
        except Exception as exc:
            record["claim_release_error"] = repr(exc)
            record["status"] = "BLOCKED"
            record["error"] = "ClaimReleaseError:" + repr(exc)

def process_task(task: dict, expected_base_sha: str) -> dict:
    raise RuntimeError("legacy_local_executor_disabled")


def main() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    head_sha = run(["git", "rev-parse", "HEAD"], 30).stdout.strip()
    target_sha = str(os.environ.get("ASTRA_TARGET_SHA", "")).strip()
    if target_sha:
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", target_sha):
            print(json.dumps({"status": "BLOCKED", "reason": "queue_target_sha_invalid"}, sort_keys=True))
            return 2
        if head_sha.lower() != target_sha.lower():
            print(json.dumps({
                "status": "BLOCKED",
                "reason": "queue_target_sha_not_current_head",
                "head_sha": head_sha,
                "target_sha": target_sha,
            }, sort_keys=True))
            return 2
        base_sha = target_sha
    else:
        base_sha = head_sha
    if not base_sha:
        print(json.dumps({"status": "BLOCKED", "reason": "queue_base_sha_unavailable"}, sort_keys=True))
        return 2
    discovered = load_tasks()
    inventory = []
    for task in discovered:
        task_id = str(task["task_id"])
        done = completed(task_id, base_sha)
        deps_ok = dependencies_satisfied(task, base_sha)
        inventory.append({
            "task_id": task_id,
            "priority": task.get("priority"),
            "status": task.get("status"),
            "completed_for_target": done,
            "dependencies_satisfied": deps_ok,
        })
    tasks = [
        t for t in discovered
        if not completed(str(t["task_id"]), base_sha) and dependencies_satisfied(t, base_sha)
    ]
    if not tasks:
        print(json.dumps({
            "status": "IDLE",
            "reason": "no_ready_tasks",
            "base_sha": base_sha,
            "discovered_tasks": inventory,
        }, sort_keys=True))
        return 0
    selected = select_distributed_tasks(tasks, MAX_WORKERS)
    if not selected:
        print(json.dumps({
            "status": "BLOCKED",
            "reason": "no_eligible_distributed_tasks",
            "base_sha": base_sha,
            "discovered_tasks": inventory,
        }, sort_keys=True))
        return 2
    # Canonical Astra Gold execution is always distributed GitHub transport with
    # permanent Claude lanes. There is deliberately no local executor fallback.
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected)) as pool:
        results = list(pool.map(lambda task: process_task_remote(task, base_sha), selected))
    all_verified = all(r["status"] == "VERIFIED" for r in results)
    print(json.dumps({
        "status": "PASS" if all_verified else "BLOCKED",
        "workers": len(selected),
        "executor_pool": PERMANENT_EXECUTOR_POOL,
        "max_parallel_claims": MAX_WORKERS,
        "mode": "github_remote_claude_only",
        "selected_tasks": [str(t["task_id"]) for t in selected],
        "results": results,
    }, sort_keys=True))
    return 0 if all_verified else 2

if __name__ == "__main__":
    raise SystemExit(main())