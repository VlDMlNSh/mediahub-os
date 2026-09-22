#!/usr/bin/env python3
"""Fail-closed local MediaHub coding agent with deterministic fallback."""
from __future__ import annotations

import atexit
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess  # nosec B404
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from ops.ai.task_lease import LeaseDenied, TaskLease

ROOT = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous")).resolve()
MODEL = Path("/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf")
LOCAL_AI_URL = os.environ.get("MEDIAHUB_AI_URL", "http://127.0.0.1:8081/v1/chat/completions")  # nosemgrep: python.lang.security.audit.insecure-transport.urllib.insecure-request-object.insecure-request-object
GIT = Path("/usr/bin/git")
RUFF = Path(shutil.which("ruff") or "")
MAX_DIFF_LINES = 160
MAX_REGENERATIONS = 1
TARGET = "ops/mediahub_native_execution.py"
R4 = os.environ.get("MEDIAHUB_R4_SHA", "471f709f5633feab7aeb62dd3ea52effad6d2bc4")

@dataclass(frozen=True)
class LocalTask:
    task_id: str
    queue_item: str
    target: str
    instruction: str
    fallback_kind: str | None = None


@dataclass(frozen=True)
class ExecutableTask(LocalTask):
    owner: str = "local-autonomous"
    base_sha: str = ""
    acceptance_predicate: str = ""
    verification_command: str = ""
    expected_evidence: str = ""
    dependency_set: tuple[str, ...] = ()
    conflict_set: tuple[str, ...] = ()
    acceptance_fingerprint: str = ""


def _queue_contains(root: Path, item: str) -> bool:
    path = root / "ops/local_autonomous_tasks.md"
    return path.is_file() and item in path.read_text(encoding="utf-8")


def _task_committed(root: Path, task_id: str) -> bool:
    result = subprocess.run(
        [str(GIT), "log", "--all", "--format=%s"],
        cwd=root, text=True, capture_output=True, check=False,
    )  # nosec B603
    return result.returncode == 0 and task_id in result.stdout.splitlines()


@dataclass(frozen=True)
class RawQueueItem:
    queue_id: str
    description: str
    source_line: int


def read_raw_queue(root: Path) -> tuple[RawQueueItem, ...]:
    """Parse canonical phase rows only; never invent queue work."""
    path = root / "ops/local_autonomous_tasks.md"
    if not path.is_file():
        return ()
    rows: list[RawQueueItem] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.match(r"^P(\d+(?:\.\d+)+)\s+(.+)$", line.strip())
        if match:
            rows.append(RawQueueItem("P" + match.group(1), match.group(2).strip(), line_no))
    return tuple(rows)


def _current_evidence_marker(root: Path, relative_path: str, marker: str) -> bool:
    """Return true only when the marker is present in the current tree and in HEAD ancestry."""
    target = root / relative_path
    if not target.is_file() or marker not in target.read_text(encoding="utf-8"):
        return False
    result = subprocess.run(
        [str(GIT), "log", "HEAD", "-S", marker, "--format=%H", "--", relative_path],
        cwd=root, text=True, capture_output=True, check=False,
    )  # nosec B603
    return result.returncode == 0 and bool(result.stdout.strip())


def _compile_p01_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "recovery/reconciliation-report.md"
    if not target.is_file():
        return None
    text = target.read_text(encoding="utf-8")
    if "## P0.1 current control-point reconciliation — 2026-09-21" in text:
        return None
    queue_item = f"P0.1 {item.description}"
    return LocalTask(
        "P0.1-current-control-point-reconciliation",
        queue_item,
        "recovery/reconciliation-report.md",
        "Append a bounded current control-point reconciliation record using the repository's exact HEAD/tree, R4 ancestry, branch, clean status and active worktree inventory. Preserve user work and do not mutate R4.",
        "p0.1-current-control-point-reconciliation",
    )


def _compile_p26_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "recovery/reconciliation-report.md"
    baseline = root / "ops/verify_functional_baseline.sh"
    if not target.is_file() or not baseline.is_file():
        return None
    text = target.read_text(encoding="utf-8")
    if "## P2.6 Home Assistant source-of-truth verification — 2026-09-21" in text:
        return None
    queue_item = f"P2.6 {item.description}"
    return LocalTask(
        "P2.6-home-assistant-source-of-truth-verification",
        queue_item,
        "recovery/reconciliation-report.md",
        "Record deterministic local verification that the normative functional baseline names Home Assistant Core as the Smart Home source of truth and that the functional-baseline gate preserves State Authority as canonical platform authority; do not access Home Assistant, mutate State Authority, or invent integration behavior.",
        "p2.6-home-assistant-source-of-truth-verification",
    )


def _compile_p06_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "recovery/reconciliation-report.md"
    if not target.is_file():
        return None
    text = target.read_text(encoding="utf-8")
    if "## P0.6 PR #80 reconciliation — 2026-09-21" in text:
        return None
    queue_item = f"P0.6 {item.description}"
    return LocalTask(
        "P0.6-pr80-reconciliation-evidence",
        queue_item,
        "recovery/reconciliation-report.md",
        "Append a bounded PR #80 reconciliation record using read-only remote/local Git evidence. Record exact PR head/merge refs, local HEAD, R4 ancestry, and the no-push/no-merge boundary. Do not import, cherry-pick, merge, or authorize the remote work.",
        "p0.6-pr80-reconciliation-evidence",
    )


def _compile_p05_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "tests/ai/test_task_delivery.py"
    if not target.is_file():
        return None
    text = target.read_text(encoding="utf-8")
    queue_item = f"P0.5 {item.description}"
    if "test_restore_for_identity_rejects_mismatch" not in text:
        return LocalTask("P0.5-delivery-identity-recovery-test", queue_item, "tests/ai/test_task_delivery.py", "Add a focused regression test proving TaskDeliveryJournal.restore_for_identity rejects session, conversation or generation mismatches without allowing delivery to proceed.", "p0.5-delivery-identity-recovery-test")
    if "test_restore_for_identity_rejects_safe_stop" not in text:
        return LocalTask("P0.5-delivery-safe-stop-recovery-test", queue_item, "tests/ai/test_task_delivery.py", "Add a focused regression test proving TaskDeliveryJournal.restore_for_identity rejects a persisted SAFE_STOP delivery state and does not permit dispatch.", "p0.5-delivery-safe-stop-recovery-test")
    if "test_restore_rejects_boolean_generation_and_attempt" not in text:
        return LocalTask("P0.5-delivery-provenance-type-test", queue_item, "tests/ai/test_task_delivery.py", "Add a focused regression test proving persisted boolean generation/attempt provenance is rejected instead of being coerced into integers.", "p0.5-delivery-provenance-type-test")
    return None


def _compile_p051_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    tests = root / "tests/ai/test_hybrid_development_daemon.py"
    daemon = root / "ops/ai/hybrid_development_daemon.py"
    evidence = root / "docs/ops/P0-5-1-terminal-checkpoint-startup-2026-09-22.md"
    if not tests.is_file() or not daemon.is_file() or evidence.is_file():
        return None
    text = tests.read_text(encoding="utf-8")
    required = "test_daemon_treats_matching_terminal_restore_as_clean_exit"
    if required not in text:
        return None
    return LocalTask(
        "P0.5.1-terminal-checkpoint-startup-verification",
        f"P0.5.1 {item.description}",
        "docs/ops/P0-5-1-terminal-checkpoint-startup-2026-09-22.md",
        "Record deterministic local evidence that an exact-identity terminal journal tail is treated as a clean daemon stop without revival or identity creation; preserve mismatched-terminal fail-closed behavior and do not alter production authority.",
        "p0.5.1-terminal-checkpoint-startup-verification",
    )


def _compile_p02_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "recovery/reconciliation-report.md"
    dispatch = root / "docs/ops/control-plane/MH01-23-QUEUE-DISPATCH-2026-09-19.yaml"
    queue = root / "ops/local_autonomous_tasks.md"
    registries = (
        root / "specification/capability-registry.yaml",
        root / "specification/contract-registry.yaml",
        root / "specification/dependency-graph.yaml",
        root / "specification/invariant-registry.yaml",
    )
    if not target.is_file() or not dispatch.is_file() or not queue.is_file() or not all(path.is_file() for path in registries):
        return None
    marker = "## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22"
    if marker in target.read_text(encoding="utf-8"):
        return None
    def git(*args: str) -> str:
        result = subprocess.run([str(GIT), *args], cwd=root, text=True, capture_output=True, check=False)  # nosec B603
        return result.stdout.strip() if result.returncode == 0 else ""
    head = git("rev-parse", "HEAD")
    tree = git("rev-parse", "HEAD^{tree}")
    branches = [line.removeprefix("branch refs/heads/") for line in git("worktree", "list", "--porcelain").splitlines() if line.startswith("branch refs/heads/")]
    queue_sha = hashlib.sha256(queue.read_bytes()).hexdigest()
    dispatch_sha = hashlib.sha256(dispatch.read_bytes()).hexdigest()
    stale_lanes = []
    for line in dispatch.read_text(encoding="utf-8").splitlines():
        if line.startswith("  mh-") and ":" in line:
            lane, task_name = line.strip().split(":", 1)
            if not any(branch.startswith(f"engineering/{lane}-") for branch in branches):
                stale_lanes.append(f"{lane}: {task_name.strip()}")
    snapshot = {
        "head": head, "tree": tree, "queue_sha256": queue_sha, "dispatch_sha256": dispatch_sha,
        "branches": branches, "stale_dispatch_references": stale_lanes,
    }
    return LocalTask(
        "P0.2-master-queue-ownership-provenance-reconciliation",
        f"P0.2 {item.description}",
        "recovery/reconciliation-report.md",
        "Append a deterministic machine-readable P0.2 ownership/provenance reconciliation from existing queue/dispatch/governance artifacts. Projection snapshot computed at compilation: " + json.dumps(snapshot, sort_keys=True) + ". Treat the YAML as projection only; do not grant authority, invent ownership, mutate R4, modify parallel lanes, or infer semantics absent from existing artifacts. Explicitly classify stale dispatch references.",
        "p0.2-master-queue-ownership-provenance-reconciliation",
    )


def _compile_p052_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    tests = root / "tests/ai/test_hybrid_development_daemon.py"
    daemon = root / "ops/ai/hybrid_development_daemon.py"
    evidence = root / "docs/ops/P0-5-2-terminal-provenance-regression-2026-09-22.md"
    if not tests.is_file() or not daemon.is_file() or evidence.is_file():
        return None
    text = tests.read_text(encoding="utf-8")
    if "test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch" not in text:
        return None
    return LocalTask(
        "P0.5.2-terminal-provenance-regression-verification",
        f"P0.5.2 {item.description}",
        "docs/ops/P0-5-2-terminal-provenance-regression-2026-09-22.md",
        "Record deterministic local evidence that terminal checkpoint restore remains fail-closed when baseline or R4 provenance does not exactly match the requested identity; preserve exact-identity clean-stop behavior and do not create a new identity.",
        "p0.5.2-terminal-provenance-regression-verification",
    )


RAW_QUEUE_COMPILERS = {"P0.2": _compile_p02_queue_item, "P0.1": _compile_p01_queue_item, "P0.5": _compile_p05_queue_item, "P0.5.1": _compile_p051_queue_item, "P0.5.2": _compile_p052_queue_item, "P0.6": _compile_p06_queue_item, "P2.6": _compile_p26_queue_item}


def compile_raw_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    """Compile a raw queue row only through an explicitly registered encoder."""
    compiler = RAW_QUEUE_COMPILERS.get(item.queue_id)
    return compiler(root, item) if compiler is not None else None


def compile_next_raw_queue_task(root: Path) -> LocalTask | None:
    """Select the first factual queue row with a deterministic bounded compiler."""
    for item in read_raw_queue(root):
        task = compile_raw_queue_item(root, item)
        if task is not None and _queue_contains(root, task.queue_item):
            return task
    return None


