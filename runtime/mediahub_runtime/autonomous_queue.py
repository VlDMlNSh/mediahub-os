"""Bounded autonomous development queue for the Astra reference runtime.

Promotion-safe: workers create task branches and evidence, but never merge to main.
"""
from __future__ import annotations

import concurrent.futures
import functools
import json
import os
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

from .agent_fabric import AgentClaim, ClaimStore

ROOT = Path(__file__).resolve().parents[2]
TASK_DIR = ROOT / "ops" / "agent-fabric" / "tasks"
STATE = Path(os.environ.get("ASTRA_QUEUE_STATE_DIR", "/var/lib/mediahub-astra/queue"))
CLAIMS = STATE / "claims"

# Three permanent executor lanes; Astra Gold permits up to three active claims.
PERMANENT_EXECUTOR_POOL = {
    "mh-dev-01": "claude",
    "mh-dev-02": "codex",
    "Voktors-Mac-mini.local": "claude",
}

CODEX_HOME_ROOT = Path(os.environ.get("ASTRA_CODEX_HOME_ROOT", str(Path.home() / ".cache" / "mediahub" / "astra-codex")))

def _codex_home(prefix: str) -> tempfile.TemporaryDirectory:
    Path(CODEX_HOME_ROOT).mkdir(parents=True, exist_ok=True)
    return tempfile.TemporaryDirectory(prefix=prefix, dir=str(CODEX_HOME_ROOT))

def bounded_worker_count(requested: int) -> int:
    return max(1, min(int(requested), 3))


MAX_WORKERS = bounded_worker_count(int(os.environ.get("ASTRA_QUEUE_MAX_WORKERS", "3")))
CODEX = os.environ.get("ASTRA_CODEX_BIN", "/usr/local/bin/codex")
TASK_TIMEOUT = max(60, int(os.environ.get("ASTRA_QUEUE_TASK_TIMEOUT", "1800")))


@functools.lru_cache(maxsize=4)
def _local_codex_agentic_probe(model: str) -> bool:
    """Require the local Codex+Ollama path to perform a bounded real file edit."""
    try:
        home = _codex_home("agentic-")
        config = Path(home.name) / "config.toml"
        config.write_text(
            f'model_provider = "ollama"\n'
            f'model = "{model}"\n'
            'approval_policy = "never"\n'
            'web_search = "disabled"\n'
            '[features]\n'
            'multi_agent = false\n'
            'multi_agent_v2 = false\n'
            'apps = false\n'
            'tool_search = false\n'
            'plugins = false\n',
            encoding="utf-8",
        )
        probe_dir = Path(tempfile.mkdtemp(prefix="astra-local-agentic-work-"))
        probe_file = probe_dir / "probe.txt"
        env = os.environ.copy()
        env["CODEX_HOME"] = home.name
        probe_timeout = max(90, min(int(os.environ.get("ASTRA_LOCAL_AGENTIC_PROBE_TIMEOUT", "300")), 600))
        result = run(
            [
                CODEX,
                "exec",
                "--oss",
                "--local-provider",
                "ollama",
                "--model",
                model,
                "--sandbox",
                "workspace-write",
                "--skip-git-repo-check",
                "--config",
                "model_reasoning_effort=none",
                (
                    "Create exactly one file at "
                    f"{probe_file} containing exactly "
                    "\"MEDIAHUB_LOCAL_CODEX_AGENTIC_OK\". "
                    "Do not call the network and do not modify any other files."
                ),
            ],
            probe_timeout,
            probe_dir,
            env,
        )
        ok = (
            result.returncode == 0
            and probe_file.is_file()
            and probe_file.read_text(encoding="utf-8", errors="replace").strip()
            == "MEDIAHUB_LOCAL_CODEX_AGENTIC_OK"
        )
        return ok
    except (OSError, subprocess.SubprocessError):
        return False
    finally:
        try:
            home.cleanup()
        except Exception:
            pass


