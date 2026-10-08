from __future__ import annotations

import json
from pathlib import Path

from ops.qualification import run_distributed_local_worker as worker


def test_safe_id_rejects_path_escape():
    for value in ("../x", "a/b", "a b", ""):
        try:
            worker.safe_id(value)
        except RuntimeError:
            pass
        else:
            raise AssertionError(value)


def test_scope_paths_rejects_forbidden_and_outside():
    task = {
        "boundary": ["tests/", "ops/agent-fabric/"],
        "forbidden": ["ops/agent-fabric/secret/"],
    }
    assert worker.scope_paths(task, {"tests/test_ok.py"}) == []
    assert worker.scope_paths(task, {"docs/outside.md"}) == ["docs/outside.md"]
    assert worker.scope_paths(task, {"ops/agent-fabric/secret/x"}) == ["ops/agent-fabric/secret/x"]


def test_node_config_has_primary_and_fast_pools():
    assert worker.NODE_CONFIG["mh-dev-02"]["pool"] == "primary_local"
    assert worker.NODE_CONFIG["mh-dev-02"]["model"] == "qwen2.5-coder:3b"
    assert worker.NODE_CONFIG["Voktors-Mac-mini.local"]["pool"] == "fast_local"
    assert worker.NODE_CONFIG["Voktors-Mac-mini.local"]["model"] == "qwen2.5-coder:1.5b"


def test_canonical_three_executor_tasks_are_ready_and_disjoint():
    task_ids = ["MH25-QUEUE-002", "MH25-QUEUE-003", "MH25-QUEUE-004"]
    tasks = [
        json.loads(Path(f"ops/agent-fabric/tasks/{task_id}.json").read_text(encoding="utf-8"))
        for task_id in task_ids
    ]
    assert [t["executor"] for t in tasks] == ["claude", "claude", "codex"]
    assert [t["node_id"] for t in tasks] == [
        "Voktors-Mac-mini.local", "mh-dev-01", "mh-dev-02"
    ]
    assert all(t["status"] == "READY" for t in tasks)
    assert len({tuple(t["boundary"]) for t in tasks}) == 1
    assert all(t["boundary"] == ["docs/operations/"] for t in tasks)