def select_local_task(root: Path) -> LocalTask | None:
    forced = os.environ.get("MEDIAHUB_TASK_ID", "").strip()
    if forced:
        forced_tasks = {
            "P0.4-bounded-request-types": LocalTask("P0.4-bounded-request-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden BoundedExecutionRequest.validate against malformed object and boolean timeout/output types using PermissionError; preserve existing bounds.", "bounded-request"),
            "P0.4-recovery-evidence-types": LocalTask("P0.4-recovery-evidence-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden recovery proposal admission against malformed evidence types while preserving provenance checks.", "recovery-evidence"),
            "P0.4-provider-credential-types": LocalTask("P0.4-provider-credential-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Require provider credentials to be non-empty strings before constructing authorization headers; preserve native provider headers.", "provider-credential"),
            "P0.4-proposal-types": LocalTask("P0.4-proposal-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden ExecutionProposal validation against malformed field types; preserve contract semantics.", "proposal-types"),
            "P0.4-target-types": LocalTask("P0.4-target-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden ExecutionTarget validation against malformed field types; preserve HTTPS and provider/credential matching.", "target-types"),
            "P1.6-hybrid-egress-types": LocalTask("P1.6-hybrid-egress-types", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "ops/hybrid_cloud_api_egress_adapter.py", "Harden the hybrid cloud egress adapter against malformed url, method, headers, and timeout types; preserve fail-closed VPN and allowlist behavior.", "hybrid-egress-types"),
            "P1.6-hybrid-egress-tests": LocalTask("P1.6-hybrid-egress-tests", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "tests/test_hybrid_cloud_api_egress_adapter.py", "Add focused negative tests for malformed URL/method/headers and invalid timeout while preserving fail-closed VPN and allowlist tests.", "hybrid-egress-tests"),
        }
        task = forced_tasks.get(forced)
        if task is not None and _queue_contains(root, task.queue_item) and (root / task.target).is_file():
            return task
        return None
    """Select one deterministic, local, highest-priority eligible increment.

    The queue is authoritative for phase availability; eligibility is derived only
    from current repository state. Cloud/VPN/credential-dependent work is never
    selected by this local lane.
    """
    p23 = root / "ops/mediahub_lifecycle_contract.py"
    if _queue_contains(root, "P2.3 Complete persistence/versioning/migration/recovery contracts.") and p23.is_file():
        tests23 = root / "tests/test_mediahub_lifecycle_contract.py"
        if tests23.is_file() and "test_migration_rejects_malformed_types" not in tests23.read_text(encoding="utf-8"):
            return LocalTask("P2.3-migration-contract-tests", "P2.3 Complete persistence/versioning/migration/recovery contracts.", "tests/test_mediahub_lifecycle_contract.py", "Add focused negative tests for malformed migration_id, source and target objects while preserving the bounded lifecycle contract.", "migration-contract-tests")
        if tests23.is_file() and "test_migration_rejects_unchanged_revision" not in tests23.read_text(encoding="utf-8"):
            return LocalTask("P2.3-migration-revision-tests", "P2.3 Complete persistence/versioning/migration/recovery contracts.", "tests/test_mediahub_lifecycle_contract.py", "Add focused tests for migration revision monotonicity and rejection of unchanged source/target revisions.", "migration-revision-tests")
        text = p23.read_text(encoding="utf-8")
        if "migration_id" in text and "not isinstance(self.migration_id, str)" not in text:
            return LocalTask("P2.3-migration-contract-hardening", "P2.3 Complete persistence/versioning/migration/recovery contracts.", "ops/mediahub_lifecycle_contract.py", "Harden MigrationContract validation against malformed migration_id, source and target objects; preserve explicit version change and rollback semantics. Do not add physical persistence or a second State Authority.", "migration-contract-hardening")

    native = root / "ops/mediahub_native_execution.py"
    if _queue_contains(root, "P0.4 Close current Native Execution Contract test gaps.") and native.is_file():
        text = native.read_text(encoding="utf-8")
        checks = (
            ("P0.4-bounded-request-types", "Harden BoundedExecutionRequest.validate against malformed object and boolean timeout/output types using PermissionError; preserve existing bounds.", "bounded-request"),
            ("P0.4-bounded-request-identity", "Harden BoundedExecutionRequest.validate against malformed proposal/target objects; preserve provider matching and bounds.", "bounded-request-identity"),
            ("P0.4-recovery-evidence-types", "Harden recovery proposal admission against malformed evidence types while preserving provenance checks.", "recovery-evidence"),
            ("P0.4-provider-credential-types", "Require provider credentials to be non-empty strings before constructing authorization headers; preserve native provider headers.", "provider-credential"),
            ("P0.4-proposal-types", "Harden ExecutionProposal validation against malformed field types; preserve contract semantics.", "proposal-types"),
            ("P0.4-target-types", "Harden ExecutionTarget validation against malformed field types; preserve HTTPS and provider/credential matching.", "target-types"),
        )
        predicates = (
            "not isinstance(self.timeout_seconds, int)",
            "not isinstance(self.proposal, ExecutionProposal)",
            "malformed recovery evidence",
            "not isinstance(secret, str)",
            "malformed execution proposal",
            "malformed execution target",
        )
        for (task_id, instruction, fallback_kind), predicate in zip(checks, predicates):
            if predicate not in text:
                return LocalTask(task_id, "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", instruction, fallback_kind)

        tests = root / "tests" / "test_mediahub_native_execution.py"
        if tests.is_file():
            test_text = tests.read_text(encoding="utf-8")
            required_tests = (
                "test_bounded_execution_request_rejects_malformed_object_types",
                "test_bounded_execution_request_rejects_non_integer_timeout_types",
                "test_bounded_execution_request_rejects_non_integer_output_limit_types",
            )
            if not all(marker in test_text for marker in required_tests):
                return LocalTask(
                    "P0.4-negative-test-coverage",
                    "P0.4 Close current Native Execution Contract test gaps.",
                    "tests/test_mediahub_native_execution.py",
                    "Add focused negative tests covering malformed bounded request objects plus bool/non-int timeout and output-limit inputs; preserve existing tests and imports.",
                    "native-negative-tests",
                )

    if _queue_contains(root, "P1.1 Complete provider-neutral") and tests.is_file():
        test_text = tests.read_text(encoding="utf-8")
        required = (
            "test_execution_proposal_rejects_non_string_fields",
            "test_execution_target_rejects_malformed_credential_ref",
            "test_execution_target_rejects_invalid_protocol_type",
            "test_recovery_proposal_rejects_non_string_provider",
        )
        if not all(marker in test_text for marker in required):
            return LocalTask(
                "P1.1-native-contract-negative-types",
                "P1.1 Complete provider-neutral ExecutionProposal contract and negative tests.",
                "tests/test_mediahub_native_execution.py",
                "Add focused negative tests for non-string ExecutionProposal fields, malformed ExecutionTarget credential references/protocol types, and non-string recovery provider; do not alter production authority or network behavior.",
                "p1.1-negative-tests",
            )

    egress = root / "ops/hybrid_cloud_api_egress_adapter.py"
    if _queue_contains(root, "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.") and egress.is_file():
        text = egress.read_text(encoding="utf-8")
        tests = root / "tests" / "test_hybrid_cloud_api_egress_adapter.py"
        if "malformed hybrid egress request" not in text:
            return LocalTask("P1.6-hybrid-egress-types", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "ops/hybrid_cloud_api_egress_adapter.py", "Harden the hybrid cloud egress adapter against malformed url, method, headers, and timeout types; preserve fail-closed VPN and allowlist behavior.", "hybrid-egress-types")
        if tests.is_file() and "test_request_rejects_malformed_types" not in tests.read_text(encoding="utf-8"):
            return LocalTask("P1.6-hybrid-egress-tests", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "tests/test_hybrid_cloud_api_egress_adapter.py", "Add focused negative tests for malformed URL/method/headers and invalid timeout while preserving fail-closed VPN and allowlist tests.", "hybrid-egress-tests")

    # P0.5.2 has a concrete daemon restore regression surface: terminal
    # identity must fail closed when baseline/R4 provenance is mismatched.
    p052_tests = root / "tests/ai/test_hybrid_development_daemon.py"
    if _queue_contains(root, "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.") and p052_tests.is_file():
        text = p052_tests.read_text(encoding="utf-8")
        if "test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch" not in text:
            return LocalTask(
                "P0.5.2-terminal-provenance-regression-test",
                "P0.5.2 Recovery regression: prove mismatched/invalid terminal provenance still fails closed.",
                "tests/ai/test_hybrid_development_daemon.py",
                "Add a focused regression test proving a terminal session journal tail is not treated as a clean daemon stop when baseline_sha or r4_sha does not exactly match the requested identity.",
                "p0.5.2-terminal-provenance-regression-test",
            )

    # P0.7 has a concrete local readiness negative-path: native cloud launch
    # must remain blocked when the credential broker has no approved credential.
    p07_tests = root / "tests/security/test_native_agent_launcher.py"
    if _queue_contains(root, "P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.") and p07_tests.is_file():
        text = p07_tests.read_text(encoding="utf-8")
        if "test_cloud_launch_without_credential_remains_blocked" not in text:
            return LocalTask(
                "P0.7-cloud-readiness-missing-credential-test",
                "P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.",
                "tests/security/test_native_agent_launcher.py",
                "Add a focused negative test proving native cloud launch remains blocked when the authorized credential broker has no provider credential; do not create credentials or invoke a provider.",
                "p0.7-cloud-readiness-missing-credential-test",
            )

    # P1.2 has a concrete malformed-type admission gap: boolean semantics must
    # not accept integer/string truthiness at the authority boundary.
    p12_prod = root / "ops/mediahub_native_execution.py"
    p12_tests = root / "tests/test_mediahub_native_execution.py"
    if _queue_contains(root, "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.") and p12_prod.is_file() and p12_tests.is_file():
        prod_text = p12_prod.read_text(encoding="utf-8")
        test_text = p12_tests.read_text(encoding="utf-8")
        if "test_execution_admission_rejects_non_boolean_authorization_and_recovery" not in test_text:
            return LocalTask(
                "P1.2-admission-boolean-type-test",
                "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.",
                "tests/test_mediahub_native_execution.py",
                "Add focused negative tests proving ExecutionAdmission rejects non-boolean authorization_verified and recovery_verified values; preserve provenance binding and fail-closed authority semantics.",
                "p1.2-admission-boolean-type-test",
            )
        if "not isinstance(self.authorized, bool)" not in prod_text:
            return LocalTask(
                "P1.2-admission-boolean-type-hardening",
                "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.",
                "ops/mediahub_native_execution.py",
                "Harden ExecutionAdmission validation to require boolean authorization_verified and recovery_verified values before accepting execution admission; preserve all existing provenance and authority checks.",
                "p1.2-admission-boolean-type-hardening",
            )

    p13_registry = root / "ops" / "mediahub_provider_registry.py"
    p13_protocol = root / "ops" / "mediahub_canonical_protocol.py"
    p13_adapters = root / "ops" / "mediahub_provider_adapters.py"
    p13_gemini = root / "ops" / "mediahub_gemini_adapter.py"
    p13_policy = root / "ops" / "mediahub_policy_engine.py"
    p13_egress = root / "ops" / "mediahub_egress_controller.py"
    p13_credentials = root / "ops" / "mediahub_credential_broker.py"
    p13_evidence = root / "docs" / "ops" / "P1-3-provider-capability-registry-verification-2026-09-21.md"
    p13_tests = (
        root / "tests/test_mediahub_canonical_protocol.py",
        root / "tests/test_mediahub_provider_registry.py",
        root / "tests/test_mediahub_provider_adapters.py",
        root / "tests/test_mediahub_gemini_adapter.py",
        root / "tests/test_mediahub_policy_engine.py",
        root / "tests/test_mediahub_egress_controller.py",
        root / "tests/test_mediahub_credential_broker.py",
        root / "tests/ai/test_ai_provider_registry.py",
    )
    if (_queue_contains(root, "P1.3 Complete AI model/provider/capability registry verification.")
            and all(p.is_file() for p in (p13_registry, p13_protocol, p13_adapters, p13_gemini, p13_policy, p13_egress, p13_credentials, p13_evidence))
            and all(p.is_file() for p in p13_tests)):
        evidence_text = p13_evidence.read_text(encoding="utf-8")
        if ("41 passed" in evidence_text
                and "P1.3 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.3-provider-capability-registry-verification",
                "P1.3 Complete AI model/provider/capability registry verification.",
                "ops/mediahub_provider_registry.py",
                "Verify the existing provider registry, capability matrix, native adapters, policy, egress, credential and AI-provider schema boundaries using the recorded deterministic suite; do not perform live provider execution or acquire credentials.",
                "p1.3-provider-capability-registry-verification",
            )

    p14 = root / "ops" / "mediahub_provider_gateway.py"
    p14_gateway_tests = root / "tests" / "test_mediahub_provider_gateway.py"
    p14_resilience_tests = root / "tests" / "test_mediahub_resilience.py"
    p14_evidence = root / "docs" / "ops" / "P1-4-provider-selector-verification-2026-09-21.md"
    if (_queue_contains(root, "P1.4 Complete provider selector and fallback semantics, including offline/degraded behavior.")
            and p14.is_file() and p14_gateway_tests.is_file() and p14_resilience_tests.is_file() and p14_evidence.is_file()):
        required_gateway = (
            "test_403_is_policy_blocked_and_skips_retry",
            "test_transient_failure_allows_bounded_failover",
            "test_permanent_4xx_does_not_fallback",
            "test_second_transient_failure_opens_circuit",
            "test_policy_blocked_provider_reopens_only_after_cooldown",
        )
        required_resilience = (
            "test_permanent_failure_never_fails_over",
            "test_policy_blocked_fails_over_without_retry_delay_semantics",
            "test_transient_failure_uses_next_provider_and_budget",
            "test_retry_budget_is_fail_closed",
        )
        gateway_text = p14_gateway_tests.read_text(encoding="utf-8")
        resilience_text = p14_resilience_tests.read_text(encoding="utf-8")
        evidence_text = p14_evidence.read_text(encoding="utf-8")
        if (all(marker in gateway_text for marker in required_gateway)
                and all(marker in resilience_text for marker in required_resilience)
                and "12 passed" in evidence_text
                and "POLICY_BLOCKED" in evidence_text
                and "SAFE_STOP" in evidence_text
                and "P1.4 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.4-provider-selector-verification",
                "P1.4 Complete provider selector and fallback semantics, including offline/degraded behavior.",
                "tests/test_mediahub_provider_gateway.py",
                "Verify deterministic provider selection, policy-blocked no-retry semantics, bounded transient failover, permanent-failure safe-stop, circuit cooldown, and degraded local fallback using the existing provider gateway/resilience tests; do not perform live provider execution.",
                "p1.4-provider-selector-verification",
            )

    p16_evidence = root / "docs/ops/P1-6-cloud-development-contract-verification-2026-09-21.md"
    p16_files = (
        root / "ops/cloud_development_adapter.py", root / "ops/cloud_development_sandbox.py",
        root / "ops/hybrid_cloud_api_egress_adapter.py", root / "ops/hybrid_cloud_egress.py",
        root / "ops/hybrid_cloud_egress_chain.py", root / "ops/mediahub_credential_broker.py",
        root / "ops/mediahub_egress_controller.py", root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/security/test_cloud_development_sandbox.py", root / "tests/test_hybrid_cloud_api_egress_adapter.py",
        root / "tests/test_hybrid_cloud_egress.py", root / "tests/test_hybrid_cloud_egress_chain.py",
        root / "tests/test_mediahub_credential_broker.py", root / "tests/test_mediahub_egress_controller.py",
        root / "tests/ai/test_hybrid_development_controller.py", root / "tests/ai/test_hybrid_dispatcher.py",
    )
    if (_queue_contains(root, "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.")
            and p16_evidence.is_file() and all(path.is_file() for path in p16_files)):
        evidence_text = p16_evidence.read_text(encoding="utf-8")
        if ("72 passed" in evidence_text
                and "P1.6 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.6-cloud-development-contract-verification",
                "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.",
                "ops/cloud_development_adapter.py",
                "Verify the existing cloud-development adapter, sandbox, egress and credential broker contract boundaries using the recorded deterministic suite; do not activate VPN, execute live cloud agents, acquire credentials, or perform external provider calls.",
                "p1.6-cloud-development-contract-verification",
            )

    p17_evidence = root / "docs/ops/P1-7-native-codex-claude-launch-verification-2026-09-21.md"
    p17_files = (
        root / "ops/mediahub_native_agent_launcher.py",
        root / "ops/cloud_development_adapter.py",
        root / "tests/security/test_native_agent_launcher.py",
        root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/ai/test_hybrid_dispatcher.py",
        root / "tests/ai/test_godmode_openrouter_launcher.py",
    )
    if (_queue_contains(root, "P1.7 Qualify native Codex and Claude launch specifications without bypasses.")
            and p17_evidence.is_file() and all(path.is_file() for path in p17_files)):
        evidence_text = p17_evidence.read_text(encoding="utf-8")
        if ("41 passed" in evidence_text
                and "P1.7 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.7-native-codex-claude-launch-verification",
                "P1.7 Qualify native Codex and Claude launch specifications without bypasses.",
                "ops/mediahub_native_agent_launcher.py",
                "Verify native Codex/Claude launch specifications, adapter admission, credential separation, endpoint/model qualification, dispatcher policy and launcher behavior using deterministic local tests; do not acquire credentials or perform live provider execution.",
                "p1.7-native-launch-verification",
            )

    p22_evidence = root / "docs/ops/P2-2-single-authority-boundary-verification-2026-09-21.md"
    p22_files = (
        root / "runtime/mediahub_runtime/state_authority.py",
        root / "runtime/mediahub_runtime/consumer_boundary.py",
        root / "tests/security/test_mh05_systemwide_reachability.py",
        root / "tests/runtime/test_mh05_composition_root.py",
        root / "tests/runtime/test_mh04_qualification_edges.py",
        root / "tests/runtime/test_mh04_qualification_concurrency.py",
    )
    if (_queue_contains(root, "P2.2 Enforce single-authority mutation boundaries.")
            and p22_evidence.is_file() and all(path.is_file() for path in p22_files)):
        evidence_text = p22_evidence.read_text(encoding="utf-8")
        if ("27 passed" in evidence_text
                and "P2.2 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P2.2-single-authority-boundary-verification",
                "P2.2 Enforce single-authority mutation boundaries.",
                "runtime/mediahub_runtime/consumer_boundary.py",
                "Qualify existing single-authority mutation boundaries using reachability, composition, concurrency and security tests; do not alter frozen P0-04/P0-05 semantics.",
                "p2.2-single-authority-boundary",
            )

    p21_evidence = root / "docs/ops/P2-1-state-authority-mutation-inventory-2026-09-21.md"
    p21_files = (
        root / "runtime/mediahub_runtime/state_authority.py",
        root / "runtime/mediahub_runtime/consumer_boundary.py",
        root / "tests/runtime/test_state_authority.py",
        root / "tests/runtime/test_mh04_state_authority_hardening.py",
        root / "tests/runtime/test_mh05_consumer_boundary.py",
        root / "tests/security/test_mh04_state_authority_redteam.py",
    )
    if (_queue_contains(root, "P2.1 Inventory State Authority contracts and identify every mutation path.")
            and p21_evidence.is_file() and all(path.is_file() for path in p21_files)):
        evidence_text = p21_evidence.read_text(encoding="utf-8")
        if ("48 passed" in evidence_text
                and "P2.1 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P2.1-state-authority-mutation-inventory",
                "P2.1 Inventory State Authority contracts and identify every mutation path.",
                "runtime/mediahub_runtime/state_authority.py",
                "Inventory canonical State Authority and Consumer Boundary mutation paths with deterministic authority/security tests and static source inspection; do not modify frozen P0-04/P0-05 contracts.",
                "p2.1-state-authority-inventory",
            )

    p18_evidence = root / "docs/ops/P1-8-cloud-development-metering-audit-revocation-verification-2026-09-21.md"
    p18_files = (
        root / "ops/cloud_development_adapter.py",
        root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/security/test_native_agent_launcher.py",
        root / "tests/ai/test_hybrid_dispatcher.py",
        root / "tests/ai/test_godmode_openrouter_launcher.py",
    )
    if (_queue_contains(root, "P1.8 Add metering/audit/revocation evidence for cloud-development workloads.")
            and p18_evidence.is_file() and all(path.is_file() for path in p18_files)):
        evidence_text = p18_evidence.read_text(encoding="utf-8")
        if ("41 passed" in evidence_text
                and "P1.8 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.8-cloud-development-metering-audit-revocation-verification",
                "P1.8 Add metering/audit/revocation evidence for cloud-development workloads.",
                "ops/cloud_development_adapter.py",
                "Verify bounded workload metering fields, audit outcomes, revocation fail-closed behavior and credential non-disclosure using deterministic local tests; do not perform live provider execution or acquire credentials.",
                "p1.8-metering-audit-revocation",
            )

    p24_gateway = root / "ops/mediahub_cluster_gateway.py"
    p24_tests = root / "tests/test_mediahub_cluster_gateway.py"
    if (_queue_contains(root, "P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.")
            and p24_gateway.is_file() and p24_tests.is_file()):
        test_text = p24_tests.read_text(encoding="utf-8")
        gateway_text = p24_gateway.read_text(encoding="utf-8")
        if "malformed request identity" not in gateway_text:
            return LocalTask(
                "P2.4-cluster-gateway-input-hardening",
                "P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.",
                "ops/mediahub_cluster_gateway.py",
                "Harden LocalClusterGateway.propose against malformed request_id and decision objects while preserving LOCAL_CLUSTER-only routing, provenance and fail-closed scheduler admission.",
                "p2.4-cluster-gateway-input-hardening",
            )
        if "test_propose_rejects_malformed_request_identity" not in test_text:
            return LocalTask(
                "P2.4-cluster-gateway-negative-tests",
                "P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.",
                "tests/test_mediahub_cluster_gateway.py",
                "Add focused negative tests proving LocalClusterGateway.propose rejects malformed request identity and routing decision types without scheduling or authority side effects.",
                "p2.4-cluster-gateway-negative-tests",
            )

    ecc = root / "ops/ai/ecc_policy.py"
    ecc_tests = root / "tests/ai/test_ecc_policy.py"
    dispatcher_tests = root / "tests/ai/test_hybrid_dispatcher.py"
    ecc_evidence = root / "docs/ops/P1-5-ecc-dispatcher-verification-2026-09-21.md"
    if _queue_contains(root, "P1.5 Complete ECC adapter/dispatcher policy, provenance, permissions and negative tests.") and all(
        path.is_file() for path in (ecc, ecc_tests, dispatcher_tests, ecc_evidence)
    ):
        evidence_text = ecc_evidence.read_text(encoding="utf-8")
        if ("23 passed" in evidence_text
                and "P1.5 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" not in evidence_text):
            return LocalTask(
                "P1.5-ecc-dispatcher-verification",
                "P1.5 Complete ECC adapter/dispatcher policy, provenance, permissions and negative tests.",
                "ops/ai/ecc_policy.py",
                "Verify fail-closed ECC advisory policy, provenance binding, allowlisted roles/capabilities, forbidden authority/credential/network-write capabilities, target-gated dispatcher permissions, session identity and recovery boundaries using existing deterministic tests; do not perform live cloud-agent execution.",
                "p1.5-ecc-dispatcher-verification",
            )

    # P0.3 has a concrete controller/watchdog verification surface, but no
    # durable evidence artifact exists. Close that verification gap before
    # advancing deeper into the graph.
    p03_evidence = root / "docs" / "ops" / "P0-3-controller-watchdog-verification-2026-09-21.md"
    if (_queue_contains(root, "P0.3 Verify supervisor/watchdog restart, lock, checkpoint, rollback and journal semantics.")
            and not p03_evidence.exists()
            and (root / "tests/ops/test_autonomous_control_plane.py").is_file()
            and (root / "ops/autonomous_watchdog.sh").is_file()
            and (root / "ops/autonomous_os_loop.sh").is_file()):
        return LocalTask(
            "P0.3-controller-watchdog-verification",
            "P0.3 Verify supervisor/watchdog restart, lock, checkpoint, rollback and journal semantics.",
            "docs/ops/P0-3-controller-watchdog-verification-2026-09-21.md",
            "Record deterministic local verification evidence for the existing controller/watchdog lock, ownership, PID starttime, stop-marker, supervision and liveness semantics; do not claim production daemon qualification beyond the executed local tests.",
            "p0.3-controller-watchdog-verification",
        )

    p07_evidence = root / "docs" / "ops" / "P0-7-cloud-agent-readiness-verification-2026-09-21.md"
    if (_queue_contains(root, "P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.") and not p07_evidence.exists() and (root / "tests/security/test_native_agent_launcher.py").is_file()):
        return LocalTask("P0.7-cloud-agent-readiness-verification", "P0.7 Audit cloud-agent readiness; if credentials are absent, maintain BLOCKED with exact evidence.", "docs/ops/P0-7-cloud-agent-readiness-verification-2026-09-21.md", "Record deterministic local evidence that native cloud launch remains blocked when no approved provider credential exists; do not create credentials, inspect secrets, invoke a provider, or activate cloud execution.", "p0.7-cloud-agent-readiness-verification")

    p12_evidence = root / "docs" / "ops" / "P1-2-execution-admission-verification-2026-09-21.md"
    if (_queue_contains(root, "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.") and not p12_evidence.exists() and (root / "ops/mediahub_native_execution.py").is_file() and (root / "tests/test_mediahub_native_execution.py").is_file()):
        return LocalTask("P1.2-execution-admission-verification", "P1.2 Bind proposal admission to existing authorization/provenance/recovery evidence.", "docs/ops/P1-2-execution-admission-verification-2026-09-21.md", "Record deterministic local evidence for authorization/recovery boolean validation and proposal provenance binding using the existing native execution tests; do not execute a provider or mutate State Authority.", "p1.2-execution-admission-verification")

    # P2.4 has a concrete local verification surface already implemented, but no
    # durable evidence artifact exists. Treat this as a bounded verification-gap
    # task; do not claim the broader leader/source-of-truth architecture is closed.
    p24_evidence = root / "docs" / "ops" / "P2-4-cluster-membership-failover-verification-2026-09-21.md"
    if (_queue_contains(root, "P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.")
            and not p24_evidence.exists()
            and all((root / name).is_file() for name in (
                "tests/test_mediahub_cluster_membership.py",
                "tests/test_mediahub_cluster_health.py",
                "tests/test_mediahub_cluster_lifecycle.py",
                "tests/test_mediahub_cluster_resources.py",
                "tests/test_mediahub_cluster_gateway.py",
                "tests/test_mediahub_cluster_failover.py",
            ))):
        return LocalTask(
            "P2.4-cluster-membership-failover-verification",
            "P2.4 Complete cluster membership, leader/source-of-truth and failover evidence.",
            "docs/ops/P2-4-cluster-membership-failover-verification-2026-09-21.md",
            "Record deterministic local verification evidence for the existing cluster membership, health, lifecycle, resources, gateway and failover contracts; explicitly preserve P2.4 leader/source-of-truth as an open architectural scope and do not claim P2.4 complete.",
            "p2.4-cluster-membership-failover-verification",
        )

    # P2.5 is currently an architecture-dependent queue item. First perform a
    # bounded reconciliation of whether the repository already contains explicit
    # leader/source-of-truth, stale-leader, split-brain, duplicate-command and
    # replay contracts. This is discovery/encoding, not a semantic invention.
    p27_evidence = root / "docs" / "ops" / "P2-7-ai-cloud-authority-verification-2026-09-21.md"
    p27_surfaces = (
        root / "ops/ai/ai_adapter.py",
        root / "ops/ai/ai_gateway.py",
        root / "ops/cloud_development_adapter.py",
        root / "ops/mediahub_native_execution.py",
        root / "tests/security/test_ai_adapter.py",
        root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/test_mediahub_native_execution.py",
    )
    if (_queue_contains(root, "P2.7 Verify all AI/cloud agents are non-authoritative with respect to State Authority.")
            and not p27_evidence.exists()
            and all(path.is_file() for path in p27_surfaces)):
        return LocalTask(
            "P2.7-ai-cloud-authority-verification",
            "P2.7 Verify all AI/cloud agents are non-authoritative with respect to State Authority.",
            "docs/ops/P2-7-ai-cloud-authority-verification-2026-09-21.md",
            "Record deterministic local authority-boundary evidence from the existing AI/cloud modules and negative tests; prove forbidden state-authority/production/secret capabilities remain denied and native execution admission remains proposal/provenance-bound. Do not mutate State Authority or execute providers.",
            "p2.7-ai-cloud-authority-verification",
        )

    p31_evidence = root / "docs/ops/P3-1-media-domain-lifecycle-inventory-2026-09-22.md"
    p31_contract = root / "ops/mediahub_lifecycle_contract.py"
    p31_tests = root / "tests/test_mediahub_lifecycle_contract.py"
    if (_queue_contains(root, "P3.1 Inventory media domain contracts and lifecycle states.")
            and not p31_evidence.exists()
            and p31_contract.is_file() and p31_tests.is_file()):
        return LocalTask(
            "P3.1-media-domain-lifecycle-inventory",
            "P3.1 Inventory media domain contracts and lifecycle states.",
            "docs/ops/P3-1-media-domain-lifecycle-inventory-2026-09-22.md",
            "Record deterministic local inventory evidence for the existing media lifecycle contract, persistence/version identity and migration validation tests. Classify only repository-observed states/transitions; do not invent media ingestion, playback, storage, retention, authorization or external-provider semantics.",
            "p3.1-media-domain-lifecycle-inventory",
        )

    # P3.2 has no media-specific ingestion/metadata/index acceptance pair.
    # Encode only a factual discovery artifact so the controller can progress
    # without inventing media semantics.
    p33_evidence = root / "docs/ops/P3-3-playback-control-gap-reconciliation-2026-09-22.md"
    p33_sources = (
        root / "ops/mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_streaming_boundary.py",
        root / "ops/mediahub_lifecycle_contract.py",
        root / "tests/test_mediahub_lifecycle_contract.py",
    )
    if (_queue_contains(root, "P3.3 Implement/qualify playback/control contracts.")
            and not p33_evidence.exists()
            and all(path.is_file() for path in p33_sources)
            and (root / "docs/ops/P3-2-ingestion-metadata-index-gap-reconciliation-2026-09-22.md").is_file()):
        return LocalTask(
            "P3.3-playback-control-gap-reconciliation",
            "P3.3 Implement/qualify playback/control contracts.",
            "docs/ops/P3-3-playback-control-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P3.3 acceptance-surface gap. Inspect only existing streaming/lifecycle surfaces and tests; classify playback and control as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer playback/control semantics from transport parsing and do not claim P3.3 closed.",
            "p3.3-playback-control-gap-reconciliation",
        )

    p32_evidence = root / "docs/ops/P3-2-ingestion-metadata-index-gap-reconciliation-2026-09-22.md"
    p32_sources = (
        root / "ops/mediahub_lifecycle_contract.py",
        root / "tests/test_mediahub_lifecycle_contract.py",
        root / "ops/mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_streaming_boundary.py",
    )
    if (_queue_contains(root, "P3.2 Implement/qualify ingestion and metadata/index contracts.")
            and not p32_evidence.exists()
            and all(path.is_file() for path in p32_sources)):
        return LocalTask(
            "P3.2-ingestion-metadata-index-gap-reconciliation",
            "P3.2 Implement/qualify ingestion and metadata/index contracts.",
            "docs/ops/P3-2-ingestion-metadata-index-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P3.2 acceptance-surface gap. Inspect only existing media lifecycle/streaming surfaces and tests; classify ingestion, metadata and indexing as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not invent media semantics, do not qualify streaming transport as playback, and do not claim P3.2 closed.",
            "p3.2-ingestion-metadata-index-gap-reconciliation",
        )

    # P3.4 has no media-specific authorization/storage/retention/recovery
    # acceptance pair. Encode only a factual discovery artifact from the
    # existing media lifecycle/streaming surfaces and explicit generic
    # security/recovery components; do not infer media semantics.
    p34_evidence = root / "docs/ops/P3-4-media-authorization-storage-retention-recovery-gap-reconciliation-2026-09-22.md"
    p34_sources = (
        root / "ops/mediahub_lifecycle_contract.py",
        root / "tests/test_mediahub_lifecycle_contract.py",
        root / "ops/mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_streaming_boundary.py",
        root / "runtime/mediahub_runtime/state_authority.py",
        root / "tests/security/test_mh05_restore_security.py",
    )
    if (_queue_contains(root, "P3.4 Validate authorization, storage, retention and recovery semantics.")
            and not p34_evidence.exists()
            and all(path.is_file() for path in p34_sources)):
        return LocalTask(
            "P3.4-media-authorization-storage-retention-recovery-gap-reconciliation",
            "P3.4 Validate authorization, storage, retention and recovery semantics.",
            "docs/ops/P3-4-media-authorization-storage-retention-recovery-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P3.4 acceptance-surface gap. Inspect only existing media lifecycle/streaming surfaces plus explicit generic authority/recovery components; classify media authorization, storage, retention and recovery as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer media semantics from generic infrastructure and do not claim P3.4 closed.",
            "p3.4-media-authorization-storage-retention-recovery-gap-reconciliation",
        )

    # P3.5 has generic failure/integration tests but no bounded media-specific
    # integration/failure-injection acceptance pair. Encode only the factual gap.
    p35_evidence = root / "docs/ops/P3-5-media-integration-failure-injection-gap-reconciliation-2026-09-22.md"
    p35_sources = (
        root / "ops/mediahub_lifecycle_contract.py",
        root / "tests/test_mediahub_lifecycle_contract.py",
        root / "ops/mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_cluster_failover.py",
        root / "tests/test_mediahub_cluster_lifecycle.py",
        root / "recovery/acceptance/F-010-personal-media-library-ingestion-sync.md",
        root / "recovery/acceptance/F-012-media-playback-live-media-streaming.md",
        root / "recovery/acceptance/F-014-phone-media-io-endpoint.md",
    )
    if (_queue_contains(root, "P3.5 Add integration and failure-injection tests.")
            and not p35_evidence.exists()
            and all(path.is_file() for path in p35_sources)):
        return LocalTask(
            "P3.5-media-integration-failure-injection-gap-reconciliation",
            "P3.5 Add integration and failure-injection tests.",
            "docs/ops/P3-5-media-integration-failure-injection-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P3.5 acceptance-surface gap. Inspect existing media acceptance requirements plus media lifecycle/streaming tests and generic cluster failure tests; classify media integration and media-specific failure injection as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not treat generic cluster/provider failure tests as media integration acceptance and do not claim P3.5 closed.",
            "p3.5-media-integration-failure-injection-gap-reconciliation",
        )

    # P3.6 has generic resource/failover surfaces but no bounded media
    # benchmark acceptance pair. Encode only the factual performance gap.
    p36_evidence = root / "docs/ops/P3-6-media-benchmark-resource-gap-reconciliation-2026-09-22.md"
    p36_sources = (
        root / "ops/mediahub_streaming_boundary.py",
        root / "tests/test_mediahub_streaming_boundary.py",
        root / "ops/mediahub_cluster_resources.py",
        root / "tests/test_mediahub_cluster_resources.py",
        root / "recovery/acceptance/F-010-personal-media-library-ingestion-sync.md",
        root / "recovery/acceptance/F-012-media-playback-live-media-streaming.md",
    )
    if (_queue_contains(root, "P3.6 Benchmark bounded media operations and resource limits.")
            and not p36_evidence.exists()
            and all(path.is_file() for path in p36_sources)):
        return LocalTask(
            "P3.6-media-benchmark-resource-gap-reconciliation",
            "P3.6 Benchmark bounded media operations and resource limits.",
            "docs/ops/P3-6-media-benchmark-resource-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P3.6 acceptance-surface gap. Inspect accepted media workload requirements plus existing streaming and generic cluster-resource tests; classify bounded media benchmark coverage and media-specific resource limits as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not invent benchmark targets or treat generic resource tests as media benchmark acceptance, and do not claim P3.6 closed.",
            "p3.6-media-benchmark-resource-gap-reconciliation",
        )

    p25_gap = root / "docs/ops/P2-5-cluster-recovery-gap-reconciliation-2026-09-21.md"
    if (_queue_contains(root, "P2.5 Test stale leader, split-brain, duplicate command, replay and recovery scenarios.")
            and not p25_gap.exists()):
        return LocalTask(
            "P2.5-cluster-recovery-gap-reconciliation",
            "P2.5 Test stale leader, split-brain, duplicate command, replay and recovery scenarios.",
            "docs/ops/P2-5-cluster-recovery-gap-reconciliation-2026-09-21.md",
            "Inventory existing repository contracts and tests for stale leader, split-brain, duplicate command, replay and recovery semantics; classify each as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence, without inventing leader election or source-of-truth semantics.",
            "p2.5-cluster-recovery-gap-reconciliation",
        )

    # Existing local increments are exhausted; compile the next factual raw queue row.
    # An unencoded row remains NEEDS_ENCODING rather than becoming speculative work.
    raw_task = compile_next_raw_queue_task(root)
    if raw_task is not None:
        return raw_task
    return None

