import inspect
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_controller_and_watchdog_are_valid_shell():
    for name in ("ops/autonomous_os_loop.sh", "ops/autonomous_watchdog.sh"):
        result = subprocess.run(["bash", "-n", str(ROOT / name)], capture_output=True, text=True, check=False)
        assert result.returncode == 0, result.stderr


def test_autonomous_code_has_no_history_rewrite_commands():
    paths = [ROOT / "ops/autonomous_os_loop.sh", ROOT / "ops/autonomous_watchdog.sh", ROOT / "ops/local_autonomous_agent.py"]
    forbidden = ("git reset", "git rebase", "git commit --amend", "force-push", "--force")
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not any(token in text for token in forbidden), path


def test_controller_requires_r4_clean_baseline_and_ancestor_commit():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert "merge-base --is-ancestor 471f709f5633feab7aeb62dd3ea52effad6d2bc4 HEAD" in text
    assert 'git status --porcelain' in text
    assert 'git merge-base --is-ancestor "$BASE_HEAD" "$POST_HEAD"' in text


def test_agent_does_not_treat_noop_as_success():
    text = (ROOT / "ops/local_autonomous_agent.py").read_text(encoding="utf-8")
    assert "LOCAL_AGENT_NOOP: no admissible downstream change" in text
    assert "return 30" in text
    assert "commit.returncode != 0" in text


def test_watchdog_validates_controller_ownership_before_termination():
    text = (ROOT / "ops/autonomous_watchdog.sh").read_text(encoding="utf-8")
    assert 'owned=0' in text
    assert 'ps -p "$pid" -o args=' in text
    assert 'if [ "$stale" -eq 1 ] && [ "$owned" -eq 1 ]' in text
    assert 'if [ "$owned" -eq 0 ]; then' in text


def test_watchdog_never_replaces_a_controller_that_ignored_graceful_term():
    text = (ROOT / "ops/autonomous_watchdog.sh").read_text(encoding="utf-8")
    assert 'stopped=0' in text
    assert 'stopped=1' in text
    assert 'replacement blocked pid=$pid' in text
    assert 'else\n\t\t\towned=1' in text


def test_agent_runs_deterministic_lint_repair_before_verification():
    text = (ROOT / "ops/local_autonomous_agent.py").read_text(encoding="utf-8")
    assert 'str(RUFF), "check", "--fix"' in text
    assert 'LOCAL_AGENT_BLOCKED: deterministic lint repair failed' in text




def _git_init_with_commit(root: Path) -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)

from ops.local_autonomous_agent import (
    ExecutableTask,
    LocalTask,
    compile_executable_task,
    fallback_patch,
    inspect_queue_encoding,
    safe_patch,
    select_local_task,
    state,
)


def test_local_task_selector_advances_deterministically(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text("P0.4 Close current Native Execution Contract test gaps.\n", encoding="utf-8")
    target = queue / "mediahub_native_execution.py"
    target.write_text("class BoundedExecutionRequest:\n", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.4-bounded-request-types"
    assert task.target == "ops/mediahub_native_execution.py"

    target.write_text("not isinstance(self.timeout_seconds, int)\n", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.4-bounded-request-identity"


def test_local_task_selector_replans_to_next_eligible_level(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.4 Close current Native Execution Contract test gaps.\n"
        "P1.1 Complete provider-neutral ExecutionProposal contract and negative tests.\n",
        encoding="utf-8",
    )
    target = queue / "mediahub_native_execution.py"
    target.write_text(
        "not isinstance(self.timeout_seconds, int)\n"
        "not isinstance(self.proposal, ExecutionProposal)\n"
        "malformed recovery evidence\n"
        "not isinstance(secret, str)\n"
        "malformed execution proposal\n"
        "malformed execution target\n",
        encoding="utf-8",
    )
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_mediahub_native_execution.py").write_text(
        "test_bounded_execution_request_rejects_malformed_object_types\n"
        "test_bounded_execution_request_rejects_non_integer_timeout_types\n"
        "test_bounded_execution_request_rejects_non_integer_output_limit_types\n",
        encoding="utf-8",
    )
    task = select_local_task(tmp_path)
    assert task is not None
    assert task.task_id == "P1.1-native-contract-negative-types"
    assert task.target == "tests/test_mediahub_native_execution.py"


def test_local_task_selector_stops_when_no_local_acceptance_criteria_exist(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.4 Close current Native Execution Contract test gaps.\n"
        "P1.1 Complete provider-neutral ExecutionProposal contract and negative tests.\n",
        encoding="utf-8",
    )
    target = queue / "mediahub_native_execution.py"
    target.write_text(
        "not isinstance(self.timeout_seconds, int)\n"
        "not isinstance(self.proposal, ExecutionProposal)\n"
        "malformed recovery evidence\n"
        "not isinstance(secret, str)\n"
        "malformed execution proposal\n"
        "malformed execution target\n",
        encoding="utf-8",
    )
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_mediahub_native_execution.py").write_text(
        "test_bounded_execution_request_rejects_malformed_object_types\n"
        "test_bounded_execution_request_rejects_non_integer_timeout_types\n"
        "test_bounded_execution_request_rejects_non_integer_output_limit_types\n"
        "test_execution_proposal_rejects_non_string_fields\n"
        "test_execution_target_rejects_malformed_credential_ref\n"
        "test_execution_target_rejects_invalid_protocol_type\n"
        "test_recovery_proposal_rejects_non_string_provider\n",
        encoding="utf-8",
    )
    assert select_local_task(tmp_path) is None


def test_p07_readiness_evidence_task_is_selected_when_missing(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests" / "security").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.\n",
        encoding="utf-8",
    )
    (tmp_path / "tests" / "security" / "test_native_agent_launcher.py").write_text(
        "def test_cloud_launch_without_credential_remains_blocked(): pass\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.7-cloud-agent-readiness-verification"


def test_p12_admission_evidence_task_is_selected_when_missing(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.\n",
        encoding="utf-8",
    )
    (tmp_path / "ops" / "mediahub_native_execution.py").write_text(
        "class ExecutionAdmission: pass\nnot isinstance(self.authorized, bool)\n", encoding="utf-8"
    )
    (tmp_path / "tests" / "test_mediahub_native_execution.py").write_text(
        "def test_execution_admission_rejects_non_boolean_authorization_and_recovery(): pass\n",
        encoding="utf-8",
    )
    task = select_local_task(tmp_path)
    assert task is not None
    assert task.task_id == "P1.2-execution-admission-verification"


def test_queue_encoding_marks_current_p02_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding

    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: marker.startswith("## P0.2"))
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.2 Persist this master queue and generate machine-readable ownership/provenance only if justified by existing architecture.\n", encoding="utf-8"
    )
    (tmp_path / "recovery" / "reconciliation-report.md").write_text(
        "## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22\n", encoding="utf-8"
    )
    rows = inspect_queue_encoding(tmp_path)
    assert rows[0].status == "ENCODED"


def test_p25_reconciliation_evidence_is_encoded_when_marker_is_current(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P2.5 Test stale leader, split-brain, duplicate command, replay and recovery scenarios.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "ops" / "P2-5-cluster-recovery-gap-reconciliation-2026-09-21.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / IMPLEMENTATION NOT AUTHORIZED BY THIS RECORD\n",
        encoding="utf-8",
    )
    rows = inspect_queue_encoding(tmp_path)
    assert next(row for row in rows if row.queue_id == "P2.5").status == "ENCODED"


def test_p05_delivery_recovery_increment_is_selected_when_prior_markers_are_closed(tmp_path, monkeypatch):
    import ops.local_autonomous_agent as agent

    monkeypatch.setattr(agent, "ROOT", tmp_path)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests" / "ai").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5 Close hybrid session/delivery/conversation recovery gaps.\n", encoding="utf-8"
    )
    delivery = tmp_path / "tests" / "ai" / "test_task_delivery.py"
    delivery.write_text("from ops.ai.task_delivery import TaskDeliveryJournal\n", encoding="utf-8")
    selected = agent.select_local_task(tmp_path)
    assert selected is not None
    assert selected.task_id == "P0.5-delivery-identity-recovery-test"


