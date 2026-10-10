import json
import os
from pathlib import Path
from mediahub_runtime import autonomous_queue

def test_load_tasks_prefers_ready(monkeypatch, tmp_path: Path):
    task_dir = tmp_path / "tasks"; task_dir.mkdir()
    (task_dir / "b.json").write_text(json.dumps({"task_id":"B","status":"WAIT","priority":"P0"}))
    (task_dir / "a.json").write_text(json.dumps({"task_id":"A","status":"READY","priority":"P1"}))
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    assert [t["task_id"] for t in autonomous_queue.load_tasks()] == ["A"]

def test_load_tasks_sorts_ready_by_priority_then_task_id(monkeypatch, tmp_path: Path):
    task_dir = tmp_path / "tasks"; task_dir.mkdir()
    for name, task_id, priority in [("z.json", "Z", "P1"), ("a.json", "A", "P0"), ("b.json", "B", "P0")]:
        (task_dir / name).write_text(json.dumps({"task_id":task_id,"status":"READY","priority":priority}))
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    assert [t["task_id"] for t in autonomous_queue.load_tasks()] == ["A", "B", "Z"]


def test_main_suppresses_completed_tasks(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"; task_dir.mkdir()
    state = tmp_path / "state"
    target = "a" * 40
    (task_dir / "a.json").write_text(json.dumps({"task_id":"A","status":"READY","priority":"P0"}))
    (state / "completed").mkdir(parents=True)
    (state / "completed" / "A.json").write_text(
        json.dumps({"status":"VERIFIED","base_sha":target}),
        encoding="utf-8",
    )
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)
    class R:
        returncode = 0
        stdout = target + "\n"
        stderr = ""
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    assert autonomous_queue.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "IDLE"
    assert payload["reason"] == "no_ready_tasks"
def test_main_returns_idle_when_no_ready_tasks(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"; task_dir.mkdir()
    state = tmp_path / "state"
    (task_dir / "a.json").write_text(json.dumps({"task_id":"A","status":"WAIT","priority":"P0"}))
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)
    class R:
        returncode = 0
        stdout = "b" * 40 + "\n"
        stderr = ""
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    assert autonomous_queue.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "IDLE"
    assert payload["reason"] == "no_ready_tasks"
    assert payload["base_sha"] == "b" * 40
    assert payload["discovered_tasks"] == []
def test_claim_uses_task_boundary(monkeypatch):
    class R: stdout = "abc123\n"
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    claim = autonomous_queue.claim_for({"task_id":"T1","mission":"m","boundary":["docs/a","ops/b"]}, "targetsha")
    assert claim.base_sha == "targetsha"
    assert claim.paths == ("docs/a","ops/b")
    assert claim.agent == "A2-BUILDER"


def test_remote_dispatch_claim_persists_quarantine_recovery_identity(monkeypatch, tmp_path: Path):
    captured = {}

    class Store:
        def acquire(self, claim):
            captured["claim"] = claim

        def release(self, task_id, status, *, remote_terminal_confirmed=False):
            captured["release"] = (task_id, status, remote_terminal_confirmed)

    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "claims")
    store = Store()
    monkeypatch.setattr(autonomous_queue, "ClaimStore", lambda root: store)
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"PATH": "/bin"})
    monkeypatch.setenv("ASTRA_COMMAND_ID", "CMD-1")

    class BaselineFailure:
        returncode = 1
        stdout = ""
        stderr = "synthetic baseline failure"

    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: BaselineFailure())
    task = {
        "task_id": "TASK-1",
        "node_id": "mh-dev-01",
        "executor": "claude",
        "verifier": "claude",
        "independent_verifier_process": True,
        "boundary": ["src"],
    }
    result = autonomous_queue.process_task_remote(task, "a" * 40)

    assert result["status"] == "BLOCKED"
    claim = captured["claim"]
    assert claim.command_id == "CMD-1"
    assert claim.node_id == "mh-dev-01"
    assert claim.executor == "claude"
    assert captured["release"] == ("TASK-1", "REJECTED", False)