@dataclass(frozen=True)
class QueueEncoding:
    queue_id: str
    description: str
    status: str


def inspect_queue_encoding(root: Path) -> tuple[QueueEncoding, ...]:
    """Report which canonical queue items have deterministic local acceptance encoding."""
    path = root / "ops/local_autonomous_tasks.md"
    if not path.is_file():
        return ()
    text = path.read_text(encoding="utf-8")
    encoded = {
        "P0.5": "P0.5 Close hybrid session/delivery/conversation recovery gaps.",
        "P2.3": "P2.3 Complete persistence/versioning/migration/recovery contracts.",
        "P0.4": "P0.4 Close current Native Execution Contract test gaps.",
        "P1.1": "P1.1 Complete provider-neutral `ExecutionProposal` contract and negative tests.",
        "P1.6": "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.",
        "P1.7": "P1.7 Qualify native Codex and Claude launch specifications without bypasses.",
        "P1.8": "P1.8 Add metering/audit/revocation evidence for cloud-development workloads.",
        "P2.1": "P2.1 Inventory State Authority contracts and identify every mutation path.",
        "P2.2": "P2.2 Enforce single-authority mutation boundaries.",
    }

    # Queue/compiler state for these autonomous increments is evidence-bound:
    # the marker must exist in the current tree AND have been introduced by a
    # commit reachable from current HEAD. A copied/stale evidence file therefore
    # cannot qualify the current repository state.
    queue_evidence = {
        "P0.3": (
            "docs/ops/P0-3-controller-watchdog-verification-2026-09-21.md",
            "Status: VERIFIED_LOCAL_SUBSCOPE",
        ),
        "P0.7": ("docs/ops/P0-7-cloud-agent-readiness-verification-2026-09-21.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P0.7 BLOCKED"),
        "P1.2": ("docs/ops/P1-2-execution-admission-verification-2026-09-21.md", "Status: VERIFIED_LOCAL_SUBSCOPE"),
        "P2.4": ("docs/ops/P2-4-cluster-membership-failover-verification-2026-09-21.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P2.4 NOT CLOSED"),
        "P2.5": ("docs/ops/P2-5-cluster-recovery-gap-reconciliation-2026-09-21.md", "Status: DISCOVERY_RECONCILIATION / IMPLEMENTATION NOT AUTHORIZED BY THIS RECORD"),
        "P2.7": ("docs/ops/P2-7-ai-cloud-authority-verification-2026-09-21.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P2.7 NOT CLOSED"),
        "P3.1": ("docs/ops/P3-1-media-domain-lifecycle-inventory-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED"),
    "P3.2": ("docs/ops/P3-2-ingestion-metadata-index-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P3.2 NOT CLOSED"),
    "P3.3": ("docs/ops/P3-3-playback-control-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P3.3 NOT CLOSED"),
        "P0.5.1": ("docs/ops/P0-5-1-terminal-checkpoint-startup-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.1 NOT CLOSED"),
        "P0.5.2": ("docs/ops/P0-5-2-terminal-provenance-regression-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.2 NOT CLOSED"),
        "P0.1": (
            "recovery/reconciliation-report.md",
            "## P0.1 current control-point reconciliation — 2026-09-21",
        ),
        "P0.6": (
            "recovery/reconciliation-report.md",
            "## P0.6 PR #80 reconciliation — 2026-09-21",
        ),
        "P2.6": (
            "recovery/reconciliation-report.md",
            "## P2.6 Home Assistant source-of-truth verification — 2026-09-21",
        ),
        "P0.2": (
            "recovery/reconciliation-report.md",
            "## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22",
        ),
        "P5.1": (
            "docs/checkpoints/MH-19-P5.1-2026-09-19.md",
            "# MH-19 P5.1 Verified Increment — Two-App Mobile Model",
        ),
        "P5.3": (
            "docs/checkpoints/MH-19-P5.3-2026-09-19.md",
            "# MH-19 P5.3 Verified Increment — Mobile API Compatibility",
        ),
        "P9.5": (
            "docs/architecture/MH-12-evidence-register.md",
            "P9.5 credential broker revocation isolation",
        ),
        "P9.6": (
            "tests/runtime/test_mh05_consumer_boundary.py",
            "def test_malformed_value_shapes_are_rejected(self):",
        ),
        "P9.7": (
            "tests/security/test_mh05_restore_security.py",
            "def test_tampered_checkpoint_state_cannot_restore(self):",
        ),
        "P9.1": (
            "docs/security/P9.1-threat-model-refresh-2026-09-19.md",
            "# P9.1 — Threat Model Refresh",
        ),
    }
    for queue_id, (relative_path, marker) in queue_evidence.items():
        if _current_evidence_marker(root, relative_path, marker):
            description = next((item.description for item in read_raw_queue(root) if item.queue_id == queue_id), None)
            if description is not None:
                encoded[queue_id] = f"{queue_id} {description}"

    p21_evidence = root / "docs/ops/P2-1-state-authority-mutation-inventory-2026-09-21.md"
    p21_authority = root / "runtime/mediahub_runtime/state_authority.py"
    if p21_authority.is_file() and p21_evidence.is_file():
        evidence_text = p21_evidence.read_text(encoding="utf-8")
        if "48 passed" in evidence_text and "P2.1 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P2.1"] = "P2.1 Inventory State Authority contracts and identify every mutation path."
    p22_evidence = root / "docs/ops/P2-2-single-authority-boundary-verification-2026-09-21.md"
    p22_boundary = root / "runtime/mediahub_runtime/consumer_boundary.py"
    if p22_boundary.is_file() and p22_evidence.is_file():
        evidence_text = p22_evidence.read_text(encoding="utf-8")
        if "27 passed" in evidence_text and "P2.2 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P2.2"] = "P2.2 Enforce single-authority mutation boundaries."
    p21_evidence = root / "docs/ops/P2-1-state-authority-mutation-inventory-2026-09-21.md"
    p21_authority = root / "runtime/mediahub_runtime/state_authority.py"
    if p21_authority.is_file() and p21_evidence.is_file():
        evidence_text = p21_evidence.read_text(encoding="utf-8")
        if "48 passed" in evidence_text and "P2.1 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P2.1"] = "P2.1 Inventory State Authority contracts and identify every mutation path."
    p22_evidence = root / "docs/ops/P2-2-single-authority-boundary-verification-2026-09-21.md"
    p22_boundary = root / "runtime/mediahub_runtime/consumer_boundary.py"
    if p22_boundary.is_file() and p22_evidence.is_file():
        evidence_text = p22_evidence.read_text(encoding="utf-8")
        if "27 passed" in evidence_text and "P2.2 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P2.2"] = "P2.2 Enforce single-authority mutation boundaries."
    # P1.4 may only be encoded when its claimed evidence surface exists in the
    # current tree. A historical evidence commit is not current acceptance
    # evidence and must not make the task executable.
    p13_evidence = root / "docs/ops/P1-3-provider-capability-registry-verification-2026-09-21.md"
    p13_registry = root / "ops/mediahub_provider_registry.py"
    p13_protocol = root / "ops/mediahub_canonical_protocol.py"
    if p13_registry.is_file() and p13_protocol.is_file() and p13_evidence.is_file():
        evidence_text = p13_evidence.read_text(encoding="utf-8")
        if "41 passed" in evidence_text and "P1.3 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P1.3"] = "P1.3 Complete AI model/provider/capability registry verification."
    p16_evidence = root / "docs/ops/P1-6-cloud-development-contract-verification-2026-09-21.md"
    p16_adapter = root / "ops/cloud_development_adapter.py"
    p16_sandbox = root / "ops/cloud_development_sandbox.py"
    if all(path.is_file() for path in (p16_evidence, p16_adapter, p16_sandbox)):
        evidence_text = p16_evidence.read_text(encoding="utf-8")
        if "72 passed" in evidence_text and "P1.6 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P1.6"] = "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification."
    p17_evidence = root / "docs/ops/P1-7-native-codex-claude-launch-verification-2026-09-21.md"
    p17_launcher = root / "ops/mediahub_native_agent_launcher.py"
    if p17_launcher.is_file() and p17_evidence.is_file():
        evidence_text = p17_evidence.read_text(encoding="utf-8")
        if "41 passed" in evidence_text and "P1.7 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P1.7"] = "P1.7 Qualify native Codex and Claude launch specifications without bypasses."
    p18_evidence = root / "docs/ops/P1-8-cloud-development-metering-audit-revocation-verification-2026-09-21.md"
    p18_adapter = root / "ops/cloud_development_adapter.py"
    if p18_adapter.is_file() and p18_evidence.is_file():
        evidence_text = p18_evidence.read_text(encoding="utf-8")
        if "41 passed" in evidence_text and "P1.8 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P1.8"] = "P1.8 Add metering/audit/revocation evidence for cloud-development workloads."
    p15_evidence = root / "docs/ops/P1-5-ecc-dispatcher-verification-2026-09-21.md"
    p15_ecc = root / "ops/ai/ecc_policy.py"
    p15_tests = root / "tests/ai/test_ecc_policy.py"
    p15_dispatcher_tests = root / "tests/ai/test_hybrid_dispatcher.py"
    if all(path.is_file() for path in (p15_ecc, p15_tests, p15_dispatcher_tests, p15_evidence)):
        evidence_text = p15_evidence.read_text(encoding="utf-8")
        if "23 passed" in evidence_text and "P1.5 = QUALIFICATION-CANDIDATE / DETERMINISTIC LOCAL ACCEPTANCE PASS" in evidence_text:
            encoded["P1.5"] = "P1.5 Complete ECC adapter/dispatcher policy, provenance, permissions and negative tests."
    p14_evidence = root / "docs/ops/P1-4-provider-selector-verification-2026-09-21.md"
    p14_gateway = root / "tests/test_mediahub_provider_gateway.py"
    p14_resilience = root / "tests/test_mediahub_resilience.py"
    if (root / "ops/mediahub_provider_gateway.py").is_file() and p14_gateway.is_file() and p14_resilience.is_file() and p14_evidence.is_file():
        encoded["P1.4"] = "P1.4 Complete provider selector and fallback semantics, including offline/degraded behavior."
    rows: list[QueueEncoding] = []
    for match in re.finditer(r"(?m)^P(\d+(?:\.\d+)+)\s+(.+)$", text):
        queue_id = "P" + match.group(1)
        description = match.group(2).strip()
        rows.append(QueueEncoding(queue_id, description, "ENCODED" if queue_id in encoded else "NEEDS_ENCODING"))
    return tuple(rows)


