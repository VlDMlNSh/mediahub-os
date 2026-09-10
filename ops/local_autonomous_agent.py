#!/usr/bin/env python3
"""Fail-closed local MediaHub coding agent."""
from __future__ import annotations

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
LOCAL_AI_URL = "http://127.0.0.1:8081/v1/chat/completions"
GIT = Path("/usr/bin/git")
RUFF = Path(shutil.which("ruff") or "")
MAX_DIFF_LINES = 160
MAX_REGENERATIONS = 3
TARGET = "tests/test_mediahub_free_model_catalog.py"
PROTECTED = {".git", ".autonomous", ".github", "ops/cloud-development-adapter.py", "ops/cloud_development_adapter.py", "ops/local_autonomous_agent.py", "ops/autonomous_os_loop.sh", "ops/autonomous_watchdog.sh"}
ALLOWED_TOP = {"architecture", "planning", "specification", "ops", "tests", "docs", "contracts", "development", "governance", "verification", "runtime", "security"}
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(request.full_url, code, "redirect denied", headers, None)


LOCAL_AI_OPENER = urllib.request.build_opener(NoRedirectHandler)


def run(cmd: list[str], timeout: int = 120, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=check)  # nosec B603


def prompt(feedback: str = "") -> str:
    head = run(["git", "rev-parse", "HEAD"]).stdout.strip()
    target = ROOT / TARGET
    current = target.read_text(encoding="utf-8")
    feedback_block = f"\nPATCH CHECK ERROR:\n{feedback}\nReturn a corrected complete diff.\n" if feedback else ""
    return f"""LOCAL MediaHub coding agent.
HEAD={head}; R4={R4} immutable.
TARGET={TARGET}
Return ONLY a complete unified git diff, no fences, no commentary.
Modify ONLY TARGET, which is already tracked. No new files, modes, renames, secrets, .git, .github, .autonomous, production, cloud activation.
The diff must pass `git apply --check`; use the exact TARGET path and real file context below.
Add exactly ONE useful deterministic regression/invariant test. Keep the change small.
CURRENT TARGET CONTENT:
{current}
{feedback_block}"""


def extract(text: str) -> str:
    text = text.strip()
    if "```" in text:
        blocks = re.findall(r"```(?:diff|patch)?\s*\n(.*?)```", text, flags=re.DOTALL)
        text = max(blocks, key=len) if blocks else text.replace("```diff", "").replace("```patch", "").replace("```", "")
    start = text.find("diff --git ")
    return text[start:].strip() if start >= 0 else ""


def safe_patch(patch: str) -> bool:
    lines = patch.splitlines()
    if not patch or len(lines) > MAX_DIFF_LINES:
        return False
    old_path = new_path = None
    saw_hunk = False
    for line in lines:
        if line.startswith(("old mode ", "new mode ", "new file mode ", "deleted file mode ", "similarity index ", "rename from ", "rename to ")):
            return False
        if line.startswith("--- a/"):
            old_path = line[6:].strip()
        elif line.startswith("+++ b/"):
            new_path = line[6:].strip()
        elif line.startswith("@@ "):
            saw_hunk = True
    if old_path != TARGET or new_path != TARGET or not saw_hunk:
        return False
    return not (new_path in PROTECTED or any(part in {".git", ".autonomous", ".github"} for part in Path(new_path).parts))


def verify() -> bool:
    for cmd in (["git", "diff", "--check"], ["bash", "ops/security_scan_local.sh"]):
        p = run(cmd, timeout=600)
        if p.returncode != 0:
            print(p.stdout + p.stderr, file=sys.stderr)
            return False
    return True


def generate(prompt_text: str) -> tuple[int, str]:
    health = urllib.request.Request("http://127.0.0.1:8081/health", method="GET")
    try:
        with LOCAL_AI_OPENER.open(health, timeout=5) as response:
            if response.status != 200:
                raise urllib.error.URLError("local ai health status")
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"LOCAL_AGENT_LOCAL_AI_ERROR: {type(exc).__name__}", file=sys.stderr)
        return 28, ""
    payload = {"messages": [{"role": "system", "content": "Return only a complete unified git diff."}, {"role": "user", "content": prompt_text}], "max_tokens": 256, "temperature": 0}
    request = urllib.request.Request(LOCAL_AI_URL, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with LOCAL_AI_OPENER.open(request, timeout=75) as response:
            raw = response.read(1_048_577)
        if len(raw) > 1_048_576:
            return 28, ""
        body = json.loads(raw.decode("utf-8"))
        return 0, str(body["choices"][0]["message"]["content"])
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
    last_error = ""
    patch = ""
    for attempt in range(1, MAX_REGENERATIONS + 1):
        rc, output = generate(prompt(last_error))
        if rc != 0:
            return rc
        patch = extract(output)
        if not safe_patch(patch):
            last_error = "structural safety validation failed: use exactly tests/test_mediahub_free_model_catalog.py"
            continue
        check = subprocess.run([str(GIT), "apply", "--check", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)  # nosec B603
        if check.returncode == 0:
            break
        last_error = check.stderr.strip()[-1200:] or "git apply --check rejected the patch"
        if attempt == MAX_REGENERATIONS:
            print("LOCAL_AGENT_BLOCKED: patch check failed after bounded regeneration\n" + last_error, file=sys.stderr)
            return 25
    else:
        print("LOCAL_AGENT_BLOCKED: no admissible patch", file=sys.stderr)
        return 24

    apply = subprocess.run([str(GIT), "apply", "--index", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)  # nosec B603
    if apply.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: patch apply failed\n" + apply.stderr, file=sys.stderr)
        return 26
    changed = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    if changed != [TARGET]:
        run(["git", "restore", "--staged", "--worktree", "--", "."])
        print("LOCAL_AGENT_ROLLBACK: proposal touched an unexpected file", file=sys.stderr)
        return 27
    if RUFF.is_file():
        lint = subprocess.run([str(RUFF), "check", "--fix", TARGET], cwd=ROOT, text=True, capture_output=True, check=False)  # nosec B603
        if lint.returncode != 0:
            print("LOCAL_AGENT_BLOCKED: deterministic lint repair failed", file=sys.stderr)
            return 33
        run(["git", "add", "--", TARGET])
    if not verify():
        rollback = run(["git", "restore", "--staged", "--worktree", "--", "."], timeout=120)
        if rollback.returncode != 0 or run(["git", "status", "--porcelain"]).stdout.strip():
            print("LOCAL_AGENT_ROLLBACK_BLOCKED: non-destructive restore failed", file=sys.stderr)
            return 29
        print("LOCAL_AGENT_ROLLBACK: verification failed; HEAD preserved", file=sys.stderr)
        return 27
    commit = run(["git", "commit", "-m", "chore: local autonomous verified downstream increment"], timeout=120)
    if commit.returncode != 0:
        print("LOCAL_AGENT_BLOCKED: commit failed\n" + commit.stderr, file=sys.stderr)
        return 31
    print("LOCAL_AGENT_COMMIT=" + run(["git", "rev-parse", "HEAD"]).stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