def test_raw_queue_compiler_turns_factual_p02_item_into_bounded_reconciliation_task(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "docs" / "ops" / "control-plane").mkdir(parents=True)
    (tmp_path / "specification").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.2 Persist this master queue and generate machine-readable ownership/provenance only if justified by existing architecture.\n", encoding="utf-8"
    )
    (tmp_path / "recovery" / "reconciliation-report.md").write_text("# Reconciliation\n", encoding="utf-8")
    (tmp_path / "docs" / "ops" / "control-plane" / "MH01-23-QUEUE-DISPATCH-2026-09-19.yaml").write_text("version: 1\n", encoding="utf-8")
    for name in ("capability-registry.yaml", "contract-registry.yaml", "dependency-graph.yaml", "invariant-registry.yaml"):
        (tmp_path / "specification" / name).write_text("version: 1\n", encoding="utf-8")
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.2-master-queue-ownership-provenance-reconciliation"
    assert task.target == "recovery/reconciliation-report.md"
    assert task.fallback_kind == "p0.2-master-queue-ownership-provenance-reconciliation"


def test_p02_compiler_requires_existing_architecture_sources(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "docs" / "ops" / "control-plane").mkdir(parents=True)
    (tmp_path / "specification").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.2 Persist this master queue and generate machine-readable ownership/provenance only if justified by existing architecture.\n", encoding="utf-8"
    )
    (tmp_path / "recovery" / "reconciliation-report.md").write_text("# Reconciliation\n", encoding="utf-8")
    (tmp_path / "docs" / "ops" / "control-plane" / "MH01-23-QUEUE-DISPATCH-2026-09-19.yaml").write_text("version: 1\n", encoding="utf-8")
    for name in ("capability-registry.yaml", "contract-registry.yaml", "dependency-graph.yaml"):
        (tmp_path / "specification" / name).write_text("version: 1\n", encoding="utf-8")
    assert compile_next_raw_queue_task(tmp_path) is None


def test_raw_queue_compiler_turns_factual_p05_item_into_bounded_task(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task, read_raw_queue

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests" / "ai").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5 Close hybrid session/delivery/conversation recovery gaps.\n"
        "P0.6 Reconcile PR #80 remote/local evidence without push or merge.\n", encoding="utf-8"
    )
    (tmp_path / "tests" / "ai" / "test_task_delivery.py").write_text(
        "from ops.ai.task_delivery import TaskDeliveryJournal\n", encoding="utf-8"
    )
    rows = read_raw_queue(tmp_path)
    assert [row.queue_id for row in rows] == ["P0.5", "P0.6"]
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.5-delivery-identity-recovery-test"
    assert task.target == "tests/ai/test_task_delivery.py"


def test_raw_queue_compiler_turns_factual_p26_item_into_bounded_ha_evidence_task(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P2.6 Verify Home Assistant Core remains Smart Home source of truth and cannot be bypassed.\n", encoding="utf-8"
    )
    (tmp_path / "ops" / "verify_functional_baseline.sh").write_text("#!/bin/sh\n", encoding="utf-8")
    (tmp_path / "recovery" / "reconciliation-report.md").write_text(
        "# Reconciliation\n", encoding="utf-8"
    )
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P2.6-home-assistant-source-of-truth-verification"
    assert task.target == "recovery/reconciliation-report.md"


def test_raw_queue_compiler_turns_factual_p01_item_into_bounded_reconciliation_task(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.1 Reconcile current local HEAD, R4 ancestry, functional baseline and active worktrees.\n", encoding="utf-8"
    )
    (tmp_path / "recovery" / "reconciliation-report.md").write_text(
        "# Reconciliation\n", encoding="utf-8"
    )
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.1-current-control-point-reconciliation"
    assert task.target == "recovery/reconciliation-report.md"


def test_raw_queue_compiler_turns_factual_p06_item_into_bounded_evidence_task(tmp_path):
    from ops.local_autonomous_agent import (
        compile_next_raw_queue_task,
        inspect_queue_encoding,
    )

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "recovery").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.6 Reconcile PR #80 remote/local evidence without push or merge.\n", encoding="utf-8"
    )
    (tmp_path / "recovery" / "reconciliation-report.md").write_text(
        "# Reconciliation\n", encoding="utf-8"
    )
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.6-pr80-reconciliation-evidence"
    assert task.target == "recovery/reconciliation-report.md"
    assert inspect_queue_encoding(tmp_path)[0].status == "NEEDS_ENCODING"


def test_raw_queue_compiler_returns_none_for_unencoded_real_item(tmp_path):
    from ops.local_autonomous_agent import (
        compile_next_raw_queue_task,
        inspect_queue_encoding,
    )

    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.6 Reconcile PR #80 remote/local evidence without push or merge.\n", encoding="utf-8"
    )
    assert compile_next_raw_queue_task(tmp_path) is None
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P0.6"] == "NEEDS_ENCODING"