def test_worktree_path_is_task_scoped_and_deterministic(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    first = autonomous_queue.worktree_path("TASK-1")
    second = autonomous_queue.worktree_path("TASK-1")
    other = autonomous_queue.worktree_path("TASK-2")
    assert first == second
    assert first != other
    assert first.parent == tmp_path / "state" / "worktrees"
    assert first.name == "TASK-1"


def test_max_workers_is_bounded_by_three_concurrent_claims():
    assert autonomous_queue.bounded_worker_count(99) == 3
    assert autonomous_queue.bounded_worker_count(0) == 1


def test_worker_run_title_requires_a_safe_nonempty_command_id():
    assert autonomous_queue.worker_run_title(
        "cmd-20261010.01", "TASK-1", "mh-dev-01", "claude"
    ) == "Astra distributed worker / cmd-20261010.01 / TASK-1 / mh-dev-01 / claude"
    for invalid in ("", "bad command", "../unsafe", "x" * 129):
        try:
            autonomous_queue.worker_run_title(invalid, "TASK-1", "mh-dev-01", "claude")
        except ValueError as exc:
            assert str(exc) == "invalid_command_id"
        else:
            raise AssertionError("unsafe command ID must be rejected")


def test_worker_run_matching_requires_exact_title_and_a_new_run_id():
    expected = "Astra distributed worker / cmd-1 / TASK-1 / mh-dev-01 / claude"
    rows = [
        {"databaseId": 10, "displayTitle": expected},
        {"databaseId": 11, "displayTitle": expected + " / stale"},
        {"databaseId": 12, "displayTitle": expected},
        {"databaseId": "bad", "displayTitle": expected},
    ]
    matches = autonomous_queue.matching_new_worker_runs(rows, expected, {10})
    assert matches == [{"databaseId": 12, "displayTitle": expected}]


def test_queue_source_does_not_force_push():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert "--force-with-lease" not in source
    assert '"git", "push", "--force"' not in source
    assert '"git", "push", "--force-with-lease"' not in source


def test_a3_verifier_requires_exact_machine_verdict():
    assert autonomous_queue._verifier_passed("ASTRA_VERDICT: PASS\n")
    assert not autonomous_queue._verifier_passed("PASS\n")
    assert not autonomous_queue._verifier_passed("ASTRA_VERDICT: PASS\nASTRA_VERDICT: BLOCKED\n")


def test_completed_rejects_stale_base_sha(monkeypatch, tmp_path: Path):
    state = tmp_path / "state"
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    (completed_dir / "T.json").write_text(
        json.dumps({"status": "VERIFIED", "base_sha": "oldsha"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    assert autonomous_queue.completed("T", "oldsha")
    assert not autonomous_queue.completed("T", "newsha")


def test_main_does_not_suppress_stale_completion(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    state = tmp_path / "state"
    (task_dir / "a.json").write_text(
        json.dumps({"task_id": "A", "status": "READY", "priority": "P0"})
    )
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    (completed_dir / "A.json").write_text(
        json.dumps({"status": "VERIFIED", "base_sha": "oldsha"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)

    class R:
        returncode = 0
        stdout = "newsha\n"
        stderr = ""

    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    monkeypatch.setattr(
        autonomous_queue,
        "process_task",
        lambda task, base_sha: {"task_id": task["task_id"], "status": "BLOCKED", "base_sha": base_sha},
    )
    result = autonomous_queue.main()
    payload = json.loads(capsys.readouterr().out)
    assert result == 2
    assert payload["status"] == "BLOCKED"
    assert payload["reason"] == "no_eligible_distributed_tasks"
    assert payload["base_sha"] == "newsha"
def test_existing_dirty_worktree_is_not_force_removed(monkeypatch, tmp_path: Path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    class Status:
        returncode = 0
        stdout = " M user_change.py\\n"
        stderr = ""
    calls = []
    def fake_run(argv, *args, **kwargs):
        calls.append(argv)
        return Status()
    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    try:
        autonomous_queue.prepare_worktree(worktree)
    except RuntimeError as exc:
        assert str(exc) == "stale_worktree_dirty"
    else:
        raise AssertionError("dirty worktree must block")
    assert all(argv[:4] != ["git", "worktree", "remove", "--force"] for argv in calls)


def test_controller_claim_requires_explicit_success_status():
    source = (Path(__file__).resolve().parents[1] / "astra_github_agent.py").read_text(encoding="utf-8")
    assert 'claim_status = "VERIFIED" if rc == 0 and result_status == "PASS" else "REJECTED"' in source

def test_dependencies_require_same_base_sha(monkeypatch, tmp_path: Path):
    state = tmp_path / "state"
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    (completed_dir / "DEP.json").write_text(
        json.dumps({"status": "VERIFIED", "base_sha": "oldsha"}),
        encoding="utf-8",
    )
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    task = {"task_id": "TASK", "dependencies": ["DEP"]}
    assert autonomous_queue.dependencies_satisfied(task, "oldsha")
    assert not autonomous_queue.dependencies_satisfied(task, "newsha")


def test_scope_check_rejects_untracked_files(monkeypatch, tmp_path: Path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    class R:
        returncode = 0
        stdout = ""
        stderr = ""
    def fake_run(argv, *args, **kwargs):
        if argv[:3] == ["git", "diff", "--name-only"]:
            return R()
        if argv[:3] == ["git", "status", "--porcelain"] and "--untracked-files=all" in argv:
            class S:
                returncode = 0
                stdout = "?? forbidden.txt\n"
                stderr = ""
            return S()
        return R()
    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    assert autonomous_queue._diff_outside_scope({"boundary": ["tests"]}, worktree, "a"*40) == ["forbidden.txt"]


def test_scope_check_rejects_untracked_files_with_explicit_status_probe(monkeypatch, tmp_path: Path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    class R:
        returncode = 0
        stdout = ""
        stderr = ""
    # The implementation must inspect untracked files through git status; this
    # sentinel path is intentionally outside the task boundary.
    calls = []
    def fake_run(argv, *args, **kwargs):
        calls.append(argv)
        if argv[:3] == ["git", "diff", "--name-only"]:
            return R()
        if argv[:3] == ["git", "status", "--porcelain"] and "--untracked-files=all" in argv:
            class S:
                returncode = 0
                stdout = "?? forbidden.txt\n"
                stderr = ""
            return S()
        return R()
    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    assert autonomous_queue._diff_outside_scope({"boundary": ["tests"]}, worktree, "a"*40) == ["forbidden.txt"]



def test_scope_check_rejects_tracked_worktree_changes(monkeypatch, tmp_path: Path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()

    class R:
        returncode = 0
        stdout = ""
        stderr = ""

    def fake_run(argv, *args, **kwargs):
        if argv == ["git", "diff", "--name-only", "a" * 40]:
            return type("Tracked", (), {
                "returncode": 0,                "stdout": "runtime/mediahub_runtime/autonomous_queue.py\n",
                "stderr": "",
            })()
        if argv[:4] == ["git", "diff", "--cached", "--name-only"]:
            return R()
        if argv[:3] == ["git", "status", "--porcelain"] and "--untracked-files=all" in argv:
            return R()
        return R()

    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    assert autonomous_queue._diff_outside_scope(
        {"boundary": ["tests/"], "forbidden_surfaces": ["runtime/"]},
        worktree,
        "a" * 40,
    ) == ["runtime/mediahub_runtime/autonomous_queue.py"]


def test_remote_queue_supports_explicit_no_change_verification():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'task.get("allow_no_changes", False)' in source
    assert '"NOT_REQUIRED"' in source
    assert 'remote_nochange_sha_mismatch' in source


def test_task_id_cannot_escape_queue_state(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    for bad in ("../escape", "a/b", "", "a b"):
        try:
            autonomous_queue.worktree_path(bad)
        except ValueError as exc:
            assert str(exc) == "invalid_task_id"
        else:
            raise AssertionError("unsafe task id must be rejected")


def test_remote_finalization_errors_cannot_remain_verified():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'record["status"] = "BLOCKED"' in source
    assert '"ClaimReleaseError:" + repr(exc)' in source
    assert '"remote_evidence_claim_release_error"' in source


def test_remote_worker_persistence_path_is_created_before_verified_state():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert '(STATE / "completed").mkdir(parents=True, exist_ok=True)' in source
    assert 'record["status"] = "BLOCKED"' in source
    assert 'remote_evidence_error_present' in source
    assert 'remote_evidence_claim_release_error' in source


def test_queue_verifies_remote_push_sha():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'git", "ls-remote", "origin", f"refs/heads/{branch}"' in source
    assert 'remote_push_sha_mismatch' in source
    assert '"push_verification"' in source
    assert 'remote_sha' in source
    assert '"status": "PASS"' in source


def test_remote_queue_requires_remote_branch_sha_consistency():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'controller_remote_branch_sha_mismatch' in source
    assert 'git", "ls-remote", "origin"' in source


def test_canonical_queue_contains_no_legacy_codex_execution_path():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8").lower()
    assert "codex" not in source
    assert "local_ollama" not in source
    assert "hugging face" not in source


def test_queue_pins_workers_to_explicit_target_sha():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'ASTRA_TARGET_SHA' in source
    assert 'queue_target_sha_not_current_head' in source
    assert 'def claim_for(\n    task: dict,\n    base_sha: str,' in source
    assert 'command_id=command_id' in source
    assert 'node_id=node_id' in source
    assert 'executor=executor' in source
    assert 'base_sha' in source
    assert 'target_sha_not_current_head' in source



def test_remote_dispatch_accepts_canonical_fast_pool_node():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert '"Voktors-Mac-mini.local"' in source
    assert 'PERMANENT_EXECUTOR_POOL' in source
    assert 'node_id not in PERMANENT_EXECUTOR_POOL' in source


def test_remote_dispatch_rejects_unknown_nodes():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'node_id not in PERMANENT_EXECUTOR_POOL' in source
    assert 'permanent_executor_binding_mismatch' in source
    assert 'unsupported_remote_node' in source


def test_worker_has_bounded_builder_retry_for_no_change_outcome():
    worker = (Path(__file__).resolve().parents[1] / "ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert 'builder_attempts = max(1, min(int(task.get("builder_attempts", 2)), 2))' in worker
    assert 'RETRY REQUIREMENT' in worker
    assert 'changed_probe = changed_paths(target_sha)' in worker
    assert 'no_changes' in worker


def test_permanent_executor_pool_matches_canonical_three_lane_topology():
    assert autonomous_queue.PERMANENT_EXECUTOR_POOL == {
        "mh-dev-01": "claude",
        "mh-dev-02": "claude",
        "Voktors-Mac-mini.local": "claude",
    }
    assert autonomous_queue.bounded_worker_count(3) == 3

def test_worker_run_title_requires_nonempty_safe_command_id():
    assert autonomous_queue.worker_run_title("MH-QUEUE-1", "TASK-1", "mh-dev-01", "claude") == (
        "Astra distributed worker / MH-QUEUE-1 / TASK-1 / mh-dev-01 / claude"
    )
    for command_id in ("", "   ", "../escape", "bad id", "x" * 129):
        try:
            autonomous_queue.worker_run_title(command_id, "TASK-1", "mh-dev-01", "claude")
        except ValueError as exc:
            assert str(exc) == "invalid_command_id"
        else:
            raise AssertionError("invalid command id must be rejected")


def test_worker_run_matching_requires_exact_title_and_new_run_id():
    title = autonomous_queue.worker_run_title("CMD-1", "TASK-1", "mh-dev-01", "claude")
    rows = [
        {"databaseId": 1, "displayTitle": title},
        {"databaseId": 2, "displayTitle": title + "-stale"},
        {"databaseId": 3, "displayTitle": title},
    ]
    assert autonomous_queue.matching_new_worker_runs(rows, title, {1}) == [rows[2]]
    assert autonomous_queue.matching_new_worker_runs(rows, title, {1, 3}) == []


def test_queue_does_not_release_claim_when_acquire_fails(monkeypatch, tmp_path: Path):
    released = []
    class Store:
        def __init__(self, root):
            pass
        def acquire(self, claim):
            raise RuntimeError("claim_exists")
        def release(self, task_id, status):
            released.append((task_id, status))

    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "claims")
    monkeypatch.setattr(autonomous_queue, "ClaimStore", Store)
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"GH_TOKEN": "test-token"})
    monkeypatch.setenv("ASTRA_COMMAND_ID", "CMD-1")
    task = {
        "task_id": "TASK-1", "node_id": "mh-dev-01", "executor": "claude",
        "verifier": "claude", "independent_verifier_process": True,
        "boundary": ["docs/operations/"],
    }
    result = autonomous_queue.process_task_remote(task, "a" * 40)
    assert result["status"] == "BLOCKED"
    assert "claim_exists" in result["error"]
    assert released == []



def test_queue_state_preflight_checks_state_and_claims(monkeypatch, tmp_path: Path):
    state = tmp_path / "state"
    claims = state / "claims"
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.setattr(autonomous_queue, "CLAIMS", claims)
    assert autonomous_queue.queue_state_preflight() is None
    assert state.is_dir() and claims.is_dir()
    assert not list(state.glob(".astra-queue-preflight-*"))
    assert not list(claims.glob(".astra-queue-preflight-*"))


def test_queue_state_preflight_reports_claim_permission_failure(monkeypatch, tmp_path: Path):
    state = tmp_path / "state"
    claims = state / "claims"
    claims.mkdir(parents=True)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.setattr(autonomous_queue, "CLAIMS", claims)
    real_mkstemp = autonomous_queue.tempfile.mkstemp
    def fail_claim_probe(*, prefix, dir):
        if Path(dir) == claims:
            raise PermissionError(13, "permission denied")
        return real_mkstemp(prefix=prefix, dir=dir)
    monkeypatch.setattr(autonomous_queue.tempfile, "mkstemp", fail_claim_probe)
    assert autonomous_queue.queue_state_preflight() == {
        "component": "claims", "error_type": "PermissionError", "errno": 13,
    }


def test_main_blocks_before_git_or_dispatch_when_state_preflight_fails(monkeypatch, tmp_path: Path, capsys):
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "state" / "claims")
    monkeypatch.setattr(autonomous_queue, "queue_state_preflight", lambda: {
        "component": "claims", "error_type": "PermissionError", "errno": 13,
    })
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("git/worker path must not be reached")))
    assert autonomous_queue.main() == 2
    assert json.loads(capsys.readouterr().out) == {
        "status": "BLOCKED", "reason": "queue_state_preflight_failed",
        "component": "claims", "error_type": "PermissionError", "errno": 13,
    }


def test_remote_worker_unknown_state_quarantines_instead_of_releasing_claim():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'dispatch_attempted = True' in source
    assert 'worker_terminal_confirmed = True' in source
    assert 'gh", "run", "cancel"' in source
    assert 'store.quarantine(task_key, "remote_worker_may_still_be_active")' in source
    assert 'if not dispatch_attempted or worker_terminal_confirmed:' in source
    assert 'remote_terminal_confirmed=worker_terminal_confirmed' in source
    assert 'def heartbeat_claim_if_due(' in source
    assert 'claim_heartbeat_failed_remote_state_unconfirmed' in source


def test_claim_heartbeat_is_renewed_during_run_discovery_and_polling():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert source.count('heartbeat_claim_if_due(store, task_key, last_heartbeat=last_heartbeat)') >= 2
    assert 'claim_heartbeat_failed_remote_state_unconfirmed' in source


def test_heartbeat_claim_if_due_renews_only_when_due(monkeypatch):
    class Store:
        calls = 0
        def heartbeat(self, task_id, lease_seconds):
            self.calls += 1
            assert task_id == "TASK-1"
            assert lease_seconds >= 60
    store = Store()
    assert autonomous_queue.heartbeat_claim_if_due(store, "TASK-1", last_heartbeat=100, now=150, interval=60) == 100
    assert store.calls == 0
    assert autonomous_queue.heartbeat_claim_if_due(store, "TASK-1", last_heartbeat=100, now=160, interval=60) == 160
    assert store.calls == 1


def test_heartbeat_claim_if_due_fails_closed(monkeypatch):
    class Store:
        def heartbeat(self, task_id, lease_seconds):
            raise OSError("claim storage unavailable")
    try:
        autonomous_queue.heartbeat_claim_if_due(Store(), "TASK-1", last_heartbeat=100, now=160, interval=60)
    except RuntimeError as exc:
        assert str(exc) == "claim_heartbeat_failed_remote_state_unconfirmed"
    else:
        raise AssertionError("heartbeat failure must block dispatch/poll progress")


def test_remote_run_id_is_persisted_before_worker_polling():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'store.set_worker_run_id(task_key, str(run_id))' in source
    assert 'remote_terminal_confirmed=worker_terminal_confirmed' in source


def test_quarantine_recovery_requires_persisted_run_id_and_confirmed_completion(monkeypatch, tmp_path):
    import time
    from mediahub_runtime.agent_fabric import AgentClaim, ClaimStore

    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "claims")
    store = ClaimStore(autonomous_queue.CLAIMS)
    claim = AgentClaim("builder", "TASK-1", "test", ("src/a.py",), (), (), "ACTIVE", time.time(), time.time(), time.time() + 1000, "base", command_id="CMD-1", node_id="mh-dev-01", executor="claude")
    store.acquire(claim)
    store.quarantine("TASK-1", "unknown")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"PATH": "/bin"})
    view_stdout = '{"status":"in_progress","conclusion":null,"displayTitle":"Astra distributed worker / CMD-1 / TASK-1 / mh-dev-01 / claude"}'

    class Result:
        returncode = 0
        stdout = ""

    def fake_run(argv, *args, **kwargs):
        if argv[1:3] == ["run", "list"]:
            return ResultWith('[]')
        return ResultWith(view_stdout)

    class ResultWith:
        returncode = 0
        def __init__(self, stdout):
            self.stdout = stdout

    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    missing_run = autonomous_queue.recover_quarantined_claim("TASK-1")
    assert missing_run["error"] == "quarantined_claim_run_not_found"
    assert store.get_claim("TASK-1").status == "QUARANTINED"

    store.set_worker_run_id("TASK-1", "123456")
    nonterminal = autonomous_queue.recover_quarantined_claim("TASK-1")
    assert nonterminal["error"] == "remote_worker_not_terminal"
    assert store.get_claim("TASK-1").status == "QUARANTINED"
    view_stdout = '{"status":"completed","conclusion":"cancelled","displayTitle":"unrelated workflow"}'
    mismatch = autonomous_queue.recover_quarantined_claim("TASK-1")
    assert mismatch["error"] == "remote_worker_identity_mismatch"
    assert store.get_claim("TASK-1").status == "QUARANTINED"
    view_stdout = '{"status":"completed","conclusion":"cancelled","displayTitle":"Astra distributed worker / CMD-1 / TASK-1 / mh-dev-01 / claude"}'
    recovered = autonomous_queue.recover_quarantined_claim("TASK-1")
    assert recovered["status"] == "RECOVERED"
    assert store.get_claim("TASK-1").status == "REJECTED"


def test_quarantine_recovery_discovers_exact_run_without_releasing_active_claim(monkeypatch, tmp_path):
    import time
    from mediahub_runtime.agent_fabric import AgentClaim, ClaimStore

    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "claims")
    store = ClaimStore(autonomous_queue.CLAIMS)
    title = "Astra distributed worker / CMD-2 / TASK-2 / mh-dev-01 / claude"
    claim = AgentClaim("builder", "TASK-2", "test", ("src/b.py",), (), (), "ACTIVE", time.time(), time.time(), time.time() + 1000, "base", command_id="CMD-2", node_id="mh-dev-01", executor="claude")
    store.acquire(claim)
    store.quarantine("TASK-2", "dispatch_response_lost")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"PATH": "/bin"})
    view_stdout = '{"status":"in_progress","conclusion":null,"displayTitle":"' + title + '"}'

    class Result:
        returncode = 0
        def __init__(self, stdout):
            self.stdout = stdout

    def fake_run(argv, *args, **kwargs):
        if argv[1:3] == ["run", "list"]:
            return Result('[{"databaseId":765432,"displayTitle":"' + title + '","status":"in_progress","createdAt":"2099-01-01T00:00:00Z"}]')
        return Result(view_stdout)

    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    active = autonomous_queue.recover_quarantined_claim("TASK-2")
    assert active["error"] == "remote_worker_not_terminal"
    assert active["worker_status"] == "in_progress"
    assert store.get_claim("TASK-2").worker_run_id == "765432"
    assert store.get_claim("TASK-2").status == "QUARANTINED"

    view_stdout = '{"status":"completed","conclusion":"failure","displayTitle":"' + title + '"}'
    recovered = autonomous_queue.recover_quarantined_claim("TASK-2")
    assert recovered["status"] == "RECOVERED"
    assert recovered["worker_run_id"] == "765432"
    assert store.get_claim("TASK-2").status == "REJECTED"


def test_quarantine_recovery_refuses_ambiguous_exact_runs(monkeypatch, tmp_path):
    import time
    from mediahub_runtime.agent_fabric import AgentClaim, ClaimStore

    monkeypatch.setattr(autonomous_queue, "CLAIMS", tmp_path / "claims")
    store = ClaimStore(autonomous_queue.CLAIMS)
    title = "Astra distributed worker / CMD-3 / TASK-3 / mh-dev-01 / claude"
    claim = AgentClaim("builder", "TASK-3", "test", ("src/c.py",), (), (), "ACTIVE", time.time(), time.time(), time.time() + 1000, "base", command_id="CMD-3", node_id="mh-dev-01", executor="claude")
    store.acquire(claim)
    store.quarantine("TASK-3", "ambiguous")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"PATH": "/bin"})

    class Result:
        returncode = 0
        stdout = '[{"databaseId":1,"displayTitle":"' + title + '","createdAt":"2099-01-01T00:00:00Z"},{"databaseId":2,"displayTitle":"' + title + '","createdAt":"2099-01-01T00:00:00Z"}]'

    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: Result())
    result = autonomous_queue.recover_quarantined_claim("TASK-3")
    assert result["error"] == "quarantined_claim_run_ambiguous"
    assert store.get_claim("TASK-3").status == "QUARANTINED"
    assert not store.get_claim("TASK-3").worker_run_id


