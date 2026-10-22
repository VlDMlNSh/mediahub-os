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
        if argv[:3] == ["git", "status", "--porcelain", "--untracked-files=all"]:
            class S:
                returncode = 0
                stdout = "?? forbidden.txt\n"
                stderr = ""
            return S()
        return R()
    monkeypatch.setattr(autonomous_queue, "run", fake_run)
    assert autonomous_queue._diff_outside_scope({"boundary": ["tests"]}, worktree, "a"*40) == ["forbidden.txt"]


def test_scope_check_rejects_untracked_files(monkeypatch, tmp_path: Path):
    worktree = tmp_path / "worktree"
    worktree.mkdir()
    class R:
        returncode = 0
        stdout = ""
        stderr = ""
    monkeypatch.setattr(
        autonomous_queue,
        "run",
        lambda argv, *args, **kwargs: R(),
    )
    # The implementation must inspect untracked files through git status; this
    # sentinel path is intentionally outside the task boundary.
    original = autonomous_queue.run
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
    assert 'def claim_for(task: dict, base_sha: str)' in source
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
    assert 'builder_attempts = max(1, min(int(task.get("builder_attempts", 2)), 3))' in worker
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

def test_autonomous_queue_switches_to_next_task_after_verified_completion(
    monkeypatch, tmp_path: Path, capsys
):
    """Exercise two real queue cycles with a deterministic remote-worker double."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    state = tmp_path / "state"
    target = "c" * 40
    common = {
        "status": "READY",
        "priority": "P0",
        "node_id": "Voktors-Mac-mini.local",
        "executor": "claude",
        "verifier": "claude",
        "independent_verifier_process": True,
        "boundary": ["docs/operations"],
        "dependencies": [],
    }
    for task_id in ("QUEUE-A", "QUEUE-B"):
        (task_dir / f"{task_id}.json").write_text(
            json.dumps({**common, "task_id": task_id, "mission": f"Transition test {task_id}"}),
            encoding="utf-8",
        )

    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    monkeypatch.setattr(autonomous_queue, "MAX_WORKERS", 3)
    monkeypatch.delenv("ASTRA_TARGET_SHA", raising=False)

    class Head:
        returncode = 0
        stdout = target + "\\n"
        stderr = ""

    monkeypatch.setattr(autonomous_queue, "run", lambda *args, **kwargs: Head())
    dispatched = []

    def verified_remote_worker(task, base_sha):
        task_id = task["task_id"]
        dispatched.append(task_id)
        completed_dir = state / "completed"
        completed_dir.mkdir(parents=True, exist_ok=True)
        (completed_dir / f"{task_id}.json").write_text(
            json.dumps({"task_id": task_id, "status": "VERIFIED", "base_sha": base_sha}),
            encoding="utf-8",
        )
        return {"task_id": task_id, "status": "VERIFIED", "base_sha": base_sha}

    monkeypatch.setattr(autonomous_queue, "process_task_remote", verified_remote_worker)

    assert autonomous_queue.main() == 0
    first = json.loads(capsys.readouterr().out)
    assert first["status"] == "PASS"
    assert first["selected_tasks"] == ["QUEUE-A"]

    assert autonomous_queue.main() == 0
    second = json.loads(capsys.readouterr().out)
    assert second["status"] == "PASS"
    assert second["selected_tasks"] == ["QUEUE-B"]

    assert autonomous_queue.main() == 0
    third = json.loads(capsys.readouterr().out)
    assert third["status"] == "IDLE"
    assert third["reason"] == "no_ready_tasks"
    assert dispatched == ["QUEUE-A", "QUEUE-B"]
