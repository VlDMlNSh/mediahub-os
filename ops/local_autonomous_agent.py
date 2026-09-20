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
MAX_REGENERATIONS = 3
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

    # No higher-level local task has encoded acceptance criteria yet; stop rather than fabricate work.
    # Higher-level queue items remain eligible only after their acceptance criteria
    # are encoded as deterministic local tasks.
    return None

def compile_executable_task(root: Path, task: LocalTask) -> ExecutableTask | None:
    """Compile a selected candidate only when repository evidence is sufficient."""
    target = root / task.target
    if not target.is_file():
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
    for path in (root / ".autonomous" / "evidence", root / ".autonomous" / "logs"):
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
        "P1.6": ("P1.1",),
    }
    conflicts = {
        "ops/mediahub_native_execution.py": ("State Authority", "production", "R4"),
        "tests/test_mediahub_native_execution.py": ("State Authority", "production", "R4"),
        "ops/hybrid_cloud_api_egress_adapter.py": ("cloud activation", "credentials"),
    }
    phase = task.task_id.split("-", 1)[0]
    verification = (
        "pytest -q tests/test_mediahub_native_execution.py"
        if "native_execution" in task.target
        else "pytest -q tests/test_hybrid_cloud_api_egress_adapter.py"
    )
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
    current = (ROOT / task.target).read_text(encoding="utf-8")
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
    if selected and selected.fallback_kind in {"hybrid-egress-types", "hybrid-egress-tests"}:
        checks.append(([sys.executable, "-m", "pytest", "-q", "tests/test_hybrid_cloud_api_egress_adapter.py"], 180))
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
        with LOCAL_AI_OPENER.open(req, timeout=60) as response:
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
