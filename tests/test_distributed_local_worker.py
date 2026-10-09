from __future__ import annotations

import json
import subprocess
from pathlib import Path
from unittest import mock

from ops.qualification import run_distributed_local_worker as worker


def test_remaining_budget_is_nonnegative_and_uses_one_monotonic_deadline():
    assert worker.remaining_budget(100.0, now=90.0) == 10
    assert worker.remaining_budget(100.0, now=100.0) == 0
    assert worker.remaining_budget(100.0, now=120.0) == 0


def test_exec_claude_converts_process_timeout_to_bounded_evidence(tmp_path: Path):
    model = "qwen2.5-coder:3b"
    env_file = tmp_path / "fcc.env"
    auth_name = "ANTHROPIC_AUTH" + "_TOKEN"
    env_file.write_text(
        "\n".join((
            "MODEL=ollama/" + model,
            "HOST=127.0.0.1",
            "PORT=8093",
            auth_name + "=x",
        )) + "\n",
        encoding="utf-8",
    )

    class HealthResponse:
        status = 200
        def __enter__(self):
            return self
        def __exit__(self, *_args):
            return False

    with (
        mock.patch.object(worker.urllib.request, "urlopen", return_value=HealthResponse()),
        mock.patch.object(worker.shutil, "which", return_value="/usr/bin/claude"),
        mock.patch.object(
            worker,
            "run",
            side_effect=subprocess.TimeoutExpired(
                cmd=["claude"], timeout=1, output="partial-output", stderr="model-timeout"
            ),
        ),
    ):
        result, server = worker.exec_claude(
            "small bounded test prompt", model, 1, env_file, max_turns=1
        )

    assert result["returncode"] == 124
    assert result["stdout"] == "partial-output"
    assert "claude_execution_timeout" in result["stderr"]
    assert "model-timeout" in result["stderr"]
    assert server is None


def test_builder_attempts_share_one_total_deadline():
    source = Path(worker.__file__).read_text(encoding="utf-8")
    assert "builder_deadline = time.monotonic() + builder_budget_seconds" in source
    assert "attempt_timeout = remaining_budget(builder_deadline)" in source
    assert "artifact_timeout = remaining_budget(builder_deadline)" in source


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


def test_23wave_codex_candidate_qualification_is_read_only():
    workflow = Path(".github/workflows/mh25-dual-local-23wave.yml").read_text(encoding="utf-8")
    assert "--sandbox read-only" in workflow
    assert "--sandbox workspace-write" not in workflow
    assert "--sandbox danger-full-access" not in workflow


def test_canonical_distributed_worker_has_no_codex_execution_path():
    source = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert "def exec_codex(" not in source
    assert 'if verifier == "codex"' not in source
    assert 'permanent_verifier_policy_violation' in source


def test_distributed_selection_rejects_codex_from_permanent_pool():
    tasks = [
        {"task_id": "codex-a", "priority": "P0", "node_id": "mh-dev-02", "executor": "codex"},
        {"task_id": "codex-b", "priority": "P0", "node_id": "mh-dev-02", "executor": "codex"},
        {"task_id": "claude-mh1", "priority": "P0", "node_id": "mh-dev-01", "executor": "claude"},
        {"task_id": "claude-mac", "priority": "P1", "node_id": "Voktors-Mac-mini.local", "executor": "claude"},
    ]
    selected = __import__("mediahub_runtime.autonomous_queue", fromlist=["select_distributed_tasks"]).select_distributed_tasks(tasks, 3)
    assert [t["task_id"] for t in selected] == ["claude-mh1", "claude-mac"]
    assert all(t["executor"] == "claude" for t in selected)
    assert len({t["node_id"] for t in selected}) == len(selected)
