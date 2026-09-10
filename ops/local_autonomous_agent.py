#!/usr/bin/env python3
"""Fail-closed local MediaHub coding agent.

The local model proposes one bounded unified diff. Git and verification gates decide
whether that proposal is admissible. The model never becomes an authority.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path("/home/mediahub/dev/mediahub-os-autonomous")
MODEL = Path("/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf")
LOCAL_AI_URL = "http://127.0.0.1:8081/v1/chat/completions"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(request.full_url, code, "redirect denied", headers, None)


LOCAL_AI_OPENER = urllib.request.build_opener(NoRedirectHandler)
GIT = Path("/usr/bin/git")
MAX_DIFF_LINES = 500
PROTECTED = {".git", ".autonomous", ".github", "ops/cloud-development-adapter.py", "ops/cloud_development_adapter.py", "ops/local_autonomous_agent.py", "ops/autonomous_os_loop.sh", "ops/autonomous_watchdog.sh"}
ALLOWED_TOP = {"architecture", "planning", "specification", "ops", "tests", "docs", "contracts", "development", "governance", "verification", "runtime", "security"}
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"


def run(cmd: list[str], timeout: int = 120, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=check)


def snapshot() -> str:
    status = run(["git", "status", "--short"])
    diff = run(["git", "diff", "--stat"])
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    return f"HEAD={head}\nSTATUS:\n{status.stdout}\nDIFFSTAT:\n{diff.stdout}"


def task() -> str:
    queue = ROOT / "ops/local_autonomous_tasks.md"
    base = queue.read_text() if queue.exists() else "Perform the smallest safe architecture-consistency improvement discoverable from the repository."
    return base + "\n\nCURRENT TASK STATE\n- The first-wave Cloud Development Adapter skeleton already exists at ops/cloud-development-adapter.py and is already tracked. Treat that implementation item as COMPLETE for this local cycle. Do NOT create, re-add, or replace that file.\n- The Cloud Development second wave (Claude/Codex provider integration) is gated and must NOT be activated by the local-only agent.\n- Select exactly one small change in an EXISTING repository file: preferably a regression test, contract, invariant, documentation correction, or deterministic validation.\n- Before emitting a diff, inspect CURRENT STATE and choose a path that is already tracked. Never modify, re-add, rename, or replace either Cloud Development Adapter entry point: ops/cloud-development-adapter.py or ops/cloud_development_adapter.py.\n"


def prompt() -> str:
    return f"""You are a LOCAL MediaHub coding agent. Internet/cloud AI is unavailable and must not be required.
Repository: {ROOT}
Immutable R4: {R4}. Never modify it or rewrite history.
Authority rules: AI output is advisory; State Authority remains canonical; fail closed; do not unlock qualification, release, or production.
You may make exactly ONE small downstream change per cycle.
Return ONLY a unified git diff, no markdown fences, no commentary.
Allowed: existing repository files under architecture/, planning/, specification/, ops/, tests/, docs/.
Forbidden: .git/, .autonomous/, secrets, credentials, workflows that grant authority, history rewriting.
The diff must be <= {MAX_DIFF_LINES} lines and must be directly applicable with `git apply`.
Never change file modes, executable bits, rename metadata, or file type; preserve the existing mode of every tracked file. Do not emit `new file mode`, `old mode`, or `new mode` lines.
Prefer tests, contracts, registries, documentation, and deterministic validation over speculative runtime changes.

CURRENT STATE
{snapshot()}