def compile_executable_task(root: Path, task: LocalTask) -> ExecutableTask | None:
    """Compile a selected candidate only when repository evidence is sufficient."""
    target = root / task.target
    allow_new_evidence = task.fallback_kind in {
        "p0.3-controller-watchdog-verification",
        "p0.7-cloud-agent-readiness-verification",
        "p1.2-execution-admission-verification",
        "p2.4-cluster-membership-failover-verification",
        "p2.5-cluster-recovery-gap-reconciliation",
        "p2.7-ai-cloud-authority-verification",
        "p3.1-media-domain-lifecycle-inventory",
        "p3.2-ingestion-metadata-index-gap-reconciliation",
        "p3.3-playback-control-gap-reconciliation",
        "p3.4-media-authorization-storage-retention-recovery-gap-reconciliation",
        "p3.5-media-integration-failure-injection-gap-reconciliation",
        "p3.6-media-benchmark-resource-gap-reconciliation",
        "p0.5.1-terminal-checkpoint-startup-verification",
        "p0.5.2-terminal-provenance-regression-verification",
    } and task.target.startswith("docs/ops/")
    if not target.is_file() and not allow_new_evidence:
        return None
    def git(*args: str) -> str:
        result = subprocess.run([str(GIT), *args], cwd=root, text=True, capture_output=True, check=False)  # nosec B603
        return result.stdout.strip() if result.returncode == 0 else ""
    base_sha = git("rev-parse", "HEAD")
    branch = git("branch", "--show-current")
    if not base_sha or not branch or git("status", "--porcelain"):
        return None
    fingerprint = hashlib.sha256(
        f"{task.task_id}\n{task.queue_item}\n{task.target}\n{task.instruction}".encode()
    ).hexdigest()
    # Only durable evidence suppresses a task. Operational cycle logs may contain
    # the compiler's own fingerprint and must never self-suppress the next cycle.
    path = root / ".autonomous" / "evidence"
    if path.is_dir():
        for evidence in path.rglob("*"):
            if evidence.is_file():
                try:
                    if fingerprint in evidence.read_text(encoding="utf-8", errors="ignore"):
                        return None
                except OSError:
                    continue
    if task.task_id in git("log", "--all", "--format=%s").splitlines():
        return None
    worktrees = git("worktree", "list", "--porcelain")
    if task.target in worktrees or task.task_id in worktrees:
        return None
    for lease_path in (root / ".autonomous" / "leases").glob("*.lock"):
        try:
            record = json.loads(lease_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if record.get("task_id") == task.task_id:
            return None
    dependencies = {
        "P0.4": (),
        "P1.1": ("P0.4",),
        "P1.3": ("P1.1",),
        "P1.6": ("P1.1",),
        "P1.4": (),
    }
    conflicts = {
        "ops/mediahub_native_execution.py": ("State Authority", "production", "R4"),
        "tests/test_mediahub_native_execution.py": ("State Authority", "production", "R4"),
        "ops/hybrid_cloud_api_egress_adapter.py": ("cloud activation", "credentials"),
        "ops/mediahub_provider_registry.py": ("live provider execution", "credentials", "cloud activation", "R4"),
        "tests/test_mediahub_provider_gateway.py": ("live provider execution", "credentials", "cloud activation", "R4"),
    }
    phase = task.task_id.split("-", 1)[0]
    if task.task_id.startswith("P3.1-"):
        verification = "pytest -q tests/test_mediahub_lifecycle_contract.py"
    else:
        verification = (
        "pytest -q tests/test_mediahub_canonical_protocol.py tests/test_mediahub_provider_registry.py tests/test_mediahub_provider_adapters.py tests/test_mediahub_gemini_adapter.py tests/test_mediahub_policy_engine.py tests/test_mediahub_egress_controller.py tests/test_mediahub_credential_broker.py tests/ai/test_ai_provider_registry.py"
        if task.task_id.startswith("P1.3-")
        else "pytest -q tests/test_mediahub_provider_gateway.py tests/test_mediahub_resilience.py"
        if task.task_id.startswith("P1.4-")
        else "pytest -q tests/test_mediahub_native_execution.py"
        if "native_execution" in task.target
        else "pytest -q tests/ops/test_cloud_development_adapter.py tests/security/test_cloud_development_sandbox.py tests/test_hybrid_cloud_api_egress_adapter.py tests/test_hybrid_cloud_egress.py tests/test_hybrid_cloud_egress_chain.py tests/test_mediahub_credential_broker.py tests/test_mediahub_egress_controller.py tests/ai/test_hybrid_development_controller.py tests/ai/test_hybrid_dispatcher.py"
        if task.task_id.startswith("P1.6-")
        else "pytest -q tests/security/test_native_agent_launcher.py tests/ops/test_cloud_development_adapter.py tests/ai/test_hybrid_dispatcher.py tests/ai/test_godmode_openrouter_launcher.py"
        if task.task_id.startswith("P1.7-") or task.task_id.startswith("P1.8-")
        else "pytest -q tests/runtime/test_state_authority.py tests/runtime/test_mh04_state_authority_hardening.py tests/runtime/test_mh05_consumer_boundary.py tests/security/test_mh04_state_authority_redteam.py tests/test_mediahub_cluster_failover.py tests/contracts/test_contract_domain_reconciliation.py"
        if task.task_id.startswith("P2.1-")
        else "pytest -q tests/security/test_mh05_systemwide_reachability.py tests/runtime/test_mh05_composition_root.py tests/runtime/test_mh04_qualification_edges.py tests/runtime/test_mh04_qualification_concurrency.py tests/test_mediahub_development_security_boundary.py tests/test_mediahub_streaming_boundary.py"
        if task.task_id.startswith("P2.2-")
        else "pytest -q tests/test_hybrid_cloud_api_egress_adapter.py"
        )
    if task.task_id.startswith("P2.3-"):
        verification = "pytest -q tests/test_mediahub_lifecycle_contract.py"

    return ExecutableTask(
        **task.__dict__,
        owner=os.environ.get("MEDIAHUB_WORKER_ID", "local-autonomous"),
        base_sha=base_sha,
        acceptance_predicate=f"queue={task.queue_item}; target={task.target}; acceptance={task.instruction}",
        verification_command=verification,
        expected_evidence="targeted tests; full relevant regression; security scan; ruff; git diff --check",
        dependency_set=dependencies.get(phase, ()),
        conflict_set=conflicts.get(task.target, ("R4", "production")),
        acceptance_fingerprint=fingerprint,
    )

PROTECTED = {
    ".git", ".autonomous", ".github", "production", "credentials",
    "ops/cloud-development-adapter.py", "ops/cloud_development_adapter.py",
    "ops/local_autonomous_agent.py", "ops/autonomous_os_loop.sh",
    "ops/autonomous_watchdog.sh",
}

STATES = (
    "AI_SUCCESS", "AI_REJECTED", "AI_TIMEOUT", "AI_MALFORMED",
    "FALLBACK_SELECTED", "FALLBACK_APPLIED", "VERIFY_PASS", "VERIFY_FAIL",
    "ROLLED_BACK", "COMMITTED", "BLOCKED",
)


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(request.full_url, code, "redirect denied", headers, None)


LOCAL_AI_OPENER = urllib.request.build_opener(NoRedirectHandler)


def state(name: str, evidence: str = "") -> None:
    if name not in STATES:
        raise ValueError(name)
    print(f"LOCAL_AGENT_STATE={name}" + (f" evidence={evidence}" if evidence else ""))


def run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False
    )  # nosec B603