def test_p1_1_fallback_is_applyable(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent

    target = tmp_path / "tests" / "test_mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text("from ops.mediahub_native_execution import NativeExecutionContract\n", encoding="utf-8")
    task = LocalTask(
        "P1.1-native-contract-negative-types",
        "P1.1 Complete provider-neutral ExecutionProposal contract and negative tests.",
        "tests/test_mediahub_native_execution.py",
        "add negative tests",
        "p1.1-negative-tests",
    )
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch(task)
    assert safe_patch(patch, task.target)
    checked = subprocess.run(
        ["git", "apply", "--check", "-"], cwd=tmp_path, input=patch,
        text=True, capture_output=True, check=False,
    )
    assert checked.returncode == 0, checked.stderr


def test_fallback_patch_is_applyable_and_idempotent(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir()
    target.write_text(
        "class NativeExecutionContract:\n"
        "    def prepare_proposal(self, request_id, workload_id, source_sha, provider):\n"
        "        return (request_id, workload_id, source_sha, provider)\n"
        "\n"
        "    def prepare_headers(self):\n"
        "        return {}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch()
    assert safe_patch(patch)
    assert patch.startswith("--- a/ops/mediahub_native_execution.py")
    checked = subprocess.run(
        ["git", "apply", "--check", "-"], cwd=tmp_path, input=patch,
        text=True, capture_output=True, check=False,
    )
    assert checked.returncode == 0, checked.stderr
    applied = subprocess.run(
        ["git", "apply", "-"], cwd=tmp_path, input=patch,
        text=True, capture_output=True, check=False,
    )
    assert applied.returncode == 0, applied.stderr
    assert "class VerificationBoundary:" in target.read_text(encoding="utf-8")
    target.write_text(target.read_text() + "\nclass VerificationBoundary:\n", encoding="utf-8")
    assert fallback_patch() == ""


def test_safe_patch_rejects_wrong_target(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text("class NativeExecutionContract:\n", encoding="utf-8")
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch().replace("ops/mediahub_native_execution.py", "tests/not_allowed.py")
    assert not safe_patch(patch)


def test_safe_patch_rejects_multiple_targets(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text("class NativeExecutionContract:\n", encoding="utf-8")
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch()
    if not patch:
        return
    extra = "--- a/tests/other.py\n+++ b/tests/other.py\n@@ -1 +1 @@\n-x\n+y\n"
    assert not safe_patch(patch + extra)


def test_safe_patch_rejects_new_file_rename_and_mode_changes(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text("class NativeExecutionContract:\n", encoding="utf-8")
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch()
    if not patch:
        return
    assert not safe_patch(patch.replace("--- a/", "new file mode 100644\n--- /dev/null\n--- a/", 1))
    assert not safe_patch(patch.replace("--- a/", "rename from ops/mediahub_native_execution.py\n--- a/", 1))
    assert not safe_patch(patch.replace("--- a/", "old mode 100644\n--- a/", 1))


def test_safe_patch_rejects_protected_path_and_malformed_hunk(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent
    target = tmp_path / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text("class NativeExecutionContract:\n", encoding="utf-8")
    monkeypatch.setattr(agent, "ROOT", tmp_path)
    patch = fallback_patch()
    if not patch:
        return
    assert not safe_patch(patch.replace("ops/mediahub_native_execution.py", ".github/workflows/x.yml"))
    first_hunk = next(line for line in patch.splitlines() if line.startswith("@@ "))
    assert not safe_patch(patch.replace(first_hunk, "@@ malformed", 1))


def test_state_rejects_unknown_state():
    import pytest
    with pytest.raises(ValueError):
        state("UNKNOWN_STATE")


def test_fallback_source_has_no_network_or_credential_usage():
    from ops import local_autonomous_agent as agent
    source = inspect.getsource(agent.fallback_patch)
    assert "urllib" not in source
    assert "socket" not in source.lower()
    assert "subprocess" not in source


def test_exact_target_rejects_additional_staged_path(monkeypatch):
    from ops import local_autonomous_agent as agent

    class Result:
        stdout = "ops/mediahub_native_execution.py\nops/extra.py\n"
        returncode = 0

    monkeypatch.setattr(agent, "run", lambda *args, **kwargs: Result())
    assert not agent.exact_target()


def test_exact_target_accepts_only_target(monkeypatch):
    from ops import local_autonomous_agent as agent

    class Result:
        stdout = "ops/mediahub_native_execution.py\n"
        returncode = 0

    monkeypatch.setattr(agent, "run", lambda *args, **kwargs: Result())
    monkeypatch.setattr(agent, "select_local_task", lambda root: None)
    assert agent.exact_target()


def _init_temp_repo(tmp_path):
    repo = tmp_path / "repo"
    target = repo / "ops" / "mediahub_native_execution.py"
    target.parent.mkdir(parents=True)
    target.write_text(
        "class NativeExecutionContract:\n"
        "    def prepare_proposal(self, request_id, workload_id, source_sha, provider):\n"
        "        return (request_id, workload_id, source_sha, provider)\n"
        "\n"
        "    def prepare_headers(self):\n"
        "        return {}\n",
        encoding="utf-8",
    )
    (repo / "model.gguf").write_bytes(b"test")
    queue = repo / "ops" / "local_autonomous_tasks.md"
    queue.write_text("P0.4 Close current Native Execution Contract test gaps.\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.invalid"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "test"], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "baseline"], check=True)
    return repo, target


def _configure_temp_agent(monkeypatch, repo, target):
    from ops import local_autonomous_agent as agent
    monkeypatch.setattr(agent, "ROOT", repo)
    model = repo / "model.gguf"
    monkeypatch.setattr(agent, "MODEL", model)
    monkeypatch.setattr(agent, "RUFF", Path("/definitely/missing/ruff"))
    monkeypatch.setattr(agent, "MAX_REGENERATIONS", 1)
    monkeypatch.setattr(agent, "TARGET", str(target.relative_to(repo)))
    monkeypatch.setenv("MEDIAHUB_LEASE_ROOT", str(repo.parent / "leases"))
    monkeypatch.setenv("MEDIAHUB_WORKER_ID", "test-worker")
    return agent


def test_ai_malformed_never_reaches_apply_or_commit(monkeypatch):
    from ops import local_autonomous_agent as agent
    calls = []
    monkeypatch.setattr(agent, "apply_checked", lambda patch: calls.append(patch) or True)
    malformed = "not a unified diff"
    extracted = agent.extract(malformed)
    assert extracted == ""
    assert not agent.safe_patch(extracted)
    assert calls == []


def test_ai_timeout_selects_eligible_fallback(tmp_path, monkeypatch, capsys):
    repo, target = _init_temp_repo(tmp_path)
    agent = _configure_temp_agent_wave4(monkeypatch, repo, target)
    monkeypatch.setattr(agent, "generate", lambda text: (28, "", "AI_TIMEOUT"))
    monkeypatch.setattr(agent, "verify", lambda task=None: True)
    rc = agent.main()
    output = capsys.readouterr().out
    assert rc == 0
    assert "LOCAL_AGENT_STATE=AI_TIMEOUT" in output
    assert "LOCAL_AGENT_STATE=FALLBACK_SELECTED" in output
    assert "LOCAL_AGENT_STATE=FALLBACK_APPLIED" in output
    assert "LOCAL_AGENT_STATE=VERIFY_PASS" in output
    assert "LOCAL_AGENT_STATE=COMMITTED" in output


def test_fallback_validation_failure_blocks_without_commit(tmp_path, monkeypatch, capsys):
    repo, target = _init_temp_repo(tmp_path)
    agent = _configure_temp_agent_wave4(monkeypatch, repo, target)
    monkeypatch.setattr(agent, "generate", lambda text: (28, "", "AI_TIMEOUT"))
    monkeypatch.setattr(agent, "apply_checked", lambda patch, target=None: False)
    rc = agent.main()
    output = capsys.readouterr().out
    assert rc == 25
    assert "LOCAL_AGENT_STATE=FALLBACK_SELECTED" in output
    assert "LOCAL_AGENT_STATE=BLOCKED evidence=fallback failed" in output
    assert "LOCAL_AGENT_STATE=COMMITTED" not in output
    assert subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout == ""


def test_verify_failure_rolls_back_and_never_commits(tmp_path, monkeypatch, capsys):
    repo, target = _init_temp_repo(tmp_path)
    agent = _configure_temp_agent_wave4(monkeypatch, repo, target)
    baseline = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    monkeypatch.setattr(agent, "generate", lambda text: (28, "", "AI_TIMEOUT"))
    monkeypatch.setattr(agent, "verify", lambda task=None: False)
    rc = agent.main()
    output = capsys.readouterr().out
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    status = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout
    assert rc == 27
    assert "LOCAL_AGENT_STATE=VERIFY_FAIL" in output
    assert "LOCAL_AGENT_STATE=ROLLED_BACK evidence=working tree clean" in output
    assert "LOCAL_AGENT_STATE=COMMITTED" not in output
    assert head == baseline
    assert status == ""


def test_commit_failure_blocks_and_never_emits_committed(tmp_path, monkeypatch, capsys):
    repo, target = _init_temp_repo(tmp_path)
    agent = _configure_temp_agent_wave4(monkeypatch, repo, target)
    monkeypatch.setattr(agent, "generate", lambda text: (28, "", "AI_TIMEOUT"))
    monkeypatch.setattr(agent, "verify", lambda task=None: True)
    real_run = agent.run

    def failing_commit(cmd, timeout=120):
        if cmd[:2] == ["git", "commit"]:
            return subprocess.CompletedProcess(cmd, 1, "", "injected commit failure")
        return real_run(cmd, timeout)

    monkeypatch.setattr(agent, "run", failing_commit)
    rc = agent.main()
    output = capsys.readouterr().out
    assert rc == 31
    assert "LOCAL_AGENT_STATE=BLOCKED evidence=commit gate failed" in output
    assert "LOCAL_AGENT_STATE=COMMITTED" not in output
    assert subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout != ""


def test_state_machine_has_no_noop_or_unknown_pass_state():
    from ops import local_autonomous_agent as agent
    assert "NOOP" not in agent.STATES
    assert "PASS" not in agent.STATES
    assert "UNKNOWN_STATE" not in agent.STATES
    assert agent.STATES[-1] == "BLOCKED"


def test_rollback_requires_clean_tree(tmp_path, monkeypatch):
    repo, target = _init_temp_repo(tmp_path)
    agent = _configure_temp_agent_wave4(monkeypatch, repo, target)
    target.write_text(target.read_text() + "# dirty\n", encoding="utf-8")
    assert agent.rollback()
    assert subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout == ""


def test_provenance_controller_records_required_commit_coordinates():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    for token in (
        "SOURCE_SHA=", "BASE_TREE=", "POST_HEAD=", "POST_TREE=", "ROLLBACK=", "RESULT=",
        "git merge-base --is-ancestor \"$BASE_HEAD\" \"$POST_HEAD\"",
        "git status --porcelain",
    ):
        assert token in text


def test_failure_injection_matrix_is_explicitly_guarded():
    patch = _synthetic_target_patch()
    injections = {
        "MALFORMED_AI": not safe_patch("not a diff"),
        "WRONG_TARGET": not safe_patch(patch.replace("ops/mediahub_native_execution.py", "tests/x.py")),
        "MULTI_TARGET": not safe_patch(patch + "--- a/tests/x.py\n+++ b/tests/x.py\n@@ -1 +1 @@\n-a\n+b\n"),
        "NEW_FILE": not safe_patch(patch.replace("--- a/", "new file mode 100644\n--- /dev/null\n--- a/", 1)),
        "RENAME": not safe_patch(patch.replace("--- a/", "rename from ops/mediahub_native_execution.py\n--- a/", 1)),
        "MODE_CHANGE": not safe_patch(patch.replace("--- a/", "old mode 100644\n--- a/", 1)),
        "PROTECTED_PATH": not safe_patch(patch.replace("ops/mediahub_native_execution.py", ".github/workflows/x.yml")),
    }
    assert all(injections.values()), injections


# Wave 4 test helpers override the immutable production R4 anchor only inside isolated temp repositories.
def _configure_temp_agent_wave4(monkeypatch, repo, target):
    agent = _configure_temp_agent(monkeypatch, repo, target)
    baseline = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    monkeypatch.setattr(agent, "R4", baseline)
    return agent


def _synthetic_target_patch():
    return (
        "diff --git a/ops/mediahub_native_execution.py b/ops/mediahub_native_execution.py\n"
        "--- a/ops/mediahub_native_execution.py\n"
        "+++ b/ops/mediahub_native_execution.py\n"
        "@@ -1 +1,2 @@\n"
        " from dataclasses import dataclass\n"
        "+\n"
    )


def test_hybrid_development_systemd_unit_requires_explicit_environment():
    text = (ROOT / "ops/systemd/mediahub-hybrid-development.service").read_text(encoding="utf-8")
    assert "ConditionPathExists=/etc/mediahub/hybrid-development.env" in text
    assert "Restart=on-failure" in text
    assert "Restart=always" not in text


def test_hybrid_development_systemd_unit_is_fail_closed_on_terminal_restore():
    text = (ROOT / "ops/systemd/mediahub-hybrid-development.service").read_text(encoding="utf-8")
    assert "Restart=on-failure" in text
    assert "Restart=always" not in text
    assert "--r4-sha 471f709f5633feab7aeb62dd3ea52effad6d2bc4" in text


def test_systemd_autonomous_service_runs_continuous_controller():
    loop = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert 'export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"' in loop
    text = (ROOT / "ops/systemd/mediahub-local-autonomous.service").read_text(encoding="utf-8")
    assert "Type=simple" in text
    assert "ExecStart=/home/mediahub/dev/mediahub-os-autonomous/ops/autonomous_os_loop.sh" in text
    assert "Restart=on-failure" in text
    assert "TimeoutStartSec=0" in text
    assert "ExecStart=/usr/bin/python3 /home/mediahub/dev/mediahub-os-autonomous/ops/local_autonomous_agent.py" not in text


def test_systemd_autonomous_timer_is_repository_approved():
    text = (ROOT / "ops/systemd/mediahub-local-autonomous.timer").read_text(encoding="utf-8")
    assert "OnBootSec=3min" in text
    assert "OnUnitActiveSec=10min" in text
    assert "Persistent=true" in text
    assert "Unit=mediahub-local-autonomous.service" in text


def test_service_entrypoint_delegates_to_same_continuous_controller():
    text = (ROOT / "ops/autonomous_service_entrypoint.sh").read_text(encoding="utf-8")
    assert 'exec "$ROOT/ops/autonomous_os_loop.sh"' in text
    assert "local_autonomous_agent.py" not in text


def test_controller_retains_liveness_when_preflight_blocks_a_cycle():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert "AUTONOMY_RETAINED: controller remains alive" in text
    assert "exit 21" not in text
    assert "exit 22" not in text
    assert "exit 70" not in text


def test_systemd_autonomous_service_is_enableable_at_boot():
    text = (ROOT / "ops/systemd/mediahub-local-autonomous.service").read_text(encoding="utf-8")
    assert "[Install]" in text
    assert "WantedBy=multi-user.target" in text
    assert "After=local-fs.target mediahub-local-ai.service" in text
    assert "Wants=mediahub-local-ai.service" in text
    assert "Requires=mediahub-local-ai.service" not in text


def test_astra_child_does_not_inherit_loop_lock_fd():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert "2>&1 9>&- &" in text


def test_astra_pidfile_is_owned_by_astra_supervisor():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert 'ASTRA_PIDFILE=' not in text
    assert '>$ASTRA_PIDFILE' not in text


def test_controller_pid_identity_is_bound_to_process_starttime():
    text = (ROOT / "ops/autonomous_os_loop.sh").read_text(encoding="utf-8")
    assert 'PROC_STARTTIME="$(awk' in text
    assert 'PROC_STARTTIME' in text and 'PIDFILE' in text
    assert "PROC_STARTTIME=%s" in text


def test_watchdog_rejects_pid_reuse_by_process_starttime():
    text = (ROOT / "ops/autonomous_watchdog.sh").read_text(encoding="utf-8")
    assert 'recorded_starttime="${pid_record#*:}"' in text
    assert 'current_starttime="$(awk' in text
    assert '[ "$recorded_starttime" = "$current_starttime" ]' in text


def test_watchdog_does_not_replace_after_stop_marker_race():
    text = (ROOT / "ops/autonomous_watchdog.sh").read_text(encoding="utf-8")
    assert 'if [ -e "$STOPFILE" ]; then' in text
    assert 'recovery suppressed' in text


def test_watchdog_systemd_unit_is_continuously_supervised():
    text = (ROOT / "ops/systemd/mediahub-local-autonomous-watchdog.service").read_text(encoding="utf-8")
    assert "Type=simple" in text
    assert "ExecStart=/home/mediahub/dev/mediahub-os-autonomous/ops/autonomous_watchdog.sh" in text
    assert "Restart=always" in text
    assert "WantedBy=multi-user.target" in text
    assert "Wants=mediahub-local-autonomous.service" in text



def _git_init_for_compiler(root):
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=root, check=True)
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "baseline"], cwd=root, check=True)


def test_task_compiler_binds_acceptance_and_repository_provenance(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent

    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text("P0.4 Close current Native Execution Contract test gaps.\n", encoding="utf-8")
    target = queue / "mediahub_native_execution.py"
    target.write_text("bounded request\n", encoding="utf-8")
    (tmp_path / ".autonomous").mkdir()
    (tmp_path / ".autonomous" / "leases").mkdir(parents=True)
    _git_init_for_compiler(tmp_path)
    monkeypatch.setattr(agent, "GIT", Path("git"))
    candidate = LocalTask("task-compiler-1", "P0.4 queue", "ops/mediahub_native_execution.py", "bounded acceptance")
    compiled = compile_executable_task(tmp_path, candidate)
    assert isinstance(compiled, ExecutableTask)
    assert compiled.base_sha
    assert compiled.acceptance_fingerprint
    assert compiled.verification_command.startswith("pytest -q")
    assert compiled.expected_evidence
    assert compiled.dependency_set == ()
    assert "R4" in compiled.conflict_set


def test_task_compiler_suppresses_existing_equivalent_commit(tmp_path, monkeypatch):
    from ops import local_autonomous_agent as agent

    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text("P0.4 queue\n", encoding="utf-8")
    target = queue / "mediahub_native_execution.py"
    target.write_text("bounded request\n", encoding="utf-8")
    (tmp_path / ".autonomous").mkdir()
    (tmp_path / ".autonomous" / "leases").mkdir(parents=True)
    _git_init_for_compiler(tmp_path)
    subprocess.run(["git", "commit", "--allow-empty", "-qm", "task-compiler-2"], cwd=tmp_path, check=True)
    monkeypatch.setattr(agent, "GIT", Path("git"))
    candidate = LocalTask("task-compiler-2", "P0.4 queue", "ops/mediahub_native_execution.py", "bounded acceptance")
    assert compile_executable_task(tmp_path, candidate) is None



def test_queue_encoding_requires_current_p1_4_evidence_surface(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P1.4 Complete provider selector and fallback semantics, including offline/degraded behavior.\n",
        encoding="utf-8",
    )
    (queue / "mediahub_provider_gateway.py").write_text("gateway\n", encoding="utf-8")
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_mediahub_provider_gateway.py").write_text("def test_gateway(): pass\n", encoding="utf-8")
    (tmp_path / "tests" / "test_mediahub_resilience.py").write_text("def test_resilience(): pass\n", encoding="utf-8")
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P1.4"] == "NEEDS_ENCODING"
    evidence = tmp_path / "docs" / "ops"
    evidence.mkdir(parents=True)
    (evidence / "P1-4-provider-selector-verification-2026-09-21.md").write_text("evidence\n", encoding="utf-8")
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P1.4"] == "ENCODED"


def test_queue_encoding_marks_only_explicit_local_items_encoded(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.4 Close current Native Execution Contract test gaps.\n"
        "P1.3 Complete AI model/provider/capability registry verification.\n"
        "P2.1 Inventory State Authority contracts and identify every mutation path.\n",
        encoding="utf-8",
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows == {"P0.4": "ENCODED", "P1.3": "NEEDS_ENCODING", "P2.1": "ENCODED"}


def test_queue_encoding_marks_current_p03_evidence_encoded(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.3 Verify supervisor/watchdog restart, lock, checkpoint, rollback and journal semantics.\n",
        encoding="utf-8",
    )
    evidence = tmp_path / "docs" / "ops"
    evidence.mkdir(parents=True)
    (evidence / "P0-3-controller-watchdog-verification-2026-09-21.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE\n", encoding="utf-8"
    )
    _git_init_with_commit(tmp_path)
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P0.3"] == "ENCODED"


def test_queue_encoding_marks_current_p01_evidence_encoded(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.1 Reconcile current local HEAD, R4 ancestry, functional baseline and active worktrees.\n", encoding="utf-8"
    )
    evidence = tmp_path / "recovery"
    evidence.mkdir()
    report = evidence / "reconciliation-report.md"
    report.write_text("## P0.1 current control-point reconciliation — 2026-09-21\n", encoding="utf-8")
    _git_init_with_commit(tmp_path)
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P0.1"] == "ENCODED"


def test_queue_encoding_marks_current_p06_evidence_encoded(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.6 Reconcile PR #80 remote/local evidence without push or merge.\n", encoding="utf-8"
    )
    evidence = tmp_path / "recovery"
    evidence.mkdir()
    (evidence / "reconciliation-report.md").write_text(
        "## P0.6 PR #80 reconciliation — 2026-09-21\n", encoding="utf-8"
    )
    _git_init_with_commit(tmp_path)
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P0.6"] == "ENCODED"


def test_queue_encoding_marks_current_p26_evidence_encoded(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P2.6 Verify Home Assistant Core remains Smart Home source of truth and cannot be bypassed.\n", encoding="utf-8"
    )
    evidence = tmp_path / "recovery"
    evidence.mkdir()
    (evidence / "reconciliation-report.md").write_text(
        "## P2.6 Home Assistant source-of-truth verification — 2026-09-21\n", encoding="utf-8"
    )
    _git_init_with_commit(tmp_path)
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P2.6"] == "ENCODED"


def test_queue_encoding_rejects_stale_copied_evidence_not_in_head(tmp_path):
    queue = tmp_path / "ops"
    queue.mkdir()
    (queue / "local_autonomous_tasks.md").write_text(
        "P0.6 Reconcile PR #80 remote/local evidence without push or merge.\n", encoding="utf-8"
    )
    evidence = tmp_path / "recovery"
    evidence.mkdir()
    report = evidence / "reconciliation-report.md"
    report.write_text("base\n", encoding="utf-8")
    _git_init_with_commit(tmp_path)
    subprocess.run(["git", "checkout", "-qb", "stale-evidence"], cwd=tmp_path, check=True)
    report.write_text("base\n## P0.6 PR #80 reconciliation — 2026-09-21\n", encoding="utf-8")
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "stale evidence"], cwd=tmp_path, check=True)
    stale = report.read_text(encoding="utf-8")
    subprocess.run(["git", "checkout", "-q", "master"], cwd=tmp_path, check=True)
    report.write_text(stale, encoding="utf-8")
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P0.6"] == "NEEDS_ENCODING"


def test_p33_gap_reconciliation_is_selected_after_p32_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.2 Implement/qualify ingestion and metadata/index contracts.\n"
        "P3.3 Implement/qualify playback/control contracts.\n", encoding="utf-8"
    )
    for rel in (
        "ops/mediahub_lifecycle_contract.py", "tests/test_mediahub_lifecycle_contract.py",
        "ops/mediahub_streaming_boundary.py", "tests/test_mediahub_streaming_boundary.py",
    ):
        (tmp_path / rel).write_text("", encoding="utf-8")
    (tmp_path / "docs/ops/P3-2-ingestion-metadata-index-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P3.2 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.3-playback-control-gap-reconciliation"


def test_p32_gap_reconciliation_is_selected_when_media_acceptance_is_missing(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.1 Inventory media domain contracts and lifecycle states.\n"
        "P3.2 Implement/qualify ingestion and metadata/index contracts.\n", encoding="utf-8"
    )
    for rel in (
        "ops/mediahub_lifecycle_contract.py", "tests/test_mediahub_lifecycle_contract.py",
        "ops/mediahub_streaming_boundary.py", "tests/test_mediahub_streaming_boundary.py",
    ):
        (tmp_path / rel).write_text("", encoding="utf-8")
    (tmp_path / "docs/ops/P3-1-media-domain-lifecycle-inventory-2026-09-22.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.2-ingestion-metadata-index-gap-reconciliation"


def test_p45_gap_reconciliation_is_selected_after_p44_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests/ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(exist_ok=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P4.4 Ensure external retrieval cannot mutate State Authority directly.\n"
        "P4.5 Add audit/revocation and offline/degraded behavior.\n", encoding="utf-8"
    )
    for rel in (
        "ops/cloud_development_adapter.py", "ops/mediahub_credential_broker.py", "ops/mediahub_resilience.py",
        "tests/ops/test_cloud_development_adapter.py", "tests/test_mediahub_credential_broker.py",
        "tests/test_mediahub_resilience.py", "docs/architecture/MH-21-audit.md",
        "docs/architecture/MH-21-provider-quarantine.md", "docs/architecture/MH-21-offline-mode.md",
    ):
        (tmp_path / rel).write_text("audit revocation offline degraded", encoding="utf-8")
    (tmp_path / "docs/ops/P4-4-external-retrieval-state-authority-boundary-verification-2026-09-22.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE / P4.4 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P4.5-audit-revocation-offline-degraded-gap-reconciliation"


def test_p44_authority_boundary_verification_is_selected_after_p43_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops/ai").mkdir(parents=True)
    (tmp_path / "tests/security").mkdir(parents=True)
    (tmp_path / "tests/ops").mkdir(parents=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops").mkdir(exist_ok=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P4.3 Add source trust/verification and stale-data handling.\n"
        "P4.4 Ensure external retrieval cannot mutate State Authority directly.\n", encoding="utf-8"
    )
    for rel in (
        "docs/architecture/MH-21-cloud-boundary.md", "docs/architecture/MH-21-security-invariants.md",
        "docs/architecture/MH-21-rag-boundary.md", "docs/architecture/MH-21-rag-security.md",
        "ops/ai/ai_adapter.py", "ops/cloud_development_adapter.py",
        "tests/security/test_mh05_systemwide_reachability.py", "tests/security/test_ai_adapter.py",
        "tests/ops/test_cloud_development_adapter.py",
    ):
        (tmp_path / rel).write_text("state authority retrieval rag", encoding="utf-8")
    (tmp_path / "docs/ops/P4-3-source-trust-stale-data-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P4.3 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P4.4-external-retrieval-state-authority-boundary-verification"


def test_p43_gap_reconciliation_is_selected_after_p42_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "specification").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.\n"
        "P4.3 Add source trust/verification and stale-data handling.\n", encoding="utf-8"
    )
    for rel in (
        "specification/contract-registry.yaml", "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "docs/architecture/MH-21-provider-trust.md", "docs/architecture/MH-21-rag-security.md",
        "docs/architecture/MH-21-unknowns.md",
    ):
        (tmp_path / rel).write_text("trust verification stale retention", encoding="utf-8")
    (tmp_path / "docs/ops/P4-2-trusted-sources-intelligence-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P4.2 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P4.3-source-trust-stale-data-gap-reconciliation"


def test_p42_gap_reconciliation_is_selected_after_p41_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "specification").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P4.1 Complete document ingestion/index/search contracts.\n"
        "P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.\n", encoding="utf-8"
    )
    for rel in (
        "specification/contract-registry.yaml", "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "docs/architecture/MH-21-rag-boundary.md", "docs/architecture/MH-21-rag-security.md",
        "docs/architecture/MH-21-cloud-boundary.md", "docs/architecture/MH-21-data-egress.md",
        "docs/architecture/MH-21-audit.md",
    ):
        (tmp_path / rel).write_text("trusted-source retrieval verification provenance evidence", encoding="utf-8")
    (tmp_path / "docs/ops/P4-1-document-ingestion-index-search-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P4.1 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P4.2-trusted-sources-intelligence-gap-reconciliation"


def test_p41_gap_reconciliation_is_selected_after_p36_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "specification").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.6 Benchmark bounded media operations and resource limits.\n"
        "P4.1 Complete document ingestion/index/search contracts.\n", encoding="utf-8"
    )
    for rel in (
        "specification/contract-registry.yaml", "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "docs/architecture/MH-21-rag-boundary.md", "docs/architecture/MH-21-rag-security.md",
        "docs/architecture/MH-21-resource-governance.md",
    ):
        (tmp_path / rel).write_text("document ingestion index search", encoding="utf-8")
    (tmp_path / "docs/ops/P3-6-media-benchmark-resource-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P3.6 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P4.1-document-ingestion-index-search-gap-reconciliation"


def test_p36_gap_reconciliation_is_selected_after_p35_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "recovery/acceptance").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.5 Add integration and failure-injection tests.\n"
        "P3.6 Benchmark bounded media operations and resource limits.\n", encoding="utf-8"
    )
    for rel in (
        "ops/mediahub_streaming_boundary.py", "tests/test_mediahub_streaming_boundary.py",
        "ops/mediahub_cluster_resources.py", "tests/test_mediahub_cluster_resources.py",
        "recovery/acceptance/F-010-personal-media-library-ingestion-sync.md",
        "recovery/acceptance/F-012-media-playback-live-media-streaming.md",
    ):
        (tmp_path / rel).write_text("", encoding="utf-8")
    (tmp_path / "docs/ops/P3-5-media-integration-failure-injection-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P3.5 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.6-media-benchmark-resource-gap-reconciliation"


def test_p35_gap_reconciliation_is_selected_after_p34_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "recovery/acceptance").mkdir(parents=True)
    (tmp_path / "tests").mkdir(exist_ok=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.4 Validate authorization, storage, retention and recovery semantics.\n"
        "P3.5 Add integration and failure-injection tests.\n", encoding="utf-8"
    )
    for rel in (
        "ops/mediahub_lifecycle_contract.py", "tests/test_mediahub_lifecycle_contract.py",
        "ops/mediahub_streaming_boundary.py", "tests/test_mediahub_streaming_boundary.py",
        "tests/test_mediahub_cluster_failover.py", "tests/test_mediahub_cluster_lifecycle.py",
        "recovery/acceptance/F-010-personal-media-library-ingestion-sync.md",
        "recovery/acceptance/F-012-media-playback-live-media-streaming.md",
        "recovery/acceptance/F-014-phone-media-io-endpoint.md",
    ):
        (tmp_path / rel).write_text("", encoding="utf-8")
    (tmp_path / "docs/ops/P3-4-media-authorization-storage-retention-recovery-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P3.4 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.5-media-integration-failure-injection-gap-reconciliation"


def test_p34_gap_reconciliation_is_selected_after_p33_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests/security").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "runtime/mediahub_runtime").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P3.3 Implement/qualify playback/control contracts.\n"
        "P3.4 Validate authorization, storage, retention and recovery semantics.\n", encoding="utf-8"
    )
    for rel in (
        "ops/mediahub_lifecycle_contract.py", "tests/test_mediahub_lifecycle_contract.py",
        "ops/mediahub_streaming_boundary.py", "tests/test_mediahub_streaming_boundary.py",
        "runtime/mediahub_runtime/state_authority.py", "tests/security/test_mh05_restore_security.py",
    ):
        (tmp_path / rel).write_text("", encoding="utf-8")
    (tmp_path / "docs/ops/P3-3-playback-control-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P3.3 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.4-media-authorization-storage-retention-recovery-gap-reconciliation"


def test_p31_media_domain_inventory_is_selected_from_existing_contract_surface(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text("P3.1 Inventory media domain contracts and lifecycle states.\n", encoding="utf-8")
    (tmp_path / "ops" / "mediahub_lifecycle_contract.py").write_text("class LifecycleState: pass\n", encoding="utf-8")
    (tmp_path / "tests" / "test_mediahub_lifecycle_contract.py").write_text("def test_lifecycle_contract(): pass\n", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P3.1-media-domain-lifecycle-inventory"


def test_p31_current_evidence_encodes_queue_item(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text("P3.1 Inventory media domain contracts and lifecycle states.\n", encoding="utf-8")
    (tmp_path / "docs" / "ops" / "P3-1-media-domain-lifecycle-inventory-2026-09-22.md").write_text("Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED\n", encoding="utf-8")
    assert inspect_queue_encoding(tmp_path)[0].status == "ENCODED"


def test_p31_stale_evidence_does_not_encode_queue_item(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: False)
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text("P3.1 Inventory media domain contracts and lifecycle states.\n", encoding="utf-8")
    (tmp_path / "docs" / "ops" / "P3-1-media-domain-lifecycle-inventory-2026-09-22.md").write_text("Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED\n", encoding="utf-8")
    assert inspect_queue_encoding(tmp_path)[0].status == "NEEDS_ENCODING"


def test_raw_queue_parser_preserves_multi_segment_queue_ids(tmp_path):
    from ops.local_autonomous_agent import read_raw_queue
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5.1 Terminal checkpoint startup: classify an exact-identity terminal journal tail as a clean daemon stop; never revive it or create a new identity.\n"
        "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.\n",
        encoding="utf-8",
    )
    rows = read_raw_queue(tmp_path)
    assert [row.queue_id for row in rows] == ["P0.5.1", "P0.5.2"]


def test_raw_queue_compiler_encodes_p051_from_existing_daemon_contract(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5.1 Terminal checkpoint startup: classify an exact-identity terminal journal tail as a clean daemon stop; never revive it or create a new identity.\n",
        encoding="utf-8",
    )
    (tmp_path / "ops" / "ai").mkdir(parents=True)
    (tmp_path / "ops" / "ai" / "hybrid_development_daemon.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "tests" / "ai").mkdir(parents=True)
    (tmp_path / "tests" / "ai" / "test_hybrid_development_daemon.py").write_text(
        "def test_daemon_treats_matching_terminal_restore_as_clean_exit(): pass\n", encoding="utf-8"
    )
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.5.1-terminal-checkpoint-startup-verification"

def test_multisegment_evidence_marker_encodes_current_p051_queue_row(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5.1 Terminal checkpoint startup: classify an exact-identity terminal journal tail as a clean daemon stop; never revive it or create a new identity.\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "ops" / "P0-5-1-terminal-checkpoint-startup-2026-09-22.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.1 NOT CLOSED\n", encoding="utf-8"
    )
    rows = inspect_queue_encoding(tmp_path)
    assert next(row for row in rows if row.queue_id == "P0.5.1").status == "ENCODED"

def test_raw_queue_compiler_encodes_p052_from_existing_daemon_regression(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.\n",
        encoding="utf-8",
    )
    (tmp_path / "ops" / "ai").mkdir(parents=True)
    (tmp_path / "ops" / "ai" / "hybrid_development_daemon.py").write_text("def main(): pass\n", encoding="utf-8")
    (tmp_path / "tests" / "ai").mkdir(parents=True)
    (tmp_path / "tests" / "ai" / "test_hybrid_development_daemon.py").write_text(
        "def test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch(): pass\n", encoding="utf-8"
    )
    task = compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P0.5.2-terminal-provenance-regression-verification"

def test_p052_evidence_task_compiles_as_new_durable_artifact(tmp_path):
    from ops.local_autonomous_agent import LocalTask, compile_executable_task
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.\n", encoding="utf-8"
    )
    import subprocess
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=tmp_path, check=True)
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "base"], cwd=tmp_path, check=True)
    task = LocalTask(
        "P0.5.2-terminal-provenance-regression-verification",
        "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.",
        "docs/ops/P0-5-2-terminal-provenance-regression-2026-09-22.md",
        "record evidence",
        "p0.5.2-terminal-provenance-regression-verification",
    )
    compiled = compile_executable_task(tmp_path, task)
    assert compiled is not None
    assert compiled.acceptance_fingerprint


