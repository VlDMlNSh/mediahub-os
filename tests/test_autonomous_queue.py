import json
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


def test_boundary_allows_normalized_paths():
    assert autonomous_queue.boundary_allows("./docs/a.txt", ("docs/a",))
    assert autonomous_queue.boundary_allows("docs/a/b.txt", ("docs/a",))
    assert not autonomous_queue.boundary_allows("docs/ab.txt", ("docs/a",))
    assert not autonomous_queue.boundary_allows("runtime/x.py", ("docs/a",))
