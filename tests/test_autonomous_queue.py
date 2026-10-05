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
    (state / "completed" / "A.json").write_text("{}")
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
    assert payload == {"reason":"no_ready_tasks","status":"IDLE"}


def test_claim_uses_task_boundary(monkeypatch):
    class R: stdout = "abc123\n"
    monkeypatch.setattr(autonomous_queue, "run", lambda *a, **k: R())
    claim = autonomous_queue.claim_for({"task_id":"T1","mission":"m","boundary":["docs/a","ops/b"]})
    assert claim.base_sha == "abc123"
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
    assert payload["selected_tasks"] == ["A"]


def test_controller_claim_requires_explicit_success_status():
    source = Path(__file__).resolve().parents[1] / "astra_github_agent.py".read_text(encoding="utf-8")
    assert 'claim_status = "VERIFIED" if rc == 0 and result_status in {"PASS", "ready"} else "REJECTED"' in source