def test_queue_encoding_marks_current_p51_and_p53_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "checkpoints").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P5.1 Preserve two-app model: MediaHub Core + separate Remote Mobile Application.\n"
        "P5.3 Implement API/client compatibility and offline/degraded states.\n",
        encoding="utf-8",
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P5.1"] == "ENCODED"
    assert rows["P5.3"] == "ENCODED"


def test_p73_trusted_sources_gap_reconciliation_is_selected_after_p72_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "specification").mkdir(parents=True); (tmp_path / "docs/architecture").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P7.2 Enforce consent, scope, provenance, audit and revocation.\nP7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.\n", encoding="utf-8")
    (tmp_path / "docs/ops/P7-2-human-clone-governance-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P7.2 NOT CLOSED\n", encoding="utf-8")
    (tmp_path / "specification/contract-registry.yaml").write_text("CTR-042 trusted-source discovery retrieval verification provenance change detection evidence separation", encoding="utf-8")
    for rel in ("docs/architecture/MH-21-rag-boundary.md","docs/architecture/MH-21-rag-security.md","docs/architecture/MH-21-knowledge-graph-interaction.md"):
        (tmp_path / rel).write_text("retrieval provenance evidence separation knowledge", encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P7.3-trusted-sources-knowledge-workflow-gap-reconciliation"


def test_p72_human_clone_governance_gap_reconciliation_is_selected_after_p71_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "specification").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True); (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.\n"
        "P7.2 Enforce consent, scope, provenance, audit and revocation.\n", encoding="utf-8")
    (tmp_path / "docs/ops/P7-1-human-clone-contract-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P7.1 NOT CLOSED\n", encoding="utf-8")
    (tmp_path / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md").write_text(
        "AI Human Clone consent authorization identity provenance rights-holder scope model/asset provenance audit revocation", encoding="utf-8")
    (tmp_path / "specification/contract-registry.yaml").write_text(
        "CTR-043 ai-human-clone consent authorization use scope provenance revocation audit", encoding="utf-8")
    for rel in ("ops/cloud_development_adapter.py", "ops/mediahub_credential_broker.py", "tests/ops/test_cloud_development_adapter.py", "tests/test_mediahub_credential_broker.py"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("authorization provenance audit revocation", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P7.2-human-clone-governance-gap-reconciliation"


def test_p71_human_clone_contract_gap_reconciliation_is_selected_after_p65_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "specification").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P6.5 Add provider outage/fallback tests without changing authority semantics.\n"
        "P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.\n", encoding="utf-8")
    (tmp_path / "docs/ops/P6-5-provider-outage-fallback-gap-reconciliation-2026-09-22.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE / P6.5 NOT CLOSED\n", encoding="utf-8")
    (tmp_path / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md").write_text(
        "AI Human Clone separate Cloud Development AI subsystem consent authorization provenance revocation audit", encoding="utf-8")
    (tmp_path / "specification/contract-registry.yaml").write_text(
        "CTR-043 ai-human-clone consent/authorization use scope asset/model provenance revocation audit", encoding="utf-8")
    (tmp_path / "specification/capability-registry.yaml").write_text(
        "authorized_ai_human_clone_real_person_generated_media_participation", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P7.1-human-clone-contract-gap-reconciliation"



def test_p74_ordinary_user_cloud_access_gap_reconciliation_is_selected_after_p73_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "specification").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True); (tmp_path / "recovery/acceptance").mkdir(parents=True); (tmp_path / "tests/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.\n"
        "P7.4 Ensure ordinary users have no direct corporate Cloud Development AI access.\n", encoding="utf-8")
    (tmp_path / "docs/ops/P7-3-trusted-sources-knowledge-workflow-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P7.3 NOT CLOSED\n", encoding="utf-8")
    for rel in (
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        "specification/invariant-registry.yaml",
        "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        "ops/cloud_development_adapter.py",
        "tests/ops/test_cloud_development_adapter.py",
    ):
        (tmp_path / rel).write_text("Cloud Development AI ordinary users no direct access controlled escalation", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P7.4-ordinary-user-cloud-development-access-gap-reconciliation"

def test_p65_provider_fallback_gap_reconciliation_is_selected_after_p64_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "ops").mkdir(parents=True); (tmp_path / "tests").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P6.4 Route Smart Home mutations through Home Assistant Core.\n"
        "P6.5 Add provider outage/fallback tests without changing authority semantics.\n", encoding="utf-8")
    for rel in (
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        "specification/invariant-registry.yaml",
        "specification/decision-registry.yaml",
        "ops/verify_functional_baseline.sh",
    ):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text("Home Assistant Core smart_home source of truth", encoding="utf-8")
    (tmp_path / "docs/ops/P6-4-home-assistant-mutation-boundary-gap-reconciliation-2026-09-22.md").write_text(
        "Status: VERIFIED_LOCAL_SUBSCOPE / P6.4 NOT CLOSED\n", encoding="utf-8")
    for rel in ("ops/mediahub_provider_gateway.py", "ops/mediahub_resilience.py", "tests/test_mediahub_provider_gateway.py", "tests/test_mediahub_resilience.py"):
        (tmp_path / rel).write_text("provider fallback contract", encoding="utf-8")
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P6.5-provider-outage-fallback-gap-reconciliation"