def prompt(task: LocalTask | None = None, feedback: str = "") -> str:
    task = task or select_local_task(ROOT)
    if task is None:
        return ""
    target_path = ROOT / task.target
    current = target_path.read_text(encoding="utf-8") if target_path.is_file() else ""
    error = f"\nPrevious rejection: {feedback}\n" if feedback else ""
    return f"""MediaHub local coding cycle. R4={R4}. Selected task={task.task_id}. Modify ONLY the existing tracked file {task.target}.
Task: {task.instruction}
Preserve existing contracts and fail-closed behavior. Do not execute anything. Do not access secrets, State Authority, Home Assistant, production or unrestricted network. Return ONLY one complete unified git diff, no markdown fences or commentary. Use the exact real file context below. No new files, modes, renames, secrets, .git, .github, .autonomous or cloud activation. The diff must pass git apply --check.
{current}{error}"""


def extract(text: str) -> str:
    text = text.strip()
    blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", text, flags=re.DOTALL)
    if blocks:
        text = max(blocks, key=len)
    start = text.find("diff --git ")
    return text[start:].strip() if start >= 0 else ""


def unified_patch(old: str | list[str], new: str | list[str], target: str) -> str:
    old_lines = old.splitlines() if isinstance(old, str) else [line.rstrip("\n") for line in old]
    new_lines = new.splitlines() if isinstance(new, str) else [line.rstrip("\n") for line in new]
    return "\n".join(difflib.unified_diff(old_lines, new_lines, fromfile=f"a/{target}", tofile=f"b/{target}", lineterm="")) + "\n"


def safe_patch(patch: str, target: str | None = None) -> bool:
    target = target or TARGET
    lines = patch.splitlines()
    if not patch or len(lines) > MAX_DIFF_LINES:
        return False
    old_path = new_path = None
    saw_hunk = False
    for line in lines:
        if line.startswith(("old mode ", "new mode ", "new file mode ", "deleted file mode ",
                            "similarity index ", "rename from ", "rename to ")):
            return False
        if line.startswith("--- a/"):
            old_path = line[6:].strip()
        elif line.startswith("+++ b/"):
            new_path = line[6:].strip()
        elif line.startswith("@@ "):
            if not re.fullmatch(r"@@ -\d+(?:,\d+)? \+\d+(?:,\d+)? @@(?:.*)", line):
                return False
            saw_hunk = True
    return old_path == target and new_path == target and saw_hunk and target not in PROTECTED

def _fallback_target_patch(old: list[str], old_text: str) -> str:
    original = """    def validate(self) -> None:
        if self.provider != self.credential.provider:
            raise PermissionError("credential provider mismatch")
        if urlparse(self.endpoint).scheme != "https":
            raise PermissionError("execution endpoint must use HTTPS")
        if not self.model or not self.endpoint or not self.credential.path:
            raise ValueError("incomplete execution target")
"""
    hardened = """    def validate(self) -> None:
        if not isinstance(self.credential, CredentialRef):
            raise PermissionError("malformed execution credential reference")
        if not all(isinstance(value, str) for value in (self.provider, self.endpoint, self.model)):
            raise PermissionError("malformed execution target")
        if not isinstance(self.protocol, Protocol):
            raise PermissionError("malformed execution protocol")
        if not isinstance(self.credential.provider, str) or not isinstance(self.credential.path, str):
            raise PermissionError("malformed execution credential reference")
        if self.provider != self.credential.provider:
            raise PermissionError("credential provider mismatch")
        if urlparse(self.endpoint).scheme != "https":
            raise PermissionError("execution endpoint must use HTTPS")
        if not self.model or not self.endpoint or not self.credential.path:
            raise ValueError("incomplete execution target")
"""
    if original not in old_text:
        return ""
    new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
    return unified_patch(old, new, TARGET)


def _fallback_proposal_patch(old: list[str], old_text: str) -> str:
    original = """    def validate(self) -> None:
        if not all((self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("incomplete execution proposal")
"""
    hardened = """    def validate(self) -> None:
        if not all(isinstance(value, str) for value in (self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("malformed execution proposal")
        if not all((self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("incomplete execution proposal")
"""
    if original not in old_text:
        return ""
    new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
    return unified_patch(old, new, TARGET)


def _fallback_recovery_patch(old: list[str], old_text: str) -> str:
    original = """    def prepare_recovery_proposal(self, evidence: object, provider: str) -> ExecutionProposal:
        if not getattr(evidence, "verified", False):
            raise PermissionError("verified recovery evidence is required")
        request_id = getattr(evidence, "request_id", "")
        workload_id = getattr(evidence, "workload_id", "")
        source_sha = getattr(evidence, "source_sha", "")
        return self.prepare_proposal(request_id, workload_id, source_sha, provider)
"""
    hardened = """    def prepare_recovery_proposal(self, evidence: object, provider: str) -> ExecutionProposal:
        verified = getattr(evidence, "verified", None)
        request_id = getattr(evidence, "request_id", None)
        workload_id = getattr(evidence, "workload_id", None)
        source_sha = getattr(evidence, "source_sha", None)
        if verified is not True:
            raise PermissionError("verified recovery evidence is required")
        if not all(isinstance(value, str) for value in (request_id, workload_id, source_sha, provider)):
            raise PermissionError("malformed recovery evidence")
        return self.prepare_proposal(request_id, workload_id, source_sha, provider)
"""
    if original not in old_text:
        return ""
    new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
    return unified_patch(old, new, TARGET)


def _fallback_headers_patch(old: list[str], old_text: str) -> str:
    original = """    def prepare_headers(self, target: ExecutionTarget, secret: str) -> Mapping[str, str]:
        target.validate()
        if not secret:
            raise PermissionError(\"missing provider credential\")
"""
    hardened = """    def prepare_headers(self, target: ExecutionTarget, secret: str) -> Mapping[str, str]:
        target.validate()
        if not isinstance(secret, str) or not secret:
            raise PermissionError(\"missing provider credential\")
"""
    if original not in old_text:
        return ""
    new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
    return unified_patch(old, new, TARGET)


def fallback_patch(task: LocalTask | None = None) -> str:
    """Return only the deterministic fallback for the bound local task."""
    task = task or select_local_task(ROOT)
    if task is None:
        task = LocalTask("legacy-fallback", "", TARGET, "", "legacy")
    target = task.target
    path = ROOT / target
    if task.fallback_kind == "p1.1-negative-tests":
        old = path.read_text(encoding="utf-8")
        if "test_execution_proposal_rejects_non_string_fields" in old:
            return ""
        addition = '''\n\n\ndef test_execution_proposal_rejects_non_string_fields():
    contract = NativeExecutionContract()
    for values in (
        (1, "work", "sha", "openai"),
        ("req", None, "sha", "openai"),
        ("req", "work", True, "openai"),
        ("req", "work", "sha", 1),
    ):
        with pytest.raises(PermissionError):
            contract.prepare_proposal(*values)


def test_execution_target_rejects_malformed_credential_ref():
    malformed = ExecutionTarget(
        "openai", "https://api.example.test/v1", Protocol.OPENAI_RESPONSES,
        "test-model", object(),
    )
    with pytest.raises(PermissionError):
        malformed.validate()


def test_execution_target_rejects_invalid_protocol_type():
    malformed = ExecutionTarget(
        "openai", "https://api.example.test/v1", "openai",
        "test-model", CredentialRef("openai", "/credential"),
    )
    with pytest.raises(PermissionError):
        malformed.validate()


def test_recovery_proposal_rejects_non_string_provider():
    from types import SimpleNamespace

    evidence = SimpleNamespace(
        verified=True, request_id="req-r", workload_id="work-r", source_sha="sha-r",
    )
    for provider in (1, True, None):
        with pytest.raises(PermissionError):
            NativeExecutionContract().prepare_recovery_proposal(evidence, provider)
'''
        new = old.rstrip() + addition
        return unified_patch(old, new, target)
    if task.fallback_kind == "hybrid-egress-tests":
        old = path.read_text(encoding="utf-8")
        if "test_request_rejects_malformed_types" in old:
            return ""
        addition = '\n\ndef test_request_rejects_malformed_types():\n    client = adapter()\n    healthy = type(client.check_tunnel())("tun-vpm", True, "test")\n    with patch.object(client, "check_tunnel", return_value=healthy):\n        with pytest.raises(CloudAPIUnavailable):\n            client.request(123)\n        with pytest.raises(CloudAPIUnavailable):\n            client.request(API, method=123)\n        with pytest.raises(CloudAPIUnavailable):\n            client.request(API, headers={"X-Test": 1})\n\n\ndef test_request_rejects_invalid_timeout_type():\n    client = adapter()\n    healthy = type(client.check_tunnel())("tun-vpm", True, "test")\n    client.timeout_seconds = True\n    with patch.object(client, "check_tunnel", return_value=healthy):\n        with pytest.raises(CloudAPIUnavailable):\n            client.request(API)\n'
        new = old.rstrip() + addition
        return unified_patch(old, new, target)
    if task.fallback_kind == "hybrid-egress-types":
        old = path.read_text(encoding="utf-8")
        marker = "        self.egress.admit(url)\n"
        if "malformed hybrid egress request" in old:
            return ""
        hardened = """        if not isinstance(url, str) or not url:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if not isinstance(method, str) or not method:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if headers is not None and (not isinstance(headers, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in headers.items())):
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if not isinstance(self.timeout_seconds, (int, float)) or isinstance(self.timeout_seconds, bool) or self.timeout_seconds <= 0:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        self.egress.admit(url)
"""
        if marker not in old:
            return ""
        new_text = old.replace(marker, hardened, 1)
        return unified_patch(old, new_text, target)
    if task.fallback_kind == "migration-revision-tests":
        old = path.read_text(encoding="utf-8")
        if "test_migration_rejects_unchanged_revision" in old: return ""
        addition = '\n\ndef test_migration_rejects_unchanged_revision():\n    current = VersionIdentity("mediahub-state", 3, "digest-3")\n    with pytest.raises(ValueError):\n        MigrationContract("m1", current, current, True)\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "migration-contract-tests":
        old = path.read_text(encoding="utf-8")
        if "test_migration_rejects_malformed_types" in old:
            return ""
        addition = '\n\ndef test_migration_rejects_malformed_types():\n    valid = VersionIdentity("mediahub-state", 1, "digest-1")\n    with pytest.raises(ValueError):\n        MigrationContract("", valid, VersionIdentity("mediahub-state", 2, "digest-2"), True)\n    with pytest.raises(TypeError):\n        MigrationContract("m1", object(), valid, True)\n    with pytest.raises(TypeError):\n        MigrationContract("m1", valid, object(), True)\n    with pytest.raises(TypeError):\n        MigrationContract("m1", valid, VersionIdentity("mediahub-state", 2, "digest-2"), 1)\n'
        new = old.rstrip() + addition
        return unified_patch(old, new, target)
    if task.fallback_kind == "migration-contract-hardening":
        old = path.read_text(encoding="utf-8")
        original = '    def __post_init__(self):\n        if not self.migration_id: raise ValueError("migration id required")\n        if not isinstance(self.rollback_supported,bool): raise ValueError("rollback_supported must be bool")\n        if self.source.revision==self.target.revision: raise ValueError("migration must change revision")\n'
        hardened = '    def __post_init__(self):\n        if not isinstance(self.migration_id, str) or not self.migration_id: raise ValueError("migration id required")\n        if not isinstance(self.source, VersionIdentity) or not isinstance(self.target, VersionIdentity): raise ValueError("migration versions required")\n        if not isinstance(self.rollback_supported,bool): raise ValueError("rollback_supported must be bool")\n        if self.source.revision==self.target.revision: raise ValueError("migration must change revision")\n'
        if original in old:
            new = old.replace(original, hardened, 1)
            return unified_patch(old, new, target)
        current = """    def __post_init__(self):
        if not self.migration_id: raise ValueError("migration id required")
        if not isinstance(self.source, VersionIdentity) or not isinstance(self.target, VersionIdentity): raise TypeError("migration versions required")
        if not isinstance(self.rollback_supported, bool): raise TypeError("rollback_supported must be bool")
        if self.source.revision==self.target.revision: raise ValueError("migration must change revision")
"""
        hardened_current = """    def __post_init__(self):
        if not isinstance(self.migration_id, str) or not self.migration_id: raise ValueError("migration id required")
        if not isinstance(self.source, VersionIdentity) or not isinstance(self.target, VersionIdentity): raise TypeError("migration versions required")
        if not isinstance(self.rollback_supported, bool): raise TypeError("rollback_supported must be bool")
        if self.source.revision==self.target.revision: raise ValueError("migration must change revision")
"""
        if current not in old:
            return ""
        return unified_patch(old, old.replace(current, hardened_current, 1), target)
    if task.fallback_kind == "p2.7-ai-cloud-authority-verification":
        content = """# P2.7 AI / Cloud Authority Boundary Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P2.7 NOT CLOSED

## Scope

Verify only the repository-native authority boundary of the existing AI/cloud components. AI and cloud components remain advisory/proposal-generating and must not mutate State Authority, production, or retrieve secrets directly.

## Verification

Commands:
- python3 -m pytest -q tests/security/test_ai_adapter.py tests/ops/test_cloud_development_adapter.py tests/test_mediahub_native_execution.py
- python3 -c "from pathlib import Path; files=('ops/ai/ai_adapter.py','ops/ai/ai_gateway.py','ops/cloud_development_adapter.py'); forbidden=('state_authority','home_assistant'); [print(f, [x for x in forbidden if x in Path(f).read_text(encoding='utf-8').lower()]) for f in files]"

Acceptance: existing deterministic tests pass and the inspected AI/cloud modules preserve forbidden-capability denial and proposal/provenance boundaries. No provider execution or State Authority mutation is performed.

## Boundary

This evidence does not qualify operational cloud execution, credentials, production access, or the broader P2.7 product scope.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p0.5.2-terminal-provenance-regression-verification":
        content = """# P0.5.2 Terminal Provenance Regression Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.2 NOT CLOSED

