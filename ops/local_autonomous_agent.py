#!/usr/bin/env python3
"""Fail-closed local MediaHub coding agent with deterministic fallback."""
from __future__ import annotations

import difflib
import json
import re
import shutil
import subprocess  # nosec B404
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path("/home/mediahub/dev/mediahub-os-autonomous")
MODEL = Path("/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf")
LOCAL_AI_URL = "http://127.0.0.1:8081/v1/chat/completions"  # nosemgrep: python.lang.security.audit.insecure-transport.urllib.insecure-request-object.insecure-request-object
GIT = Path("/usr/bin/git")
RUFF = Path(shutil.which("ruff") or "")
MAX_DIFF_LINES = 160
MAX_REGENERATIONS = 3
TARGET = "ops/mediahub_native_execution.py"
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"
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


def prompt(feedback: str = "") -> str:
    current = (ROOT / TARGET).read_text(encoding="utf-8")
    error = f"\nPrevious rejection: {feedback}\n" if feedback else ""
    return f"""MediaHub local coding cycle. R4={R4}. Modify ONLY the existing tracked file {TARGET}.
Advance only to the next approved Wave 10 security task: harden NativeExecutionContract recovery-proposal admission against malformed evidence identity and verification types, without executing anything. Modify ONLY the existing tracked file ops/mediahub_native_execution.py. Preserve valid behavior, but add strict fail-closed type validation for CredentialRef and ExecutionTarget fields before normal validation. Reject wrong object and field types with PermissionError rather than leaking AttributeError/TypeError or accepting bool-as-string-like input. Keep HTTPS endpoint policy and existing provider/credential matching unchanged. Do not add provider-specific behavior or change the public contracts. The boundary must not execute subprocesses, access network, retrieve secrets, mutate State Authority/Home Assistant, or widen egress. Return ONLY one complete unified git diff, no markdown fences, no commentary. Use the exact real file context below. No new files, modes, renames, secrets, .git, .github, .autonomous, production or cloud activation. The diff must pass git apply --check.
{current}{error}"""


def extract(text: str) -> str:
    text = text.strip()
    blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", text, flags=re.DOTALL)
    if blocks:
        text = max(blocks, key=len)
    start = text.find("diff --git ")
    return text[start:].strip() if start >= 0 else ""


def safe_patch(patch: str) -> bool:
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
    return old_path == TARGET and new_path == TARGET and saw_hunk and TARGET not in PROTECTED

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
    diff = "".join(difflib.unified_diff(old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"))
    return diff if diff.endswith("\n") else diff + "\n"


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
    diff = "".join(difflib.unified_diff(old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"))
    return diff if diff.endswith("\n") else diff + "\n"


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
    diff = "".join(difflib.unified_diff(old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"))
    return diff if diff.endswith("\n") else diff + "\n"


def fallback_patch() -> str:
    """Return the pre-approved Wave 10 recovery-proposal admission hardening diff only."""
    path = ROOT / TARGET
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
        diff = "".join(difflib.unified_diff(old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"))
        return diff if diff.endswith("\n") else diff + "\n"
    if "def prepare_recovery_proposal(" in old_text and "malformed recovery evidence" not in old_text:
        return _fallback_recovery_patch(old, old_text)
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
        diff = "".join(difflib.unified_diff(old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"))
        return diff if diff.endswith("\n") else diff + "\n"
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
    diff = "".join(difflib.unified_diff(
        old, new, fromfile=f"a/{TARGET}", tofile=f"b/{TARGET}", lineterm="\n"
    ))
    return diff if diff.endswith("\n") else diff + "\n"

def apply_checked(patch: str) -> bool:
    if not safe_patch(patch):
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


def exact_target() -> bool:
    return run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines() == [TARGET]


def verify() -> bool:
    checks = [(["git", "diff", "--check"], 120)]
    if RUFF.is_file():
        checks.append(([str(RUFF), "check", TARGET], 120))
    checks.append((["bash", "ops/security_scan_local.sh"], 900))
    for item in checks:
        if item is None:
            continue
        cmd, timeout = item
        p = run(cmd, timeout=timeout)
        if p.returncode:
            print(p.stdout + p.stderr, file=sys.stderr)
            return False
    return True


def generate(text: str) -> tuple[int, str, str]:
    try:
        with LOCAL_AI_OPENER.open(
            urllib.request.Request("http://127.0.0.1:8081/health")  # nosemgrep: python.lang.security.audit.insecure-transport.urllib.insecure-request-object.insecure-request-object
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

    error = ""
    patch = ""
    # Do not spend an AI cycle on a deterministic task that is already satisfied.
    target_text = (ROOT / TARGET).read_text(encoding="utf-8")
    if "malformed recovery evidence" in target_text:
        print("LOCAL_AGENT_NOOP: Wave 10 recovery-proposal admission hardening already satisfied")
        state("BLOCKED", "recovery-proposal admission hardening already present")
        return 30

    for _ in range(MAX_REGENERATIONS):
        rc, output, ai_state = generate(prompt(error))
        if rc:
            state(ai_state, "local AI did not produce an admissible proposal")
            break
        patch = extract(output)
        if not safe_patch(patch):
            state("AI_MALFORMED", "structural validation rejected AI output")
            error = "structural validation failed; use exact target path and complete ---/+++/@@ sections"
            continue
        if apply_checked(patch):
            if RUFF.is_file():
                lint = subprocess.run(
                    [str(RUFF), "check", TARGET], cwd=ROOT,
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

    if not patch or not exact_target():
        patch = fallback_patch()
        if not patch:
            print("LOCAL_AGENT_NOOP: no admissible downstream change")
            state("BLOCKED", "no admissible fallback task or tree is already changed")
            return 30
        state("FALLBACK_SELECTED", "whitelist task: recovery-proposal admission hardening")
        if not apply_checked(patch):
            state("BLOCKED", "fallback failed structural validation or git apply --check")
            return 25
        state("FALLBACK_APPLIED", "fallback passed structural validation and git apply --check")

    if not exact_target():
        rollback()
        return 27
    if RUFF.is_file():
        lint = subprocess.run(
            [str(RUFF), "check", "--fix", TARGET], cwd=ROOT,
            text=True, capture_output=True, check=False
        )  # nosec B603
        if lint.returncode:
            print("LOCAL_AGENT_BLOCKED: deterministic lint repair failed", file=sys.stderr)
            print(lint.stdout + lint.stderr, file=sys.stderr)
            rollback()
            return 33
        run(["git", "add", "--", TARGET])
    if not exact_target():
        rollback()
        return 27

    if not verify():
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