def test_completion_marker_is_not_authoritative_until_claim_release_finishes(monkeypatch, tmp_path):
    import json
    path = tmp_path / "completed" / "TASK-1.json"
    payload = {"status": "FINALIZING", "base_sha": "a" * 40}
    autonomous_queue.persist_json_atomic(path, payload)
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path)
    assert not autonomous_queue.completed("TASK-1", "a" * 40)
    assert not autonomous_queue.completed("TASK-1")
    assert json.loads(path.read_text(encoding="utf-8"))["status"] == "FINALIZING"
    autonomous_queue.persist_json_atomic(path, {**payload, "status": "BLOCKED"})
    assert not autonomous_queue.completed("TASK-1")
    autonomous_queue.persist_json_atomic(path, {**payload, "status": "VERIFIED"})
    assert autonomous_queue.completed("TASK-1", "a" * 40)
    assert autonomous_queue.completed("TASK-1")
    assert list(path.parent.glob("*.tmp")) == []


def test_completion_marker_uses_atomic_durable_writer():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert '"status": "FINALIZING"' in source
    assert 'persist_json_atomic(completed_path, record)' in source
    assert 'os.fsync(handle.fileno())' in source
    assert 'os.fsync(directory_fd)' in source


def test_failed_completion_promotion_rewrites_finalizing_as_blocked():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    promotion = source.index('persist_json_atomic(completed_path, record)')
    fallback = source.index('if record["status"] != "VERIFIED" and record.get("worker_run_id")', promotion)
    return_stmt = source.index('    return record', fallback)
    assert promotion < fallback < return_stmt
    assert 'record["status"] = "BLOCKED"' in source[promotion:fallback]
    assert 'persist_json_atomic(STATE / "completed" / f"{task_key}.json", record)' in source[fallback:return_stmt]