def test_p64_gap_reconciliation_is_selected_after_p63_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "specification").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P6.3 Enforce consent, authorization, command provenance and replay protection.\nP6.4 Route Smart Home mutations through Home Assistant Core.\n",encoding="utf-8")
    for rel in ("specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md","specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml","specification/invariant-registry.yaml","specification/decision-registry.yaml","ops/verify_functional_baseline.sh"):
        (tmp_path / rel).write_text("Home Assistant Core smart_home source of truth",encoding="utf-8")
    (tmp_path / "docs/ops/P6-3-voice-consent-authorization-provenance-replay-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P6.3 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P6.4-home-assistant-mutation-boundary-gap-reconciliation"


def test_p63_gap_reconciliation_is_selected_after_p62_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "specification").mkdir(parents=True); (tmp_path / "docs/architecture").mkdir(parents=True); (tmp_path / "tests/security").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P6.2 Implement each provider through bounded adapters.\nP6.3 Enforce consent, authorization, command provenance and replay protection.\n",encoding="utf-8")
    for rel in ("specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md","docs/architecture/MH-12-authentication.md","docs/architecture/MH-12-authorization.md","docs/architecture/MH-21-device-interaction.md","tests/security/test_mh05_bypass_audit.py"):
        (tmp_path / rel).write_text("consent authorization provenance replay",encoding="utf-8")
    (tmp_path / "docs/ops/P6-2-voice-provider-adapter-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P6.2 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P6.3-voice-consent-authorization-provenance-replay-gap-reconciliation"


def test_p62_gap_reconciliation_is_selected_after_p61_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "specification").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.\nP6.2 Implement each provider through bounded adapters.\n",encoding="utf-8")
    for rel in ("specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml","specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md","ops/verify_functional_baseline.sh"):
        (tmp_path / rel).write_text("Google Assistant Яндекс Алиса Apple Siri",encoding="utf-8")
    (tmp_path / "docs/ops/P6-1-voice-provider-order-gap-reconciliation-2026-09-22.md").write_text("Status: VERIFIED_LOCAL_SUBSCOPE / P6.1 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P6.2-voice-provider-adapter-gap-reconciliation"


def test_p61_gap_reconciliation_is_selected_after_p56_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "specification").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P5.6 Add iOS integration, lifecycle, accessibility and security qualification.\nP6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.\n",encoding="utf-8")
    for rel in ("specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml","specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md","ops/verify_functional_baseline.sh"):
        (tmp_path / rel).write_text("Google Assistant Яндекс Алиса Apple Siri",encoding="utf-8")
    (tmp_path / "docs/ops/P5-6-ios-integration-lifecycle-accessibility-security-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P5.6 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P6.1-voice-provider-order-gap-reconciliation"


def test_p56_gap_reconciliation_is_selected_after_p55_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "contracts/mobile").mkdir(parents=True); (tmp_path / "recovery/acceptance").mkdir(parents=True); (tmp_path / "tests/contracts").mkdir(parents=True); (tmp_path / "docs/architecture").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P5.5 Validate that Mobile Access Layer is not an AI compute tier.\nP5.6 Add iOS integration, lifecycle, accessibility and security qualification.\n",encoding="utf-8")
    for rel in ("contracts/mobile/mobile-api-compatibility.schema.json","recovery/acceptance/F-014-phone-media-io-endpoint.md","recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md","tests/contracts/test_mobile_api_compatibility.py","docs/architecture/MH-21-device-interaction.md"):
        (tmp_path / rel).write_text("ios ipados accessibility lifecycle security",encoding="utf-8")
    (tmp_path / "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md").write_text("Status: VERIFIED_LOCAL_SUBSCOPE / P5.5 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation"


def test_p55_gap_reconciliation_is_selected_after_p54_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "contracts/mobile").mkdir(parents=True); (tmp_path / "ops/ai").mkdir(parents=True); (tmp_path / "recovery/acceptance").mkdir(parents=True); (tmp_path / "docs/architecture").mkdir(parents=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P5.4 Add remote-control and state synchronization tests.\nP5.5 Validate that Mobile Access Layer is not an AI compute tier.\n",encoding="utf-8")
    for rel in ("contracts/mobile/mobile-api-compatibility.schema.json","ops/ai/ai_gateway.py","recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md","docs/architecture/MH-21-device-interaction.md","ops/verify_functional_baseline.sh"):
        (tmp_path / rel).write_text("Mobile Access Layer Local AI Local Cluster AI Cloud Development AI compute tier",encoding="utf-8")
    (tmp_path / "docs/ops/P5-4-remote-control-state-synchronization-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P5.4 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P5.5-mobile-access-not-ai-compute-gap-reconciliation"


def test_p54_gap_reconciliation_is_selected_after_p52_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "contracts/mobile").mkdir(parents=True); (tmp_path / "recovery/acceptance").mkdir(parents=True); (tmp_path / "docs/architecture").mkdir(parents=True); (tmp_path / "ops").mkdir(parents=True); (tmp_path / "tests/security").mkdir(parents=True); (tmp_path / "tests").mkdir(exist_ok=True); (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text("P5.2 Implement authenticated session and authorization contracts.\nP5.4 Add remote-control and state synchronization tests.\n",encoding="utf-8")
    for rel in ("contracts/mobile/mobile-api-compatibility.schema.json","recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md","recovery/acceptance/F-014-phone-media-io-endpoint.md","docs/architecture/MH-21-device-interaction.md","ops/mediahub_lifecycle_contract.py","tests/test_mediahub_lifecycle_contract.py","tests/security/test_mh05_bypass_audit.py"):
        (tmp_path / rel).write_text("remote control state synchronization",encoding="utf-8")
    (tmp_path / "docs/ops/P5-2-authenticated-session-authorization-gap-reconciliation-2026-09-22.md").write_text("Status: DISCOVERY_RECONCILIATION / P5.2 NOT CLOSED\n",encoding="utf-8")
    task=select_local_task(tmp_path)
    assert task is not None and task.task_id == "P5.4-remote-control-state-synchronization-gap-reconciliation"


def test_p52_gap_reconciliation_is_selected_after_p45_evidence(tmp_path):
    from ops.local_autonomous_agent import select_local_task
    (tmp_path / "contracts/mobile").mkdir(parents=True)
    (tmp_path / "ops/ai").mkdir(parents=True)
    (tmp_path / "tests/ai").mkdir(parents=True)
    (tmp_path / "tests/contracts").mkdir(parents=True)
    (tmp_path / "recovery/acceptance").mkdir(parents=True)
    (tmp_path / "recovery/accepted").mkdir(parents=True)
    (tmp_path / "docs/architecture").mkdir(parents=True)
    (tmp_path / "docs/ops").mkdir(parents=True)
    (tmp_path / "ops/local_autonomous_tasks.md").write_text(
        "P4.5 Add audit/revocation and offline/degraded behavior.\n"
        "P5.2 Implement authenticated session and authorization contracts.\n", encoding="utf-8"
    )
    for rel in (
        "contracts/mobile/mobile-api-compatibility.schema.json", "ops/ai/hybrid_session.py",
        "tests/ai/test_hybrid_session.py", "tests/contracts/test_mobile_api_compatibility.py",
        "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        "recovery/acceptance/F-014-phone-media-io-endpoint.md",
        "recovery/accepted/F-007-users-identity-access-authorization.md",
        "docs/architecture/MH-12-authentication.md", "docs/architecture/MH-12-authorization.md",
    ):
        (tmp_path / rel).write_text("mobile session authorization revocation offline", encoding="utf-8")
    (tmp_path / "docs/ops/P4-5-audit-revocation-offline-degraded-gap-reconciliation-2026-09-22.md").write_text(
        "Status: DISCOVERY_RECONCILIATION / P4.5 NOT CLOSED\n", encoding="utf-8"
    )
    task = select_local_task(tmp_path)
    assert task is not None and task.task_id == "P5.2-authenticated-session-authorization-gap-reconciliation"


def test_queue_encoding_marks_current_p45_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "ops").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P4.5 Add audit/revocation and offline/degraded behavior.\n", encoding="utf-8"
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P4.5"] == "ENCODED"


def test_queue_encoding_marks_current_p91_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "security").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P9.1 Full threat-model refresh against current architecture.\n", encoding="utf-8"
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P9.1"] == "ENCODED"


