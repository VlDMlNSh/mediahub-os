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
    (task_dir / "a.json").write_text(json.dumps({"task_id":"A","status":"READY","priority":"P0"}))
    (state / "completed").mkdir(parents=True)
    (state / "completed" / "A.json").write_text(\n        json.dumps({"status": "VERIFIED", "base_sha": "deadbeef"}),\n        encoding="utf-8",\n    )
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    assert autonomous_queue.main() == 0
    assert json.loads(capsys.readouterr().out)["status"] == "IDLE"


def test_main_returns_idle_when_no_ready_tasks(monkeypatch, tmp_path: Path, capsys):
    task_dir = tmp_path / "tasks"; task_dir.mkdir()
    state = tmp_path / "state"
    (task_dir / "a.json").write_text(json.dumps({"task_id":"A","status":"WAIT","priority":"P0"}))
    monkeypatch.setattr(autonomous_queue, "TASK_DIR", task_dir)
    monkeypatch.setattr(autonomous_queue, "STATE", state)
    assert autonomous_queue.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "IDLE"\n    assert payload["reason"] == "no_ready_tasks"\n    assert payload["base_sha"] == autonomous_queue.run(["git", "rev-parse", "HEAD"], 30).stdout.strip()\n    assert payload["discovered_tasks"] == []


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


def test_max_workers_is_bounded_by_three():
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
    class R:
        stdout = "newsha\n"
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    # No builder should be started here; the stale completion makes the task eligible.
    result = autonomous_queue.main()
    payload = json.loads(capsys.readouterr().out)
    assert result == 2
    assert payload["status"] == "BLOCKED"
    assert payload["selected_tasks"] == ["A"]\n    assert payload["results"][0]["task_id"] == "A"



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



def test_task_id_cannot_escape_queue_state(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(autonomous_queue, "STATE", tmp_path / "state")
    for bad in ("../escape", "a/b", "", "a b"):
        try:
            autonomous_queue.worktree_path(bad)
        except ValueError as exc:
            assert str(exc) == "invalid_task_id"
        else:
            raise AssertionError("unsafe task id must be rejected")


def test_queue_verifies_remote_push_sha():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert '"git", "ls-remote", "origin", f"refs/heads/{branch}"' in source
    assert 'raise RuntimeError("git_push_sha_mismatch")' in source
    assert '"push_verification": {' in source


def test_queue_blocks_existing_remote_branch_before_worktree_creation():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'raise RuntimeError("queue_branch_already_exists")' in source
    assert 'raise RuntimeError("queue_branch_probe_failed")' in source


def test_local_executor_contract_uses_qualified_ollama_marker_and_provider():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert "MEDIAHUB_LOCAL_EXECUTOR_QUALIFICATION_OK" in source
    assert '"--profile", "huggingface"' not in source
    assert 'if "MEDIAHUB_LOCAL_EXECUTOR_QUALIFICATION_OK" in output' in source
    assert 'preferred = ("qwen2.5-coder:3b", "qwen2.5-coder-3b:latest")' in source


def test_queue_pins_workers_to_explicit_target_sha():
    source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
    assert 'ASTRA_TARGET_SHA' in source
    assert 'queue_target_sha_not_current_head' in source
    assert 'def claim_for(task: dict, base_sha: str)' in source
    assert 'raise RuntimeError("queue_base_sha_not_current_head")' in source