TASK QUEUE
{task()}
"""


def extract(text: str) -> str:
    text = text.strip()
    if "```" in text:
        blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", text, flags=re.DOTALL)
        text = max(blocks, key=len) if blocks else text.replace("```diff", "").replace("```", "")
    start = text.find("diff --git ")
    if start < 0:
        return ""
    return text[start:].strip()


def safe_patch(patch: str) -> bool:
    if not patch or len(patch.splitlines()) > MAX_DIFF_LINES:
        return False
    old_path = None
    for line in patch.splitlines():
        if line.startswith(("old mode ", "new mode ", "new file mode ", "deleted file mode ")):
            return False
        if line.startswith("--- /dev/null"):
            old_path = "/dev/null"
        elif line.startswith("--- a/"):
            old_path = line[6:].strip()
        elif line.startswith("+++ b/"):
            path = line[6:].strip()
            parts = Path(path).parts
            if path in PROTECTED or any(part in {".git", ".autonomous", ".github"} for part in parts):
                return False
            if parts and parts[0] not in ALLOWED_TOP:
                return False
            if path.startswith((".env", "/")) or "secret" in path.lower() or "credential" in path.lower():
                return False
            # A tracked file must never be reintroduced as a new file. This makes
            # model output idempotent even when the model ignores the task hint.
            if old_path == "/dev/null" and run(["git", "ls-files", "--error-unmatch", path]).returncode == 0:
                return False
    return True


def verify() -> bool:
    checks = [
        ["git", "diff", "--check"],
        ["bash", "ops/security_scan_local.sh"],
    ]
    for cmd in checks:
        p = run(cmd, timeout=600)
        if p.returncode != 0:
            print(p.stdout + p.stderr, file=sys.stderr)
            return False
    return True


def generate(prompt_file: Path) -> tuple[int, str]:
    health = urllib.request.Request("http://127.0.0.1:8081/health", method="GET")
    try:
        with LOCAL_AI_OPENER.open(health, timeout=5) as response:
            if response.status != 200:
                raise urllib.error.URLError("local ai health status")
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"LOCAL_AGENT_LOCAL_AI_ERROR: {type(exc).__name__}", file=sys.stderr)
        return 28, ""
    payload = {
        "messages": [
            {"role": "system", "content": "Return only a directly applicable unified git diff. No commentary."},
            {"role": "user", "content": prompt_file.read_text(encoding="utf-8")},
        ],
        "max_tokens": 192,
        "temperature": 0,
    }
    request = urllib.request.Request(
        LOCAL_AI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with LOCAL_AI_OPENER.open(request, timeout=90) as response:
            raw = response.read(1_048_577)
        if len(raw) > 1_048_576:
            print("LOCAL_AGENT_LOCAL_AI_ERROR: response_too_large", file=sys.stderr)
            return 28, ""
        body = json.loads(raw.decode("utf-8"))
        content = body["choices"][0]["message"]["content"]
        return 0, str(content)
    except (KeyError, IndexError, urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"LOCAL_AGENT_LOCAL_AI_ERROR: {type(exc).__name__}", file=sys.stderr)
        return 28, ""


def main() -> int:
    if not MODEL.is_file():
        print("LOCAL_AGENT_BLOCKED: local model runtime/model unavailable", file=sys.stderr)
        return 20
    if run(["git", "merge-base", "--is-ancestor", R4, "HEAD"]).returncode != 0:
        print("LOCAL_AGENT_BLOCKED: R4 ancestry invariant failed", file=sys.stderr)
        return 21
    if run(["git", "status", "--porcelain"]).stdout.strip():
        print("LOCAL_AGENT_BLOCKED: working tree is not clean", file=sys.stderr)
        return 22
    prompt_file = ROOT / ".autonomous" / "local-agent-prompt.txt"
    prompt_file.write_text(prompt(), encoding="utf-8")
    try:
        rc, output = generate(prompt_file)
    finally:
        prompt_file.unlink(missing_ok=True)
    if rc != 0:
        return rc
    patch = extract(output)
    if not safe_patch(patch):
        # One bounded regeneration is permitted. The first model response is
        # untrusted; a malformed/protected patch must never be applied.
        prompt_file.write_text(prompt() + "\nREGENERATION CONSTRAINT: previous proposal was rejected. Return a diff touching exactly one already-tracked file from the admissible repository paths; never touch protected paths, file modes, or new files.\n", encoding="utf-8")
        rc, output = generate(prompt_file)
        if rc != 0:
            return rc
        patch = extract(output)
        if not safe_patch(patch):
            print("LOCAL_AGENT_BLOCKED: invalid or oversized patch after bounded regeneration", file=sys.stderr)
            return 24
    check = subprocess.run([str(GIT), "apply", "--check", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)
    if check.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: patch check failed\n" + check.stderr, file=sys.stderr)
        return 25
    apply = subprocess.run([str(GIT), "apply", "--index", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)
    if apply.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: patch apply failed\n" + apply.stderr, file=sys.stderr)
        return 26
    changed = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    python_files = [path for path in changed if path.endswith(".py")]
    if python_files:
        lint_fix = subprocess.run(["ruff", "check", "--fix", *python_files], cwd=ROOT, text=True, capture_output=True, check=False)
        if lint_fix.returncode != 0:
            print("LOCAL_AGENT_BLOCKED: deterministic lint repair failed\n" + lint_fix.stderr, file=sys.stderr)
            return 33
        restage = run(["git", "add", "--", *changed], timeout=120)
        if restage.returncode != 0:
            print("LOCAL_AGENT_BLOCKED: restage after lint repair failed\n" + restage.stderr, file=sys.stderr)
            return 34
    if not verify():
        # Baseline is fail-closed clean; restore index+worktree without moving HEAD.
        rollback = run(["git", "restore", "--staged", "--worktree", "--", "."], timeout=120)
        if rollback.returncode != 0 or run(["git", "status", "--porcelain"]).stdout.strip():
            print("LOCAL_AGENT_ROLLBACK_BLOCKED: non-destructive restore failed", file=sys.stderr)
            return 29
        print("LOCAL_AGENT_ROLLBACK: verification failed; HEAD preserved", file=sys.stderr)
        return 27
    msg = run(["git", "diff", "--cached", "--name-only"]).stdout.strip().splitlines()
    if not msg:
        print("LOCAL_AGENT_NOOP: no admissible downstream change")
        return 30
    subject = "chore: local autonomous verified downstream increment"
    commit = run(["git", "commit", "-m", subject], timeout=120)
    if commit.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: commit failed\n" + commit.stderr, file=sys.stderr)
        return 31
    post_head = run(["git", "rev-parse", "HEAD"])
    if post_head.returncode != 0 or not post_head.stdout.strip():
        print("LOCAL_AGENT_BLOCKED: post-commit HEAD verification failed", file=sys.stderr)
        return 32
    print("LOCAL_AGENT_COMMIT=" + post_head.stdout.strip())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