def test_queue_encoding_marks_current_p96_and_p97_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "tests" / "runtime").mkdir(parents=True)
    (tmp_path / "tests" / "security").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P9.6 Fuzz/malformed-input tests for public contracts where justified.\n"
        "P9.7 Recovery and tamper-evidence tests.\n", encoding="utf-8"
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P9.6"] == "ENCODED"
    assert rows["P9.7"] == "ENCODED"


def test_queue_encoding_marks_current_p95_evidence_encoded(tmp_path, monkeypatch):
    from ops.local_autonomous_agent import inspect_queue_encoding
    monkeypatch.setattr("ops.local_autonomous_agent._current_evidence_marker", lambda root, path, marker: True)
    (tmp_path / "ops").mkdir(parents=True)
    (tmp_path / "docs" / "architecture").mkdir(parents=True)
    (tmp_path / "ops" / "local_autonomous_tasks.md").write_text(
        "P9.5 Credential broker isolation and revocation tests.\n", encoding="utf-8"
    )
    rows = {row.queue_id: row.status for row in inspect_queue_encoding(tmp_path)}
    assert rows["P9.5"] == "ENCODED"


def test_raw_queue_compiler_encodes_p81_escalation_path_from_existing_surfaces(tmp_path):
    from ops.local_autonomous_agent import compile_next_raw_queue_task
    for rel in (
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md",
        "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md",
        "ops/mediahub_provider_gateway.py",
        "ops/cloud_development_adapter.py",
    ):
        q=tmp_path/rel
        q.parent.mkdir(parents=True, exist_ok=True)
        q.write_text("existing evidence\n", encoding="utf-8")
    queue=tmp_path/"ops/local_autonomous_tasks.md"
    queue.parent.mkdir(parents=True, exist_ok=True)
    queue.write_text("P8.1 Validate escalation path: Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI.\n", encoding="utf-8")
    task=compile_next_raw_queue_task(tmp_path)
    assert task is not None
    assert task.task_id == "P8.1-escalation-path-reconciliation"
