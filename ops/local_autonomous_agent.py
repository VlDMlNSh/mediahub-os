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
R4 = "471f709f5633feab7aeb62dd3ea52effad6d2bc4"


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(request.full_url, code, "redirect denied", headers, None)


LOCAL_AI_OPENER = urllib.request.build_opener(NoRedirectHandler)


def run(cmd: list[str], timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)  # nosec B603


def prompt(feedback: str = "") -> str:
    current = (ROOT / TARGET).read_text(encoding="utf-8")
    error = f"\nPrevious rejection: {feedback}\n" if feedback else ""
    return f"""MediaHub local coding cycle. R4={R4}. Modify ONLY the existing tracked file {TARGET}.
Add exactly one test named test_catalog_has_unique_provider_model_pairs that asserts provider/model pairs in FREE_MODEL_CANDIDATES are unique.
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
        if line.startswith(("old mode ", "new mode ", "new file mode ", "deleted file mode ", "similarity index ", "rename from ", "rename to ")):
            return False
        if line.startswith("--- a/"):
            old_path = line[6:].strip()
        elif line.startswith("+++ b/"):
            new_path = line[6:].strip()
        elif line.startswith("@@ "):
            saw_hunk = True
    return old_path == TARGET and new_path == TARGET and saw_hunk and TARGET not in PROTECTED


def verify() -> bool:
    for cmd in (["git", "diff", "--check"], ["bash", "ops/security_scan_local.sh"]):
        p = run(cmd, timeout=600)
        if p.returncode:
            print(p.stdout + p.stderr, file=sys.stderr)
            return False
    return True


def generate(text: str) -> tuple[int, str]:
    try:
        with LOCAL_AI_OPENER.open(urllib.request.Request("http://127.0.0.1:8081/health"), timeout=5) as r:
            if r.status != 200:
                return 28, ""
    except (urllib.error.URLError, TimeoutError):
        return 28, ""
    payload = {"messages": [{"role": "system", "content": "Return only a complete unified git diff."}, {"role": "user", "content": text}], "max_tokens": 256, "temperature": 0}
    req = urllib.request.Request(LOCAL_AI_URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"}, method="POST")
    try:
        with LOCAL_AI_OPENER.open(req, timeout=60) as response:
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
        return 20
    if run(["git", "merge-base", "--is-ancestor", R4]).returncode:
        return 21
    if run(["git", "status", "--porcelain"]).stdout.strip():
        return 22
    error = ""
    patch = ""
    for _ in range(MAX_REGENERATIONS):
        rc, output = generate(prompt(error))
        if rc:
            return rc
        patch = extract(output)
        if not safe_patch(patch):
            error = "structural validation failed; use exact target path and complete ---/+++/@@ sections"
            continue
        check = subprocess.run([str(GIT), "apply", "--check", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)  # nosec B603
        if check.returncode == 0:
            break
        error = check.stderr.strip()[-1200:] or "git apply --check rejected the patch"
    else:
        print("LOCAL_AGENT_BLOCKED: patch check failed after bounded regeneration\n" + error, file=sys.stderr)
        return 25
    apply = subprocess.run([str(GIT), "apply", "--index", "-"], cwd=ROOT, input=patch, text=True, capture_output=True, check=False)  # nosec B603
    if apply.returncode:
        return 26
    changed = run(["git", "diff", "--cached", "--name-only"]).stdout.splitlines()
    if changed != [TARGET]:
        run(["git", "restore", "--staged", "--worktree", "--", "."])
        return 27
    if RUFF.is_file() and subprocess.run([str(RUFF), "check", "--fix", TARGET], cwd=ROOT, text=True, capture_output=True, check=False).returncode:
        return 33
    run(["git", "add", "--", TARGET])
    if not verify():
        rollback = run(["git", "restore", "--staged", "--worktree", "--", "."])
        if rollback.returncode or run(["git", "status", "--porcelain"]).stdout.strip():
            return 29
        return 27
    commit = run(["git", "commit", "-m", "chore: local autonomous verified downstream increment"], timeout=120)
    if commit.returncode:
        return 31
    print("LOCAL_AGENT_COMMIT=" + run(["git", "rev-parse", "HEAD"]).stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