def test_final_completion_promotion_failure_rewrites_marker_and_rejects_claim(monkeypatch, tmp_path):
    import json
    state = tmp_path / "state"
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    marker = completed_dir / "TASK-1.json"
    marker.write_text(json.dumps({"status": "FINALIZING", "base_sha": "a" * 40}))
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    original_writer = autonomous_queue.persist_json_atomic
    calls = []

    def fail_verified_once(path, payload):
        calls.append((path, payload.get("status")))
        if payload.get("status") == "VERIFIED":
            raise OSError("simulated promotion write failure")
        return original_writer(path, payload)

    class Store:
        released = []
        def release(self, task_id, status, *, remote_terminal_confirmed=False):
            self.released.append((task_id, status, remote_terminal_confirmed))

    store = Store()
    monkeypatch.setattr(autonomous_queue, "persist_json_atomic", fail_verified_once)
    result = autonomous_queue._persist_final_completion(
        {"task_id": "TASK-1", "status": "VERIFIED", "worker_run_id": 123, "base_sha": "a" * 40},
        store,
        "TASK-1",
    )
    assert result["status"] == "BLOCKED"
    assert result["error"].startswith("CompletionPersistError:")
    assert json.loads(marker.read_text())["status"] == "BLOCKED"
    assert store.released == [("TASK-1", "REJECTED", True)]
    assert calls == [(marker, "VERIFIED"), (marker, "BLOCKED")]
    assert not autonomous_queue.completed("TASK-1", "a" * 40)


