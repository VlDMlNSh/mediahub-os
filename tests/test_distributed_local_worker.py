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
        "mh-dev-02", "mh-dev-01", "Voktors-Mac-mini.local"
    ]
    assert tasks[0]["deterministic_checks"]["required_patterns"]
    assert tasks[2]["deliverable"] == "docs/operations/ASTRA-VOKTORS-MAC-CLAUDE-EXECUTOR.md"
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


def test_23wave_legacy_codex_qualification_remains_read_only():
    workflow = Path(".github/workflows/mh25-dual-local-23wave.yml").read_text(encoding="utf-8")
    assert "--sandbox read-only" in workflow
    assert "--sandbox danger-full-access" not in workflow


def test_codex_worker_disables_reasoning_for_local_models():
    worker = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
    assert 'model_reasoning_effort = "none"' in worker


def test_distributed_selection_allows_three_claude_claims_on_distinct_nodes():
    tasks = [
        {"task_id": "claude-mh1", "priority": "P0", "node_id": "mh-dev-01", "executor": "claude"},
        {"task_id": "duplicate-mh1", "priority": "P0", "node_id": "mh-dev-01", "executor": "claude"},
        {"task_id": "claude-mac", "priority": "P1", "node_id": "Voktors-Mac-mini.local", "executor": "claude"},
        {"task_id": "claude-mh2", "priority": "P2", "node_id": "mh-dev-02", "executor": "claude"},
    ]
    selected = __import__("mediahub_runtime.autonomous_queue", fromlist=["select_distributed_tasks"]).select_distributed_tasks(tasks, 3)
    assert [t["task_id"] for t in selected] == ["claude-mh1", "claude-mac", "claude-mh2"]
    assert len({t["node_id"] for t in selected}) == len(selected) == 3
    assert {t["executor"] for t in selected} == {"claude"}


def test_verifier_verdict_requires_standalone_canonical_line():
    assert worker.parse_verifier_verdict("ASTRA_VERDICT: PASS") == "PASS"
    assert worker.parse_verifier_verdict("**ASTRA_VERDICT: PASS**") == "PASS"
    assert worker.parse_verifier_verdict("ASTRA_VERDICT: BLOCKED") == "BLOCKED"
    assert worker.parse_verifier_verdict("Here is my review: ASTRA_VERDICT: PASS") is None
    assert worker.parse_verifier_verdict("**ASTRA_VERDICT: PASS**\n### Verification") is None


def test_deterministic_acceptance_blocks_incorrect_lane_mapping():
    task = {
        "boundary": ["docs/operations/topology.md"],
        "deliverable": "docs/operations/topology.md",
        "deterministic_checks": {
            "required_patterns": [
                r"(?im)^.*mh-dev-01.*controller/authority.*$",
                r"(?im)^.*mh-dev-02.*primary local pool.*$",
                r"(?im)^.*Voktors-Mac-mini\.local.*fast pool.*$",
            ],
            "forbidden_patterns": [],
            "required_text": ["fail-closed"],
        },
    }
    with __import__("tempfile").TemporaryDirectory() as td:
        root = Path(td)
        target = root / "docs/operations/topology.md"
        target.parent.mkdir(parents=True)
        target.write_text(
            "- mh-dev-01\n  - Primary local pool\n"
            "- mh-dev-02\n  - Fast pool\n"
            "- Voktors-Mac-mini.local\n  - Fast pool\n"
            "fail-closed\n",
            encoding="utf-8",
        )
        from unittest import mock
        with mock.patch.object(worker, "ROOT", root):
            result = worker.deterministic_acceptance(task)
    assert result["status"] == "BLOCKED"
    assert any("controller/authority" in item for item in result["failures"])
    assert any("primary local pool" in item for item in result["failures"])


def test_security_gate_detects_secret_assignment_patterns():
    with __import__("tempfile").TemporaryDirectory() as td:
        root = Path(td)
        target = root / "docs/operations/secret.md"
        target.parent.mkdir(parents=True)
        fake_value = "0123456789abcdef" + "012345"
        target.write_text(("api" + "_key = ") + repr(fake_value) + chr(10), encoding="utf-8")
        from unittest import mock
        with mock.patch.object(worker, "ROOT", root):
            findings = worker.security_gate({"docs/operations/secret.md"}, {"boundary": ["docs/operations/"]})
    assert any("possible_secret" in finding for finding in findings)


def test_deterministic_acceptance_accepts_canonical_topology_contract():
    task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
    document = """# Permanent Claude executor topology
- mh-dev-01: Controller/Authority
- mh-dev-02: Primary Local Pool
- Voktors-Mac-mini.local: Fast Pool

Claude uses an A2 Builder and independent A3 Verifier. Exact target-SHA binding is enforced.
Each worker uses isolated branches. GitHub evidence transport is required.
Promotion is fail-closed. There are no direct writes to main.
G5=3: three simultaneous disjoint claims, one per permanent executor lane.
The production executor matrix contains exactly three Claude lanes.
Legacy and candidate execution surfaces are not permanent queue executors.
No credentials or secrets are included.
"""
    with __import__("tempfile").TemporaryDirectory() as td:
        root = Path(td)
        target = root / task["deliverable"]
        target.parent.mkdir(parents=True)
        target.write_text(document, encoding="utf-8")
        from unittest import mock
        with mock.patch.object(worker, "ROOT", root):
            result = worker.deterministic_acceptance(task)
    assert result["status"] == "PASS", result["failures"]
    assert result["checks_run"] >= 15


def test_builder_prompt_exposes_deterministic_acceptance_contract():
    task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
    import os
    from unittest import mock
    with mock.patch.dict(os.environ, {"ASTRA_TARGET_SHA": "a" * 40}):
        prompt = worker.task_prompt(task, "A2 Builder")
    assert "Deterministic acceptance checks" in prompt
    assert "mh-dev-01: Controller/Authority" in prompt
    assert "mh-dev-02: Primary Local Pool" in prompt
    assert "G5=3" in prompt
