"""Bounded autonomous development queue for the Astra reference runtime.

Promotion-safe: workers create task branches and evidence, but never merge to main.
"""
from __future__ import annotations

import concurrent.futures
import datetime
import hashlib
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


def active_controller_preflight() -> dict | None:
    """Block a new queue if another supervisor run is queued or active.

    Workflow-level concurrency groups are ref-scoped. A branch qualification can
    therefore overlap a main-branch run; this check gives the queue a repository-wide
    single-controller guard before it dispatches any child workers.
    """
    if os.environ.get("ASTRA_SINGLE_CONTROLLER_RUN") != "1":
        return None
    gh_env = github_auth_env()
    if gh_env is None:
        return {"status": "BLOCKED", "reason": "controller_concurrency_auth_missing"}
    try:
        listed = run([
            "gh", "run", "list", "--workflow", "astra-autonomous-supervisor.yml",
            "--limit", "100", "--json", "databaseId,status,conclusion,createdAt,headSha",
        ], 30, env=gh_env)
    except Exception as exc:
        return {"status": "BLOCKED", "reason": "controller_concurrency_query_failed",
                "error_type": type(exc).__name__}
    if listed.returncode != 0:
        return {"status": "BLOCKED", "reason": "controller_concurrency_query_failed"}
    try:
        rows = json.loads(listed.stdout or "[]")
    except (TypeError, json.JSONDecodeError):
        return {"status": "BLOCKED", "reason": "controller_concurrency_query_invalid"}
    if not isinstance(rows, list):
        return {"status": "BLOCKED", "reason": "controller_concurrency_query_invalid"}
    current_run_id = str(os.environ.get("GITHUB_RUN_ID", "")).strip()
    active_states = {"queued", "in_progress", "waiting", "requested", "pending"}
    blockers = []
    for row in rows:
        if not isinstance(row, dict) or str(row.get("databaseId", "")) == current_run_id:
            continue
        if str(row.get("status", "")).lower() not in active_states:
            continue
        try:
            blockers.append(int(row["databaseId"]))
        except (TypeError, ValueError, KeyError):
            return {"status": "BLOCKED", "reason": "controller_concurrency_identity_invalid"}
    if blockers:
        return {
            "status": "BLOCKED",
            "reason": "another_supervisor_run_active",
            "blocking_run_ids": sorted(set(blockers)),
        }
    return None


def wait_for_controller_slot() -> dict | None:
    """Wait on the hosted dispatcher until other supervisor runs become terminal.

    Only the specific concurrency blocker is retryable. Authentication/API/schema
    errors fail closed immediately; no worker may be dispatched on uncertain state.
    """
    if os.environ.get("ASTRA_SINGLE_CONTROLLER_RUN") != "1":
        return None
    try:
        max_wait = max(0, min(int(os.environ.get("ASTRA_CONTROLLER_CONCURRENCY_WAIT_SECONDS", "0")), 21600))
        poll_seconds = max(5, min(int(os.environ.get("ASTRA_CONTROLLER_CONCURRENCY_POLL_SECONDS", "30")), 300))
    except (TypeError, ValueError):
        return {"status": "BLOCKED", "reason": "controller_concurrency_config_invalid"}
    deadline = time.monotonic() + max_wait
    while True:
        result = active_controller_preflight()
        if result is None:
            return None
        if result.get("reason") != "another_supervisor_run_active":
            return result
        remaining = deadline - time.monotonic()
        if max_wait <= 0 or remaining <= 0:
            return {**result, "reason": "controller_concurrency_wait_timeout"}
        time.sleep(min(float(poll_seconds), remaining))