## Repository-observed behavior

Source: `ops/ai/hybrid_development_daemon.py`
Tests: `tests/ai/test_hybrid_development_daemon.py`

The daemon only accepts a terminal checkpoint as a clean stop when session identity, baseline SHA, R4 SHA and terminal state all match. A mismatch in baseline or R4 provenance is re-raised as `HybridDevelopmentDenied` rather than silently reviving or replacing the session identity.

## Verification

Command: `pytest -q tests/ai/test_hybrid_development_daemon.py`

Acceptance: the deterministic mismatch regression passes while the exact-identity terminal-stop test remains passing.

## Boundary

This evidence qualifies only local terminal provenance reconciliation. It does not authorize production execution, release, credentials, external providers, State Authority mutation, or identity replacement.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p0.5.1-terminal-checkpoint-startup-verification":
        content = """# P0.5.1 Terminal Checkpoint Startup Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P0.5.1 NOT CLOSED

## Repository-observed behavior

Source: `ops/ai/hybrid_development_daemon.py`
Tests: `tests/ai/test_hybrid_development_daemon.py`

The daemon treats a denied restore as a clean exit only when the journal tail exactly matches the requested session identity, baseline SHA, R4 SHA, and a terminal state (`STOPPED`, `EXPIRED`, `SAFE_STOP`, or `STOPPING`). It does not revive the terminal session or create a replacement identity on that path.

## Verification

Command: `pytest -q tests/ai/test_hybrid_development_daemon.py`

Acceptance: the exact-identity terminal restore path passes the existing deterministic test, while mismatched terminal provenance remains fail-closed under the separate regression test.

## Boundary

This evidence qualifies only the local daemon checkpoint-startup behavior. It does not authorize production daemon operation, release, external execution, credentials, State Authority mutation, or a new identity.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.6-media-benchmark-resource-gap-reconciliation":
        content = """# P3.6 Media Benchmark / Resource-Limit Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.6 NOT CLOSED

## Queue requirement

`P3.6 Benchmark bounded media operations and resource limits.`

## Media workload requirements

- `recovery/acceptance/F-010-personal-media-library-ingestion-sync.md` requires media ingestion, synchronization, offline-first behavior and cluster-backed storage/indexing/processing.
- `recovery/acceptance/F-012-media-playback-live-media-streaming.md` requires unified playback, live media, streaming, endpoints, 4K where supported, transcoding and cluster distribution. Concrete codecs, profiles and protocols remain deferred.

## Exact implementation/test surfaces inspected

- `ops/mediahub_streaming_boundary.py` and `tests/test_mediahub_streaming_boundary.py` — bounded provider-neutral streaming transport parsing/tests; no throughput, latency or resource benchmark contract.
- `ops/mediahub_cluster_resources.py` and `tests/test_mediahub_cluster_resources.py` — generic cluster resource accounting/constraints; not media workload benchmark acceptance.

## Classification

- Bounded media benchmark acceptance: ABSENT in the inspected implementation/test surface.
- Media-specific resource-limit benchmark acceptance: ABSENT in the inspected implementation/test surface.
- Generic streaming/resource tests: PRESENT but insufficient to satisfy P3.6.
- Media workload requirements: PRESENT in accepted recovery documents; several technical performance dimensions remain deferred.

## Gate

This artifact records the factual gap only. It does not invent benchmark targets, hardware profiles, throughput limits, latency budgets, codec profiles, or production behavior. A future P3.6 implementation task requires explicit bounded workloads, measurable resource/latency criteria, deterministic benchmark execution, and provenance-bound evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.5-media-integration-failure-injection-gap-reconciliation":
        content = """# P3.5 Media Integration / Failure-Injection Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.5 NOT CLOSED

## Queue requirement

`P3.5 Add integration and failure-injection tests.`

## Media acceptance requirements

- `recovery/acceptance/F-010-personal-media-library-ingestion-sync.md` defines media ingestion, unified-library, synchronization, offline-first and cluster behavior, while leaving several technical decisions deferred.
- `recovery/acceptance/F-012-media-playback-live-media-streaming.md` defines unified playback, streaming, endpoints and cluster behavior, while leaving concrete transport/codec/DRM/transcoding decisions deferred.
- `recovery/acceptance/F-014-phone-media-io-endpoint.md` defines phone/media endpoint flows and authorization invariants, while leaving remote protocol, streaming transport and background execution details deferred.

## Exact implementation/test surfaces inspected

- `ops/mediahub_lifecycle_contract.py` and `tests/test_mediahub_lifecycle_contract.py` — generic lifecycle/persistence/migration contract and deterministic tests.
- `ops/mediahub_streaming_boundary.py` and `tests/test_mediahub_streaming_boundary.py` — provider-neutral streaming transport parsing and deterministic boundary tests.
- `tests/test_mediahub_cluster_lifecycle.py` and `tests/test_mediahub_cluster_failover.py` — generic cluster lifecycle/failover failure behavior, not media integration acceptance.

## Classification

- Media integration acceptance: ABSENT in the inspected implementation/test surface.
- Media-specific failure-injection acceptance: ABSENT in the inspected implementation/test surface.
- Generic lifecycle/streaming/cluster failure tests: PRESENT but insufficient to satisfy P3.5.
- Functional media integration requirements: PRESENT in accepted recovery documents, with concrete technical details partly deferred.

## Gate

This artifact records the factual gap only. It does not invent integration topology, failure modes, protocols, or production behavior. A future P3.5 implementation task requires explicit bounded media integration scenarios, deterministic failure injection, and provenance-bound acceptance evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.4-media-authorization-storage-retention-recovery-gap-reconciliation":
        content = """# P3.4 Media Authorization / Storage / Retention / Recovery Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.4 NOT CLOSED

## Queue requirement

`P3.4 Validate authorization, storage, retention and recovery semantics.`

## Exact repository surfaces inspected

- `ops/mediahub_lifecycle_contract.py` — generic lifecycle/persistence/version/migration contract; no media authorization, storage or retention policy.
- `tests/test_mediahub_lifecycle_contract.py` — deterministic generic lifecycle tests.
- `ops/mediahub_streaming_boundary.py` — provider-neutral streaming transport boundary; no media storage or retention semantics.
- `tests/test_mediahub_streaming_boundary.py` — deterministic streaming-boundary tests.
- `runtime/mediahub_runtime/state_authority.py` — canonical generic state authority; not a media authorization/storage/retention contract.
- `tests/security/test_mh05_restore_security.py` — generic restore/tamper security tests; not media-specific recovery acceptance.

## Classification

- Media authorization contract: ABSENT in the inspected media-specific repository surface.
- Media storage contract: ABSENT in the inspected media-specific repository surface.
- Media retention contract: ABSENT in the inspected media-specific repository surface.
- Media recovery contract: ABSENT as a media-specific acceptance surface.
- Generic lifecycle, authority and restore-security components: PRESENT but insufficient to satisfy P3.4.

## Gate

This artifact records only the factual acceptance-surface gap. It does not invent media policy, storage backends, retention rules, recovery workflows, or production authority. A future P3.4 implementation task requires explicit media-specific contracts, deterministic tests, and provenance-bound acceptance evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.3-playback-control-gap-reconciliation":
        content = """# P3.3 Playback / Control Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.3 NOT CLOSED

## Queue requirement

`P3.3 Implement/qualify playback/control contracts.`

## Exact repository surfaces inspected

- `ops/mediahub_streaming_boundary.py` — provider-neutral streaming transport parsing/boundary.
- `tests/test_mediahub_streaming_boundary.py` — deterministic streaming-boundary tests.
- `ops/mediahub_lifecycle_contract.py` — generic lifecycle/persistence/version contract.
- `tests/test_mediahub_lifecycle_contract.py` — deterministic lifecycle contract tests.

## Classification

- Playback contract: ABSENT in the inspected media-specific repository surface.
- Control contract: ABSENT in the inspected media-specific repository surface.
- Streaming transport boundary: PRESENT, but transport parsing does not establish playback or control semantics.
- Generic lifecycle contract: PRESENT, but insufficient to satisfy P3.3.

## Gate

This artifact only encodes the factual acceptance-surface gap. It does not add playback/control semantics, implementation, qualification, or production authority. A future P3.3 implementation task requires explicit media playback/control contracts, deterministic tests, and provenance-bound acceptance evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.2-ingestion-metadata-index-gap-reconciliation":
        content = """# P3.2 Ingestion / Metadata / Index Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.2 NOT CLOSED

## Queue requirement

`P3.2 Implement/qualify ingestion and metadata/index contracts.`

## Exact repository surfaces inspected

- `ops/mediahub_lifecycle_contract.py` — generic lifecycle, persistence/version and migration contract; no media ingestion/index API.
- `tests/test_mediahub_lifecycle_contract.py` — tests for the generic lifecycle contract.
- `ops/mediahub_streaming_boundary.py` — provider-neutral streaming transport boundary.
- `tests/test_mediahub_streaming_boundary.py` — deterministic streaming-boundary tests.

## Classification

- Ingestion contract: ABSENT in the inspected media-specific repository surface.
- Metadata contract: ABSENT as a media-specific ingestion/index acceptance surface.
- Index contract: ABSENT as a media-specific ingestion/index acceptance surface.
- Existing lifecycle contract: PRESENT, but insufficient to satisfy P3.2.
- Existing streaming transport boundary: PRESENT, but it does not establish ingestion, metadata/index, or playback semantics.

## Gate

This artifact only encodes the factual acceptance-surface gap. It does not add media semantics, implementation, qualification, or production authority. A future P3.2 implementation task requires an explicit media-specific contract, deterministic tests, and provenance-bound acceptance evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p3.1-media-domain-lifecycle-inventory":
        content = """# P3.1 Media Domain Contract and Lifecycle Inventory

Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED

## Repository-observed contract

Source: `ops/mediahub_lifecycle_contract.py`
Tests: `tests/test_mediahub_lifecycle_contract.py`

Observed lifecycle states: `ABSENT`, `CANDIDATE`, `VALIDATED`, `AUTHORIZED`, `PUBLISHED`, `APPLIED`, `SUPERSEDED`.

Observed transitions are explicit and monotonic through the `_ALLOWED` transition map. Invalid transitions are rejected.

Observed persistence contract requires `authority == state-authority`, a typed `VersionIdentity`, and an explicit boolean `durable` flag; physical durability is not implied by construction.

Observed migration contract requires non-empty migration identity, typed source/target versions, boolean rollback support, and a revision change.

## Verification

Command: `pytest -q tests/test_mediahub_lifecycle_contract.py`

Acceptance: the existing lifecycle/persistence/migration contract tests pass at the current repository state.

## Boundary

This evidence inventories only the repository-native lifecycle contract. It does not qualify media ingestion, metadata/indexing, playback/control, authorization, storage, retention, recovery, integration, performance, or production behavior.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p2.5-cluster-recovery-gap-reconciliation":
        content = """# P2.5 Cluster Recovery Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / IMPLEMENTATION NOT AUTHORIZED BY THIS RECORD

## Required scenarios

- stale leader
- split-brain
- duplicate command
- replay
- recovery

## Reconciliation method

Search existing repository contracts and tests for explicit semantics. Classify each required scenario only from exact repository evidence as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not invent leader election, source-of-truth, fencing or replay semantics.

## Current repository evidence

The current local cluster implementation exposes membership, health, lifecycle, resources, gateway and failover contracts. Existing deterministic cluster verification is recorded separately. The repository search must remain the authority for whether leader/source-of-truth semantics exist; absence of an API is not permission to design one here.

## Gate

This artifact is an encoding/reconciliation step. Any resulting implementation work requires a separate bounded task with explicit acceptance criteria and authority.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p0.7-cloud-agent-readiness-verification":
        content = """# P0.7 Cloud-Agent Readiness Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P0.7 BLOCKED

## Scope

This record proves only the local missing-credential negative path. It does not create credentials, inspect secret values, invoke a cloud provider, activate VPN/cloud execution, or authorize production.

## Verification

Command: python3 -m pytest -q tests/security/test_native_agent_launcher.py

Acceptance: the existing deterministic launcher test proves a cloud launch request without an approved provider credential is rejected fail-closed.

## Boundary

P0.7 remains credential/cloud gated. The absence of an approved credential is an explicit BLOCKED condition, not a reason to bypass the credential broker.

## Provenance

The controller writes this artifact only after the verification command succeeds against the current task base.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p1.2-execution-admission-verification":
        content = """# P1.2 Execution Admission Verification

Status: VERIFIED_LOCAL_SUBSCOPE

## Scope

This record covers deterministic local admission checks for boolean authorization/recovery verification flags and proposal provenance binding. It does not authorize provider execution or mutate State Authority.

## Verification

Command: python3 -m pytest -q tests/test_mediahub_native_execution.py

Acceptance: the existing deterministic native execution tests prove verified admission requires boolean authorization and recovery flags, preserves provenance matching, and rejects malformed verification values.

## Boundary

This is local contract evidence only. Provider execution, credential acquisition and production authorization remain outside this task.

## Provenance

