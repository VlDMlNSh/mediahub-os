#!/usr/bin/env python3
"""Fail-closed local MediaHub coding agent.

The local model proposes one bounded unified diff. Git and verification gates decide
whether that proposal is admissible. The model never becomes an authority.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous"))
MODEL = Path(os.environ.get("MEDIAHUB_LOCAL_MODEL", "/home/mediahub/local-ai/models/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"))
LLAMA = Path(os.environ.get("MEDIAHUB_LLAMA_CLI", "/home/mediahub/local-ai/bin/llama-cli"))
MAX_DIFF_LINES = 500
PROTECTED = {".git", ".autonomous", ".github"}
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
    return queue.read_text() if queue.exists() else "Perform the smallest safe architecture-consistency improvement discoverable from the repository."


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
Prefer tests, contracts, registries, documentation, and deterministic validation over speculative runtime changes.

CURRENT STATE
{snapshot()}

TASK QUEUE
{task()}
"""


def extract(text: str) -> str:
    text = text.strip()
    if "```" in text:
        blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", text, flags=re.S)
        text = max(blocks, key=len) if blocks else text.replace("```diff", "").replace("```", "")
    start = text.find("diff --git ")
    if start < 0:
        return ""
    return text[start:].strip()


def safe_patch(patch: str) -> bool:
    if not patch or len(patch.splitlines()) > MAX_DIFF_LINES:
        return False
    for line in patch.splitlines():
        if line.startswith("+++ b/") or line.startswith("--- a/"):
            path = line[6:].strip()
            if any(part in PROTECTED for part in Path(path).parts):
                return False
            if path.startswith((".env", "/")) or "secret" in path.lower() or "credential" in path.lower():
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


def main() -> int:
    if not LLAMA.is_file() or not MODEL.is_file():
        print("LOCAL_AGENT_BLOCKED: local model runtime/model unavailable", file=sys.stderr)
        return 20
    if run(["git", "merge-base", "--is-ancestor", R4, "HEAD"]).returncode != 0:
        print("LOCAL_AGENT_BLOCKED: R4 ancestry invariant failed", file=sys.stderr)
        return 21
    if run(["git", "status", "--porcelain"]).stdout.strip():
        print("LOCAL_AGENT_BLOCKED: working tree is not clean", file=sys.stderr)
        return 22
    with tempfile.NamedTemporaryFile("w", delete=False, dir="/tmp", prefix="mediahub-local-agent-prompt-") as f:
        f.write(prompt())
        prompt_file = f.name
    try:
        p = subprocess.run([str(LLAMA), "-m", str(MODEL), "-f", prompt_file, "-n", "384", "-c", "2048", "--temp", "0"], cwd=ROOT, text=True, capture_output=True, timeout=900)
    finally:
        Path(prompt_file).unlink(missing_ok=True)
    if p.returncode != 0:
        print("LOCAL_AGENT_MODEL_RC=" + str(p.returncode), file=sys.stderr)
        print(p.stderr[-4000:], file=sys.stderr)
        return 23
    patch = extract(p.stdout)
    if not safe_patch(patch):
        print("LOCAL_AGENT_BLOCKED: invalid or oversized patch", file=sys.stderr)
        return 24
    check = subprocess.run(["git", "apply", "--check", "-"], cwd=ROOT, input=patch, text=True, capture_output=True)
    if check.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: patch check failed\n" + check.stderr, file=sys.stderr)
        return 25
    apply = subprocess.run(["git", "apply", "--index", "-"], cwd=ROOT, input=patch, text=True, capture_output=True)
    if apply.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: patch apply failed\n" + apply.stderr, file=sys.stderr)
        return 26
    if not verify():
        run(["git", "reset", "--hard", "HEAD"], timeout=120)
        print("LOCAL_AGENT_ROLLBACK: verification failed", file=sys.stderr)
        return 27
    msg = run(["git", "diff", "--cached", "--name-only"]).stdout.strip().splitlines()
    if not msg:
        print("LOCAL_AGENT_NOOP")
        return 0
    subject = "chore: local autonomous verified downstream increment"
    run(["git", "commit", "-m", subject], timeout=120)
    print("LOCAL_AGENT_COMMIT=" + run(["git", "rev-parse", "HEAD"]).stdout.strip())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