def queue_state_preflight() -> dict | None:
    """Fail closed before dispatch if durable state/claims cannot be persisted."""
    for component, path in (("state", STATE), ("claims", CLAIMS)):
        probe_name = None
        try:
            path.mkdir(parents=True, exist_ok=True)
            fd, probe_name = tempfile.mkstemp(prefix=".astra-queue-preflight-", dir=str(path))
            with os.fdopen(fd, "wb") as handle:
                handle.write(b"astra-queue-preflight-v1\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.unlink(probe_name)
            probe_name = None
        except OSError as exc:
            if probe_name:
                try:
                    os.unlink(probe_name)
                except OSError:
                    pass
            return {"component": component, "error_type": type(exc).__name__, "errno": exc.errno}
    return None


def persist_json_atomic(path: Path, payload: dict) -> None:
    """Atomically and durably persist controller evidence/state JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def worker_workflow_ref() -> str:
    """Select the workflow-definition ref for a controlled qualification run.

    By default this follows the ref that launched the queue controller, allowing
    a feature-branch qualification to test its own worker workflow. Production
    dispatches launched from main remain pinned to main.
    """
    explicit_ref = os.environ.get("ASTRA_WORKFLOW_REF")
    if explicit_ref is not None:
        value = explicit_ref.strip()
    else:
        value = str(os.environ.get("GITHUB_REF_NAME") or "main").strip()
    if (
        not value
        or len(value) > 255
        or value.startswith(("-", "/"))
        or value.endswith(("/", ".", ".lock"))
        or ".." in value
        or "\\" in value
        or re.fullmatch(r"[A-Za-z0-9._/-]+", value) is None
        or any(part in {"", ".", ".."} for part in value.split("/"))
    ):
        raise ValueError("invalid_worker_workflow_ref")
    return value


def worker_run_title(command_id: str, task_id: str, node_id: str, executor: str) -> str:
    """Build the exact workflow run title and reject missing or unsafe command IDs."""
    command = str(command_id).strip()
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,128}", command):
        raise ValueError("invalid_command_id")
    return f"Astra distributed worker / {command} / {safe_task_id(task_id)} / {node_id} / {executor}"


def matching_new_worker_runs(
    rows: list[dict], expected_title: str, previous_run_ids: set[int]
) -> list[dict]:
    """Match only exact run titles and exclude runs visible before this dispatch."""
    matches = []
    for row in rows:
        try:
            run_id = int(row["databaseId"])
        except (KeyError, TypeError, ValueError):
            continue
        if run_id in previous_run_ids:
            continue
        if str(row.get("displayTitle", "")) != expected_title:
            continue
        matches.append(row)
    return matches


def matching_runs_after_claim_start(
    rows: list[dict], expected_title: str, *, claim_started_at: float
) -> list[dict]:
    """Match exact-title worker runs created at/after the durable claim start.

    A title alone is not a dispatch nonce: retries may reuse a command identity.
    Missing or malformed creation timestamps fail closed and are never candidates.
    """
    matches = []
    for row in rows:
        if str(row.get("displayTitle", "")) != expected_title:
            continue
        created_at = row.get("createdAt")
        if not isinstance(created_at, str) or not created_at:
            continue
        try:
            parsed = datetime.datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                continue
            created_epoch = parsed.timestamp()
            run_id = int(row["databaseId"])
        except (ValueError, TypeError, KeyError, OverflowError):
            continue
        if created_epoch >= float(claim_started_at):
            matches.append({**row, "databaseId": run_id})
    return matches


def heartbeat_claim_if_due(store: ClaimStore, task_id: str, *, last_heartbeat: float, now: float | None = None, interval: float = 60.0) -> float:
    """Renew a remote task claim on every long-running dispatch/poll path."""
    current = time.time() if now is None else now
    if current - last_heartbeat < interval:
        return last_heartbeat
    lease_seconds = max(60, min(int(os.environ.get("ASTRA_CLAIM_LEASE_SECONDS", "600")), 21600))
    try:
        store.heartbeat(task_id, lease_seconds=lease_seconds)
    except Exception as exc:
        raise RuntimeError("claim_heartbeat_failed_remote_state_unconfirmed") from exc
    return current


def recover_quarantined_claim(task_id: str) -> dict:
    """Release a quarantined claim only after its exact GitHub run is confirmed terminal."""
    task_key = safe_task_id(task_id)
    store = ClaimStore(CLAIMS)
    try:
        claim = store.get_claim(task_key)
    except Exception as exc:
        return {"task_id": task_key, "status": "BLOCKED", "error": "claim_read_failed:" + type(exc).__name__}
    if claim.status != "QUARANTINED":
        return {"task_id": task_key, "status": "BLOCKED", "error": "claim_not_quarantined", "claim_status": claim.status}
    if not (claim.command_id and claim.node_id and claim.executor):
        return {"task_id": task_key, "status": "BLOCKED", "error": "quarantined_claim_missing_run_identity"}
    try:
        expected_title = worker_run_title(claim.command_id, task_key, claim.node_id, claim.executor)
    except ValueError:
        return {"task_id": task_key, "status": "BLOCKED", "error": "quarantined_claim_invalid_run_identity"}
    gh_env = github_auth_env()
    if gh_env is None:
        return {"task_id": task_key, "status": "BLOCKED", "error": "remote_transport_auth_missing"}
    try:
        # A dispatch can succeed while run discovery fails transiently. Recover the
        # exact run by its unique title, never by "latest" or by partial matching.
        if not claim.worker_run_id:
            listed = run([
                "gh", "run", "list", "--workflow", "astra-distributed-local-worker.yml",
                "--limit", "30", "--json", "databaseId,displayTitle,status,conclusion,createdAt",
            ], 30, env=gh_env)
            if listed.returncode != 0:
                return {"task_id": task_key, "status": "BLOCKED", "error": "remote_worker_discovery_unavailable"}
            rows = json.loads(listed.stdout or "[]")
            if not isinstance(rows, list):
                return {"task_id": task_key, "status": "BLOCKED", "error": "remote_worker_discovery_invalid"}
            matches = matching_runs_after_claim_start(
                rows, expected_title, claim_started_at=claim.started
            )
            if not matches:
                return {"task_id": task_key, "status": "BLOCKED", "error": "quarantined_claim_run_not_found"}
            if len(matches) != 1:
                return {"task_id": task_key, "status": "BLOCKED", "error": "quarantined_claim_run_ambiguous"}
            worker_run_id = str(int(matches[0]["databaseId"]))
            claim = store.set_worker_run_id_if_quarantined_matches(
                task_key, worker_run_id, expected_identity={
                    "command_id": claim.command_id,
                    "node_id": claim.node_id,
                    "executor": claim.executor,
                },
            )
        view = run(["gh", "run", "view", claim.worker_run_id, "--json", "status,conclusion,displayTitle"], 30, env=gh_env)
        if view.returncode != 0:
            return {"task_id": task_key, "status": "BLOCKED", "error": "remote_worker_status_unavailable"}
        data = json.loads(view.stdout or "{}")
        if data.get("displayTitle") != expected_title:
            return {"task_id": task_key, "status": "BLOCKED", "error": "remote_worker_identity_mismatch"}
        if data.get("status") != "completed":
            return {"task_id": task_key, "status": "BLOCKED", "error": "remote_worker_not_terminal", "worker_status": data.get("status"), "worker_run_id": claim.worker_run_id}
        store.release_quarantined_if_matches(
            task_key,
            expected_run_id=claim.worker_run_id,
            expected_identity={
                "command_id": claim.command_id,
                "node_id": claim.node_id,
                "executor": claim.executor,
            },
            status="REJECTED",
        )
        return {"task_id": task_key, "status": "RECOVERED", "worker_run_id": claim.worker_run_id, "worker_conclusion": data.get("conclusion")}
    except Exception as exc:
        return {"task_id": task_key, "status": "BLOCKED", "error": "recovery_failed:" + type(exc).__name__}


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


def select_distributed_tasks(
    tasks: list[dict],
    max_workers: int = MAX_WORKERS,
    *,
    excluded_nodes: set[str] | None = None,
) -> list[dict]:
    """Select one task per lane, excluding nodes occupied by the controller itself."""
    selected: list[dict] = []
    used_nodes: set[str] = set()
    excluded = set(excluded_nodes or ())
    for task in tasks:
        node_id = str(task.get("node_id", "")).strip()
        executor = str(task.get("executor", "")).strip()
        if node_id in excluded or node_id in used_nodes:
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
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    if payload.get("status") != "VERIFIED":
        return False
    return base_sha is None or payload.get("base_sha") == base_sha


def dependencies_satisfied(task: dict, base_sha: str | None = None) -> bool:
    return all(completed(str(dep), base_sha) for dep in task.get("dependencies", ()))


def evidence(task_id: str, payload: dict) -> None:
    target = STATE / "evidence"
    target.mkdir(parents=True, exist_ok=True)
    (target / f"{safe_task_id(task_id)}.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def claim_for(
    task: dict,
    base_sha: str,
    *,
    command_id: str = "",
    node_id: str = "",
    executor: str = "",
) -> AgentClaim:
    """Build a claim with the remote identity needed for safe quarantine recovery."""
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
        expiry=now + max(60.0, min(float(os.environ.get("ASTRA_CLAIM_LEASE_SECONDS", "600")), 21600.0)),
        base_sha=base_sha,
        command_id=command_id,
        node_id=node_id,
        executor=executor,
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


def worker_evidence_digest_matches(remote: object) -> bool:
    """Verify the worker artifact's canonical digest before trusting its claims."""
    if not isinstance(remote, dict):
        return False
    claimed = remote.get("evidence_digest")
    if not isinstance(claimed, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", claimed):
        return False
    unsigned = {key: value for key, value in remote.items() if key != "evidence_digest"}
    canonical = json.dumps(unsigned, sort_keys=True, separators=(",", ":"))
    expected = "sha256:" + hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return claimed == expected


def remote_verifier_result_passed(remote: object) -> bool:
    """Require the independent verifier process itself to return its sole PASS verdict."""
    if not isinstance(remote, dict):
        return False
    verifier = remote.get("verifier")
    if not isinstance(verifier, dict):
        return False
    if type(verifier.get("returncode")) is not int or verifier.get("returncode") != 0:
        return False
    stdout = verifier.get("stdout")
    return isinstance(stdout, str) and _verifier_passed(stdout)


def remote_worker_conclusion_passed(status: object, conclusion: object) -> bool:
    """A terminal job is not successful unless GitHub's workflow conclusion is success."""
    return status == "completed" and conclusion == "success"


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
    started = time.time()
    task_key = safe_task_id(str(task["task_id"]))
    node_id = str(task.get("node_id", "")).strip()
    executor = str(task.get("executor", "")).strip()
    verifier = str(task.get("verifier", "")).strip()
    command_id = str(os.environ.get("ASTRA_COMMAND_ID", "")).strip()
    try:
        expected_run_title = worker_run_title(command_id, task_key, node_id, executor)
    except ValueError as exc:
        return {
            "task_id": task_key,
            "command_id": command_id,
            "status": "BLOCKED",
            "error": str(exc),
        }
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
        return {"task_id": task_key, "command_id": command_id, "status": "BLOCKED", "error": "remote_transport_auth_missing"}
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "completed").mkdir(parents=True, exist_ok=True)
    store = ClaimStore(CLAIMS)
    claim = claim_for(
        task,
        expected_base_sha,
        command_id=command_id,
        node_id=node_id,
        executor=executor,
    )
    record = {
        "task_id": task_key,
        "command_id": command_id,
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
    acquired = False
    dispatch_attempted = False
    worker_terminal_confirmed = False
    run_id = None
    last_heartbeat = started
    try:
        store.acquire(claim)
        acquired = True
        baseline = run([
            "gh", "run", "list", "--workflow", "astra-distributed-local-worker.yml",
            "--limit", "30", "--json", "databaseId,displayTitle,status,conclusion,createdAt"
        ], 30, env=gh_env)
        if baseline.returncode != 0:
            raise RuntimeError("remote_run_baseline_failed")
        try:
            baseline_rows = json.loads(baseline.stdout or "[]")
        except json.JSONDecodeError as exc:
            raise RuntimeError("remote_run_baseline_invalid") from exc
        if not isinstance(baseline_rows, list):
            raise RuntimeError("remote_run_baseline_invalid")
        previous_run_ids = set()
        for row in baseline_rows:
            if str(row.get("displayTitle", "")) != expected_run_title:
                continue
            try:
                previous_run_ids.add(int(row["databaseId"]))
            except (KeyError, TypeError, ValueError):
                continue
        task_json = json.dumps(task_payload, sort_keys=True, separators=(",", ":"))
        workflow_ref = worker_workflow_ref()
        record["worker_workflow_ref"] = workflow_ref
        # From this point, a nonzero CLI result does not prove GitHub rejected
        # the dispatch; preserve the claim unless worker termination is confirmed.
        dispatch_attempted = True
        dispatch = run([
            "gh", "workflow", "run", ".github/workflows/astra-distributed-local-worker.yml",
            "--ref", workflow_ref,
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

        deadline = time.time() + max(300, int(os.environ.get("ASTRA_REMOTE_WORKER_WAIT_SECONDS", "4200")))
        while time.time() < deadline:
            last_heartbeat = heartbeat_claim_if_due(store, task_key, last_heartbeat=last_heartbeat)
            listed = run([
                "gh", "run", "list", "--workflow", "astra-distributed-local-worker.yml",
                "--limit", "30", "--json", "databaseId,displayTitle,status,conclusion,createdAt"
            ], 30, env=gh_env)
            if listed.returncode == 0:
                try:
                    rows = json.loads(listed.stdout or "[]")
                    if not isinstance(rows, list):
                        rows = []
                except Exception:
                    rows = []
                matches = matching_new_worker_runs(rows, expected_run_title, previous_run_ids)
                if len(matches) > 1:
                    raise RuntimeError("remote_run_ambiguous")
                if len(matches) == 1:
                    run_id = int(matches[0]["databaseId"])
                    store.set_worker_run_id(task_key, str(run_id))
                    break
            time.sleep(5)
        if not run_id:
            raise RuntimeError("remote_run_not_found")

        record["worker_run_id"] = run_id
        while time.time() < deadline:
            last_heartbeat = heartbeat_claim_if_due(store, task_key, last_heartbeat=last_heartbeat)
            view = run(["gh", "run", "view", str(run_id), "--json", "status,conclusion"], 30, env=gh_env)
            if view.returncode == 0:
                data = json.loads(view.stdout or "{}")
                status = data.get("status")
                if status == "completed":
                    record["worker_run_status"] = status
                    record["worker_conclusion"] = data.get("conclusion")
                    worker_terminal_confirmed = True
                    break
            time.sleep(10)
        if record.get("worker_run_status") != "completed":
            raise RuntimeError("remote_worker_timeout")
        if not remote_worker_conclusion_passed(
            record.get("worker_run_status"), record.get("worker_conclusion")
        ):
            raise RuntimeError("remote_worker_conclusion_not_success")

        temp = tempfile.TemporaryDirectory(prefix="astra-remote-worker-")
        download = run([
            "gh", "run", "download", str(run_id), "-n", f"astra-distributed-worker-{run_id}", "-D", temp.name
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
        if not worker_evidence_digest_matches(remote):
            raise RuntimeError("remote_evidence_digest_mismatch")
        if not remote_verifier_result_passed(remote):
            raise RuntimeError("remote_independent_verifier_not_PASS")
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
        record["independent_verifier"] = {"status": "PASS", "returncode": 0}
        if record.get("error"):
            raise RuntimeError("remote_evidence_error_present")
        if record.get("claim_release_error"):
            raise RuntimeError("remote_evidence_claim_release_error")
        record["status"] = "VERIFIED"
        record["elapsed_seconds"] = round(time.time() - started, 3)
    except Exception as exc:
        record["status"] = "BLOCKED"
        record["error"] = type(exc).__name__ + ":" + str(exc)
    finally:
        if acquired:
            # A dispatch attempt may have reached GitHub even when the CLI failed,
            # and a timed-out run may still execute. Cancel is only a request;
            # release is permitted only after gh confirms status=completed.
            if dispatch_attempted and not worker_terminal_confirmed:
                if run_id is not None:
                    try:
                        cancel = run(["gh", "run", "cancel", str(run_id)], 30, env=gh_env)
                        record["worker_cancel_requested"] = cancel.returncode == 0
                    except Exception as cancel_exc:
                        record["worker_cancel_error"] = type(cancel_exc).__name__ + ":" + str(cancel_exc)
                    for _ in range(3):
                        try:
                            view = run(["gh", "run", "view", str(run_id), "--json", "status,conclusion"], 30, env=gh_env)
                            if view.returncode == 0:
                                data = json.loads(view.stdout or "{}")
                                if data.get("status") == "completed":
                                    worker_terminal_confirmed = True
                                    record["worker_run_status"] = "completed"
                                    record["worker_conclusion"] = data.get("conclusion")
                                    record["worker_terminal_after_cancel_confirmed"] = True
                                    break
                        except Exception as status_exc:
                            record["worker_status_check_error"] = type(status_exc).__name__ + ":" + str(status_exc)
                        time.sleep(2)
                if not worker_terminal_confirmed:
                    try:
                        store.quarantine(task_key, "remote_worker_may_still_be_active")
                        record["claim_state"] = "QUARANTINED"
                        record["claim_quarantine_reason"] = "remote_worker_may_still_be_active"
                    except Exception as quarantine_exc:
                        record["claim_quarantine_error"] = repr(quarantine_exc)
                    record["status"] = "BLOCKED"
                    record["error"] = record.get("error", "remote_worker_state_unconfirmed_claim_quarantined")
            if not dispatch_attempted or worker_terminal_confirmed:
                # Persist a non-authoritative intent marker before releasing the claim.
                # A crash after release but before final promotion remains retryable: only
                # status=VERIFIED is authoritative to completed() and dependency checks.
                if record["status"] == "VERIFIED":
                    try:
                        persist_json_atomic(
                            STATE / "completed" / f"{task_key}.json",
                            {**record, "status": "FINALIZING"},
                        )
                    except Exception as exc:
                        record["status"] = "BLOCKED"
                        record["error"] = "CompletionPreparePersistError:" + repr(exc)
                try:
                    store.release(
                        task_key,
                        "VERIFIED" if record["status"] == "VERIFIED" else "REJECTED",
                        remote_terminal_confirmed=worker_terminal_confirmed,
                    )
                except Exception as exc:
                    record["claim_release_error"] = repr(exc)
                    record["status"] = "BLOCKED"
                    record["error"] = "ClaimReleaseError:" + repr(exc)
    return _persist_final_completion(record, store, task_key)


def _persist_final_completion(record: dict, store, task_key: str) -> dict:
    """Promote VERIFIED only after claim release; fail closed on persistence errors."""
    if record["status"] == "VERIFIED":
        completed_path = STATE / "completed" / f"{task_key}.json"
        try:
            persist_json_atomic(completed_path, record)
        except Exception as exc:
            record["status"] = "BLOCKED"
            record["error"] = "CompletionPersistError:" + repr(exc)
            try:
                store.release(task_key, "REJECTED", remote_terminal_confirmed=True)
            except Exception as release_exc:
                record["completion_claim_release_error"] = repr(release_exc)
    if record["status"] != "VERIFIED" and record.get("worker_run_id"):
        # Any failed finalization must replace a prior FINALIZING marker with a
        # non-authoritative failure record; this is intentionally independent of
        # the preceding if so promotion errors are covered as well.
        try:
            persist_json_atomic(STATE / "completed" / f"{task_key}.json", record)
        except Exception as exc:
            record["completion_persist_error"] = type(exc).__name__ + ":" + str(exc)
    return record


def process_task(task: dict, expected_base_sha: str) -> dict:
    raise RuntimeError("legacy_local_executor_disabled")


def main() -> int:
    recovery_task_id = str(os.environ.get("ASTRA_RECOVER_QUARANTINED_TASK_ID", "")).strip()
    if recovery_task_id:
        try:
            result = recover_quarantined_claim(recovery_task_id)
        except ValueError as exc:
            result = {"task_id": recovery_task_id, "status": "BLOCKED", "error": str(exc)}
        print(json.dumps(result, sort_keys=True))
        return 0 if result.get("status") == "RECOVERED" else 2
    state_failure = queue_state_preflight()
    if state_failure is not None:
        print(json.dumps({
            "status": "BLOCKED",
            "reason": "queue_state_preflight_failed",
            **state_failure,
        }, sort_keys=True))
        return 2
    controller_failure = wait_for_controller_slot()
    if controller_failure is not None:
        print(json.dumps(controller_failure, sort_keys=True))
        return 2
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
    controller_node = str(os.environ.get("ASTRA_CONTROLLER_NODE_ID", "")).strip()
    if controller_node and controller_node not in PERMANENT_EXECUTOR_POOL:
        print(json.dumps({
            "status": "BLOCKED",
            "reason": "controller_node_identity_invalid",
            "controller_node_id": controller_node,
            "base_sha": base_sha,
        }, sort_keys=True))
        return 2
    selected = select_distributed_tasks(
        tasks,
        MAX_WORKERS,
        excluded_nodes={controller_node} if controller_node else None,
    )
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
        "command_id": os.environ.get("ASTRA_COMMAND_ID", ""),
        "base_sha": base_sha,
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