def test_final_completion_release_failure_is_recorded_and_blocked_marker_persisted(monkeypatch, tmp_path):
    import json
    state = tmp_path / "state"
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    marker = completed_dir / "TASK-1.json"
    marker.write_text(json.dumps({"status": "FINALIZING", "base_sha": "a" * 40}))
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    original_writer = autonomous_queue.persist_json_atomic

    def fail_verified_once(path, payload):
        if payload.get("status") == "VERIFIED":
            raise OSError("simulated promotion write failure")
        return original_writer(path, payload)

    class Store:
        def release(self, task_id, status, *, remote_terminal_confirmed=False):
            raise RuntimeError("simulated claim release failure")

    monkeypatch.setattr(autonomous_queue, "persist_json_atomic", fail_verified_once)
    result = autonomous_queue._persist_final_completion(
        {"task_id": "TASK-1", "status": "VERIFIED", "worker_run_id": 123, "base_sha": "a" * 40},
        Store(),
        "TASK-1",
    )
    assert result["status"] == "BLOCKED"
    assert "simulated claim release failure" in result["completion_claim_release_error"]
    assert json.loads(marker.read_text())["status"] == "BLOCKED"
    assert not autonomous_queue.completed("TASK-1")


def test_final_completion_persistence_remains_blocked_if_storage_stays_unavailable(monkeypatch, tmp_path):
    import json
    state = tmp_path / "state"
    completed_dir = state / "completed"
    completed_dir.mkdir(parents=True)
    marker = completed_dir / "TASK-1.json"
    marker.write_text(json.dumps({"status": "FINALIZING", "base_sha": "a" * 40}))
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    calls = []

    def fail_all_writes(path, payload):
        calls.append(payload.get("status"))
        raise OSError("simulated persistent storage failure")

    class Store:
        def release(self, task_id, status, *, remote_terminal_confirmed=False):
            pass

    monkeypatch.setattr(autonomous_queue, "persist_json_atomic", fail_all_writes)
    result = autonomous_queue._persist_final_completion(
        {"task_id": "TASK-1", "status": "VERIFIED", "worker_run_id": 123, "base_sha": "a" * 40},
        Store(),
        "TASK-1",
    )
    assert result["status"] == "BLOCKED"
    assert result["completion_persist_error"].startswith("OSError:")
    assert calls == ["VERIFIED", "BLOCKED"]
    # Storage failure prevents replacing FINALIZING; completed() must still fail closed.
    assert json.loads(marker.read_text())["status"] == "FINALIZING"
    assert not autonomous_queue.completed("TASK-1")


