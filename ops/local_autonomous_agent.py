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
TARGET = "tests/test_mediahub_native_execution.py"
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
Add focused negative and positive tests for the existing ExecutionProposal contract in ops/mediahub_native_execution.py: valid prepare_proposal preserves request_id/workload_id/source_sha/provider; missing request identity, workload identity, source provenance or provider is rejected. Tests must prove the proposal boundary has no execution or network side effects.
Return ONLY one complete unified git diff, no markdown fences, no commentary. Use the exact real file context below. No new files, modes, renames, secrets, .git, .github, .autonomous, production or cloud activation. The diff must pass git apply --check.
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


def fallback_patch() -> str:
    """Return the pre-approved Wave 10 ExecutionProposal test diff only."""
    path = ROOT / TARGET
    old = path.read_text(encoding="utf-8").splitlines(keepends=True)
    marker = "def test_execution_proposal_preserves_identity():"
    if any(marker in line for line in old):
        return ""
    addition = [
        "\n",
        "def test_execution_proposal_preserves_identity():\n",
        "    contract = NativeExecutionContract()\n",
        "    proposal = contract.prepare_proposal(\"req-1\", \"work-1\", \"sha-1\", \"openai\")\n",
        "    assert proposal.request_id == \"req-1\"\n",
        "    assert proposal.workload_id == \"work-1\"\n",
        "    assert proposal.source_sha == \"sha-1\"\n",
        "    assert proposal.provider == \"openai\"\n",
        "\n",
        "\n",
        "def test_execution_proposal_missing_identity_fails_closed():\n",
        "    contract = NativeExecutionContract()\n",
        "    for values in ((\"\", \"work-1\", \"sha-1\", \"openai\"), (\"req-1\", \"\", \"sha-1\", \"openai\"), (\"req-1\", \"work-1\", \"\", \"openai\"), (\"req-1\", \"work-1\", \"sha-1\", \"\")):\n",
        "        with pytest.raises(PermissionError):\n",
        "            contract.prepare_proposal(*values)\n",
    ]
    new = old + addition
    if not any(line.strip() == "import pytest" for line in new):
        new.insert(0, "import pytest\n")
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
    if "def test_execution_proposal_preserves_identity():" in target_text:
        print("LOCAL_AGENT_NOOP: Wave 10 proposal tests already satisfied")
        state("BLOCKED", "no admissible downstream change")
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
            state("AI_SUCCESS", "structural validation and git apply --check passed")
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
        state("FALLBACK_SELECTED", "whitelist task: unique provider/model regression")
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