def local_ollama_profile() -> tuple[str, str] | None:
    if os.environ.get("ASTRA_ENABLE_LOCAL_OLLAMA", "1").strip().lower() in {"0", "false", "no"}:
        return None
    base = os.environ.get("ASTRA_OLLAMA_BASE_URL", "http://127.0.0.1:11434/v1").rstrip("/")
    timeout = max(3, min(int(os.environ.get("ASTRA_LOCAL_EXECUTOR_TIMEOUT", "15")), 30))
    try:
        req = urllib.request.Request(base + "/models", method="GET", headers={"Authorization": "Bearer ollama"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            payload = json.loads(response.read(128 * 1024).decode("utf-8", "replace"))
        models = [str(item.get("id") or "").strip() for item in payload.get("data", []) if isinstance(item, dict)]
        models = [m for m in models if m]
        if not models:
            return None
        preferred = ("qwen2.5-coder:3b", "qwen2.5-coder-3b:latest")
        model = next((candidate for candidate in preferred if candidate in models), None)
        if model is None:
            return None
        body = json.dumps({"model": model, "input": "Return exactly MEDIAHUB_LOCAL_EXECUTOR_QUALIFICATION_OK", "max_output_tokens": 16}).encode()
        probe = urllib.request.Request(base + "/responses", data=body, method="POST", headers={"Authorization": "Bearer ollama", "Content-Type": "application/json", "Accept": "application/json"})
        with urllib.request.urlopen(probe, timeout=timeout) as response:
            result = json.loads(response.read(128 * 1024).decode("utf-8", "replace"))
        output = str(result.get("output_text") or "").strip()
        if not output:
            for item in result.get("output") or []:
                if isinstance(item, dict):
                    for part in item.get("content") or []:
                        if isinstance(part, dict) and part.get("text"):
                            output += str(part["text"])
        if "MEDIAHUB_LOCAL_EXECUTOR_QUALIFICATION_OK" not in output:
            return None
        if not _local_codex_agentic_probe(model):
            return None
        return ("ollama", model)
    except (OSError, ValueError, urllib.error.URLError, urllib.error.HTTPError):
        return None


def qualified_codex_profile() -> tuple[str, str]:
    evidence_path = os.environ.get("ASTRA_PROVIDER_EVIDENCE_PATH", "").strip()
    if not evidence_path:
        raise RuntimeError("qualified_executor_evidence_missing")
    path = Path(evidence_path)
    if not path.is_file():
        raise RuntimeError("qualified_executor_evidence_missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError("qualified_executor_evidence_invalid") from exc
    if payload.get("status") != "PASS":
        raise RuntimeError("qualified_executor_evidence_not_pass")
    expected_sha = os.environ.get("ASTRA_PROVIDER_TARGET_SHA", "").strip()
    if not expected_sha:
        raise RuntimeError("qualified_executor_target_sha_missing")
    if str(payload.get("target_sha", "")).strip() != expected_sha:
        raise RuntimeError("qualified_executor_target_sha_mismatch")
    expected_command = os.environ.get("ASTRA_COMMAND_ID", "").strip()
    if expected_command and str(payload.get("command_id", "")).strip() != expected_command:
        raise RuntimeError("qualified_executor_command_id_mismatch")
    candidates = []
    for item in payload.get("providers", []):
        if (
            item.get("provider") == "Hugging Face"
            and item.get("verification_state") == "QUALIFIED"
            and isinstance(item.get("selected_model"), str)
            and item.get("selected_model").strip()
        ):
            candidates.append(item["selected_model"].strip())
    if not candidates:
        raise RuntimeError("qualified_huggingface_executor_missing")
    if not os.environ.get("HF_TOKEN"):
        raise RuntimeError("qualified_huggingface_credential_missing")
    return "huggingface", candidates[0]


def codex_sandbox_mode() -> str:
    mode = os.environ.get("ASTRA_CODEX_SANDBOX_MODE", "workspace-write").strip()
    if mode not in {"workspace-write", "danger-full-access"}:
        raise RuntimeError("invalid_codex_sandbox_mode")
    return mode


def codex_env_for_qualified_provider() -> tuple[dict[str, str], tempfile.TemporaryDirectory, str, str]:
    local = local_ollama_profile()
    profile, model = local or qualified_codex_profile()
    home = _codex_home("qualified-")
    config = Path(home.name) / "config.toml"
    config.write_text(
        f'model_provider = "{profile}"\n'
        f'model = "{model}"\n'
        'approval_policy = "never"\n'
        'web_search = "disabled"\n'
        '[features]\n'
        'multi_agent = false\n'
        'multi_agent_v2 = false\n'
        'apps = false\n'
        'tool_search = false\n'
        'plugins = false\n'
        '[model_providers.huggingface]\n'
        'name = "Hugging Face"\n'
        'base_url = "https://router.huggingface.co/v1"\n'
        'env_key = "HF_TOKEN"\n'
        'wire_api = "responses"\n'
        'supports_websockets = false\n'
        'multi_agent = false\n'
        'multi_agent_v2 = false\n'
        'apps = false\n'
        'tool_search = false\n'
        'connectors = false\n'
        'plugins = false\n',
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["CODEX_HOME"] = home.name
    return env, home, profile, model


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


def worktree_path(task_id: str) -> Path:    return STATE / "worktrees" / safe_task_id(task_id)


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
    if executor not in {"codex", "claude"} or verifier not in {"codex", "claude"} or executor == verifier:
        return {"task_id": task_key, "status": "BLOCKED", "error": "invalid_executor_split"}
    if not os.environ.get("GH_TOKEN") and not os.environ.get("GITHUB_TOKEN"):
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
        gh_env = os.environ.copy()
        if gh_env.get("GITHUB_TOKEN") and not gh_env.get("GH_TOKEN"):
            gh_env["GH_TOKEN"] = gh_env["GITHUB_TOKEN"]
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
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "completed").mkdir(parents=True, exist_ok=True)
    store = ClaimStore(CLAIMS)
    claim = claim_for(task, expected_base_sha)
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
        local_head = run(["git", "rev-parse", "HEAD"], 30)
        if local_head.returncode != 0 or local_head.stdout.strip() != expected_base_sha:
            raise RuntimeError("queue_base_sha_not_current_head")
        if claim.base_sha != expected_base_sha:
            raise RuntimeError("queue_claim_base_sha_mismatch")
        existing_branch = run(["git", "ls-remote", "--exit-code", "--heads", "origin", f"refs/heads/{branch}"], 60)
        if existing_branch.returncode == 0:
            raise RuntimeError("queue_branch_already_exists")
        if existing_branch.returncode != 2:
            raise RuntimeError("queue_branch_probe_failed")
        checkout = run(["git", "worktree", "add", "-b", branch, str(worktree), claim.base_sha], 120)
        if checkout.returncode:
            raise RuntimeError("worktree_create_failed")
        try:
            codex_env, codex_home, executor, model = codex_env_for_qualified_provider()
        except RuntimeError as exc:
            raise RuntimeError(str(exc))
        record["executor"] = {
            "executor": executor,
            "model": model,
            "qualification": "fresh_local_or_provider_qualified",
        }
        build = run(
            [CODEX, "exec", "--oss", "--local-provider", "ollama", "--model", model, "--sandbox", "workspace-write", "--skip-git-repo-check", builder_prompt(task)],
            TASK_TIMEOUT,
            worktree,
            codex_env,
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
        boundary_tests = [
            str(path).lstrip("./")
            for path in task.get("boundary", [])
            if str(path).lstrip("./").startswith("tests/")
        ]
        explicit_tests = [
            str(path).lstrip("./")
            for path in task.get("test_paths", [])
            if str(path).lstrip("./").startswith("tests/")
        ]
        selected_tests = list(dict.fromkeys(explicit_tests or boundary_tests))
        if not selected_tests:
            selected_tests = [
                "tests/test_autonomous_queue.py",
                "tests/test_autonomous_queue_contract.py",
                "tests/test_agent_fabric.py",
                "tests/test_astra_github_agent_contract.py",
            ]
        if len(selected_tests) == 1:
            test = run(
                ["python3", "-m", "pytest", "-q", selected_tests[0]],
                900,
                worktree,
            )
        else:
            test = run(
                ["python3", "-m", "pytest", "-q", *selected_tests],
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
        try:
            diff_for_verifier = run(["git", "diff", "--no-ext-diff", expected_base_sha, "HEAD"], 60, worktree)
            if diff_for_verifier.returncode != 0:
                raise RuntimeError("verifier_diff_failed")
            test_text = record["tests"].get("stderr", "") + record["tests"].get("stdout", "")
            verifier = run(
                [CODEX, "exec", "--oss", "--local-provider", "ollama", "--model", model, "--sandbox", "read-only", "--skip-git-repo-check", verifier_prompt(task, diff_for_verifier.stdout, test_text)],
                TASK_TIMEOUT,
                worktree,
                codex_env,
            )
        finally:
            codex_home.cleanup()
        record["verifier"] = {
            "returncode": verifier.returncode,
            "stdout": verifier.stdout[-12000:],
            "stderr": verifier.stderr[-8000:],
        }
        if verifier.returncode != 0 or not _verifier_passed(verifier.stdout):
            raise RuntimeError("verifier_failed")
        status = run(["git", "status", "--porcelain"], 60, worktree)
        if not status.stdout.strip():
            if not bool(task.get("allow_no_changes", False)):
                raise RuntimeError("no_changes")
            record["head_sha"] = expected_base_sha
            record["change_status"] = "NO_CHANGES_REQUIRED"
            record["push_verification"] = {
                "status": "NOT_REQUIRED",
                "reason": "task_already_satisfied",
                "branch": branch,
            }
            record["status"] = "VERIFIED"
            (STATE / "completed" / f"{task_key}.json").write_text(
                json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
            return
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
        remote_head = run(            ["git", "ls-remote", "origin", f"refs/heads/{branch}"], 60, worktree
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
            record["status"] = "BLOCKED"
            record["error"] = "ClaimReleaseError:" + repr(exc)
        try:
            if worktree.exists():
                run(["git", "worktree", "remove", "--force", str(worktree)], 120)
        except Exception:
            record["worktree_cleanup_error"] = True
            if record["status"] == "VERIFIED":
                record["status"] = "BLOCKED"
                record["error"] = "WorktreeCleanupError:cleanup_failed"
        record["elapsed_seconds"] = round(time.time() - started, 3)
        evidence(task["task_id"], record)
    return record


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
    if os.environ.get("ASTRA_DISTRIBUTED_LOCAL", "0").strip().lower() in {"1", "true", "yes"}:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected)) as pool:
            results = list(pool.map(lambda task: process_task_remote(task, base_sha), selected))
        all_verified = all(r["status"] == "VERIFIED" for r in results)
        print(json.dumps({
            "status": "PASS" if all_verified else "BLOCKED",
            "workers": len(selected),
            "executor_pool": PERMANENT_EXECUTOR_POOL,
            "max_parallel_claims": MAX_WORKERS,
            "mode": "github_remote_local_executor",
            "selected_tasks": [str(t["task_id"]) for t in selected],
            "results": results,
        }, sort_keys=True))
        return 0 if all_verified else 2
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected)) as pool:
        results = list(pool.map(lambda task: process_task(task, base_sha), selected))
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