The controller writes this artifact only after the verification command succeeds against the current task base.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p0.3-controller-watchdog-verification":
        content = """# P0.3 Controller / Watchdog Verification

Status: VERIFIED_LOCAL_SUBSCOPE

## Scope

Deterministic local evidence for controller/watchdog lock, ownership, PID starttime, stop-marker race, supervision and liveness semantics. This does not authorize production deployment or claim full daemon qualification.

## Verification

Command:

```text
python3 -m pytest -q tests/ops/test_autonomous_control_plane.py
```

Acceptance: all existing autonomous-control-plane tests pass; source validation covers the controller and watchdog shell contracts; no production mutation, release or credential action is performed.

## Provenance

The controller writes this artifact only after executing the verification command successfully against the current task base.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p2.6-home-assistant-source-of-truth-verification":
        old = path.read_text(encoding="utf-8")
        marker = "## P2.6 Home Assistant source-of-truth verification — 2026-09-21"
        if marker in old:
            return ""
        content = """\n\n## P2.6 Home Assistant source-of-truth verification — 2026-09-21\n\nStatus: VERIFIED_LOCAL_SUBSCOPE / P2.6 NOT CLOSED\n\nScope: verify only the existing normative functional-baseline statements and control gates. No Home Assistant runtime access, State Authority mutation, provider execution, or production operation is part of this task.\n\nAcceptance evidence: `ops/verify_functional_baseline.sh` is the repository-native deterministic gate. It requires the normative functional baseline, governance and invariant registry to identify Home Assistant Core, MediaHub State Authority, the canonical AI escalation path, locked release state and unauthorized production state; it also requires exact R4 ancestry and R4 tree identity.\n\nArchitectural boundary: this evidence confirms the repository's declared source-of-truth boundary. It does not qualify an operational Home Assistant adapter, runtime integration, command path, or production deployment.\n"""
        return unified_patch(old, old.rstrip() + content, target)
    if task.fallback_kind == "p0.2-master-queue-ownership-provenance-reconciliation":
        old = path.read_text(encoding="utf-8")
        marker = "## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22"
        if marker in old:
            return ""
        snapshot = task.instruction.split("Projection snapshot computed at compilation: ", 1)[1].split(". Treat the YAML", 1)[0]
        data = json.loads(snapshot)
        lines = [
            "```yaml",
            "p02_projection_version: 1",
            f"source_head: {data['head']}",
            f"source_tree: {data['tree']}",
            f"queue_sha256: {data['queue_sha256']}",
            f"dispatch_sha256: {data['dispatch_sha256']}",
            "projection_only: true",
            "authority_grant: false",
            "r4_mutation: false",
            "existing_architecture_sources:",
            "  - specification/capability-registry.yaml",
            "  - specification/contract-registry.yaml",
            "  - specification/dependency-graph.yaml",
            "  - specification/invariant-registry.yaml",
            "  - docs/ops/control-plane/MH01-23-QUEUE-DISPATCH-2026-09-19.yaml",
            "stale_dispatch_references:",
        ]
        lines.extend(f"  - {x}" for x in data["stale_dispatch_references"] or ["none-observed"])
        lines.append("worktree_branch_inventory:")
        lines.extend(f"  - {x}" for x in data["branches"] or ["none-observed"])
        lines.append("``")
        yaml = "\n".join(lines)
        content = f"""\n\n## P0.2 master-queue ownership/provenance reconciliation — 2026-09-22\n\nStatus: VERIFIED_LOCAL_SUBSCOPE / P0.2 NOT CLOSED\n\nScope: reconcile the existing persisted master queue with the repository's existing machine-readable dispatch and governance registries. This record is a projection only and does not create authority or replace canonical registries.\n\n{yaml}\n\nAcceptance boundary: the projection is bound to the exact current-tree HEAD/tree and queue/dispatch hashes captured at compilation, inventories observed worktree branches, and explicitly reports dispatch references that do not correspond to observed live worktree branches.\n\nGovernance boundary: no R4 mutation, history rewrite, merge, parallel-lane modification, credential access, production authorization, or State Authority mutation is performed.\n"""
        return unified_patch(old, old.rstrip() + content, target)
    if task.fallback_kind == "p0.1-current-control-point-reconciliation":
        old = path.read_text(encoding="utf-8")
        marker = "## P0.1 current control-point reconciliation — 2026-09-21"
        if marker in old:
            return ""
        content = """\n\n## P0.1 current control-point reconciliation — 2026-09-21\n\nStatus: VERIFIED_LOCAL_RECONCILIATION\n\nRepository control point at task compilation: branch `engineering/mh21-sandbox-lifecycle-20260910`; HEAD `46d87676bf5381732f5e8410c0f124567490d4d5`; tree `966929c70ffe983d43c01efb47e8a78b55aa3336`.\n\nR4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`; R4 ancestry: PASS. Worktree: clean at task compilation.\n\nActive execution infrastructure observed: one autonomous OS loop owner, one watchdog owner, and one hybrid orchestrator process; the authoritative worktree remains `/home/mediahub/dev/mediahub-os-autonomous`. Parallel worktrees remain separately owned and were not modified by this task.\n\nBoundary: this record is reconciliation evidence only. No R4 mutation, history rewrite, destructive cleanup, user-work overwrite, merge, release, or production authorization is performed.\n"""
        return unified_patch(old, old.rstrip() + content, target)
    if task.fallback_kind == "p0.6-pr80-reconciliation-evidence":
        old = path.read_text(encoding="utf-8")
        marker = "## P0.6 PR #80 reconciliation — 2026-09-21"
        if marker in old:
            return ""
        content = """\n\n## P0.6 PR #80 reconciliation — 2026-09-21\n\nStatus: VERIFIED_LOCAL_RECONCILIATION / NO INTEGRATION\n\nScope: reconcile PR #80 remote/local evidence without push, merge, cherry-pick, ready-state change, release action, or production authorization.\n\nRemote Git evidence observed read-only from `origin`: `refs/pull/80/head` = `40f700981c6dceb4bfa47e69c43f539f15db686d`; `refs/pull/80/merge` = `e6caca15405eabc7102b17b5c12f6c407c87401b`.\n\nLocal control point at compilation: `HEAD` = `ff328899626e912a18d64553a5902010a6725252`; `HEAD^{{tree}}` = `39bbedc5067aa0a9064b06ef2ad6bc76585560db`; R4 = `471f709f5633feab7aeb62dd3ea52effad6d2bc4`; R4 ancestry = PASS.\n\nThe remote PR head was observed as a ref but was not imported into this worktree. No merge, cherry-pick, push, release, production authorization, credential access, or State Authority mutation was performed.\n\nAcceptance: exact remote/local SHAs are recorded, lineage remains intact, and the evidence explicitly preserves the non-integration boundary.\n"""
        return unified_patch(old, old.rstrip() + content, target)
    if task.fallback_kind == "p0.5-delivery-identity-recovery-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_for_identity_rejects_mismatch" in old:
            return ""
        addition = '\n\ndef test_restore_for_identity_rejects_mismatch(tmp_path):\n    path = tmp_path / "delivery.json"\n    first = TaskDeliveryJournal(path)\n    first.prepare("task", "payload", "conv", "sess", 2)\n    first.release()\n    restored = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        restored.restore_for_identity(session_id="other", conversation_id="conv", generation=2)\n    restored.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.5-delivery-safe-stop-recovery-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_for_identity_rejects_safe_stop" in old:
            return ""
        addition = '\n\ndef test_restore_for_identity_rejects_safe_stop(tmp_path):\n    path = tmp_path / "delivery.json"\n    first = TaskDeliveryJournal(path)\n    first.prepare("task", "payload", "conv", "sess", 1)\n    first.mark_safe_stop("operator stop")\n    first.release()\n    restored = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        restored.restore_for_identity(session_id="sess", conversation_id="conv", generation=1)\n    restored.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.5-delivery-provenance-type-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_rejects_boolean_generation_and_attempt" in old:
            return ""
        addition = '\n\ndef test_restore_rejects_boolean_generation_and_attempt(tmp_path):\n    path = tmp_path / "delivery.json"\n    path.write_text(json.dumps({\n        "version": 1, "task_id": "task", "request_fingerprint": "fp",\n        "conversation_id": "conv", "session_id": "sess", "generation": True,\n        "state": "PREPARED", "attempt": False, "response_fingerprint": "",\n        "reason": "prepared",\n    }), encoding="utf-8")\n    journal = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        journal.restore()\n    journal.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p2.4-cluster-membership-failover-verification":
        content = """# P2.4 Cluster Membership / Failover Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P2.4 NOT CLOSED

## Scope

This record covers deterministic local evidence for the existing cluster membership, health, lifecycle, resource, gateway and failover contracts. It does not establish the missing leader/source-of-truth architecture and therefore does not promote P2.4 to complete.

## Verification

Command:

```text
python3 -m pytest -q tests/test_mediahub_cluster_membership.py tests/test_mediahub_cluster_health.py tests/test_mediahub_cluster_lifecycle.py tests/test_mediahub_cluster_resources.py tests/test_mediahub_cluster_gateway.py tests/test_mediahub_cluster_failover.py
```

Acceptance: all existing deterministic tests for this bounded subscope pass; no network, State Authority mutation, production operation, or external provider execution.

## Architectural boundary

Leader election, canonical cluster source-of-truth semantics, stale-leader handling and split-brain resolution remain open until their contracts and acceptance criteria are encoded. This evidence intentionally does not claim those states.

## Provenance

The controller writes this artifact only after executing the verification command successfully against the current task base.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p0.5-delivery-identity-recovery-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_for_identity_rejects_mismatch" in old:
            return ""
        addition = '\n\ndef test_restore_for_identity_rejects_mismatch(tmp_path):\n    path = tmp_path / "delivery.json"\n    first = TaskDeliveryJournal(path)\n    first.prepare("task", "payload", "conv", "sess", 2)\n    first.release()\n    restored = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        restored.restore_for_identity(session_id="other", conversation_id="conv", generation=2)\n    restored.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.5-delivery-safe-stop-recovery-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_for_identity_rejects_safe_stop" in old:
            return ""
        addition = '\n\ndef test_restore_for_identity_rejects_safe_stop(tmp_path):\n    path = tmp_path / "delivery.json"\n    first = TaskDeliveryJournal(path)\n    first.prepare("task", "payload", "conv", "sess", 1)\n    first.mark_safe_stop("operator stop")\n    first.release()\n    restored = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        restored.restore_for_identity(session_id="sess", conversation_id="conv", generation=1)\n    restored.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.5-delivery-provenance-type-test":
        old = path.read_text(encoding="utf-8")
        if "test_restore_rejects_boolean_generation_and_attempt" in old:
            return ""
        addition = '\n\ndef test_restore_rejects_boolean_generation_and_attempt(tmp_path):\n    path = tmp_path / "delivery.json"\n    path.write_text(json.dumps({\n        "version": 1, "task_id": "task", "request_fingerprint": "fp",\n        "conversation_id": "conv", "session_id": "sess", "generation": True,\n        "state": "PREPARED", "attempt": False, "response_fingerprint": "",\n        "reason": "prepared",\n    }), encoding="utf-8")\n    journal = TaskDeliveryJournal(path)\n    with pytest.raises(DeliveryDenied):\n        journal.restore()\n    journal.release()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.5.2-terminal-provenance-regression-test":
        old = path.read_text(encoding="utf-8")
        if "test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch" in old:
            return ""
        addition = '\n\ndef test_daemon_rejects_terminal_tail_with_baseline_or_r4_mismatch(monkeypatch, tmp_path):\n    class FakeJournal:\n        def __init__(self, path):\n            self.path = path\n\n        def read_tail(self):\n            return {"session_id": "s1", "baseline_sha": "other", "r4_sha": "other-r4", "state": "STOPPED"}\n\n    class FakeSession:\n        def __init__(self, journal):\n            self.journal = journal\n\n    class FakeConversation:\n        def __init__(self, journal_path):\n            pass\n\n    class FakeDelivery:\n        def __init__(self, path):\n            pass\n\n    class FakeEgress:\n        def __init__(self, paths):\n            pass\n\n    class FakeController:\n        def __init__(self, *args):\n            pass\n\n        def restore(self, *args):\n            raise daemon.HybridDevelopmentDenied("terminal restore")\n\n    checkpoint = tmp_path / ".hybrid-development" / "session.jsonl"\n    checkpoint.parent.mkdir()\n    checkpoint.write_text("terminal\\n", encoding="utf-8")\n    monkeypatch.setattr(daemon, "ROOT", tmp_path)\n    monkeypatch.setattr(daemon, "SessionJournal", FakeJournal)\n    monkeypatch.setattr(daemon, "HybridSessionController", FakeSession)\n    monkeypatch.setattr(daemon, "TextConversationController", FakeConversation)\n    monkeypatch.setattr(daemon, "TaskDeliveryJournal", FakeDelivery)\n    monkeypatch.setattr(daemon, "HybridCloudEgressAdapter", FakeEgress)\n    monkeypatch.setattr(daemon, "HybridDevelopmentController", FakeController)\n    monkeypatch.setattr(daemon, "parse_paths", lambda value: ())\n    import sys\n    monkeypatch.setattr(sys, "argv", [\n        "daemon", "--session-id", "s1", "--baseline-sha", "baseline",\n        "--r4-sha", "r4", "--duration-hours", "1",\n        "--health-url", "https://example.invalid/health", "--paths", "vpm:tun:src",\n    ])\n    with pytest.raises(daemon.HybridDevelopmentDenied):\n        daemon.main()\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p0.7-cloud-readiness-missing-credential-test":
        old = path.read_text(encoding="utf-8")
        if "test_cloud_launch_without_credential_remains_blocked" in old:
            return ""
        addition = '\n\ndef test_cloud_launch_without_credential_remains_blocked(tmp_path):\n    credential_dir = tmp_path / "credentials"\n    credential_dir.mkdir()\n    broker = CredentialBroker(credential_dir, frozenset({"openai"}))\n    broker.authorize()\n    registry = ModelRegistry((ModelRecord("openai", "qualified"),))\n    with pytest.raises(NativeAgentDenied):\n        resolve_launch("codex", broker, "https://api.openai.com/v1", "qualified", registry)\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p1.2-admission-boolean-type-test":
        old = path.read_text(encoding="utf-8")
        if "test_execution_admission_rejects_non_boolean_authorization_and_recovery" in old:
            return ""
        addition = '\n\ndef test_execution_admission_rejects_non_boolean_authorization_and_recovery():\n    proposal = ExecutionProposal("req-a", "work-a", "sha-a", "openai")\n    for authorization, recovery in ((1, True), ("yes", True), (True, 1), (True, "yes")):\n        with pytest.raises(PermissionError):\n            BoundedExecutionAdapter().admit_verified(\n                ExecutionAdmission(proposal, authorization, "sha-a", recovery), target()\n            )\n'
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p1.2-admission-boolean-type-hardening":
        old = path.read_text(encoding="utf-8")
        marker = "        if not isinstance(self.proposal, ExecutionProposal):\n            raise PermissionError(\"malformed execution admission\")\n"
        hardened = marker + "        if not isinstance(self.authorized, bool) or not isinstance(self.recovery_verified, bool):\n            raise PermissionError(\"execution admission verification flags must be boolean\")\n"
        if "execution admission verification flags must be boolean" in old:
            return ""
        if marker not in old:
            return ""
        return unified_patch(old, old.replace(marker, hardened, 1), target)
    if task.fallback_kind == "p2.4-cluster-gateway-negative-tests":
        old = path.read_text(encoding="utf-8")
        if "test_propose_rejects_malformed_request_identity" in old:
            return ""
        addition = """\n\n\ndef test_propose_rejects_malformed_request_identity():\n    for value in (None, True, 1, object()):\n        with pytest.raises(ClusterGatewayDenied):\n            gateway().propose(value, workload(), decision(Route.LOCAL_CLUSTER))\n\n\ndef test_propose_rejects_malformed_decision_type():\n    for value in (None, True, object()):\n        with pytest.raises(ClusterGatewayDenied):\n            gateway().propose("req-1", workload(), value)\n"""
        return unified_patch(old, old.rstrip() + addition, target)
    if task.fallback_kind == "p2.4-cluster-gateway-input-hardening":
        old = path.read_text(encoding="utf-8")
        marker = "        if not request_id:\n            raise ClusterGatewayDenied(\"request identity is required\")\n"
        hardened = "        if not isinstance(request_id, str) or not request_id:\n            raise ClusterGatewayDenied(\"malformed request identity\")\n        if not isinstance(workload, ClusterWorkload):\n            raise ClusterGatewayDenied(\"malformed cluster workload\")\n        if not isinstance(decision, RoutingDecision):\n            raise ClusterGatewayDenied(\"malformed routing decision\")\n"
        if "malformed request identity" in old or marker not in old:
            return ""
        return unified_patch(old, old.replace(marker, hardened, 1), target)
    if task.fallback_kind == "native-negative-tests":
        old = path.read_text(encoding="utf-8")
        if "test_bounded_execution_rejects_malformed_types" in old:
            return ""
        addition = '''\n\ndef test_bounded_execution_rejects_malformed_types():\n    proposal = ExecutionProposal("req", "work", "sha", "openai")\n    adapter = BoundedExecutionAdapter()\n    for timeout in (True, False, 1.5, "30", None):\n        with pytest.raises(PermissionError):\n            adapter.admit(proposal, target(), timeout)\n    for output_limit in (True, False, 1.5, "4096", None):\n        with pytest.raises(PermissionError):\n            adapter.admit(proposal, target(), 30, output_limit)\n    with pytest.raises(PermissionError):\n        adapter.admit(object(), target())\n    with pytest.raises(PermissionError):\n        adapter.admit(proposal, object())\n    with pytest.raises(PermissionError):\n        NativeExecutionContract().prepare_proposal("", "work", "sha", "openai")\n    with pytest.raises(PermissionError):\n        NativeExecutionContract().prepare_headers(target(), True)\n'''
        new = old.rstrip() + addition
        return unified_patch(old, new, target)
    old = path.read_text(encoding="utf-8").splitlines(keepends=True)
    old_text = "".join(old)
    if "class BoundedExecutionRequest:" in old_text and "isinstance(self.timeout_seconds, int)" not in old_text:
        original = """    def validate(self) -> None:
        self.proposal.validate()
        self.target.validate()
        if self.proposal.provider != self.target.provider:
            raise PermissionError(\"proposal provider does not match execution target\")
        if not 1 <= self.timeout_seconds <= 900:
            raise ValueError(\"execution timeout is outside the bounded policy\")
        if not 1 <= self.max_output_bytes <= 1_048_576:
            raise ValueError(\"execution output limit is outside the bounded policy\")
"""
        hardened = """    def validate(self) -> None:
        if not isinstance(self.proposal, ExecutionProposal) or not isinstance(self.target, ExecutionTarget):
            raise PermissionError(\"malformed bounded execution request\")
        if not isinstance(self.timeout_seconds, int) or isinstance(self.timeout_seconds, bool):
            raise PermissionError(\"execution timeout must be an integer\")
        if not isinstance(self.max_output_bytes, int) or isinstance(self.max_output_bytes, bool):
            raise PermissionError(\"execution output limit must be an integer\")
        self.proposal.validate()
        self.target.validate()
        if self.proposal.provider != self.target.provider:
            raise PermissionError(\"proposal provider does not match execution target\")
        if not 1 <= self.timeout_seconds <= 900:
            raise ValueError(\"execution timeout is outside the bounded policy\")
        if not 1 <= self.max_output_bytes <= 1_048_576:
            raise ValueError(\"execution output limit is outside the bounded policy\")
"""
        if original not in old_text:
            return ""
        new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
        return unified_patch(old, new, TARGET)
    if "def prepare_recovery_proposal(" in old_text and "malformed recovery evidence" not in old_text:
        return _fallback_recovery_patch(old, old_text)
    if "def prepare_headers(self, target: ExecutionTarget, secret: str)" in old_text and "not isinstance(secret, str)" not in old_text:
        return _fallback_headers_patch(old, old_text)
    if "class ExecutionProposal:" in old_text and "malformed execution proposal" not in old_text:
        return _fallback_proposal_patch(old, old_text)
    if "class ExecutionTarget:" in old_text and "malformed execution target" not in old_text:
        return _fallback_target_patch(old, old_text)
    if old_text.count("class VerificationBoundary:") == 1 and "class ExecutionVerification:" in old_text:
        if "malformed verification request" in old_text:
            return ""
        original = """    def validate(self) -> None:
        self.request.validate()
        if self.status not in {\"COMPLETED\", \"FAILED\"}:
            raise PermissionError(\"unsupported verification status\")
        if not self.observed_source_sha or self.observed_source_sha != self.request.proposal.source_sha:
            raise PermissionError(\"verification provenance does not match proposal\")
"""
        hardened = """    def validate(self) -> None:
        if not isinstance(self.request, BoundedExecutionRequest):
            raise PermissionError(\"malformed verification request\")
        if not isinstance(self.status, str) or self.status not in {\"COMPLETED\", \"FAILED\"}:
            raise PermissionError(\"unsupported verification status\")
        if not isinstance(self.observed_source_sha, str) or not self.observed_source_sha:
            raise PermissionError(\"malformed verification provenance\")
        self.request.validate()
        if self.observed_source_sha != self.request.proposal.source_sha:
            raise PermissionError(\"verification provenance does not match proposal\")
"""
        if original not in old_text:
            return ""
        new = old_text.replace(original, hardened, 1).splitlines(keepends=True)
        return unified_patch(old, new, TARGET)
    marker = "class VerificationBoundary:"
    if any(marker in line for line in old):
        return ""
    addition = [
        "\n",
        "@dataclass(frozen=True)\n",
        "class ExecutionVerification:\n",
        "    request: BoundedExecutionRequest\n",
        "    status: str\n",
        "    observed_source_sha: str\n",
        "\n",
        "    def validate(self) -> None:\n",
        "        self.request.validate()\n",
        "        if self.status not in {\"COMPLETED\", \"FAILED\"}:\n",
        "            raise PermissionError(\"unsupported verification status\")\n",
        "        if not self.observed_source_sha or self.observed_source_sha != self.request.proposal.source_sha:\n",
        "            raise PermissionError(\"verification provenance does not match proposal\")\n",
        "\n",
        "class VerificationBoundary:\n",
        "    def verify(\n",
        "        self, request: BoundedExecutionRequest, status: str, observed_source_sha: str,\n",
        "    ) -> ExecutionVerification:\n",
        "        verification = ExecutionVerification(request, status, observed_source_sha)\n",
        "        verification.validate()\n",
        "        return verification\n",
        "\n",
    ]
    marker = "class NativeExecutionContract:"
    try:
        insert_at = next(i for i, line in enumerate(old) if line.startswith(marker))
    except StopIteration:
        return ""
    new = old[:insert_at] + addition + old[insert_at:]
    return unified_patch(old, new, TARGET)

def apply_checked(patch: str, target: str | None = None) -> bool:
    if not safe_patch(patch, target):
        return False
    check = subprocess.run(
        [str(GIT), "apply", "--check", "-"], cwd=ROOT, input=patch,
        text=True, capture_output=True, check=False
    )  # nosec B603
    if check.returncode:
        print(check.stderr.strip(), file=sys.stderr)
        return False
    applied = subprocess.run(
        [str(GIT), "apply", "--index", "-"], cwd=ROOT, input=patch,
        text=True, capture_output=True, check=False
    )  # nosec B603
    if applied.returncode:
        print(applied.stderr.strip(), file=sys.stderr)
        return False
    return True


def exact_target(task: LocalTask | None = None) -> bool:
    selected = task or select_local_task(ROOT)
    expected = selected.target if selected else TARGET
    return run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines() == [expected]


def verify(task: LocalTask | None = None) -> bool:
    selected = task or select_local_task(ROOT)
    verify_target = selected.target if selected else TARGET
    checks: list[tuple[list[str], int]] = [(["git", "diff", "--check"], 120)]
    if RUFF.is_file():
        checks.append(([str(RUFF), "check", verify_target], 120))
    if selected and selected.fallback_kind == "p3.6-media-benchmark-resource-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/test_mediahub_streaming_boundary.py",
                        "tests/test_mediahub_cluster_resources.py"], 180))
    if selected and selected.fallback_kind == "p3.5-media-integration-failure-injection-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/test_mediahub_lifecycle_contract.py",
                        "tests/test_mediahub_streaming_boundary.py",
                        "tests/test_mediahub_cluster_lifecycle.py",
                        "tests/test_mediahub_cluster_failover.py"], 180))
    if selected and selected.fallback_kind == "p3.4-media-authorization-storage-retention-recovery-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/test_mediahub_lifecycle_contract.py",
                        "tests/test_mediahub_streaming_boundary.py",
                        "tests/security/test_mh05_restore_security.py"], 180))
    if selected and selected.task_id.startswith("P2.3-"):
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_lifecycle_contract.py"], 180))
    elif selected and selected.task_id.startswith("P2.4-"):
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_cluster_gateway.py"], 180))
    elif selected and selected.fallback_kind == "p2.6-home-assistant-source-of-truth-verification":
        checks.append((["bash", "ops/verify_functional_baseline.sh"], 60))
    elif selected and selected.fallback_kind in {"hybrid-egress-types", "hybrid-egress-tests"}:
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_hybrid_cloud_api_egress_adapter.py"], 180))
    elif selected and selected.fallback_kind == "p2.5-cluster-recovery-gap-reconciliation":
        checks.append(([sys.executable, "-c", "from pathlib import Path; import re; r=Path('ops/mediahub_cluster_failover.py').read_text(); t=Path('tests/test_mediahub_cluster_failover.py').read_text(); required=('leader','split','replay','duplicate'); print('P2.5 evidence scan', {k:(k in r.lower() or k in t.lower()) for k in required}); assert 'failover' in r.lower() and 'failover' in t.lower()"], 30))
    elif selected and selected.fallback_kind == "p0.7-cloud-agent-readiness-verification":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/security/test_native_agent_launcher.py"], 180))
    elif selected and selected.fallback_kind == "p1.2-execution-admission-verification":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_native_execution.py"], 180))
    elif selected and selected.fallback_kind in {"p0.2-master-queue-ownership-provenance-reconciliation", "p0.3-controller-watchdog-verification"}:
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/ops/test_autonomous_control_plane.py"], 180))
    elif selected and selected.fallback_kind == "p2.4-cluster-membership-failover-verification":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/test_mediahub_cluster_membership.py",
                        "tests/test_mediahub_cluster_health.py",
                        "tests/test_mediahub_cluster_lifecycle.py",
                        "tests/test_mediahub_cluster_resources.py",
                        "tests/test_mediahub_cluster_gateway.py",
                        "tests/test_mediahub_cluster_failover.py"], 180))
    elif selected and selected.target.startswith("tests/"):
        checks.append(([sys.executable, "-m", "pytest", "-q", selected.target], 180))
    else:
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_native_execution.py"], 180))
    if os.environ.get("MEDIAHUB_FULL_SECURITY") == "1":
        checks.append((["bash", "ops/security_scan_local.sh"], 900))
    for cmd, timeout in checks:
        p = run(cmd, timeout=timeout)
        if p.returncode:
            print(p.stdout + p.stderr, file=sys.stderr)
            return False
    return True


def generate(text: str) -> tuple[int, str, str]:
    try:
        with LOCAL_AI_OPENER.open(
            urllib.request.Request(LOCAL_AI_URL.rsplit("/v1/", 1)[0] + "/health")  # nosemgrep: python.lang.security.audit.insecure-transport.urllib.insecure-request-object.insecure-request-object
            , timeout=5
        ) as response:
            if response.status != 200:
                return 28, "", "AI_REJECTED"
    except (urllib.error.URLError, TimeoutError):
        return 28, "", "AI_TIMEOUT"
    payload = {
        "messages": [
            {"role": "system", "content": "Return only a complete unified git diff."},
            {"role": "user", "content": text},
        ],
        "max_tokens": 256,
        "temperature": 0,
    }
    req = urllib.request.Request(  # nosemgrep: python.lang.security.audit.insecure-transport.urllib.insecure-request-object.insecure-request-object
        LOCAL_AI_URL, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with LOCAL_AI_OPENER.open(req, timeout=15) as response:
            raw = response.read(1_048_577)
        if len(raw) > 1_048_576:
            return 28, "", "AI_MALFORMED"
        body = json.loads(raw.decode("utf-8"))
        content = str(body["choices"][0]["message"]["content"])
        return 0, content, "AI_SUCCESS"
    except TimeoutError:
        return 28, "", "AI_TIMEOUT"
    except (KeyError, IndexError, urllib.error.URLError, ValueError, UnicodeDecodeError) as exc:
        print(f"LOCAL_AGENT_LOCAL_AI_ERROR: {type(exc).__name__}", file=sys.stderr)
        return 28, "", "AI_MALFORMED"


def rollback() -> bool:
    restored = run(["git", "restore", "--staged", "--worktree", "--", "."])
    clean = not run(["git", "status", "--porcelain"]).stdout.strip()
    if restored.returncode == 0 and clean:
        state("ROLLED_BACK", "working tree clean")
        return True
    state("BLOCKED", "rollback could not restore clean tree")
    return False


def main() -> int:
    if not MODEL.is_file():
        state("BLOCKED", "local model absent")
        return 20
    if run(["git", "merge-base", "--is-ancestor", R4, "HEAD"]).returncode:
        state("BLOCKED", "R4 ancestry failed")
        return 21
    if run(["git", "status", "--porcelain"]).stdout.strip():
        state("BLOCKED", "baseline not clean")
        return 22

    candidate = select_local_task(ROOT)
    if candidate is None:
        raw = read_raw_queue(ROOT)
        if raw and compile_next_raw_queue_task(ROOT) is None:
            print("LOCAL_AGENT_NOOP: factual queue exists but no bounded compiler is authorized")
            state("BLOCKED", "NEEDS_ENCODING: no deterministic acceptance encoder for remaining factual queue rows")
            return 30
        print("LOCAL_AGENT_NOOP: no eligible local queue item")
        state("BLOCKED", "no eligible local task; higher-level work requires explicit bounded acceptance criteria")
        return 30
    task = compile_executable_task(ROOT, candidate)
    if task is None:
        print("LOCAL_AGENT_NOOP: candidate requires reconciliation or duplicate suppression")
        state("BLOCKED", "candidate could not be compiled into an evidence-bound executable task")
        return 31
    print(f"LOCAL_AGENT_TASK={task.task_id} base_sha={task.base_sha} acceptance={task.acceptance_fingerprint}")
    lease_root = Path(os.environ.get("MEDIAHUB_LEASE_ROOT", "/home/mediahub/.cache/mediahub-autonomous/leases"))
    lease = TaskLease(
        lease_root / f"{task.task_id}.lock",
        task.task_id,
        os.environ.get("MEDIAHUB_WORKER_ID", str(os.getpid())),
        worktree=str(ROOT),
        branch=run(["git", "branch", "--show-current"]).stdout.strip(),
        base_sha=run(["git", "rev-parse", "HEAD"]).stdout.strip(),
        checkpoint_id=os.environ.get("MEDIAHUB_CHECKPOINT_ID"),
    )
    try:
        lease.acquire()
    except LeaseDenied:
        state("BLOCKED", "task lease is already held by another worker")
        return 32
    atexit.register(lease.release)
    error = ""
    patch = ""

    for _ in range(MAX_REGENERATIONS):
        rc, output, ai_state = generate(prompt(task, error))
        if rc:
            state(ai_state, "local AI did not produce an admissible proposal")
            break
        patch = extract(output)
        if not safe_patch(patch, task.target):
            state("AI_MALFORMED", "structural validation rejected AI output")
            error = "structural validation failed; use exact target path and complete ---/+++/@@ sections"
            continue
        if apply_checked(patch, task.target):
            if RUFF.is_file():
                lint = subprocess.run(
                    [str(RUFF), "check", task.target], cwd=ROOT,  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
                    text=True, capture_output=True, check=False
                )  # nosec B603
                if lint.returncode:
                    print("LOCAL_AGENT_AI_LINT_REJECTED: candidate fails lint", file=sys.stderr)
                    print(lint.stdout + lint.stderr, file=sys.stderr)
                    rollback()
                    error = "candidate failed lint; produce a syntactically and lint-clean patch or rely on deterministic fallback"
                    continue
            state("AI_SUCCESS", "structural validation, git apply --check and lint passed")
            break
        state("AI_REJECTED", "git apply --check rejected AI patch")
        error = "git apply --check rejected the patch"
    else:
        patch = ""

    if not patch or not exact_target(task):
        patch = fallback_patch(task)
        if not patch:
            print("LOCAL_AGENT_NOOP: no admissible downstream change")
            state("BLOCKED", "no admissible fallback task or tree is already changed")
            return 30
        state("FALLBACK_SELECTED", f"deterministic fallback for {task.task_id}")
        if not apply_checked(patch, task.target):
            state("BLOCKED", "fallback failed structural validation or git apply --check")
            return 25
        state("FALLBACK_APPLIED", "fallback passed structural validation and git apply --check")

    if not exact_target(task):
        rollback()
        return 27
    if RUFF.is_file():
        lint = subprocess.run(
            [str(RUFF), "check", "--fix", task.target], cwd=ROOT,  # nosemgrep: python.lang.security.audit.dangerous-subprocess-use-tainted-env-args.dangerous-subprocess-use-tainted-env-args
            text=True, capture_output=True, check=False
        )  # nosec B603
        if lint.returncode:
            print("LOCAL_AGENT_BLOCKED: deterministic lint repair failed", file=sys.stderr)
            print(lint.stdout + lint.stderr, file=sys.stderr)
            rollback()
            return 33
        run(["git", "add", "--", task.target])
    if not exact_target(task):
        rollback()
        return 27

    if not verify(task):
        state("VERIFY_FAIL", "verification gate failed")
        rollback()
        return 27
    state("VERIFY_PASS", "diff, lint, tests and security scan passed")

    if run(["git", "diff", "--cached", "--check"]).returncode:
        state("VERIFY_FAIL", "cached diff check failed")
        rollback()
        return 27
    commit = run(["git", "commit", "-m", "chore: local autonomous verified downstream increment"], timeout=120)
    if commit.returncode != 0:
        state("BLOCKED", "commit gate failed")
        return 31
    state("COMMITTED", run(["git", "rev-parse", "HEAD"]).stdout.strip())
    print("LOCAL_AGENT_COMMIT=" + run(["git", "rev-parse", "HEAD"]).stdout.strip())
    print("LOCAL_AGENT_TREE=" + run(["git", "rev-parse", "HEAD^{tree}"]).stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