def test_quarantine_recovery_run_discovery_excludes_same_title_runs_before_claim_start():
    title = "Astra distributed worker / CMD-4 / TASK-4 / mh-dev-01 / claude"
    rows = [
        {"databaseId": 101, "displayTitle": title, "createdAt": "2026-10-10T10:00:00Z"},
        {"databaseId": 102, "displayTitle": title, "createdAt": "2026-10-10T10:05:01Z"},
        {"databaseId": 103, "displayTitle": title, "createdAt": "not-a-timestamp"},
        {"databaseId": 104, "displayTitle": "Astra distributed worker / CMD-4 / TASK-X / mh-dev-01 / claude", "createdAt": "2026-10-10T10:06:00Z"},
    ]
    matches = autonomous_queue.matching_runs_after_claim_start(
        rows, title, claim_started_at=1791626700.0
    )
    assert [row["databaseId"] for row in matches] == [102]


def test_worker_evidence_digest_matches_canonical_payload():
    import hashlib
    payload = {"schema": "mediahub.astra.distributed-local-worker.v1", "status": "PASS", "task_id": "T1"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["evidence_digest"] = "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()
    assert autonomous_queue.worker_evidence_digest_matches(payload)
    changed = dict(payload)
    changed["status"] = "BLOCKED"
    assert not autonomous_queue.worker_evidence_digest_matches(changed)
    assert not autonomous_queue.worker_evidence_digest_matches({"status": "PASS", "evidence_digest": "sha256:bad"})


def test_remote_verifier_result_must_be_an_independent_pass():
    passed = {"verifier": {"returncode": 0, "stdout": "ASTRA_VERDICT: PASS\n"}}
    assert autonomous_queue.remote_verifier_result_passed(passed)
    assert not autonomous_queue.remote_verifier_result_passed({"verifier": {"returncode": 1, "stdout": "ASTRA_VERDICT: PASS\n"}})
    assert not autonomous_queue.remote_verifier_result_passed({"verifier": {"returncode": 0, "stdout": "ASTRA_VERDICT: BLOCKED\n"}})
    assert not autonomous_queue.remote_verifier_result_passed({})


def test_remote_worker_conclusion_is_required_to_be_success():
    assert autonomous_queue.remote_worker_conclusion_passed("completed", "success")
    assert not autonomous_queue.remote_worker_conclusion_passed("completed", "failure")
    assert not autonomous_queue.remote_worker_conclusion_passed("completed", "cancelled")
    assert not autonomous_queue.remote_worker_conclusion_passed("in_progress", "success")


def test_worker_workflow_ref_follows_current_qualification_branch(monkeypatch):
    monkeypatch.delenv("ASTRA_WORKFLOW_REF", raising=False)
    monkeypatch.setenv("GITHUB_REF_NAME", "fix/astra-gold-queue")
    assert autonomous_queue.worker_workflow_ref() == "fix/astra-gold-queue"
    monkeypatch.setenv("ASTRA_WORKFLOW_REF", "main")
    assert autonomous_queue.worker_workflow_ref() == "main"


def test_worker_workflow_ref_rejects_unsafe_refs(monkeypatch):
    monkeypatch.delenv("GITHUB_REF_NAME", raising=False)
    for value in ("", "../main", "-main", "main\\bad", "main..test", "feature//nested", "x" * 256):
        monkeypatch.setenv("ASTRA_WORKFLOW_REF", value)
        try:
            autonomous_queue.worker_workflow_ref()
        except ValueError as exc:
            assert str(exc) == "invalid_worker_workflow_ref"
        else:
            raise AssertionError(f"unsafe workflow ref accepted: {value!r}")


def test_active_controller_preflight_ignores_current_run_only(monkeypatch):
    class Result:
        returncode = 0
        stdout = json.dumps([{"databaseId": 123, "status": "in_progress", "headSha": "a" * 40}])
        stderr = ""
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"GH_TOKEN": "test"})
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: Result())
    assert autonomous_queue.active_controller_preflight() is None


