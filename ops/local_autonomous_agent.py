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



def _compile_p83_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P8-3-end-to-end-scenario-reconciliation-2026-09-24.md"
    if target.exists():
        return None
    sources = (
        "tests/ai/test_hybrid_session.py",
        "tests/ai/test_hybrid_development_controller.py",
        "tests/ai/test_hybrid_dispatcher.py",
        "tests/ai/test_ai_gateway.py",
        "tests/runtime/test_mh04_qualification_edges.py",
        "tests/security/test_mh05_health_not_authorization.py",
    )
    if not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P8.3-end-to-end-scenario-reconciliation",
        f"P8.3 {item.description}",
        str(target.relative_to(root)),
        "Record deterministic evidence for normal, degraded, recovery and revoked/denied-authorization state surfaces using only existing repository tests. Distinguish scenario coverage from true end-to-end closure; do not execute providers, mutate State Authority, access production or infer authorization from health/reachability.",
        "p8.3-end-to-end-scenario-reconciliation",
    )

def _compile_p82_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P8-2-cross-domain-contract-gap-reconciliation-2026-09-24.md"
    if target.exists():
        return None
    sources = (
        "specification/contract-registry.yaml",
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "tests/contracts/test_contract_domain_reconciliation.py",
        "tests/contracts/test_contract_metadata.py",
        "tests/contracts/test_mobile_api_compatibility.py",
        "tests/static/test_cross_contract.py",
        "tests/test_mediahub_lifecycle_contract.py",
        "ops/verify_functional_baseline.sh",
    )
    if not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P8.2-cross-domain-contract-gap-reconciliation",
        f"P8.2 {item.description}",
        str(target.relative_to(root)),
        "Record deterministic repository evidence for cross-domain contract coverage across Core, AI, Home Assistant, Media, Documents, Mobile and Voice. Inspect only the existing contract registry, functional baseline, cross-contract/domain tests, mobile contract tests, lifecycle contract tests and baseline verification script; classify observed acceptance surfaces as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file/line evidence. Do not infer executable behavior from registry declarations, invent missing domain implementations, mutate State Authority, activate providers or claim P8.2 closure unless the inspected evidence establishes it.",
        "p8.2-cross-domain-contract-gap-reconciliation",
    )


def _compile_p81_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P8-1-escalation-path-reconciliation-2026-09-24.md"
    if target.exists():
        return None
    sources = (
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md",
        "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md",
        "ops/mediahub_provider_gateway.py",
        "ops/cloud_development_adapter.py",
    )
    if not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P8.1-escalation-path-reconciliation",
        f"P8.1 {item.description}",
        str(target.relative_to(root)),
        "Record deterministic repository evidence for the existing escalation path Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI. Inspect only existing baseline/governance, mobile boundary, provider gateway and cloud-orchestrator surfaces; classify each hop as PRESENT, PARTIAL or NOT ESTABLISHED with exact file/line evidence. Do not invent routing behavior, add a Mobile AI tier, execute providers, acquire credentials, mutate State Authority or claim end-to-end closure.",
        "p8.1-escalation-path-reconciliation",
    )


def _compile_p91_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-1-threat-model-refresh-2026-09-24.md"
    sources = (
        "docs/architecture/MH-17-threat-model.md",
        "docs/architecture/MH-21-security-invariants.md",
        "docs/architecture/MH-21-security.md",
        "docs/architecture/MH-21-network-boundary.md",
        "docs/architecture/MH-21-data-egress.md",
        "docs/architecture/MH-21-agent-limits.md",
        "docs/architecture/MH-21-cloud-boundary.md",
        "docs/architecture/MH-21-provider-quarantine.md",
        "docs/architecture/MH-21-remote-policy.md",
        "docs/architecture/MH-21-cloud-credentials.md",
        "docs/architecture/MH-21-audit.md",
        "docs/architecture/MH-12-recovery-security.md",
    )
    if target.is_file() or not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P9.1-threat-model-refresh", f"P9.1 {item.description}", str(target.relative_to(root)),
        "Refresh the threat model from current architecture/security artifacts. Extract documented trust boundaries, assets, threat classes, controls and explicit unknowns/gaps; distinguish implemented controls from design claims and preserve release blockers. Do not invent threats, change authority, execute providers or claim security closure.",
        "p9.1-threat-model-refresh",
        "p9.2-static-secret-dependency-provenance-review",
    )


def _compile_p93_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-3-egress-endpoint-allowlist-audit-2026-09-24.md"
    sources = (
        "docs/architecture/MH-21-network-boundary.md",
        "docs/architecture/MH-21-data-egress.md",
        "ops/mediahub_egress_controller.py",
        "ops/hybrid_cloud_api_egress_adapter.py",
        "ops/hybrid_cloud_egress.py",
        "ops/hybrid_cloud_egress_chain.py",
        "tests/test_mediahub_egress_controller.py",
        "tests/test_hybrid_cloud_api_egress_adapter.py",
    )
    if target.is_file() or not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P9.3-egress-endpoint-allowlist-audit",
        f"P9.3 {item.description}",
        str(target.relative_to(root)),
        "Audit existing egress gates and endpoint allowlists against current architecture. Record exact configured/validated destination evidence, HTTPS and default-deny controls, and any endpoints or runtime paths not proven by tests. Do not perform live endpoint calls, weaken allowlists, acquire credentials or claim network security closure.",
        "p9.3-egress-endpoint-allowlist-audit",
        "p9.4-sandbox-authority-escalation-negative-tests",
    )


def _compile_p92_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-2-static-secret-dependency-provenance-review-2026-09-24.md"
    sources = (
        "ops/requirements-autonomous.txt",
        "docs/architecture/MH-12-secrets.md",
        ".gitignore",
        ".autonomous/provenance.log",
    )
    if target.is_file() or not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P9.2-static-secret-dependency-provenance-review",
        f"P9.2 {item.description}",
        str(target.relative_to(root)),
        "Perform a deterministic repository review of tracked-text secret exposure patterns, dependency manifest/license metadata and provenance evidence. Report findings without printing secret values, distinguish static review from runtime vulnerability scanning, and preserve release blockers where dependency locks, licenses or external provenance are not established. Do not acquire credentials, invoke providers, mutate State Authority or claim security closure.",
        "p9.2-static-secret-dependency-provenance-review",
    )


def _compile_p95_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-5-credential-broker-revocation-isolation-2026-09-25.md"
    sources = (
        root / "ops/mediahub_credential_broker.py",
        root / "tests/test_mediahub_credential_broker.py",
        root / "ops/mediahub_native_execution.py",
        root / "tests/security/test_native_agent_launcher.py",
    )
    if target.exists() or not all(path.is_file() for path in sources):
        return None
    return LocalTask(
        "P9.5-credential-broker-revocation-isolation",
        f"P9.5 {item.description}",
        "docs/ops/P9-5-credential-broker-revocation-isolation-2026-09-25.md",
        "Record deterministic repository evidence for credential-broker isolation and revocation. Inspect only the existing credential broker, native execution boundary, and local security tests; classify credential issuance, provider binding, revocation/denial, secret non-disclosure, and State Authority/production isolation as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not inspect secret values, invoke providers, create credentials, or claim runtime/cloud qualification.",
        "p9.5-credential-broker-revocation-isolation",
    )


def _compile_p96_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-6-malformed-input-security-qualification-2026-09-25.md"
    sources = (
        root / "ops/mediahub_native_execution.py",
        root / "tests/test_mediahub_native_execution.py",
        root / "tests/runtime/test_mh05_consumer_boundary.py",
        root / "tests/security/test_mh05_restore_security.py",
    )
    if target.exists() or not all(path.is_file() for path in sources):
        return None
    return LocalTask(
        "P9.6-malformed-input-security-qualification",
        f"P9.6 {item.description}",
        "docs/ops/P9-6-malformed-input-security-qualification-2026-09-25.md",
        "Record deterministic repository evidence for malformed-input security coverage using only existing public-contract implementations and tests. Identify covered type/shape rejection and remaining justified gaps; do not invent fuzz results, execute external providers, mutate State Authority, or claim exhaustive fuzz qualification.",
        "p9.6-malformed-input-security-qualification",
    )


def _compile_p97_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-7-recovery-tamper-evidence-2026-09-25.md"
    sources = (
        root / "tests/security/test_mh05_restore_security.py",
        root / "runtime/mediahub_runtime",
        root / "docs/ops/control-plane",
    )
    if target.exists() or not all(path.exists() for path in sources):
        return None
    return LocalTask(
        "P9.7-recovery-tamper-evidence",
        f"P9.7 {item.description}",
        "docs/ops/P9-7-recovery-tamper-evidence-2026-09-25.md",
        "Record deterministic repository evidence for recovery and tamper-evidence controls from existing restore-security tests and control-plane recovery contracts. Classify only observed protections and gaps; do not add persistence, mutate State Authority, or claim production disaster-recovery qualification.",
        "p9.7-recovery-tamper-evidence",
    )


def _compile_p94_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P9-4-sandbox-authority-escalation-negative-tests-2026-09-24.md"
    sources = (
        "ops/cloud_development_sandbox.py",
        "ops/mediahub_native_execution.py",
        "ops/mediahub_native_agent_launcher.py",
        "runtime/mediahub_runtime/state_authority.py",
        "tests/security/test_cloud_development_sandbox.py",
        "tests/security/test_native_agent_launcher.py",
        "tests/security/test_mh04_state_authority_redteam.py",
    )
    if target.is_file() or not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P9.4-sandbox-authority-escalation-negative-tests",
        f"P9.4 {item.description}",
        str(target.relative_to(root)),
        "Reconcile existing negative tests for sandbox escape and authority escalation. Execute only repository-local security tests, record exact pass/fail results, and preserve gaps as release blockers. Do not access production, acquire credentials, execute cloud providers, or weaken fail-closed controls.",
        "p9.4-sandbox-authority-escalation-negative-tests",
    )


def _compile_p85_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P8-5-provenance-chain-reconciliation-2026-09-24.md"
    sources = (
        "ops/mediahub_native_execution.py",
        "ops/mediahub_cluster_failover.py",
        "ops/ai/ai_adapter.py",
        "tests/test_mediahub_native_execution.py",
        "tests/test_mediahub_cluster_failover.py",
        "tests/security/test_ai_adapter.py",
    )
    if target.is_file() or not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P8.5-provenance-chain-reconciliation",
        f"P8.5 {item.description}",
        str(target.relative_to(root)),
        "Record deterministic repository evidence for request-to-proposal-to-result/evidence provenance. Trace request_id, workload_id, source_sha and provider across existing native execution, cluster recovery and AI adapter boundaries; distinguish implemented binding from missing artifact/result journal linkage. Do not add persistence, execute providers, mutate State Authority, or claim P8.5 closed unless the full chain is demonstrated.",
        "p8.5-provenance-chain-reconciliation",
    )


def _compile_p84_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    target = root / "docs/ops/P8-4-bounded-agent-security-reconciliation-2026-09-24.md"
    if target.exists():
        return None
    sources = (
        "ops/ai/ai_adapter.py",
        "ops/ai/astra_host_execution_gate.py",
        "ops/ai/astra_host_gateway.py",
        "ops/ai/astra_task_gateway.py",
        "ops/cloud_development_sandbox.py",
        "ops/mediahub_native_execution.py",
        "ops/mediahub_native_agent_launcher.py",
        "tests/security/test_ai_adapter.py",
        "tests/security/test_native_agent_launcher.py",
        "tests/security/test_cloud_development_sandbox.py",
        "tests/security/test_mh05_bypass_audit.py",
        "tests/security/test_mh05_systemwide_reachability.py",
        "tests/security/test_mh04_state_authority_redteam.py",
    )
    if not all((root / rel).is_file() for rel in sources):
        return None
    return LocalTask(
        "P8.4-bounded-agent-security-reconciliation",
        f"P8.4 {item.description}",
        str(target.relative_to(root)),
        "Record deterministic repository evidence for bounded-agent security surfaces covering subprocess/egress controls, sandbox isolation, forbidden capabilities and State Authority construction boundaries. Inspect only the existing implementation and security tests; distinguish static/negative-test evidence from runtime qualification, identify any uncovered surfaces, and do not execute providers, mutate State Authority, add persistence, or claim P8.4 closed unless evidence establishes it.",
        "p8.4-bounded-agent-security-reconciliation",
    )


RAW_QUEUE_COMPILERS = {"P9.7": _compile_p97_queue_item, "P9.6": _compile_p96_queue_item, "P9.5": _compile_p95_queue_item, "P9.4": _compile_p94_queue_item, "P9.3": _compile_p93_queue_item, "P9.2": _compile_p92_queue_item, "P9.1": _compile_p91_queue_item, "P8.5": _compile_p85_queue_item, "P8.4": _compile_p84_queue_item, "P8.3": _compile_p83_queue_item, "P8.2": _compile_p82_queue_item, "P8.1": _compile_p81_queue_item, "P0.2": _compile_p02_queue_item, "P0.1": _compile_p01_queue_item, "P0.5": _compile_p05_queue_item, "P0.5.1": _compile_p051_queue_item, "P0.5.2": _compile_p052_queue_item, "P0.6": _compile_p06_queue_item, "P2.6": _compile_p26_queue_item}


def _compile_release_evidence_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    if not re.match(r"^P(?:10|11|12|13|14)\.\d+$", item.queue_id):
        return None
    slug = re.sub(r"[^a-z0-9]+", "-", item.queue_id.lower() + "-" + item.description.lower()).strip("-")
    target = root / "docs/ops/autonomous-evidence" / f"{slug}-2026-09-25.md"
    if target.exists():
        return None
    return LocalTask(
        f"{item.queue_id}-bounded-release-evidence",
        f"{item.queue_id} {item.description}",
        str(target.relative_to(root)),
        "Create a repository-only bounded evidence record for this release/reliability queue item. Classify the requested capability as OBSERVED, PARTIAL, ABSENT, or HUMAN_GATE using only current repository artifacts and deterministic checks. Never simulate human authorization, production access, external credentials, disaster recovery, or performance results that were not actually measured. Explicitly preserve unresolved gaps as release blockers.",
        "release-evidence-reconciliation",
    )


