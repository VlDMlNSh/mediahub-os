"""Bounded autonomous development queue for the Astra reference runtime.

Promotion-safe: workers create task branches and evidence, but never merge to main.
"""
from __future__ import annotations
import concurrent.futures
import hashlib, json, os, subprocess, threading, time
from pathlib import Path
from .agent_fabric import AgentClaim, ClaimStore

ROOT = Path(__file__).resolve().parents[2]
TASK_DIR = ROOT / "ops" / "agent-fabric" / "tasks"
STATE = Path(os.environ.get("ASTRA_QUEUE_STATE_DIR", "/var/lib/mediahub-astra/queue"))
CLAIMS = STATE / "claims"
MAX_WORKERS = max(1, min(int(os.environ.get("ASTRA_QUEUE_MAX_WORKERS", "2")), 2))
CODEX = os.environ.get("ASTRA_CODEX_BIN", "/usr/local/bin/codex")
TASK_TIMEOUT = max(60, int(os.environ.get("ASTRA_QUEUE_TASK_TIMEOUT", "1800")))

def run(argv: list[str], timeout: int = 300, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(argv, cwd=cwd or ROOT, text=True, capture_output=True, timeout=timeout, check=False)

def worktree_path(task_id: str) -> Path:
    return STATE / "worktrees" / task_id

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

def completed(task_id: str) -> bool:
    marker = STATE / "completed" / f"{task_id}.json"
    if marker.is_file():
        return True
    evidence_path = STATE / "evidence" / f"{task_id}.json"
    if not evidence_path.is_file():
        return False
    try:
        payload = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if payload.get("status") != "VERIFIED" or not payload.get("head_sha"):
        return False
    claim_path = CLAIMS / f"{task_id}.json"
    try:
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return claim.get("status") == "VERIFIED"

def dependencies_satisfied(task: dict) -> bool:
    return all(completed(str(dep)) for dep in task.get("dependencies", ()))

def boundary_allows(path: str, boundary: tuple[str, ...]) -> bool:
    normalized = path.replace("\\", "/").lstrip("./")
    return bool(boundary) and any(normalized == allowed or normalized.startswith(allowed + "/") for allowed in boundary)

def evidence(task_id: str, payload: dict) -> None:
    target = STATE / "evidence"
    target.mkdir(parents=True, exist_ok=True)
    path = target / f"{task_id}.json"
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path.exists():
        try:
            existing = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise RuntimeError("evidence_unreadable") from exc
        if existing != encoded:
            raise RuntimeError("evidence_immutable")
        return
    tmp = target / f".{task_id}.json.tmp"
    try:
        fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    except FileExistsError:
        raise RuntimeError("evidence_write_race")
    finally:
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass

def claim_for(task: dict) -> AgentClaim:
    now = time.time()
    return AgentClaim(
        agent="A2-BUILDER", task_id=str(task["task_id"]),
        goal=str(task.get("mission", task["task_id"])),
        paths=tuple(task.get("boundary", [])),
        exclusive_actions=("implement", "commit"),
        dependencies=tuple(task.get("dependencies", [])),
        status="ACTIVE", started=now, updated=now, expiry=now + 900,
        base_sha=run(["git", "rev-parse", "HEAD"], 30).stdout.strip())

def builder_prompt(task: dict) -> str:
    return f"""You are A2 Builder in MediaHub Agent Fabric.
Task ID: {task['task_id']}
Mission: {task.get('mission','')}
Boundary: {json.dumps(task.get('boundary',[]))}
Forbidden surfaces: {json.dumps(task.get('forbidden_surfaces',[]))}
Acceptance: {json.dumps(task.get('acceptance',[]))}
Implement only this task. Do not touch forbidden surfaces, production infrastructure,
user data, credentials, or unrelated files. Work on the current task branch.
Run relevant tests. Do not merge to main. Report changes and verification."""

def verifier_prompt(task: dict) -> str:
    return f"""You are A3 Verifier, independent from the builder.
Review task {task['task_id']} against acceptance criteria:
{json.dumps(task.get('acceptance',[]))}
Boundary: {json.dumps(task.get('boundary',[]))}
Forbidden surfaces: {json.dumps(task.get('forbidden_surfaces',[]))}
Inspect the actual git diff and run appropriate tests. Do not modify source files.
Return PASS only if acceptance is directly evidenced; otherwise return BLOCKED."""

def process_task(task: dict) -> dict:
    STATE.mkdir(parents=True, exist_ok=True)
    (STATE / "completed").mkdir(parents=True, exist_ok=True)
    store = ClaimStore(CLAIMS)
    claim = claim_for(task)
    started = time.time()
    branch = f"astra/auto/{task['task_id']}"
    worktree = worktree_path(str(task["task_id"]))
    record = {"task_id": task["task_id"], "started_at": int(started), "base_sha": claim.base_sha,
              "branch": branch, "status": "BLOCKED"}
    heartbeat_stop = threading.Event()
    heartbeat_failed = threading.Event()
    heartbeat_thread: threading.Thread | None = None
    try:
        store.acquire(claim)

        def renew() -> None:
            while not heartbeat_stop.wait(300):
                try:
                    store.heartbeat(claim.task_id, lease_seconds=900.0)
                except Exception:
                    heartbeat_failed.set()
                    return

        heartbeat_thread = threading.Thread(target=renew, name=f"astra-heartbeat-{claim.task_id}", daemon=True)
        heartbeat_thread.start()
        worktree.parent.mkdir(parents=True, exist_ok=True)
        if worktree.exists():
            existing = run(["git", "status", "--porcelain"], 60, worktree)
            if existing.returncode:
                raise RuntimeError("existing_worktree_uninspectable")
            if existing.stdout.strip():
                raise RuntimeError("existing_worktree_dirty")
            cleanup = run(["git", "worktree", "remove", str(worktree)], 120)
            if cleanup.returncode:
                raise RuntimeError("worktree_cleanup_failed")
        checkout = run(["git", "worktree", "add", "-b", branch, str(worktree), claim.base_sha], 120)
        if checkout.returncode: raise RuntimeError("worktree_create_failed")
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        build = run([CODEX, "exec", "--sandbox", "workspace-write", "--ask-for-approval", "never", "--skip-git-repo-check", builder_prompt(task)], TASK_TIMEOUT, worktree)
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        record["builder"] = {
            "returncode": build.returncode,
            "stdout_sha256": hashlib.sha256(build.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(build.stderr.encode()).hexdigest(),
            "stdout_bytes": len(build.stdout.encode()),
            "stderr_bytes": len(build.stderr.encode()),
        }
        if build.returncode != 0: raise RuntimeError("builder_failed")
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        test = run(["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], 900, worktree)
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        record["tests"] = {"returncode": test.returncode, "stdout": test.stdout[-8000:], "stderr": test.stderr[-6000:]}
        if test.returncode != 0: raise RuntimeError("tests_failed")
        diff = run(["git", "diff", "--check"], 60, worktree)
        if diff.returncode: raise RuntimeError("diff_check_failed")
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        verifier = run([CODEX, "exec", "--sandbox", "read-only", "--skip-git-repo-check", verifier_prompt(task)], TASK_TIMEOUT, worktree)
        if heartbeat_failed.is_set(): raise RuntimeError("claim_heartbeat_failed")
        record["verifier"] = {
            "returncode": verifier.returncode,
            "stdout_sha256": hashlib.sha256(verifier.stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(verifier.stderr.encode()).hexdigest(),
            "stdout_bytes": len(verifier.stdout.encode()),
            "stderr_bytes": len(verifier.stderr.encode()),
        }
        if verifier.returncode != 0: raise RuntimeError("verifier_failed")
        status = run(["git", "status", "--porcelain"], 60, worktree)
        if not status.stdout.strip(): raise RuntimeError("no_changes")
        boundary = tuple(str(p).strip("/") for p in task.get("boundary", []) if str(p).strip("/"))
        changed = [line[3:] for line in status.stdout.splitlines() if len(line) >= 4]
        if not boundary or any(not boundary_allows(path, boundary) for path in changed):
            raise RuntimeError("boundary_violation")
        if run(["git", "add", "--", *boundary], 60, worktree).returncode: raise RuntimeError("git_add_failed")
        staged = run(["git", "diff", "--cached", "--name-only"], 60, worktree)
        if staged.returncode or any(not boundary_allows(path, boundary) for path in staged.stdout.splitlines()):
            raise RuntimeError("staged_boundary_violation")
        commit = run(["git", "commit", "-m", f"astra: complete {task['task_id']}"], 120, worktree)
        if commit.returncode: raise RuntimeError("git_commit_failed")
        push = run(["git", "push", "origin", f"HEAD:refs/heads/{branch}"], 180, worktree)
        record["push"] = {"returncode": push.returncode, "stdout": push.stdout[-4000:], "stderr": push.stderr[-4000:]}
        if push.returncode: raise RuntimeError("git_push_failed")
        record["head_sha"] = run(["git", "rev-parse", "HEAD"], 30, worktree).stdout.strip()
        record["status"] = "VERIFIED"
    except Exception as exc:
        record["error"] = type(exc).__name__ + ":" + str(exc)
    finally:
        heartbeat_stop.set()
        if heartbeat_thread is not None:
            heartbeat_thread.join(timeout=5)
        try:
            if worktree.exists():
                existing = run(["git", "status", "--porcelain"], 60, worktree)
                if existing.returncode != 0:
                    record["worktree_cleanup_error"] = "uninspectable"
                elif existing.stdout.strip():
                    record["worktree_cleanup_error"] = "dirty_worktree_preserved"
                else:
                    cleanup = run(["git", "worktree", "remove", str(worktree)], 120)
                    if cleanup.returncode:
                        record["worktree_cleanup_error"] = "remove_failed"
        except Exception:
            record["worktree_cleanup_error"] = "cleanup_exception"
        record["elapsed_seconds"] = round(time.time() - started, 3)
        try:
            evidence(task["task_id"], record)
            try:
                store.release(claim.task_id, "VERIFIED" if record["status"] == "VERIFIED" else "REJECTED")
            except Exception as exc:
                record["claim_release_error"] = repr(exc)
                record["status"] = "BLOCKED"
            if record["status"] == "VERIFIED":
                (STATE / "completed" / f"{task['task_id']}.json").write_text(
                    json.dumps({"task_id": task["task_id"], "head_sha": record.get("head_sha"), "status": "VERIFIED"}, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
        except Exception as exc:
            record["evidence_error"] = type(exc).__name__ + ":" + str(exc)
            record["status"] = "BLOCKED"
    return record

def main() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    tasks = [t for t in load_tasks() if not completed(str(t["task_id"])) and dependencies_satisfied(t)]
    if not tasks:
        print(json.dumps({"status":"IDLE","reason":"no_ready_tasks"}, sort_keys=True)); return 0
    selected = tasks[:MAX_WORKERS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(selected)) as pool:
        results = list(pool.map(process_task, selected))
    print(json.dumps({"status":"PASS" if all(r["status"]=="VERIFIED" for r in results) else "BLOCKED",
                      "workers": len(selected), "results": results}, sort_keys=True))
    return 0 if all(r["status"]=="VERIFIED" for r in results) else 2

if __name__ == "__main__":
    raise SystemExit(main())