def test_active_controller_preflight_blocks_other_active_run(monkeypatch):
    class Result:
        returncode = 0
        stdout = json.dumps([
            {"databaseId": 123, "status": "in_progress"},
            {"databaseId": 456, "status": "queued"},
            {"databaseId": 789, "status": "completed"},
        ])
        stderr = ""
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"GH_TOKEN": "test"})
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: Result())
    result = autonomous_queue.active_controller_preflight()
    assert result == {"status": "BLOCKED", "reason": "another_supervisor_run_active", "blocking_run_ids": [456]}


def test_active_controller_preflight_fails_closed_on_transport_or_invalid_payload(monkeypatch):
    class Failure:
        returncode = 1
        stdout = ""
        stderr = "transport unavailable"
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("GITHUB_RUN_ID", "123")
    monkeypatch.setattr(autonomous_queue, "github_auth_env", lambda: {"GH_TOKEN": "test"})
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: Failure())
    assert autonomous_queue.active_controller_preflight()["reason"] == "controller_concurrency_query_failed"
    class Invalid:
        returncode = 0
        stdout = "not-json"
        stderr = ""
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: Invalid())
    assert autonomous_queue.active_controller_preflight()["reason"] == "controller_concurrency_query_invalid"


def test_wait_for_controller_slot_retries_only_active_run_blocker(monkeypatch):
    answers = iter([
        {"status": "BLOCKED", "reason": "another_supervisor_run_active", "blocking_run_ids": [456]},
        None,
    ])
    sleeps = []
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("ASTRA_CONTROLLER_CONCURRENCY_WAIT_SECONDS", "120")
    monkeypatch.setenv("ASTRA_CONTROLLER_CONCURRENCY_POLL_SECONDS", "30")
    monkeypatch.setattr(autonomous_queue, "active_controller_preflight", lambda: next(answers))
    monkeypatch.setattr(autonomous_queue.time, "sleep", lambda seconds: sleeps.append(seconds))
    assert autonomous_queue.wait_for_controller_slot() is None
    assert sleeps == [30.0]


def test_wait_for_controller_slot_fails_closed_on_api_error(monkeypatch):
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("ASTRA_CONTROLLER_CONCURRENCY_WAIT_SECONDS", "120")
    monkeypatch.setattr(autonomous_queue, "active_controller_preflight", lambda: {
        "status": "BLOCKED", "reason": "controller_concurrency_query_failed"
    })
    monkeypatch.setattr(autonomous_queue.time, "sleep", lambda *_: (_ for _ in ()).throw(
        AssertionError("must not retry when active run discovery failed")))
    assert autonomous_queue.wait_for_controller_slot()["reason"] == "controller_concurrency_query_failed"