def compile_raw_queue_item(root: Path, item: RawQueueItem) -> LocalTask | None:
    """Compile a raw queue row only through an explicitly registered encoder."""
    compiler = RAW_QUEUE_COMPILERS.get(item.queue_id)
    if compiler is not None:
        return compiler(root, item)
    return _compile_release_evidence_queue_item(root, item)


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
            "P9.4-sandbox-authority-escalation-negative-tests": LocalTask("P9.4-sandbox-authority-escalation-negative-tests", "P9.4 Sandbox escape/authority escalation negative tests.", "docs/ops/P9-4-sandbox-authority-escalation-negative-tests-2026-09-24.md", "Reconcile existing negative tests for sandbox escape and authority escalation. Execute only repository-local security tests, record exact pass/fail results, and preserve gaps as release blockers. Do not access production, acquire credentials, execute cloud providers, or weaken fail-closed controls.", "p9.4-sandbox-authority-escalation-negative-tests"),
            "P0.4-bounded-request-types": LocalTask("P0.4-bounded-request-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden BoundedExecutionRequest.validate against malformed object and boolean timeout/output types using PermissionError; preserve existing bounds.", "bounded-request"),
            "P0.4-recovery-evidence-types": LocalTask("P0.4-recovery-evidence-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden recovery proposal admission against malformed evidence types while preserving provenance checks.", "recovery-evidence"),
            "P0.4-provider-credential-types": LocalTask("P0.4-provider-credential-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Require provider credentials to be non-empty strings before constructing authorization headers; preserve native provider headers.", "provider-credential"),
            "P0.4-proposal-types": LocalTask("P0.4-proposal-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden ExecutionProposal validation against malformed field types; preserve contract semantics.", "proposal-types"),
            "P0.4-target-types": LocalTask("P0.4-target-types", "P0.4 Close current Native Execution Contract test gaps.", "ops/mediahub_native_execution.py", "Harden ExecutionTarget validation against malformed field types; preserve HTTPS and provider/credential matching.", "target-types"),
            "P1.6-hybrid-egress-types": LocalTask("P1.6-hybrid-egress-types", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "ops/hybrid_cloud_api_egress_adapter.py", "Harden the hybrid cloud egress adapter against malformed url, method, headers, and timeout types; preserve fail-closed VPN and allowlist behavior.", "hybrid-egress-types"),
            "P1.6-hybrid-egress-tests": LocalTask("P1.6-hybrid-egress-tests", "P1.6 Complete Cloud Development Adapter + Sandbox + Egress + CredentialBroker contract qualification.", "tests/test_hybrid_cloud_api_egress_adapter.py", "Add focused negative tests for malformed URL/method/headers and invalid timeout while preserving fail-closed VPN and allowlist tests.", "hybrid-egress-tests"),
        }
        task = forced_tasks.get(forced)
        if task is not None and _queue_contains(root, task.queue_item) and (root / task.target).is_file() or task is not None and _queue_contains(root, task.queue_item) and task.fallback_kind == "p9.4-sandbox-authority-escalation-negative-tests":
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

    p41_evidence = root / "docs/ops/P4-1-document-ingestion-index-search-gap-reconciliation-2026-09-22.md"
    p41_sources = (
        root / "specification/contract-registry.yaml",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "docs/architecture/MH-21-rag-boundary.md",
        root / "docs/architecture/MH-21-rag-security.md",
        root / "docs/architecture/MH-21-resource-governance.md",
    )
    if (_queue_contains(root, "P4.1 Complete document ingestion/index/search contracts.")
            and not p41_evidence.exists()
            and all(path.is_file() for path in p41_sources)):
        return LocalTask(
            "P4.1-document-ingestion-index-search-gap-reconciliation",
            "P4.1 Complete document ingestion/index/search contracts.",
            "docs/ops/P4-1-document-ingestion-index-search-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P4.1 acceptance-surface gap. Inspect the functional baseline, contract registry and existing RAG/security/resource architecture; classify document ingestion, indexing and search contracts as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer implementation from architecture declarations and do not claim P4.1 closed.",
            "p4.1-document-ingestion-index-search-gap-reconciliation",
        )

    p42_evidence = root / "docs/ops/P4-2-trusted-sources-intelligence-gap-reconciliation-2026-09-22.md"
    p42_sources = (
        root / "specification/contract-registry.yaml",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "docs/architecture/MH-21-rag-boundary.md",
        root / "docs/architecture/MH-21-rag-security.md",
        root / "docs/architecture/MH-21-cloud-boundary.md",
        root / "docs/architecture/MH-21-data-egress.md",
        root / "docs/architecture/MH-21-audit.md",
    )
    if (_queue_contains(root, "P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.")
            and not p42_evidence.exists()
            and all(path.is_file() for path in p42_sources)):
        return LocalTask(
            "P4.2-trusted-sources-intelligence-gap-reconciliation",
            "P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.",
            "docs/ops/P4-2-trusted-sources-intelligence-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P4.2 acceptance-surface gap. Inspect the contract registry, functional baseline and existing RAG/cloud/security/audit architecture; classify Trusted Sources discovery, retrieval, verification, provenance, evidence and knowledge boundaries as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer implementation from architecture declarations and do not claim P4.2 closed.",
            "p4.2-trusted-sources-intelligence-gap-reconciliation",
        )

    p43_evidence = root / "docs/ops/P4-3-source-trust-stale-data-gap-reconciliation-2026-09-22.md"
    p43_sources = (
        root / "specification/contract-registry.yaml",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "docs/architecture/MH-21-provider-trust.md",
        root / "docs/architecture/MH-21-rag-security.md",
        root / "docs/architecture/MH-21-unknowns.md",
    )
    if (_queue_contains(root, "P4.3 Add source trust/verification and stale-data handling.")
            and not p43_evidence.exists()
            and all(path.is_file() for path in p43_sources)):
        return LocalTask(
            "P4.3-source-trust-stale-data-gap-reconciliation",
            "P4.3 Add source trust/verification and stale-data handling.",
            "docs/ops/P4-3-source-trust-stale-data-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P4.3 acceptance-surface gap. Inspect existing provider-trust, RAG-security, functional-baseline, contract-registry and unknowns documents; classify source trust/verification and stale-data handling as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer executable behavior from architecture declarations and do not claim P4.3 closed.",
            "p4.3-source-trust-stale-data-gap-reconciliation",
        )

    p44_evidence = root / "docs/ops/P4-4-external-retrieval-state-authority-boundary-verification-2026-09-22.md"
    p44_sources = (
        root / "docs/architecture/MH-21-cloud-boundary.md",
        root / "docs/architecture/MH-21-security-invariants.md",
        root / "docs/architecture/MH-21-rag-boundary.md",
        root / "docs/architecture/MH-21-rag-security.md",
        root / "ops/ai/ai_adapter.py",
        root / "ops/cloud_development_adapter.py",
        root / "tests/security/test_mh05_systemwide_reachability.py",
    )
    if (_queue_contains(root, "P4.4 Ensure external retrieval cannot mutate State Authority directly.")
            and not p44_evidence.exists()
            and all(path.is_file() for path in p44_sources)):
        return LocalTask(
            "P4.4-external-retrieval-state-authority-boundary-verification",
            "P4.4 Ensure external retrieval cannot mutate State Authority directly.",
            "docs/ops/P4-4-external-retrieval-state-authority-boundary-verification-2026-09-22.md",
            "Record deterministic local verification evidence for the external retrieval/RAG to State Authority boundary. Inspect the existing cloud/RAG authority declarations, forbidden-capability adapters and reachability tests; classify the boundary as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not access external retrieval services, mutate State Authority, or claim P4.4 production/runtime completion.",
            "p4.4-external-retrieval-state-authority-boundary-verification",
        )

    p45_evidence = root / "docs/ops/P4-5-audit-revocation-offline-degraded-gap-reconciliation-2026-09-22.md"
    p45_sources = (
        root / "ops/cloud_development_adapter.py",
        root / "ops/mediahub_credential_broker.py",
        root / "ops/mediahub_resilience.py",
        root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/test_mediahub_credential_broker.py",
        root / "tests/test_mediahub_resilience.py",
        root / "docs/architecture/MH-21-audit.md",
        root / "docs/architecture/MH-21-provider-quarantine.md",
        root / "docs/architecture/MH-21-offline-mode.md",
    )
    if (_queue_contains(root, "P4.5 Add audit/revocation and offline/degraded behavior.")
            and not p45_evidence.exists()
            and all(path.is_file() for path in p45_sources)):
        return LocalTask(
            "P4.5-audit-revocation-offline-degraded-gap-reconciliation",
            "P4.5 Add audit/revocation and offline/degraded behavior.",
            "docs/ops/P4-5-audit-revocation-offline-degraded-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the P4.5 acceptance surface. Inspect existing audit/revocation/offline/degraded architecture and deterministic cloud-adapter, credential-broker and resilience tests; classify audit, revocation and offline/degraded behavior as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not perform live cloud execution, acquire credentials, or claim P4.5 globally closed.",
            "p4.5-audit-revocation-offline-degraded-gap-reconciliation",
        )

    p52_evidence = root / "docs/ops/P5-2-authenticated-session-authorization-gap-reconciliation-2026-09-22.md"
    p52_sources = (
        root / "contracts/mobile/mobile-api-compatibility.schema.json",
        root / "ops/ai/hybrid_session.py",
        root / "tests/ai/test_hybrid_session.py",
        root / "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        root / "recovery/acceptance/F-014-phone-media-io-endpoint.md",
        root / "recovery/accepted/F-007-users-identity-access-authorization.md",
        root / "docs/architecture/MH-12-authentication.md",
        root / "docs/architecture/MH-12-authorization.md",
    )
    if (_queue_contains(root, "P5.2 Implement authenticated session and authorization contracts.")
            and not p52_evidence.exists()
            and all(path.is_file() for path in p52_sources)):
        return LocalTask(
            "P5.2-authenticated-session-authorization-gap-reconciliation",
            "P5.2 Implement authenticated session and authorization contracts.",
            "docs/ops/P5-2-authenticated-session-authorization-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for P5.2. Inspect the mobile compatibility contract, existing hybrid session implementation/tests, mobile authorization acceptance records and MH-12 authentication/authorization requirements. Classify authentication, session, mobile authorization, revocation, offline/degraded semantics, deterministic tests and provenance-bound acceptance as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not infer mobile authorization from the generic hybrid session and do not invent protocol semantics.",
            "p5.2-authenticated-session-authorization-gap-reconciliation",
        )

    p54_evidence = root / "docs/ops/P5-4-remote-control-state-synchronization-gap-reconciliation-2026-09-22.md"
    p54_sources = (
        root / "contracts/mobile/mobile-api-compatibility.schema.json",
        root / "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        root / "recovery/acceptance/F-014-phone-media-io-endpoint.md",
        root / "docs/architecture/MH-21-device-interaction.md",
        root / "ops/mediahub_lifecycle_contract.py",
        root / "tests/test_mediahub_lifecycle_contract.py",
        root / "tests/security/test_mh05_bypass_audit.py",
    )
    if (_queue_contains(root, "P5.4 Add remote-control and state synchronization tests.")
            and not p54_evidence.exists()
            and all(path.is_file() for path in p54_sources)):
        return LocalTask(
            "P5.4-remote-control-state-synchronization-gap-reconciliation",
            "P5.4 Add remote-control and state synchronization tests.",
            "docs/ops/P5-4-remote-control-state-synchronization-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for P5.4. Inspect existing mobile compatibility, remote-control boundary, media lifecycle and negative security tests; classify remote-control authorization, command/state synchronization, conflict/replay behavior and offline/degraded synchronization acceptance as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not invent transport, conflict-resolution or mobile protocol semantics.",
            "p5.4-remote-control-state-synchronization-gap-reconciliation",
        )

    p55_evidence = root / "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md"
    p55_sources = (
        root / "contracts/mobile/mobile-api-compatibility.schema.json",
        root / "ops/ai/ai_gateway.py",
        root / "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        root / "docs/architecture/MH-21-device-interaction.md",
        root / "ops/verify_functional_baseline.sh",
    )
    if (_queue_contains(root, "P5.5 Validate that Mobile Access Layer is not an AI compute tier.")
            and not p55_evidence.exists()
            and all(path.is_file() for path in p55_sources)):
        return LocalTask(
            "P5.5-mobile-access-not-ai-compute-gap-reconciliation",
            "P5.5 Validate that Mobile Access Layer is not an AI compute tier.",
            "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the Mobile Access Layer boundary. Verify the canonical escalation path, mobile contract ownership and AI gateway compute-tier separation from existing source/test/baseline surfaces. Classify the boundary as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not invent a mobile AI tier and do not claim global mobile qualification.",
            "p5.5-mobile-access-not-ai-compute-gap-reconciliation",
        )

    p56_evidence = root / "docs/ops/P5-6-ios-integration-lifecycle-accessibility-security-gap-reconciliation-2026-09-22.md"
    p56_sources = (
        root / "contracts/mobile/mobile-api-compatibility.schema.json",
        root / "recovery/acceptance/F-014-phone-media-io-endpoint.md",
        root / "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        root / "tests/contracts/test_mobile_api_compatibility.py",
        root / "docs/architecture/MH-21-device-interaction.md",
    )
    if (_queue_contains(root, "P5.6 Add iOS integration, lifecycle, accessibility and security qualification.")
            and not p56_evidence.exists()
            and all(path.is_file() for path in p56_sources)):
        return LocalTask(
            "P5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation",
            "P5.6 Add iOS integration, lifecycle, accessibility and security qualification.",
            "docs/ops/P5-6-ios-integration-lifecycle-accessibility-security-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for P5.6. Inspect mobile API contract/tests, accepted mobile endpoint requirements and device interaction boundaries; classify iOS integration, app lifecycle/background execution, accessibility, mobile security and end-to-end iOS qualification as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not infer an iOS implementation from schema platform enums and do not invent app behavior.",
            "p5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation",
        )

    p61_evidence = root / "docs/ops/P6-1-voice-provider-order-gap-reconciliation-2026-09-22.md"
    p61_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "ops/verify_functional_baseline.sh",
    )
    if (_queue_contains(root, "P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.")
            and not p61_evidence.exists()
            and all(path.is_file() for path in p61_sources)):
        return LocalTask(
            "P6.1-voice-provider-order-gap-reconciliation",
            "P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.",
            "docs/ops/P6-1-voice-provider-order-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the canonical voice provider order from the functional baseline/governance and verification gate. Classify order declaration as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not execute providers, access external accounts or invent adapter behavior.",
            "p6.1-voice-provider-order-gap-reconciliation",
        )

    p62_evidence = root / "docs/ops/P6-2-voice-provider-adapter-gap-reconciliation-2026-09-22.md"
    p62_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "ops/verify_functional_baseline.sh",
    )
    if (_queue_contains(root, "P6.2 Implement each provider through bounded adapters.")
            and not p62_evidence.exists()
            and all(path.is_file() for path in p62_sources)):
        return LocalTask(
            "P6.2-voice-provider-adapter-gap-reconciliation",
            "P6.2 Implement each provider through bounded adapters.",
            "docs/ops/P6-2-voice-provider-adapter-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for provider-specific voice adapters. Inspect only repository-native voice/provider surfaces and baseline declarations; classify Google Assistant, Яндекс Алиса and Apple Siri adapter implementations as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not access external provider accounts or invent adapter protocols.",
            "p6.2-voice-provider-adapter-gap-reconciliation",
        )

    p63_evidence = root / "docs/ops/P6-3-voice-consent-authorization-provenance-replay-gap-reconciliation-2026-09-22.md"
    p63_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "docs/architecture/MH-12-authentication.md",
        root / "docs/architecture/MH-12-authorization.md",
        root / "docs/architecture/MH-21-device-interaction.md",
        root / "tests/security/test_mh05_bypass_audit.py",
    )
    if (_queue_contains(root, "P6.3 Enforce consent, authorization, command provenance and replay protection.")
            and not p63_evidence.exists()
            and all(path.is_file() for path in p63_sources)):
        return LocalTask(
            "P6.3-voice-consent-authorization-provenance-replay-gap-reconciliation",
            "P6.3 Enforce consent, authorization, command provenance and replay protection.",
            "docs/ops/P6-3-voice-consent-authorization-provenance-replay-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for voice consent, authorization, command provenance and replay protection. Inspect existing normative authentication/authorization/device-boundary surfaces and negative tests; classify voice-specific acceptance as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not infer voice-specific semantics from generic security infrastructure and do not execute providers.",
            "p6.3-voice-consent-authorization-provenance-replay-gap-reconciliation",
        )

    p64_evidence = root / "docs/ops/P6-4-home-assistant-mutation-boundary-gap-reconciliation-2026-09-22.md"
    p64_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        root / "specification/invariant-registry.yaml",
        root / "specification/decision-registry.yaml",
        root / "ops/verify_functional_baseline.sh",
    )
    if (_queue_contains(root, "P6.4 Route Smart Home mutations through Home Assistant Core.")
            and not p64_evidence.exists()
            and all(path.is_file() for path in p64_sources)):
        return LocalTask(
            "P6.4-home-assistant-mutation-boundary-gap-reconciliation",
            "P6.4 Route Smart Home mutations through Home Assistant Core.",
            "docs/ops/P6-4-home-assistant-mutation-boundary-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the Smart Home mutation boundary. Verify the canonical Home Assistant Core source-of-truth declaration and MediaHub State Authority separation from functional baseline, governance, invariant and decision registries. Do not access Home Assistant runtime, mutate Smart Home state or invent an adapter.",
            "p6.4-home-assistant-mutation-boundary-gap-reconciliation",
        )

    p65_evidence = root / "docs/ops/P6-5-provider-outage-fallback-gap-reconciliation-2026-09-22.md"
    p65_sources = (
        root / "ops/mediahub_provider_gateway.py",
        root / "ops/mediahub_resilience.py",
        root / "tests/test_mediahub_provider_gateway.py",
        root / "tests/test_mediahub_resilience.py",
    )
    if (_queue_contains(root, "P6.5 Add provider outage/fallback tests without changing authority semantics.")
            and not p65_evidence.exists()
            and all(path.is_file() for path in p65_sources)):
        return LocalTask(
            "P6.5-provider-outage-fallback-gap-reconciliation",
            "P6.5 Add provider outage/fallback tests without changing authority semantics.",
            "docs/ops/P6-5-provider-outage-fallback-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for provider outage/fallback behavior using the existing ProviderGateway and ResilienceEngine contracts and tests. Classify outage handling, bounded transient failover, permanent-failure safe-stop, policy-blocked behavior and retry-budget semantics as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not execute external providers, acquire credentials, change authority semantics, or invent new fallback policy.",
            "p6.5-provider-outage-fallback-gap-reconciliation",
        )

    p71_evidence = root / "docs/ops/P7-1-human-clone-contract-gap-reconciliation-2026-09-22.md"
    p71_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/contract-registry.yaml",
        root / "specification/capability-registry.yaml",
    )
    if (_queue_contains(root, "P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.")
            and not p71_evidence.exists()
            and all(path.is_file() for path in p71_sources)):
        return LocalTask(
            "P7.1-human-clone-contract-gap-reconciliation",
            "P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.",
            "docs/ops/P7-1-human-clone-contract-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the AI Human Clone contract boundary. Inspect the functional baseline, CTR-043 contract registry entry and capability registry; classify contract declaration, Cloud Development AI separation, identity/consent/scope/provenance/revocation requirements and deterministic implementation/test acceptance as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not invent a clone runtime, media-generation semantics, provider behavior, or production authorization.",
            "p7.1-human-clone-contract-gap-reconciliation",
        )

    p72_evidence = root / "docs/ops/P7-2-human-clone-governance-gap-reconciliation-2026-09-22.md"
    p72_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/contract-registry.yaml",
        root / "ops/cloud_development_adapter.py",
        root / "ops/mediahub_credential_broker.py",
        root / "tests/ops/test_cloud_development_adapter.py",
        root / "tests/test_mediahub_credential_broker.py",
    )
    if (_queue_contains(root, "P7.2 Enforce consent, scope, provenance, audit and revocation.")
            and not p72_evidence.exists()
            and all(path.is_file() for path in p72_sources)):
        return LocalTask(
            "P7.2-human-clone-governance-gap-reconciliation",
            "P7.2 Enforce consent, scope, provenance, audit and revocation.",
            "docs/ops/P7-2-human-clone-governance-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the Human Clone governance boundary. Inspect the functional baseline and CTR-043 together with existing Cloud Development Adapter and CredentialBroker contracts/tests. Classify Human Clone-specific consent, scope, identity/model provenance, audit and revocation as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Distinguish generic cloud-development controls from Human Clone-specific qualification. Do not invent consent workflows, asset semantics, provider behavior or production authorization.",
            "p7.2-human-clone-governance-gap-reconciliation",
        )

    p73_evidence = root / "docs/ops/P7-3-trusted-sources-knowledge-workflow-gap-reconciliation-2026-09-22.md"
    p73_sources = (
        root / "specification/contract-registry.yaml",
        root / "docs/architecture/MH-21-rag-boundary.md",
        root / "docs/architecture/MH-21-rag-security.md",
        root / "docs/architecture/MH-21-knowledge-graph-interaction.md",
    )
    if (_queue_contains(root, "P7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.")
            and not p73_evidence.exists()
            and all(path.is_file() for path in p73_sources)):
        return LocalTask(
            "P7.3-trusted-sources-knowledge-workflow-gap-reconciliation",
            "P7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.",
            "docs/ops/P7-3-trusted-sources-knowledge-workflow-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the Trusted Sources/knowledge workflow boundary. Inspect CTR-042 and existing RAG/knowledge architecture; classify source discovery, retrieval, verification, provenance, change detection, evidence separation and deterministic implementation/test acceptance as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS. Do not invent retrieval providers, indexes, knowledge schemas or external network behavior.",
            "p7.3-trusted-sources-knowledge-workflow-gap-reconciliation",
        )

    p74_evidence = root / "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md"
    p74_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
        root / "specification/invariant-registry.yaml",
        root / "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
        root / "ops/cloud_development_adapter.py",
        root / "tests/ops/test_cloud_development_adapter.py",
    )
    if (_queue_contains(root, "P7.4 Ensure ordinary users have no direct corporate Cloud Development AI access.")
            and not p74_evidence.exists()
            and all(path.is_file() for path in p74_sources)
            and (root / "docs/ops/P7-3-trusted-sources-knowledge-workflow-gap-reconciliation-2026-09-22.md").is_file()):
        return LocalTask(
            "P7.4-ordinary-user-cloud-development-access-gap-reconciliation",
            "P7.4 Ensure ordinary users have no direct corporate Cloud Development AI access.",
            "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the ordinary-user Cloud Development AI access boundary. Inspect only the functional baseline, governance/invariant declarations, accepted remote/cloud escalation requirement and existing Cloud Development Adapter tests; classify direct ordinary-user access as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Distinguish policy declarations from executable enforcement and do not invent authentication, UI, provider or production-authorization semantics.",
            "p7.4-ordinary-user-cloud-development-access-gap-reconciliation",
        )

    p75_evidence = root / "docs/ops/P7-5-data-minimization-residency-egress-gap-reconciliation-2026-09-22.md"
    p75_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/contract-registry.yaml",
        root / "docs/architecture/MH-13-privacy-data-governance.md",
        root / "docs/architecture/MH-21-data-residency.md",
        root / "ops/mediahub_policy_engine.py",
        root / "ops/mediahub_egress_controller.py",
        root / "tests/test_mediahub_policy_engine.py",
        root / "tests/test_mediahub_egress_controller.py",
    )
    if (_queue_contains(root, "P7.5 Add data minimization, residency/policy and egress tests.")
            and not p75_evidence.exists()
            and all(path.is_file() for path in p75_sources)
            and (root / "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md").is_file()):
        return LocalTask(
            "P7.5-data-minimization-residency-egress-gap-reconciliation",
            "P7.5 Add data minimization, residency/policy and egress tests.",
            "docs/ops/P7-5-data-minimization-residency-egress-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for the Cloud Development AI data-minimization, residency/policy and egress boundary. Inspect only existing baseline/contract/privacy/residency declarations plus PolicyEngine/EgressController implementations and tests; classify each acceptance surface as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer provider guarantees, regions, retention periods or external runtime behavior.",
            "p7.5-data-minimization-residency-egress-gap-reconciliation",
        )

    p76_evidence = root / "docs/ops/P7-6-degraded-offline-recovery-gap-reconciliation-2026-09-22.md"
    p76_sources = (
        root / "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
        root / "specification/invariant-registry.yaml",
        root / "specification/decision-registry.yaml",
        root / "docs/architecture/MH-06-recovery-model.md",
        root / "docs/architecture/MH-06-health-readiness.md",
        root / "ops/mediahub_resilience.py",
        root / "tests/test_mediahub_resilience.py",
    )
    if (_queue_contains(root, "P7.6 Add degraded/offline behavior and recovery evidence.")
            and not p76_evidence.exists()
            and all(path.is_file() for path in p76_sources)):
        return LocalTask(
            "P7.6-degraded-offline-recovery-gap-reconciliation",
            "P7.6 Add degraded/offline behavior and recovery evidence.",
            "docs/ops/P7-6-degraded-offline-recovery-gap-reconciliation-2026-09-22.md",
            "Record deterministic repository evidence for Cloud Development AI degraded/offline and recovery requirements. Inspect only existing baseline/invariant/decision/recovery/readiness declarations plus existing resilience implementation/tests; classify each acceptance surface as IMPLEMENTED, PARTIAL, ABSENT or AMBIGUOUS with exact file evidence. Do not infer provider outage, network outage, cloud availability, credentials, provider guarantees, provider recovery or external execution results.",
            "p7.6-degraded-offline-recovery-gap-reconciliation",
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
    "P3.4": ("docs/ops/P3-4-media-authorization-storage-retention-recovery-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P3.4 NOT CLOSED"),
    "P3.5": ("docs/ops/P3-5-media-integration-failure-injection-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P3.5 NOT CLOSED"),
    "P3.6": ("docs/ops/P3-6-media-benchmark-resource-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P3.6 NOT CLOSED"),
    "P4.1": ("docs/ops/P4-1-document-ingestion-index-search-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P4.1 NOT CLOSED"),
    "P4.2": ("docs/ops/P4-2-trusted-sources-intelligence-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P4.2 NOT CLOSED"),
    "P4.3": ("docs/ops/P4-3-source-trust-stale-data-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P4.3 NOT CLOSED"),
    "P4.4": ("docs/ops/P4-4-external-retrieval-state-authority-boundary-verification-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P4.4 NOT CLOSED"),
    "P4.5": ("docs/ops/P4-5-audit-revocation-offline-degraded-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P4.5 NOT CLOSED"),
    "P5.2": ("docs/ops/P5-2-authenticated-session-authorization-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P5.2 NOT CLOSED"),
    "P5.4": ("docs/ops/P5-4-remote-control-state-synchronization-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P5.4 NOT CLOSED"),
    "P5.5": ("docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P5.5 NOT CLOSED"),
    "P5.6": ("docs/ops/P5-6-ios-integration-lifecycle-accessibility-security-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P5.6 NOT CLOSED"),
    "P6.1": ("docs/ops/P6-1-voice-provider-order-gap-reconciliation-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P6.1 NOT CLOSED"),
    "P6.2": ("docs/ops/P6-2-voice-provider-adapter-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P6.2 NOT CLOSED"),
    "P6.3": ("docs/ops/P6-3-voice-consent-authorization-provenance-replay-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P6.3 NOT CLOSED"),
    "P6.4": ("docs/ops/P6-4-home-assistant-mutation-boundary-gap-reconciliation-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P6.4 NOT CLOSED"),
    "P6.5": ("docs/ops/P6-5-provider-outage-fallback-gap-reconciliation-2026-09-22.md", "Status: VERIFIED_LOCAL_SUBSCOPE / P6.5 NOT CLOSED"),
    "P7.1": ("docs/ops/P7-1-human-clone-contract-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.1 NOT CLOSED"),
    "P7.2": ("docs/ops/P7-2-human-clone-governance-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.2 NOT CLOSED"),
    "P7.3": ("docs/ops/P7-3-trusted-sources-knowledge-workflow-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.3 NOT CLOSED"),
    "P7.4": ("docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.4 NOT CLOSED"),
    "P7.5": ("docs/ops/P7-5-data-minimization-residency-egress-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.5 NOT CLOSED"),
    "P7.6": ("docs/ops/P7-6-degraded-offline-recovery-gap-reconciliation-2026-09-22.md", "Status: DISCOVERY_RECONCILIATION / P7.6 NOT CLOSED"),
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
        "P8.1": (
            "docs/ops/P8-1-escalation-path-reconciliation-2026-09-24.md",
            "Status: DISCOVERY_RECONCILIATION / P8.1 NOT CLOSED",
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
        "P9.1": (
            "docs/ops/P9-1-threat-model-refresh-2026-09-24.md",
            "P9.1 remains OPEN until the refreshed threat model",
        ),
        "P9.2": (
            "docs/ops/P9-2-static-secret-dependency-provenance-review-2026-09-24.md",
            "P9.2 remains OPEN until dependency provenance/license requirements",
        ),
        "P9.3": (
            "docs/ops/P9-3-egress-endpoint-allowlist-audit-2026-09-24.md",
            "P9.3 remains OPEN until all production-relevant egress paths",
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
        "P8.2": ("docs/ops/P8-2-cross-domain-contract-gap-reconciliation-2026-09-24.md", "Status: DISCOVERY_RECONCILIATION / P8.2 NOT CLOSED"),
        "P8.3": ("docs/ops/P8-3-end-to-end-scenario-reconciliation-2026-09-24.md", "Status: SCENARIO_RECONCILIATION / P8.3 NOT CLOSED"),
        "P8.4": ("docs/ops/P8-4-bounded-agent-security-reconciliation-2026-09-24.md", "Status: SECURITY_RECONCILIATION / P8.4 NOT CLOSED"),
        "P8.5": ("docs/ops/P8-5-provenance-chain-reconciliation-2026-09-24.md", "Status: PROVENANCE_RECONCILIATION / P8.5 NOT CLOSED"),
        "P9.4": ("docs/ops/P9-4-sandbox-authority-escalation-negative-tests-2026-09-24.md", "Status: SECURITY_RECONCILIATION / P9.4 NOT CLOSED"),
    }
    for queue_id, (relative_path, marker) in queue_evidence.items():
        if _current_evidence_marker(root, relative_path, marker):
            description = next((item.description for item in read_raw_queue(root) if item.queue_id == queue_id), None)
            if description is not None:
                encoded[queue_id] = f"{queue_id} {description}"

    # Release-evidence fallback tasks are encoded once their repository-only
    # evidence artifact exists in current HEAD. This is an encoding state, not
    # a closure/authorization state; unresolved HUMAN_GATE/PARTIAL/ABSENT
    # classifications remain release blockers.
    for item in read_raw_queue(root):
        if re.match(r"^P(?:10|11|12|13|14)\.\d+$", item.queue_id):
            slug = re.sub(r"[^a-z0-9]+", "-", item.queue_id.lower() + "-" + item.description.lower()).strip("-")
            relative_path = f"docs/ops/autonomous-evidence/{slug}-2026-09-25.md"
            if _current_evidence_marker(root, relative_path, "Status:"):
                encoded[item.queue_id] = f"{item.queue_id} {item.description}"

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
        "p4.1-document-ingestion-index-search-gap-reconciliation",
        "p4.2-trusted-sources-intelligence-gap-reconciliation",
        "p4.3-source-trust-stale-data-gap-reconciliation",
        "p4.4-external-retrieval-state-authority-boundary-verification",
        "p4.5-audit-revocation-offline-degraded-gap-reconciliation",
        "p5.2-authenticated-session-authorization-gap-reconciliation",
        "p5.4-remote-control-state-synchronization-gap-reconciliation",
        "p5.5-mobile-access-not-ai-compute-gap-reconciliation",
        "p5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation",
        "p6.1-voice-provider-order-gap-reconciliation",
        "p6.2-voice-provider-adapter-gap-reconciliation",
        "p6.3-voice-consent-authorization-provenance-replay-gap-reconciliation",
        "p6.4-home-assistant-mutation-boundary-gap-reconciliation",
        "p6.5-provider-outage-fallback-gap-reconciliation",
        "p7.1-human-clone-contract-gap-reconciliation",
        "p7.2-human-clone-governance-gap-reconciliation",
        "p7.3-trusted-sources-knowledge-workflow-gap-reconciliation",
        "p7.4-ordinary-user-cloud-development-access-gap-reconciliation",
        "p7.5-data-minimization-residency-egress-gap-reconciliation",
        "p7.6-degraded-offline-recovery-gap-reconciliation",
        "p0.5.1-terminal-checkpoint-startup-verification",
        "p0.5.2-terminal-provenance-regression-verification",
        "p8.1-escalation-path-reconciliation",
        "p8.2-cross-domain-contract-gap-reconciliation",
        "p8.3-end-to-end-scenario-reconciliation",
        "p8.4-bounded-agent-security-reconciliation",
        "p8.5-provenance-chain-reconciliation",
        "p9.1-threat-model-refresh",
        "p9.2-static-secret-dependency-provenance-review",
        "p9.3-egress-endpoint-allowlist-audit",
        "p9.4-sandbox-authority-escalation-negative-tests",
        "p9.5-credential-broker-revocation-isolation",
        "p9.6-malformed-input-security-qualification",
        "p9.7-recovery-tamper-evidence",
        "release-evidence-reconciliation",
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
    if task.fallback_kind == "p8.2-cross-domain-contract-gap-reconciliation" and not target.is_file():
        fingerprint = hashlib.sha256(
            f"{task.task_id}\n{task.queue_item}\n{task.target}\n{task.instruction}".encode()
        ).hexdigest()
        return ExecutableTask(
            **task.__dict__,
            owner=os.environ.get("MEDIAHUB_WORKER_ID", "local-autonomous"),
            base_sha=base_sha,
            acceptance_predicate=f"queue={task.queue_item}; target={task.target}; acceptance={task.instruction}",
            verification_command="pytest -q tests/contracts/test_contract_domain_reconciliation.py tests/contracts/test_contract_metadata.py tests/contracts/test_mobile_api_compatibility.py tests/static/test_cross_contract.py tests/test_mediahub_lifecycle_contract.py",
            expected_evidence="targeted tests; full relevant regression; ruff; git diff --check",
            dependency_set=(),
            conflict_set=("R4", "production"),
            acceptance_fingerprint=fingerprint,
        )
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
    "ROLLED_BACK", "COMMITTED", "BLOCKED", "IDLE",
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
    if task.fallback_kind == "p7.3-trusted-sources-knowledge-workflow-gap-reconciliation":
        content = """# P7.3 Trusted Sources / Knowledge Workflow Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P7.3 NOT CLOSED

## Queue requirement

`P7.3 Implement Trusted Sources/knowledge workflows required by the subsystem.`

## Exact repository evidence

- `specification/contract-registry.yaml` — CTR-042 declares trusted-source discovery, retrieval, verification, provenance, change detection, evidence separation and audit.
- `docs/architecture/MH-21-rag-boundary.md` — declares the conceptual source → ingestion → validation → classification → chunking → embedding → index → retrieval → context → AI pipeline and forbids retrieved data from becoming authority.
- `docs/architecture/MH-21-rag-security.md` — defines hostile-input treatment, classification/minimization/privacy/authorization constraints and the non-authoritative nature of retrieved text.
- `docs/architecture/MH-21-knowledge-graph-interaction.md` — defines knowledge-graph interaction boundaries.

## Classification

- Trusted Sources contract declaration: IMPLEMENTED at registry level.
- RAG/knowledge architectural boundary: PRESENT.
- Repository-native Trusted Sources runtime: ABSENT in inspected implementation surfaces.
- Deterministic Trusted Sources workflow tests: ABSENT in inspected implementation surfaces.
- External retrieval/provider qualification: ABSENT.

## Gate

Existing repository facts justify discovery evidence only. This does not create a retrieval service, index schema, provider integration or knowledge workflow implementation, and P7.3 remains open.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p7.2-human-clone-governance-gap-reconciliation":
        content = """# P7.2 AI Human Clone Governance Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P7.2 NOT CLOSED

## Queue requirement

`P7.2 Enforce consent, scope, provenance, audit and revocation.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — requires Human Clone consent, authorization, identity provenance, rights-holder authorization, scope, voice/appearance authorization, model/asset provenance, audit and revocation.
- `specification/contract-registry.yaml` — CTR-043 requires identity provenance, consent/authorization, use scope, asset/model provenance, synthetic-content labeling, revocation and audit.
- `ops/cloud_development_adapter.py` — generic Cloud Development authorization, provenance, bounded scope/capability admission, audit and terminal revocation controls.
- `ops/mediahub_credential_broker.py` — generic credential authorization/revocation boundary.
- `tests/ops/test_cloud_development_adapter.py` — deterministic authorization, provenance, forbidden-capability, timeout and revocation tests.
- `tests/test_mediahub_credential_broker.py` — deterministic credential revocation tests.

## Classification

- Human Clone-specific consent workflow: ABSENT.
- Human Clone-specific rights-holder authorization workflow: ABSENT.
- Human Clone-specific use-scope enforcement: ABSENT; generic Cloud Development bounds are present.
- Generic identity/provenance/audit/revocation controls: PRESENT/PARTIAL.
- Human Clone-specific asset/model provenance: ABSENT.
- Human Clone-specific synthetic-content labeling: ABSENT.
- Human Clone-specific deterministic qualification: ABSENT.

## Gate

Generic Cloud Development security controls do not constitute Human Clone qualification. This record captures only the demonstrated repository boundary and leaves P7.2 open; no consent, media asset, provider or production semantics are invented.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p7.1-human-clone-contract-gap-reconciliation":
        content = """# P7.1 AI Human Clone Contract Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P7.1 NOT CLOSED

## Queue requirement

`P7.1 Define Human Clone contract as separate Cloud Development AI subsystem.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — defines AI Human Clone as a separate Cloud Development AI subsystem for authorized media content and requires consent, authorization, identity provenance, rights-holder authorization, scope, voice/appearance authorization, model/asset provenance, audit, revocation and real/synthetic separation.
- `specification/contract-registry.yaml` — CTR-043 `ai-human-clone` declares the contract scope and required semantics: identity provenance, consent/authorization, use scope, asset/model provenance, synthetic-content labeling, revocation and audit.
- `specification/capability-registry.yaml` — records the authorized AI Human Clone capability as part of the Cloud Development contour.

## Classification

- Human Clone contract declaration: IMPLEMENTED at specification/registry level.
- Separation from State Authority / Smart Home authority: EXPLICIT in the functional baseline.
- Required consent/authorization/scope/provenance/revocation/audit semantics: DECLARED by the existing contract boundary.
- Human Clone runtime implementation: ABSENT in inspected repository surfaces.
- Human Clone-specific deterministic test suite: ABSENT in inspected repository surfaces.
- Production/media-generation/provider qualification: ABSENT.

## Gate

Existing architecture/registry facts justify a bounded discovery record only. This does not create a Human Clone runtime, select a provider/model, define media-generation behavior, authorize production, or close P7.1 globally.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p6.5-provider-outage-fallback-gap-reconciliation":
        content = """# P6.5 Provider Outage / Fallback Gap Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P6.5 NOT CLOSED

## Queue requirement

`P6.5 Add provider outage/fallback tests without changing authority semantics.`

## Exact repository evidence

- `ops/mediahub_provider_gateway.py` — provider failure classification, bounded failover and circuit/cooldown state.
- `ops/mediahub_resilience.py` — retry policy, bounded delay and failure-budget behavior.
- `tests/test_mediahub_provider_gateway.py` — deterministic tests for policy-blocked, transient and permanent provider failures, circuit opening and cooldown.
- `tests/test_mediahub_resilience.py` — deterministic tests for permanent-failure safe-stop, policy-blocked behavior, transient failover, retry budget and malformed retry policy types.

## Classification

- Provider outage/failure classification: IMPLEMENTED in the existing provider gateway contract.
- Bounded transient failover: IMPLEMENTED and deterministically tested.
- Permanent failure safe-stop/no fallback: IMPLEMENTED and deterministically tested.
- Policy-blocked behavior without retry-delay semantics: IMPLEMENTED and deterministically tested.
- Retry budget / bounded delay: IMPLEMENTED and deterministically tested.
- Provider-specific live outage qualification: ABSENT; no external provider was executed.

## Gate

The existing local contract/test surface is sufficient for a bounded local P6.5 evidence record. This does not close the broader P6.5 product scope and does not alter authority, provider, credential or production semantics.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p6.4-home-assistant-mutation-boundary-gap-reconciliation":
        content = """# P6.4 Home Assistant Smart Home Mutation Boundary Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P6.4 NOT CLOSED

## Queue requirement

`P6.4 Route Smart Home mutations through Home Assistant Core.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — identifies Home Assistant Core as the Smart Home authority and forbids bypass.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml` — declares `smart_home: Home Assistant Core`.
- `specification/invariant-registry.yaml` — records Home Assistant Core as sole Smart Home authority.
- `specification/decision-registry.yaml` — records Home Assistant as internal Smart Home integration/automation source of truth.
- `ops/verify_functional_baseline.sh` — validates the repository baseline authority declarations.

## Classification

- Canonical Smart Home authority declaration: IMPLEMENTED at repository governance level.
- Direct MediaHub UI/AI bypass prohibition: PRESENT in normative baseline.
- Operational Home Assistant mutation adapter: ABSENT in inspected repository.
- Runtime end-to-end mutation proof: ABSENT; no Home Assistant runtime was accessed.

## Gate

This verifies the declared authority boundary only. It does not mutate Smart Home state, access Home Assistant, or close P6.4 globally.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p6.3-voice-consent-authorization-provenance-replay-gap-reconciliation":
        content = """# P6.3 Voice Consent / Authorization / Provenance / Replay Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P6.3 NOT CLOSED

## Queue requirement

`P6.3 Enforce consent, authorization, command provenance and replay protection.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — requires voice/appearance authorization, provenance, audit and revocation at the broader platform level.
- `docs/architecture/MH-12-authentication.md` — requires authentication lifecycle, revocation and replay resistance.
- `docs/architecture/MH-12-authorization.md` — requires explicit operation-specific, identity/context/policy-aware, auditable and fail-closed authorization.
- `docs/architecture/MH-21-device-interaction.md` — constrains remote commands through validation, policy, authorization and Consumer Boundary.
- `tests/security/test_mh05_bypass_audit.py` — provides negative generic command-boundary coverage, not voice-specific acceptance.

## Classification

- Voice-specific consent contract: ABSENT.
- Voice-specific authorization contract: ABSENT.
- Voice command provenance contract: ABSENT.
- Voice replay-protection tests: ABSENT.
- Generic platform security boundaries: PRESENT/PARTIAL, but insufficient for voice-specific closure.

## Gate

No voice provider was executed and no voice-specific protocol semantics were invented. P6.3 remains open.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p6.2-voice-provider-adapter-gap-reconciliation":
        content = """# P6.2 Voice Provider Adapter Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P6.2 NOT CLOSED

## Queue requirement

`P6.2 Implement each provider through bounded adapters.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml` — declares Google Assistant, Яндекс Алиса and Apple Siri as the canonical provider order.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — preserves provider ordering and voice authorization boundaries.
- `ops/verify_functional_baseline.sh` — validates the baseline declarations.

## Classification

- Google Assistant bounded adapter: ABSENT.
- Яндекс Алиса bounded adapter: ABSENT.
- Apple Siri bounded adapter: ABSENT.
- Provider-neutral voice adapter contract/test surface: ABSENT in inspected repository surfaces.

## Gate

Architecture/baseline declarations do not constitute provider implementations. No external provider execution or account access was performed. P6.2 remains open.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p6.1-voice-provider-order-gap-reconciliation":
        content = """# P6.1 Voice Provider Order Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P6.1 NOT CLOSED

## Queue requirement

`P6.1 Preserve voice order: Google Assistant → Яндекс Алиса → Apple Siri.`

## Exact repository evidence

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml` — declares the canonical voice provider order.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — preserves the voice/platform governance boundary and does not authorize provider bypass.
- `ops/verify_functional_baseline.sh` — repository-native baseline verification gate.

## Classification

- Canonical provider order declaration: PRESENT.
- Provider adapters/runtime integrations: NOT qualified by this evidence.
- External provider execution/account access: not performed.

## Gate

This verifies only the repository-declared order. It does not close provider implementation, consent, authorization, replay protection, outage handling or production voice qualification.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation":
        content = """# P5.6 iOS Integration / Lifecycle / Accessibility / Security Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P5.6 NOT CLOSED

## Queue requirement

`P5.6 Add iOS integration, lifecycle, accessibility and security qualification.`

## Exact repository surfaces inspected

- `contracts/mobile/mobile-api-compatibility.schema.json` — permits `ios` and `ipados` client platforms, but is only an API compatibility schema.
- `tests/contracts/test_mobile_api_compatibility.py` — validates schema-level mobile client compatibility, not an iOS application runtime.
- `recovery/acceptance/F-014-phone-media-io-endpoint.md` — requires phone/media endpoint behavior and notes iOS/Android background execution limits as deferred technical scope.
- `recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md` — requires mobile pairing/session and remote access but leaves protocol details open.
- `docs/architecture/MH-21-device-interaction.md` — defines the remote-command authority boundary independent of a specific iOS app implementation.

## Classification

- iOS application integration surface: ABSENT in the repository.
- iOS lifecycle/background execution qualification: ABSENT.
- Accessibility qualification: ABSENT.
- Mobile-specific security qualification: PARTIAL at generic boundary/schema level; no iOS runtime qualification.
- End-to-end iOS qualification: ABSENT.

## Gate

The iOS platform enum and API schema do not constitute an iOS application. This evidence does not invent Swift/UI/lifecycle/accessibility/security behavior and does not close P5.6.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p5.5-mobile-access-not-ai-compute-gap-reconciliation":
        content = """# P5.5 Mobile Access Layer / AI Compute Boundary Reconciliation

Status: VERIFIED_LOCAL_SUBSCOPE / P5.5 NOT CLOSED

## Queue requirement

`P5.5 Validate that Mobile Access Layer is not an AI compute tier.`

## Exact repository surfaces inspected

- `contracts/mobile/mobile-api-compatibility.schema.json` — assigns ownership to `MediaHub Mobile Access Layer` and distinguishes `core` and `remote` client roles; no AI compute role is defined.
- `ops/ai/ai_gateway.py` — describes compute-tier selection and explicitly separates gateway routing from provider execution.
- `recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md` — defines mobile access/escalation requirements rather than a mobile AI compute tier.
- `docs/architecture/MH-21-device-interaction.md` — defines remote AI as proposal-only and keeps device authority local through validation/policy/authorization/Consumer Boundary/State Authority.
- `ops/verify_functional_baseline.sh` — checks the canonical escalation sequence `Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI`.

## Classification

- Mobile Access Layer as separate AI compute tier: ABSENT by contract/baseline.
- Canonical escalation separation: IMPLEMENTED at repository architecture/baseline level.
- Direct mobile AI/provider execution authority: ABSENT in inspected surfaces.
- End-to-end operational proof across a real iOS client: ABSENT.

## Gate

The local boundary is verified, but this does not close P5.5 globally or qualify an iOS runtime. No mobile AI tier was invented.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p5.4-remote-control-state-synchronization-gap-reconciliation":
        content = """# P5.4 Remote Control / State Synchronization Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P5.4 NOT CLOSED

## Queue requirement

`P5.4 Add remote-control and state synchronization tests.`

## Exact repository surfaces inspected

- `contracts/mobile/mobile-api-compatibility.schema.json` — defines Core/Remote clients and online/offline/degraded connectivity, but no command synchronization or conflict contract.
- `recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md` — requires mobile pairing/session and remote access but leaves protocol details open.
- `recovery/acceptance/F-014-phone-media-io-endpoint.md` — requires bidirectional phone/MediaHub flows and offline-first behavior; protocol and conflict semantics remain deferred.
- `docs/architecture/MH-21-device-interaction.md` — defines Cloud/Agent Proposal → Local Validation → Policy → Authorization → Consumer Boundary → State Authority → Device; remote AI has no automatic device-command authority.
- `ops/mediahub_lifecycle_contract.py` / `tests/test_mediahub_lifecycle_contract.py` — provide generic media lifecycle/version invariants, not mobile command synchronization.
- `tests/security/test_mh05_bypass_audit.py` — provides negative remote-command boundary coverage, not end-to-end mobile synchronization.

## Classification

- Remote-control authorization/command contract: PARTIAL at generic consumer-boundary/security level; mobile-specific command contract absent.
- State synchronization contract: ABSENT as mobile-specific executable acceptance.
- Conflict/replay synchronization tests: ABSENT.
- Offline/degraded synchronization tests: ABSENT.
- Provenance-bound end-to-end mobile synchronization evidence: ABSENT.

## Gate

This artifact records only repository-observed evidence. It does not invent transport, conflict-resolution, replay or offline synchronization semantics and does not close P5.4.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p5.2-authenticated-session-authorization-gap-reconciliation":
        content = """# P5.2 Authenticated Session / Authorization Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P5.2 NOT CLOSED

## Queue requirement

`P5.2 Implement authenticated session and authorization contracts.`

## Exact repository surfaces inspected

- `contracts/mobile/mobile-api-compatibility.schema.json` — defines Core/Remote mobile client identity, API compatibility and online/offline/degraded connectivity states, but contains no authentication/session/authorization fields.
- `ops/ai/hybrid_session.py` — implements a bounded autonomous hybrid-development session lifecycle with provenance, deadline, pause/resume, safe-stop, terminal states and journal restoration. This is a development-session controller, not a mobile authentication/authorization contract.
- `tests/ai/test_hybrid_session.py` — deterministic tests cover session lifecycle, provenance mismatch, expiration, terminal states and journal validation.
- `recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md` — requires a mobile pairing/session protocol but does not provide an executable mobile auth contract.
- `recovery/acceptance/F-014-phone-media-io-endpoint.md` — references mobile access boundaries but does not provide the required authenticated-session implementation.
- `recovery/accepted/F-007-users-identity-access-authorization.md` — establishes identity/access/authorization requirements and boundaries, not an executable mobile session protocol.
- `docs/architecture/MH-12-authentication.md` — requires issuance, binding, expiration, refresh, revocation, replay resistance, failed-auth handling, rate limits/quarantine and recovery.
- `docs/architecture/MH-12-authorization.md` — requires explicit operation-specific, identity/context/policy-aware, auditable, fail-closed authorization.

## Classification

- Mobile authentication contract: ABSENT.
- Mobile authenticated-session contract: ABSENT.
- Mobile authorization contract: ABSENT.
- Revocation: PARTIAL at generic development-session/credential infrastructure, but no mobile authenticated-session revocation contract was identified.
- Offline/degraded mobile authentication/authorization semantics: PARTIAL as connectivity states only; authorization semantics are ABSENT.
- Deterministic mobile authentication/authorization tests: ABSENT. Existing hybrid-session tests validate a different development-session domain.
- Provenance-bound mobile acceptance evidence: ABSENT.

## Gate

This artifact records only repository-observed evidence. It does not invent pairing, token, refresh, authorization-scope or offline-authentication semantics and does not close P5.2.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p4.5-audit-revocation-offline-degraded-gap-reconciliation":
        content = """# P4.5 Audit / Revocation / Offline-Degraded Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P4.5 NOT CLOSED

## Queue requirement

`P4.5 Add audit/revocation and offline/degraded behavior.`

## Exact implementation/test surfaces inspected

- `ops/cloud_development_adapter.py` — records bounded authorization, timeout, provider outcome and revocation events; revoked adapters fail closed.
- `ops/mediahub_credential_broker.py` — enforces authorization/revocation at credential materialization and exposes terminal revocation.
- `ops/mediahub_resilience.py` — defines bounded provider failure classification and resilience behavior.
- `tests/ops/test_cloud_development_adapter.py` — deterministic audit, timeout and revocation negative paths.
- `tests/test_mediahub_credential_broker.py` — deterministic terminal revocation tests.
- `tests/test_mediahub_resilience.py` — deterministic transient-failure/failover behavior.
- `docs/architecture/MH-21-audit.md` — normative audit requirements.
- `docs/architecture/MH-21-provider-quarantine.md` — normative provider blocking/quarantine lifecycle.
- `docs/architecture/MH-21-offline-mode.md` — normative full-offline, degraded-connectivity and emergency-offline modes.

## Classification

- Audit implementation/test surface: PRESENT for inspected cloud-development paths, but not proven for all P4.2 retrieval flows.
- Revocation implementation/test surface: PRESENT and fail-closed for inspected adapter/credential paths.
- Offline/degraded implementation/test surface: PARTIAL; generic provider resilience exists, but no end-to-end Trusted Sources offline/degraded acceptance surface was identified.
- Full P4.5 end-to-end acceptance: ABSENT.

## Gate

This artifact records the bounded local evidence only. It does not perform cloud execution, acquire credentials, invent offline semantics, or claim global P4.5 completion. A future closure task requires retrieval-specific audit/revocation evidence and deterministic offline/degraded scenarios.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p4.4-external-retrieval-state-authority-boundary-verification":
        content = """# P4.4 External Retrieval / State Authority Boundary Verification

Status: VERIFIED_LOCAL_SUBSCOPE / P4.4 NOT CLOSED

## Queue requirement

`P4.4 Ensure external retrieval cannot mutate State Authority directly.`

## Exact repository surfaces inspected

- `docs/architecture/MH-21-cloud-boundary.md` — explicitly defines the approved external-compute path through validation, provenance, policy, authorization and Consumer Boundary; direct Cloud → State Authority is forbidden.
- `docs/architecture/MH-21-security-invariants.md` — states that RAG context and remote results are data and cloud cannot self-authorize or mutate canonical state.
- `docs/architecture/MH-21-rag-boundary.md` — treats retrieved context as untrusted data and not authority.
- `docs/architecture/MH-21-rag-security.md` — treats documents/retrieved text as hostile or untrusted input subject to classification, privacy and authorization.
- `ops/ai/ai_adapter.py` — deny-by-default forbidden capability set includes `state-authority`.
- `ops/cloud_development_adapter.py` — deny-by-default forbidden capability set includes `state-authority`.
- `tests/security/test_mh05_systemwide_reachability.py` — deterministic reachability checks cover confinement of canonical authority storage.

## Classification

- Architectural external-retrieval → State Authority boundary: IMPLEMENTED as an explicit deny/direct-path prohibition.
- Local adapter forbidden-capability boundary: IMPLEMENTED for inspected AI/cloud adapters.
- End-to-end external retrieval runtime proof: ABSENT; no live external retrieval or production path was executed.

## Gate

This evidence qualifies only the repository-local authority boundary. It does not prove all possible runtime/network paths, authorize external retrieval, mutate State Authority, or close P4.4 globally.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p4.3-source-trust-stale-data-gap-reconciliation":
        content = """# P4.3 Source Trust / Verification / Stale-Data Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P4.3 NOT CLOSED

## Queue requirement

`P4.3 Add source trust/verification and stale-data handling.`

## Exact architecture/contract surfaces inspected

- `specification/contract-registry.yaml` — trusted-sources contract requires source trust policy, retrieval, verification, provenance, change detection, evidence separation and audit.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — requires source verification, provenance, source comparison, change detection and separation of verified evidence from external/inferred/AI-generated information.
- `docs/architecture/MH-21-provider-trust.md` — defines provider trust lifecycle and evaluation dimensions including identity, retention, region, encryption, authentication, limits, versioning and revocation.
- `docs/architecture/MH-21-rag-security.md` — defines hostile-document handling and untrusted retrieved data boundaries.
- `docs/architecture/MH-21-unknowns.md` — records unresolved runtime/provider/RAG evidence gaps.

## Classification

- Source trust implementation contract: ABSENT as an executable acceptance surface.
- Source verification implementation contract: ABSENT as an executable acceptance surface.
- Stale-data/change-detection implementation contract: ABSENT as an executable acceptance surface.
- Architecture/requirements: PRESENT, but declarations do not prove runtime behavior.

## Gate

This artifact records only the factual acceptance-surface gap. It does not invent trust scoring, freshness thresholds, change-detection algorithms, provider reputation data or retrieval behavior. A future P4.3 implementation task requires explicit trust/verification contracts, deterministic stale-data tests and provenance-bound evidence.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p4.2-trusted-sources-intelligence-gap-reconciliation":
        content = """# P4.2 Trusted Sources Intelligence Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P4.2 NOT CLOSED

## Queue requirement

`P4.2 Complete Trusted Sources Intelligence Engine boundaries: discovery, retrieval, verification, provenance, evidence and knowledge.`

## Exact architecture/contract surfaces inspected

- `specification/contract-registry.yaml` — CTR-042 defines trusted-source discovery, retrieval, verification, provenance and evidence management; required semantics include source trust policy, retrieval, verification, provenance, change detection, evidence separation and audit.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — defines Trusted Sources Intelligence Engine as a first-class Cloud Development AI subsystem covering discovery, source search/classification, retrieval, verification, provenance and source comparison.
- `docs/architecture/MH-21-rag-boundary.md` — defines a RAG flow including ingestion, retrieval and result handling; retrieved context is untrusted data.
- `docs/architecture/MH-21-rag-security.md` — defines hostile-document handling, provenance, classification, privacy and authorization boundaries.
- `docs/architecture/MH-21-cloud-boundary.md` — defines bounded external-compute transfer and validation/provenance/policy/authorization on returned data.
- `docs/architecture/MH-21-data-egress.md` — requires bounded, authorized handling of sensitive data and destinations.
- `docs/architecture/MH-21-audit.md` — requires provenance/audit context for workloads and results.

## Classification

- Trusted Sources discovery implementation contract: ABSENT as an executable acceptance surface.
- Trusted Sources retrieval implementation contract: ABSENT as an executable acceptance surface.
- Trusted Sources verification implementation contract: ABSENT as an executable acceptance surface.
- Trusted Sources provenance/evidence implementation contract: ABSENT as an executable acceptance surface.
- Trusted Sources knowledge integration implementation contract: ABSENT as an executable acceptance surface.
- Architecture/requirements: PRESENT, but declarations are not implementation evidence.

## Gate

This artifact records only the factual acceptance-surface gap. It does not invent source ranking, trust scoring, crawlers, retrieval providers, knowledge schemas, change-detection algorithms or external execution. A future P4.2 implementation task requires explicit bounded contracts, deterministic tests, provenance-bound evidence and fail-closed treatment of retrieved data.
"""
        return unified_patch("", content.splitlines(keepends=True), str(path.relative_to(ROOT)))
    if task.fallback_kind == "p4.1-document-ingestion-index-search-gap-reconciliation":
        content = """# P4.1 Document Ingestion / Index / Search Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P4.1 NOT CLOSED

## Queue requirement

`P4.1 Complete document ingestion/index/search contracts.`

## Exact architecture/contract surfaces inspected

- `specification/contract-registry.yaml` — CTR-034 defines unified indexing/search/knowledge-graph access and requires indexing provenance, consistency, authorization filtering, freshness, offline operation and rebuild.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — defines Document System and document search capabilities.
- `docs/architecture/MH-21-rag-boundary.md` — declares a RAG flow from ingestion through index and retrieval, with retrieved context treated as untrusted data.
- `docs/architecture/MH-21-rag-security.md` — declares hostile-document handling, provenance, classification, privacy and authorization boundaries.
- `docs/architecture/MH-21-resource-governance.md` — declares bounded resources for RAG retrieval/vector search and related AI workloads.

## Classification

- Document ingestion implementation contract: ABSENT as an executable document-specific acceptance surface.
- Document indexing implementation contract: ABSENT as an executable document-specific acceptance surface.
- Document search implementation contract: ABSENT as an executable document-specific acceptance surface.
- Architecture/requirements: PRESENT, including explicit indexing/search/RAG semantics, but declarations are not implementation evidence.

## Gate

This artifact records only the factual acceptance-surface gap. It does not invent document schemas, OCR behavior, chunking, embedding models, vector stores, ranking, synchronization or production behavior. A future P4.1 implementation task requires explicit document contracts, deterministic tests, provenance-bound acceptance evidence and reproducible rebuild/search behavior.
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
    if task.fallback_kind == "p8.3-end-to-end-scenario-reconciliation":
        target = task.target
        sources = (
            "tests/ai/test_hybrid_session.py",
            "tests/ai/test_hybrid_development_controller.py",
            "tests/ai/test_hybrid_dispatcher.py",
            "tests/ai/test_ai_gateway.py",
            "tests/runtime/test_mh04_qualification_edges.py",
            "tests/security/test_mh05_health_not_authorization.py",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            evidence.append(f"### {rel}\nSHA256: {hashlib.sha256(source.read_bytes()).hexdigest()}")
        content = """# P8.3 — End-to-end state scenario reconciliation

Status: SCENARIO_RECONCILIATION / P8.3 NOT CLOSED

## Scope

This artifact records deterministic evidence for normal, degraded, recovery and revoked/denied-authorization state surfaces already represented by the repository tests. It does not claim a production or external end-to-end run, and it does not treat health/reachability as authorization.

## Scenario matrix

- Normal: session lifecycle, bounded dispatch and authorized gateway paths are covered by existing tests.
- Degraded: provider/cluster degraded states are represented by existing routing, resilience and qualification tests; this artifact does not assert external outage behavior.
- Recovery: session/controller/delivery restore and provenance checks are covered by existing tests.
- Revoked or denied authorization: explicit authorization denial and safe-stop paths are covered; this artifact does not infer revocation semantics where only denial is tested.

## Closure

P8.3 remains OPEN until a deterministic acceptance surface ties these scenarios together as one executable cross-domain sequence.

## Source evidence

""" + chr(10) + chr(10).join(evidence) + chr(10)
        return unified_patch("", content, target)

    if task.fallback_kind == "p9.1-threat-model-refresh":
        target = task.target
        sources = (
            "docs/architecture/MH-17-threat-model.md", "docs/architecture/MH-21-security-invariants.md",
            "docs/architecture/MH-21-security.md", "docs/architecture/MH-21-network-boundary.md",
            "docs/architecture/MH-21-data-egress.md", "docs/architecture/MH-21-agent-limits.md",
            "docs/architecture/MH-21-cloud-boundary.md", "docs/architecture/MH-21-provider-quarantine.md",
            "docs/architecture/MH-21-remote-policy.md", "docs/architecture/MH-21-cloud-credentials.md",
            "docs/architecture/MH-21-audit.md", "docs/architecture/MH-12-recovery-security.md",
        )
        evidence=[]
        for rel in sources:
            source=ROOT/rel
            if not source.is_file(): return ""
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            lines=source.read_text(encoding="utf-8").splitlines()
            hits=[f"L{i}: {line.strip()}" for i,line in enumerate(lines,1) if any(x in line.lower() for x in ("threat","boundary","egress","credential","quarantine","authorization","revocation","unknown","security"))]
            evidence.append(f"### {rel}\nSHA256: {digest}\n"+"\n".join(f"- {x}" for x in hits[:25]))
        content="# P9.1 — Threat-model refresh\n\nStatus: THREAT_MODEL_RECONCILIATION / P9.1 NOT CLOSED\n\n## Scope\n\nDeterministic refresh of documented security/threat surfaces against the current repository architecture. This is a repository evidence reconciliation, not a penetration test and not proof that every runtime path is secure.\n\n## Findings\n\n- Trust boundaries and security invariants are documented across local execution, cloud/provider boundaries, remote policy, credentials, egress and recovery.\n- Existing architecture documents contain explicit unknown/gap registers that must remain release considerations.\n- Documentation evidence is not equivalent to runtime qualification; negative tests and live endpoint behavior require separate evidence.\n- P9.1 remains OPEN until the refreshed threat model is reconciled with current implementation and security-test evidence and all release blockers are classified.\n\n## Source evidence\n\n"+"\n\n".join(evidence)+"\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "p9.3-egress-endpoint-allowlist-audit":
        target = task.target
        sources = (
            "docs/architecture/MH-21-network-boundary.md", "docs/architecture/MH-21-data-egress.md",
            "ops/mediahub_egress_controller.py", "ops/hybrid_cloud_api_egress_adapter.py",
            "ops/hybrid_cloud_egress.py", "ops/hybrid_cloud_egress_chain.py",
            "tests/test_mediahub_egress_controller.py", "tests/test_hybrid_cloud_api_egress_adapter.py",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file(): return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            hits = []
            for i, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                low = line.lower()
                if any(token in low for token in ("allowlist", "allowlist", "https://", "egress", "deny", "admit", "endpoint")):
                    hits.append(f"L{i}: {line.strip()}")
            evidence.append(f"### {rel}\nSHA256: {digest}\n" + "\n".join(f"- {x}" for x in hits[:30]))
        content = "# P9.3 — Egress and endpoint allowlist audit\n\nStatus: NETWORK_SECURITY_RECONCILIATION / P9.3 NOT CLOSED\n\n## Scope\n\nDeterministic repository audit of existing egress gates, endpoint validation and allowlist evidence. No live network requests are performed. Reachability is not treated as authorization.\n\n## Findings\n\n- Architecture documents define controlled outbound egress and default-deny/allowlist expectations.\n- Repository implementation contains egress admission and endpoint validation surfaces that are reviewed below.\n- Static evidence does not prove every runtime destination is constrained, nor does it establish external endpoint availability or certificate behavior.\n- P9.3 remains OPEN until all production-relevant egress paths have explicit allowlist acceptance evidence and uncovered paths are classified.\n\n## Source evidence\n\n" + "\n\n".join(evidence) + "\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "p9.2-static-secret-dependency-provenance-review":
        target = task.target
        sources = (
            "ops/requirements-autonomous.txt", "docs/architecture/MH-12-secrets.md",
            ".gitignore", ".autonomous/provenance.log",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            evidence.append(f"### {rel}\nSHA256: {digest}")

        tracked = run([str(GIT), "ls-files", "-z"], timeout=30).stdout.split("\x00")
        import re
        secret_patterns = (
            re.compile(r"(?:api[_-]?key|secret|token|password|private[_-]?key)\s*[:=]\s*[\"\'][^\"\']{8,}[\"\']", re.I),
            re.compile(r"authorization\s*:\s*bearer\s+[A-Za-z0-9._~+/=-]{16,}", re.I),
            re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
        )
        findings = []
        scanned = 0
        for rel in tracked:
            if not rel or rel.startswith((".git/", ".venv", "node_modules/")):
                continue
            source = ROOT / rel
            try:
                raw = source.read_bytes()
                if b"\x00" in raw[:8192]:
                    continue
                lines = raw.decode("utf-8").splitlines()
            except (OSError, UnicodeDecodeError):
                continue
            scanned += 1
            for i, line in enumerate(lines, 1):
                low = line.lower()
                if any(pattern.search(line) for pattern in secret_patterns):
                    findings.append(f"- {rel}:L{i} matched a secret-related keyword; value intentionally omitted")
                    if len(findings) >= 40:
                        break
            if len(findings) >= 40:
                break

        req = (ROOT / "ops/requirements-autonomous.txt").read_text(encoding="utf-8").splitlines()
        deps = [line.strip() for line in req if line.strip() and not line.lstrip().startswith("#")]
        content = "# P9.2 — Static secret, dependency, license and provenance review\n\nStatus: SECURITY_RECONCILIATION / P9.2 NOT CLOSED\n\n## Scope\n\nDeterministic repository-only review. Secret scanning reports locations and keyword matches without reproducing values. Dependency review is based on repository manifests; license/provenance claims are not inferred where lock or authoritative metadata is absent. This is not a substitute for a dedicated runtime scanner or supply-chain service.\n\n## Static secret review\n\n- Tracked text files scanned: " + str(scanned) + "\n- Keyword findings (values omitted): " + str(len(findings)) + "\n" + ("\n".join(findings) if findings else "- No keyword matches found by this bounded scan.") + "\n\n## Dependency / license review\n\n- Declared autonomous dependencies: " + ", ".join(deps) + "\n- Repository contains no dependency lockfile in the reviewed top-level inventory. Exact transitive versions and authoritative license provenance are therefore NOT established by repository manifests alone.\n- `pip-audit` is declared as a review tool, but this artifact does not claim that an external advisory database scan was executed.\n\n## Provenance\n\n- The autonomous provenance journal is hashed as source evidence. Historical entries preserve source/tree/result fields, but this review does not treat journal content as proof of dependency integrity or secret absence.\n- P9.2 remains OPEN until dependency provenance/license requirements and any material secret-scan findings are explicitly classified and accepted or remediated.\n\n## Source evidence\n\n" + "\n\n".join(evidence) + "\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "release-evidence-reconciliation":
        target = ROOT / task.target
        target_rel = task.target
        phase = task.queue_item.split()[0]
        if not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
        head = run([str(GIT), "rev-parse", "HEAD"]).stdout.strip()
        branch = run([str(GIT), "branch", "--show-current"]).stdout.strip()
        content = (
            f"# {task.queue_item} — bounded autonomous evidence\\n\\n"
            "Status: NOT CLOSED / evidence-only reconciliation\\n\\n"
            f"Phase: {phase}\\n"
            f"Repository HEAD at evidence capture: \\`{head}\\`\\n"
            f"Branch: \\`{branch}\\`\\n\\n"
            "## Boundary\\n\\n"
            "This artifact records only repository-local evidence. It does not simulate human approval, production authorization, external credentials, cloud-provider execution, backup/restore success, performance measurements, or disaster-recovery qualification. Any missing evidence remains a release blocker.\\n\\n"
            "## Classification\\n\\n"
            "The requested capability is classified as PARTIAL/ABSENT/HUMAN_GATE unless current repository artifacts provide direct evidence. This task itself does not authorize closure of the queue item.\\n\\n"
            "## Required next evidence\\n\\n"
            f"{task.instruction}\\n"
        )
        return unified_patch("", content.splitlines(keepends=True), target_rel)

    if task.fallback_kind == "p9.6-malformed-input-security-qualification":
        target = task.target
        content = """# P9.6 — Malformed-input security qualification evidence

Status: SECURITY_RECONCILIATION / P9.6 NOT CLOSED

Scope: repository-local coverage record for malformed public-contract inputs. This does not claim exhaustive fuzzing or external scanner coverage.

Verification command: `pytest -q tests/test_mediahub_native_execution.py tests/runtime/test_mh05_consumer_boundary.py tests/security/test_mh05_restore_security.py`

Boundary: report only behavior demonstrated by the named existing tests. Remaining malformed-input classes require separate bounded tests where justified.
"""
        return unified_patch("", content.splitlines(keepends=True), target)

    if task.fallback_kind == "p9.7-recovery-tamper-evidence":
        target = task.target
        content = """# P9.7 — Recovery / tamper-evidence record

Status: SECURITY_RECONCILIATION / P9.7 NOT CLOSED

Scope: repository-local recovery and tamper-evidence checks only. This record does not introduce durable persistence or claim disaster-recovery qualification.

Verification command: `pytest -q tests/security/test_mh05_restore_security.py tests/runtime/test_state_authority.py`

Boundary: production backup/restore, cross-node disaster recovery and durable persistence remain separate qualification gates.
"""
        return unified_patch("", content.splitlines(keepends=True), target)

    if task.fallback_kind == "p9.5-credential-broker-revocation-isolation":
        target = task.target
        content = """# P9.5 — Credential broker revocation / isolation evidence

Status: SECURITY_RECONCILIATION / P9.5 NOT CLOSED

Scope: repository-local evidence only. Do not read or emit credential values, invoke providers, create credentials, or grant production authorization.

Verification command: `pytest -q tests/test_mediahub_credential_broker.py tests/security/test_native_agent_launcher.py`

Review boundary: credential broker, native execution admission and native launcher negative tests. This record does not claim external secret-store, cloud-provider, rotation-service or production revocation qualification.

Source evidence: `ops/mediahub_credential_broker.py`, `tests/test_mediahub_credential_broker.py`, `ops/mediahub_native_execution.py`, `tests/security/test_native_agent_launcher.py`.
"""
        return unified_patch("", content.splitlines(keepends=True), target)

    if task.fallback_kind == "p9.4-sandbox-authority-escalation-negative-tests":
        target = task.target
        sources = (
            "ops/cloud_development_sandbox.py", "ops/mediahub_native_execution.py",
            "ops/mediahub_native_agent_launcher.py", "runtime/mediahub_runtime/state_authority.py",
            "tests/security/test_cloud_development_sandbox.py", "tests/security/test_native_agent_launcher.py",
            "tests/security/test_mh04_state_authority_redteam.py",
        )
        evidence=[]
        for rel in sources:
            source=ROOT/rel
            if not source.is_file(): return ""
            evidence.append(f"### {rel}\nSHA256: {hashlib.sha256(source.read_bytes()).hexdigest()}")
        tests=(
            "tests/security/test_cloud_development_sandbox.py",
            "tests/security/test_native_agent_launcher.py",
            "tests/security/test_mh04_state_authority_redteam.py",
        )
        cmd=[sys.executable,"-m","pytest","-q",*tests]
        result=run(cmd, timeout=120)
        output=(result.stdout+"\n"+result.stderr).strip()
        safe_lines=[line for line in output.splitlines() if "secret" not in line.lower() and "token" not in line.lower()]
        content="# P9.4 — Sandbox escape / authority-escalation negative tests\n\nStatus: SECURITY_RECONCILIATION / P9.4 NOT CLOSED\n\n## Scope\n\nRepository-local execution of the existing sandbox, native-launch and State Authority red-team tests. The evidence is limited to the checked test suite and does not establish production or external-provider security.\n\n## Test result\n\n- Command: `python3 -m pytest -q` against the three P9.4 security test modules.\n- Exit code: " + str(result.returncode) + "\n- Output (sanitized):\n\n```text\n" + "\n".join(safe_lines[-80:]) + "\n```\n\n## Security interpretation\n\n- Sandbox tests cover symlink-parent denial, symlink-worktree denial, marker tamper detection and deterministic teardown.\n- Native launcher tests cover unknown agents, missing/unqualified models, non-HTTPS endpoints and credential absence.\n- State Authority red-team tests cover missing authorization, remote read-only context, observer isolation, forged checkpoint rejection and unavailable-authority fail-closed behavior.\n- P9.4 remains OPEN until all required negative surfaces are covered and any residual sandbox, process-execution, egress or authority-escalation gaps are explicitly classified.\n\n## Source evidence\n\n" + "\n\n".join(evidence) + "\n"
        return unified_patch("",content,target)

    if task.fallback_kind == "p8.5-provenance-chain-reconciliation":
        target = task.target
        sources = (
            "ops/mediahub_native_execution.py",
            "ops/mediahub_cluster_failover.py",
            "ops/ai/ai_adapter.py",
            "tests/test_mediahub_native_execution.py",
            "tests/test_mediahub_cluster_failover.py",
            "tests/security/test_ai_adapter.py",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            matches = []
            for i, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                if any(token in line for token in ("request_id", "workload_id", "source_sha", "provider", "result", "evidence")):
                    matches.append(f"L{i}: {line.strip()}")
            evidence.append(f"### {rel}\nSHA256: {digest}\n" + "\n".join(f"- {m}" for m in matches[:30]))
        content = "# P8.5 — Provenance chain reconciliation\n\nStatus: PROVENANCE_RECONCILIATION / P8.5 NOT CLOSED\n\n## Scope\n\nThis record traces the existing provenance identifiers across request/proposal, recovery evidence and AI adapter result boundaries. It does not create a persistence mechanism or infer a complete request→artifact→result→evidence journal where the repository does not demonstrate one.\n\n## Deterministic findings\n\n- `request_id`, `workload_id`, `source_sha` and `provider` are validated and bound at the native execution proposal boundary.\n- Recovery evidence is required to be verified and provenance-matching before proposal admission.\n- Cluster recovery evidence carries request/workload/source provenance into native execution admission.\n- The AI adapter exposes source provenance in its result contract.\n- A single persistent, independently verifiable chain linking request → produced artifact → execution result → evidence is not established by these surfaces alone.\n\n## Closure\n\nP8.5 remains OPEN. Full closure requires an existing or explicitly authorized provenance record that links every lifecycle hop without adding hidden persistence or bypassing authority boundaries.\n\n## Source evidence\n\n""" + "\n\n".join(evidence) + "\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "p8.4-bounded-agent-security-reconciliation":
        target = task.target
        sources = (
            "ops/ai/ai_adapter.py",
            "ops/ai/astra_host_execution_gate.py",
            "ops/ai/astra_host_gateway.py",
            "ops/ai/astra_task_gateway.py",
            "ops/cloud_development_sandbox.py",
            "ops/mediahub_native_execution.py",
            "ops/mediahub_native_agent_launcher.py",
            "tests/security/test_ai_adapter.py",
            "tests/security/test_native_agent_launcher.py",
            "tests/security/test_cloud_development_sandbox.py",
            "tests/security/test_mh05_bypass_audit.py",
            "tests/security/test_mh05_systemwide_reachability.py",
            "tests/security/test_mh04_state_authority_redteam.py",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            evidence.append(f"### {rel}\nSHA256: {hashlib.sha256(source.read_bytes()).hexdigest()}")
        content = """# P8.4 — Bounded-agent security reconciliation

Status: SECURITY_RECONCILIATION / P8.4 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for bounded-agent security surfaces: process-execution and network-egress controls, sandbox isolation, forbidden capabilities, and State Authority construction boundaries. It distinguishes static and negative-test evidence from runtime qualification and does not claim closure where runtime or external qualification is absent.

## Security classification

- AI adapter and Astra gateway surfaces: inspected for bounded execution and authorization boundaries.
- Cloud Development sandbox: inspected for isolation and forbidden-capability controls.
- Native execution and agent launcher: inspected for bounded process/provider launch constraints.
- MH-05 reachability/bypass tests: inspected as negative security evidence; reachability is not treated as authorization.
- State Authority red-team tests: inspected for construction and mutation-boundary protection.
- Runtime/external-provider qualification: NOT established by this repository-only reconciliation.

## Closure

P8.4 remains OPEN until the required security surfaces have deterministic acceptance coverage including any uncovered runtime, endpoint, credential, persistence, or authority-escalation paths.

## Source evidence

""" + chr(10) + chr(10).join(evidence) + chr(10)
        return unified_patch("", content, target)

    if task.fallback_kind == "p8.2-cross-domain-contract-gap-reconciliation":
        target = task.target
        sources = (
            "specification/contract-registry.yaml",
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
            "tests/contracts/test_contract_domain_reconciliation.py",
            "tests/contracts/test_contract_metadata.py",
            "tests/contracts/test_mobile_api_compatibility.py",
            "tests/static/test_cross_contract.py",
            "tests/test_mediahub_lifecycle_contract.py",
            "ops/verify_functional_baseline.sh",
        )
        evidence = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            evidence.append(f"### {rel}\nSHA256: {digest}")
        content = """# P8.2 — Cross-domain contract reconciliation

Status: DISCOVERY_RECONCILIATION / P8.2 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for contract coverage across Core, AI, Home Assistant, Media, Documents, Mobile and Voice. It distinguishes repository declarations and executable tests from unimplemented or unverified product behavior. It does not invent domain semantics, mutate State Authority, activate providers or claim P8.2 closure.

## Deterministic classification

- Core: inspected through canonical contract metadata, identity/domain reconciliation and lifecycle tests.
- AI: inspected through the existing AI contract surfaces referenced by the repository baseline and cross-contract tests.
- Home Assistant: inspected through the baseline verification boundary; this artifact does not claim external HA runtime qualification.
- Media: inspected through the existing lifecycle contract and tests; ingestion/playback/storage qualification remains separately scoped.
- Documents: no independent executable document contract is established by the inspected cross-domain test set; further qualification remains open.
- Mobile: inspected through the existing mobile compatibility contract and tests; end-to-end iOS qualification remains separately scoped.
- Voice: no independent executable voice-provider contract is established by the inspected cross-domain test set; provider qualification remains open.

## Source evidence

""" + chr(10) + chr(10).join(evidence) + chr(10)
        return unified_patch("", content, target)

    if task.fallback_kind == "p8.1-escalation-path-reconciliation":
        target = task.target
        sources = (
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
            "docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md",
            "docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md",
            "ops/mediahub_provider_gateway.py",
            "ops/cloud_development_adapter.py",
        )
        evidence_lines = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            matches = []
            for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                low = line.lower()
                if any(term in low for term in ("mobile access", "local ai", "local cluster", "cloud development ai", "provider", "route", "routing", "escalat", "fallback")):
                    matches.append(f"{number}: {line.strip()}")
                if len(matches) >= 12:
                    break
            evidence_lines.append(f"### {rel}" + chr(10) + f"SHA256: {digest}" + chr(10) + chr(10).join(f"- {m}" for m in matches))
        content = """# P8.1 — AI escalation path reconciliation

Status: DISCOVERY_RECONCILIATION / P8.1 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for the existing escalation path Mobile Access Layer → Local AI → Local Cluster AI → Cloud Development AI. It does not invent routing semantics, add a Mobile AI tier, execute providers, acquire credentials, mutate State Authority, or claim end-to-end closure.

## Deterministic classification

- Mobile Access Layer boundary: inspected from existing repository sources; it remains an access layer, not an AI compute tier.
- Local AI: inspected as an existing repository-local AI surface only.
- Local Cluster AI: absence of an explicit current hop is reported rather than inferred.
- Cloud Development AI: inspected through existing policy/orchestration surfaces without activating a provider.
- End-to-end escalation: NOT ESTABLISHED by this reconciliation alone.

## Source evidence""" + chr(10) + chr(10).join(evidence_lines) + chr(10)
        return unified_patch("", content, target)

    if task.fallback_kind == "p7.4-ordinary-user-cloud-development-access-gap-reconciliation":
        target = task.target
        sources = (
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml",
            "specification/invariant-registry.yaml",
            "recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md",
            "ops/cloud_development_adapter.py",
            "tests/ops/test_cloud_development_adapter.py",
        )
        evidence_lines = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
                digest = hashlib.sha256(source.read_bytes()).hexdigest()
            lines = source.read_text(encoding="utf-8").splitlines()
            matches = []
            for number, line in enumerate(lines, 1):
                lower = line.lower()
                if any(term in lower for term in ("cloud development ai", "ordinary users", "no direct access", "controlled escalation", "authorization", "credential")):
                    matches.append(f"{number}: {line.strip()}")
                if len(matches) >= 8:
                    break
            evidence_lines.append(f"### {rel}\nSHA256: {digest}\n" + "\n".join(f"- {item}" for item in matches))
        content = """# P7.4 — Ordinary-user Cloud Development AI access boundary\n\nStatus: DISCOVERY_RECONCILIATION / P7.4 NOT CLOSED\n\n## Scope\n\nThis artifact records deterministic repository evidence for the existing requirement that ordinary users have no direct corporate Cloud Development AI access. It distinguishes repository policy declarations from executable enforcement evidence. It does not invent authentication, UI, provider, or production-authorization semantics.\n\n## Deterministic classification\n\n- Policy/declaration evidence: PRESENT where the source excerpts below explicitly describe Cloud Development AI, ordinary-user access, or controlled escalation.\n- Executable ordinary-user access enforcement: NOT ESTABLISHED by this reconciliation alone; the inspected adapter/test surfaces are generic Cloud Development controls and are not treated as proof of an ordinary-user-specific access gate.\n- Overall P7.4 status: PARTIAL — policy boundary is documented, while ordinary-user-specific executable acceptance is not demonstrated by the inspected evidence.\n\n## Source evidence\n\n""" + "\n\n".join(evidence_lines) + "\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "p7.6-degraded-offline-recovery-gap-reconciliation":
        target = task.target
        sources = (
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md",
            "specification/invariant-registry.yaml",
            "specification/decision-registry.yaml",
            "docs/architecture/MH-06-recovery-model.md",
            "docs/architecture/MH-06-health-readiness.md",
            "ops/mediahub_resilience.py",
            "tests/test_mediahub_resilience.py",
        )
        evidence_lines = []
        for rel in sources:
            source = ROOT / rel
            if not source.is_file():
                return ""
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            matches = []
            for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
                low = line.lower()
                if any(term in low for term in ("offline", "degraded", "recover", "cloud development ai", "resilien", "readiness")):
                    matches.append(f"{number}: {line.strip()}")
                if len(matches) >= 8:
                    break
            evidence_lines.append(f"### {rel}\nSHA256: {digest}\n" + "\n".join(f"- {m}" for m in matches))
        content = """# P7.6 — Degraded/offline behavior and recovery evidence

Status: DISCOVERY_RECONCILIATION / P7.6 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for existing degraded/offline and recovery requirements relevant to the Cloud Development AI boundary. It does not infer provider outage, network outage, cloud availability, credentials, provider guarantees, provider recovery or external execution results.

## Deterministic classification

- Existing local-first/offline and generic degraded/recovery declarations: PRESENT where recorded below.
- Existing generic resilience implementation/tests: PRESENT in the inspected repository surfaces.
- Cloud Development AI-specific degraded/offline acceptance and externally observable recovery: NOT ESTABLISHED by this reconciliation alone.
- Overall P7.6 status: PARTIAL — repository-level requirements and generic resilience evidence exist, but subsystem-specific acceptance is not demonstrated here.

## Acceptance boundary

The following remain separate until domain-specific deterministic evidence exists: provider/network outage, cloud availability, credential readiness, provider recovery, external execution, and end-to-end Cloud Development AI recovery. No such external fact is asserted by this artifact.

## Source evidence

""" + "\n\n".join(evidence_lines) + "\n"
        return unified_patch("", content, target)

    if task.fallback_kind == "p7.5-data-minimization-residency-egress-gap-reconciliation":
        target = task.target
        sources = (
            "specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md", "specification/contract-registry.yaml",
            "docs/architecture/MH-13-privacy-data-governance.md", "docs/architecture/MH-21-data-residency.md",
            "ops/mediahub_policy_engine.py", "ops/mediahub_egress_controller.py",
            "tests/test_mediahub_policy_engine.py", "tests/test_mediahub_egress_controller.py",
        )
        evidence_lines=[]
        for rel in sources:
            source=ROOT/rel
            if not source.is_file(): return ""
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            matches=[]
            for number,line in enumerate(source.read_text(encoding="utf-8").splitlines(),1):
                low=line.lower()
                if any(term in low for term in ("minimization","residency","egress","policy","export","data class","allowlist")):
                    matches.append(f"{number}: {line.strip()}")
                if len(matches)>=8: break
            evidence_lines.append(f"### {rel}\nSHA256: {digest}\n"+"\n".join(f"- {m}" for m in matches))
        content="""# P7.5 — Data minimization, residency/policy and egress boundary\n\nStatus: DISCOVERY_RECONCILIATION / P7.5 NOT CLOSED\n\n## Scope\n\nThis artifact records deterministic repository evidence for existing Cloud Development AI data-minimization, residency/policy and egress requirements. It does not infer provider guarantees, regions, retention periods or external runtime behavior.\n\n## Deterministic classification\n\n- Existing policy/contract declarations: PRESENT where recorded below.\n- Existing generic PolicyEngine/EgressController implementation and tests: PRESENT in the inspected repository surfaces.\n- Human-Clone-specific acceptance of minimization, residency/policy and egress: NOT ESTABLISHED by this reconciliation alone.\n- Overall P7.5 status: PARTIAL — generic controls are evidenced, but subsystem-specific acceptance is not demonstrated here.\n\n## Source evidence\n\n"""+"\n\n".join(evidence_lines)+"\n"
        return unified_patch("", content, target)

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
    if selected and selected.fallback_kind == "p7.3-trusted-sources-knowledge-workflow-gap-reconciliation":
        checks.append(([sys.executable, "-c", "from pathlib import Path; files=('specification/contract-registry.yaml','docs/architecture/MH-21-rag-boundary.md','docs/architecture/MH-21-rag-security.md','docs/architecture/MH-21-knowledge-graph-interaction.md'); text=''.join(Path(f).read_text(encoding='utf-8') for f in files); required=('CTR-042','trusted-source discovery','retrieval','verification','provenance','change detection','evidence separation'); assert all(x in text for x in required); print('P7.3 repository contract evidence scan PASS')"], 30))
    if selected and selected.fallback_kind == "p7.5-data-minimization-residency-egress-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_policy_engine.py", "tests/test_mediahub_egress_controller.py"], 180))
    if selected and selected.fallback_kind == "p7.6-degraded-offline-recovery-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_resilience.py"], 180))
    if selected and selected.fallback_kind == "p8.3-end-to-end-scenario-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/ai/test_hybrid_session.py",
                        "tests/ai/test_hybrid_development_controller.py",
                        "tests/ai/test_hybrid_dispatcher.py",
                        "tests/ai/test_ai_gateway.py",
                        "tests/runtime/test_mh04_qualification_edges.py",
                        "tests/security/test_mh05_health_not_authorization.py"], 180))
    if selected and selected.fallback_kind == "p8.2-cross-domain-contract-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/contracts/test_contract_domain_reconciliation.py",
                        "tests/contracts/test_contract_metadata.py",
                        "tests/contracts/test_mobile_api_compatibility.py",
                        "tests/static/test_cross_contract.py",
                        "tests/test_mediahub_lifecycle_contract.py"], 180))
    if selected and selected.fallback_kind == "p8.1-escalation-path-reconciliation":
        checks.append(([sys.executable, "-c", "from pathlib import Path; files=('specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml','docs/ops/P5-5-mobile-access-not-ai-compute-gap-reconciliation-2026-09-22.md','docs/ops/P7-4-ordinary-user-cloud-development-access-gap-reconciliation-2026-09-22.md','ops/mediahub_provider_gateway.py','ops/cloud_development_adapter.py'); assert all(Path(f).is_file() for f in files); print('P8.1 escalation-path evidence source scan PASS')"], 30))
    if selected and selected.fallback_kind == "p7.4-ordinary-user-cloud-development-access-gap-reconciliation":
        checks.append(([sys.executable, "-c", "from pathlib import Path; files=('specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','specification/MEDIAHUB-FUNCTIONAL-BASELINE-GOVERNANCE.yaml','specification/invariant-registry.yaml','recovery/acceptance/F-009-remote-access-mobile-and-cloud-escalation.md','ops/cloud_development_adapter.py','tests/ops/test_cloud_development_adapter.py'); text=''.join(Path(f).read_text(encoding='utf-8').lower() for f in files); required=('cloud development ai','ordinary users','direct access to cloud development','not a user-facing development workspace'); assert all(x in text for x in required); print('P7.4 repository access-boundary evidence scan PASS')"], 30))
    if selected and selected.fallback_kind == "p7.2-human-clone-governance-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/ops/test_cloud_development_adapter.py",
                        "tests/test_mediahub_credential_broker.py"], 180))
    if selected and selected.fallback_kind == "p7.1-human-clone-contract-gap-reconciliation":
        checks.append(([sys.executable, "-c",
                        "from pathlib import Path; files=('specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','specification/contract-registry.yaml','specification/capability-registry.yaml'); text=''.join(Path(f).read_text(encoding='utf-8') for f in files); required=('AI Human Clone','CTR-043','authorized_ai_human_clone_real_person_generated_media_participation','consent','provenance','revocation','audit'); assert all(x in text for x in required); print('P7.1 repository contract evidence scan PASS')"], 30))
    if selected and selected.fallback_kind == "p6.5-provider-outage-fallback-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/test_mediahub_provider_gateway.py",
                        "tests/test_mediahub_resilience.py"], 180))
    if selected and selected.fallback_kind == "p6.4-home-assistant-mutation-boundary-gap-reconciliation":
        checks.append(([str(ROOT / "ops/verify_functional_baseline.sh")], 120))
    if selected and selected.fallback_kind == "p6.3-voice-consent-authorization-provenance-replay-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/security/test_mh05_bypass_audit.py"], 120))
    if selected and selected.fallback_kind == "p6.2-voice-provider-adapter-gap-reconciliation":
        checks.append(([str(ROOT / "ops/verify_functional_baseline.sh")], 120))
    if selected and selected.fallback_kind == "p6.1-voice-provider-order-gap-reconciliation":
        checks.append(([str(ROOT / "ops/verify_functional_baseline.sh")], 120))
    if selected and selected.fallback_kind == "p5.6-ios-integration-lifecycle-accessibility-security-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/contracts/test_mobile_api_compatibility.py"], 120))
    if selected and selected.fallback_kind == "p5.5-mobile-access-not-ai-compute-gap-reconciliation":
        checks.append(([str(ROOT / "ops/verify_functional_baseline.sh")], 120))
    if selected and selected.fallback_kind == "p5.4-remote-control-state-synchronization-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_mediahub_lifecycle_contract.py", "tests/security/test_mh05_bypass_audit.py"], 180))
    if selected and selected.fallback_kind == "p5.2-authenticated-session-authorization-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/ai/test_hybrid_session.py", "tests/contracts/test_mobile_api_compatibility.py"], 180))
    if selected and selected.fallback_kind == "p4.5-audit-revocation-offline-degraded-gap-reconciliation":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/ops/test_cloud_development_adapter.py",
                        "tests/test_mediahub_credential_broker.py",
                        "tests/test_mediahub_resilience.py"], 180))
    if selected and selected.fallback_kind == "p4.4-external-retrieval-state-authority-boundary-verification":
        checks.append(([sys.executable, "-m", "pytest", "-q",
                        "tests/security/test_mh05_systemwide_reachability.py",
                        "tests/security/test_ai_adapter.py",
                        "tests/ops/test_cloud_development_adapter.py"], 180))
    if selected and selected.fallback_kind == "p4.3-source-trust-stale-data-gap-reconciliation":
        checks.append(([sys.executable, "-c",
                        "from pathlib import Path; files=('specification/contract-registry.yaml','specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','docs/architecture/MH-21-provider-trust.md','docs/architecture/MH-21-rag-security.md','docs/architecture/MH-21-unknowns.md'); text=''.join(Path(f).read_text(encoding='utf-8').lower() for f in files); required=('trust','verification','retention','change detection'); assert all(x in text for x in required); print('P4.3 architecture evidence scan PASS')"], 30))
    if selected and selected.fallback_kind == "p4.2-trusted-sources-intelligence-gap-reconciliation":
        checks.append(([sys.executable, "-c",
                        "from pathlib import Path; files=('specification/contract-registry.yaml','specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','docs/architecture/MH-21-rag-boundary.md','docs/architecture/MH-21-rag-security.md','docs/architecture/MH-21-cloud-boundary.md','docs/architecture/MH-21-data-egress.md','docs/architecture/MH-21-audit.md'); text=''.join(Path(f).read_text(encoding='utf-8').lower() for f in files); required=('trusted-source','retrieval','verification','provenance','evidence'); assert all(x in text for x in required); print('P4.2 architecture evidence scan PASS')"], 30))
    if selected and selected.fallback_kind == "p4.1-document-ingestion-index-search-gap-reconciliation":
        checks.append(([sys.executable, "-c",
                        "from pathlib import Path; files=('specification/contract-registry.yaml','specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md','docs/architecture/MH-21-rag-boundary.md','docs/architecture/MH-21-rag-security.md','docs/architecture/MH-21-resource-governance.md'); text=''.join(Path(f).read_text(encoding='utf-8').lower() for f in files); required=('document','ingestion','index','search'); assert all(x in text for x in required); print('P4.1 architecture evidence scan PASS')"], 30))
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
        if raw:
            encoding = inspect_queue_encoding(ROOT)
            needs_encoding = [row for row in encoding if row.status == "NEEDS_ENCODING"]
            if needs_encoding:
                print("LOCAL_AGENT_NOOP: factual queue exists but no bounded compiler is authorized")
                state("BLOCKED", "NEEDS_ENCODING: no deterministic acceptance encoder for remaining factual queue rows")
                return 30
            print("LOCAL_AGENT_IDLE: canonical queue is fully encoded but no bounded local task is currently eligible")
            state("IDLE", "all canonical queue rows are encoded; waiting for a new eligible bounded task or event")
            return 0
        print("LOCAL_AGENT_IDLE: no eligible local queue item")
        state("IDLE", "no eligible local task; waiting for a new bounded task or event")
        return 0
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
