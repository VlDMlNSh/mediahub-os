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
    assert [t["executor"] for t in tasks] == ["claude", "claude", "claude"]
    assert [t["node_id"] for t in tasks] == [
        "Voktors-Mac-mini.local", "mh-dev-01", "mh-dev-02"
    ]
    assert all(t["status"] == "READY" for t in tasks)
    assert len({tuple(t["boundary"]) for t in tasks}) == 3
    assert all(len(t["boundary"]) == 1 and t["boundary"][0].startswith("docs/operations/") for t in tasks)


def test_worker_workflow_enforces_claude_only_executor_identity():
    workflow = Path('.github/workflows/astra-distributed-local-worker.yml').read_text(encoding='utf-8')
    assert 'test "${ASTRA_EXECUTOR}" = "claude"' in workflow
    assert 'test "${ASTRA_EXECUTOR}" = "codex"' not in workflow
    assert 'ASTRA_CODEX_SANDBOX_MODE' not in workflow
    assert 'options: [claude]' in workflow


def test_claude_worker_disables_reasoning_for_non_thinking_local_models():
    worker = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert 'env["REASONING_POLICY"] = "off"' in worker
    assert 'env["CLAUDE_CODE_DISABLE_THINKING"] = "1"' in worker
    assert 'env["MAX_THINKING_TOKENS"] = "0"' in worker


def test_claude_worker_uses_isolated_config_directory():
    worker = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert 'env["CLAUDE_CONFIG_DIR"] = isolated_config' in worker
    assert 'tempfile.mkdtemp(prefix="astra-claude-config-")' in worker


def test_23wave_codex_qualification_is_not_unbounded():
    workflow = Path(".github/workflows/mh25-dual-local-23wave.yml").read_text(encoding="utf-8")
    assert "--sandbox workspace-write" in workflow
    assert "--sandbox danger-full-access" not in workflow


def test_codex_worker_disables_reasoning_for_local_models():
    worker = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert 'model_reasoning_effort = "none"' in worker


def test_distributed_selection_allows_one_claim_per_executor_lane():
    tasks = [
        {"task_id": "codex-a", "priority": "P0", "node_id": "mh-dev-02", "executor": "codex"},
        {"task_id": "codex-b", "priority": "P0", "node_id": "mh-dev-02", "executor": "codex"},
        {"task_id": "claude-mh1", "priority": "P0", "node_id": "mh-dev-01", "executor": "claude"},
        {"task_id": "claude-mac", "priority": "P1", "node_id": "Voktors-Mac-mini.local", "executor": "claude"},
    ]
    selected = __import__("mediahub_runtime.autonomous_queue", fromlist=["select_distributed_tasks"]).select_distributed_tasks(tasks, 3)
    assert [t["task_id"] for t in selected] == ["codex-a", "claude-mh1", "claude-mac"]
    assert len({t["node_id"] for t in selected}) == len(selected)
    assert len({t["executor"] for t in selected}) == len(selected)
