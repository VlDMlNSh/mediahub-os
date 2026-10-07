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
    assert worker.NODE_CONFIG["Voktors-Mini.Dlink"]["pool"] == "fast_local"
    assert worker.NODE_CONFIG["Voktors-Mini.Dlink"]["model"] == "qwen2.5-coder:1.5b"


def test_evidence_redaction_suppresses_known_credentials(monkeypatch):
    monkeypatch.setenv("GH_TOKEN", "SECRET_GH_TOKEN")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "SECRET_ANTHROPIC")
    redacted = worker.redact_evidence_text("x SECRET_GH_TOKEN y SECRET_ANTHROPIC z")
    assert "SECRET_GH_TOKEN" not in redacted
    assert "SECRET_ANTHROPIC" not in redacted
    assert redacted.count("SUPPRESSED") == 2


def test_canonical_three_ready_tasks_have_disjoint_boundaries():
    task_ids = ["MH25-QUEUE-002", "MH25-QUEUE-003", "MH25-QUEUE-004"]
    tasks = []
    for task_id in task_ids:
        tasks.append(json.loads(
            Path(f"ops/agent-fabric/tasks/{task_id}.json").read_text(encoding="utf-8")
        ))
    boundaries = [tuple(t["boundary"]) for t in tasks]
    assert len({b[0] for b in boundaries}) == 3
    assert tasks[0]["executor"] == "claude" and tasks[0]["node_id"] == "Voktors-Mac-mini.local"
    assert tasks[1]["executor"] == "claude" and tasks[1]["node_id"] == "mh-dev-01"
    assert tasks[2]["executor"] == "codex" and tasks[2]["node_id"] == "mh-dev-02"