def test_wait_for_controller_slot_times_out_with_active_run_identity(monkeypatch):
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "1")
    monkeypatch.setenv("ASTRA_CONTROLLER_CONCURRENCY_WAIT_SECONDS", "0")
    monkeypatch.setattr(autonomous_queue, "active_controller_preflight", lambda: {
        "status": "BLOCKED", "reason": "another_supervisor_run_active", "blocking_run_ids": [456]
    })
    assert autonomous_queue.wait_for_controller_slot()["reason"] == "controller_concurrency_wait_timeout"


def test_select_distributed_tasks_excludes_controller_host_lane():
    tasks = [
        {"task_id": "mac", "node_id": "Voktors-Mac-mini.local", "executor": "claude", "priority": "P0"},
        {"task_id": "one", "node_id": "mh-dev-01", "executor": "claude", "priority": "P0"},
        {"task_id": "two", "node_id": "mh-dev-02", "executor": "claude", "priority": "P0"},
    ]
    selected = autonomous_queue.select_distributed_tasks(tasks, 3, excluded_nodes={"Voktors-Mac-mini.local"})
    assert [item["task_id"] for item in selected] == ["one", "two"]


def test_select_distributed_tasks_returns_empty_when_only_controller_lane_is_ready():
    tasks = [{"task_id": "mac", "node_id": "Voktors-Mac-mini.local", "executor": "claude"}]
    assert autonomous_queue.select_distributed_tasks(
        tasks, 3, excluded_nodes={"Voktors-Mac-mini.local"}
    ) == []


def test_main_rejects_unknown_controller_node_before_dispatch(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    (task_dir / "ready.json").write_text(json.dumps({
        "task_id": "ready", "status": "READY", "priority": "P0",
        "node_id": "mh-dev-02", "executor": "claude",
    }), encoding="utf-8")
    state = tmp_path / "state"
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.setattr(autonomous_queue, "queue_state_preflight", lambda: None)
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: type("R", (), {
        "returncode": 0, "stdout": "a" * 40 + "\n", "stderr": ""
    })())
    monkeypatch.setenv("ASTRA_CONTROLLER_NODE_ID", "unknown-node")
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "0")
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)
    assert autonomous_queue.main() == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["reason"] == "controller_node_identity_invalid"


def test_main_never_passes_when_eligible_ready_tasks_are_omitted(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    tasks = [
        {"task_id": "controller-lane", "status": "READY", "priority": "P0",
         "node_id": "mh-dev-01", "executor": "claude"},
        {"task_id": "remote-lane", "status": "READY", "priority": "P1",
         "node_id": "mh-dev-02", "executor": "claude"},
    ]
    for task in tasks:
        (task_dir / f"{task['task_id']}.json").write_text(json.dumps(task), encoding="utf-8")

    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "queue_state_preflight", lambda: None)
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: type("R", (), {
        "returncode": 0, "stdout": "a" * 40 + "\n", "stderr": ""
    })())
    monkeypatch.setattr(autonomous_queue, "process_task_remote", lambda task, sha: {
        "task_id": task["task_id"], "status": "VERIFIED"
    })
    monkeypatch.setenv("ASTRA_CONTROLLER_NODE_ID", "mh-dev-01")
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "0")
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)

    assert autonomous_queue.main() == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "BLOCKED"
    assert payload["reason"] == "eligible_ready_tasks_unprocessed"
    assert payload["selected_tasks"] == ["remote-lane"]
    assert payload["pending_tasks"] == ["controller-lane"]



def test_main_blocks_ready_task_with_noncanonical_executor(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    tasks = [
        {"task_id": "codex-lane", "status": "READY", "priority": "P0",
         "node_id": "mh-dev-02", "executor": "codex"},
        {"task_id": "claude-lane", "status": "READY", "priority": "P1",
         "node_id": "mh-dev-01", "executor": "claude"},
    ]
    for task in tasks:
        (task_dir / f"{task['task_id']}.json").write_text(json.dumps(task), encoding="utf-8")

    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "queue_state_preflight", lambda: None)
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: type("R", (), {
        "returncode": 0, "stdout": "a" * 40 + "\n", "stderr": ""
    })())
    monkeypatch.setattr(autonomous_queue, "process_task_remote", lambda task, sha: {
        "task_id": task["task_id"], "status": "VERIFIED"
    })
    monkeypatch.delenv("ASTRA_CONTROLLER_NODE_ID", raising=False)
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "0")
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)

    assert autonomous_queue.main() == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "BLOCKED"
    assert payload["reason"] == "unroutable_ready_tasks"
    assert payload["pending_tasks"] == ["codex-lane"]
    assert payload["unroutable_tasks"] == ["codex-lane"]


def test_main_blocks_ready_tasks_with_unsatisfied_dependencies(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    (task_dir / "dependent.json").write_text(json.dumps({
        "task_id": "dependent", "status": "READY", "priority": "P0",
        "node_id": "mh-dev-02", "executor": "claude", "dependencies": ["missing-dependency"],
    }), encoding="utf-8")
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    monkeypatch.setattr(autonomous_queue, "queue_state_preflight", lambda: None)
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: type("R", (), {
        "returncode": 0, "stdout": "a" * 40 + "\n", "stderr": ""
    })())
    monkeypatch.setenv("ASTRA_CONTROLLER_NODE_ID", "mh-dev-01")
    monkeypatch.setenv("ASTRA_SINGLE_CONTROLLER_RUN", "0")
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)

    assert autonomous_queue.main() == 2
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "BLOCKED"
    assert payload["reason"] == "ready_tasks_blocked_by_dependencies"
    assert payload["pending_tasks"] == ["dependent"]
    assert payload["dependency_blocked_tasks"] == ["dependent"]
