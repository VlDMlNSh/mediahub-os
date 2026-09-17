#!/usr/bin/env python3
"""Static, dependency-free verification for the MediaHub AI engineering layer."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AGENTS = {
    "mediahub-architect.md": ("State Authority", "machine-checkable acceptance criteria"),
    "mediahub-implementer.md": ("State Authority", "regression"),
    "mediahub-verifier.md": ("independent verifier", "PASS / FAIL / BLOCKED"),
    "mediahub-security.md": ("secrets", "privilege"),
    "mediahub-release.md": ("human production authorization", "rollback"),
}

ROUTER_CANDIDATES = [
    ROOT / ".github" / "ai-router.yml",
    ROOT / ".github" / "mediahub-ai-router.yml",
    ROOT / ".github" / "mediahub-ai-router.yaml",
    ROOT / ".github" / "ai-router.yaml",
]


def fail(message: str) -> None:
    print(f"AI_FACTORY_CHECK=FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


for filename, needles in REQUIRED_AGENTS.items():
    path = ROOT / ".github" / "agents" / filename
    require(path.is_file(), f"missing agent file: {path}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        require(needle in text, f"{filename}: missing required contract text: {needle}")

router = next((p for p in ROUTER_CANDIDATES if p.is_file()), None)
require(router is not None, "AI router configuration not found")
router_text = router.read_text(encoding="utf-8")

for needle in (
    "fallback_must_be_free: true",
    "production_use_requires_review: true",
    "never_store_credentials_in_repo: true",
    "verification:",
    "required_before_merge: true",
    "production_authorization: human",
    "model: openrouter/free",
    "endpoint: https://openrouter.ai/api/v1",
):
    require(needle in router_text, f"router: missing required contract: {needle}")

# Never allow credential material or credential-like literals in the router policy.
secret_patterns = (
    r"sk-[A-Za-z0-9_-]{12,}",
    r"OPENROUTER_API_KEY\s*:",
    r"Authorization\s*:\s*Bearer",
    r"api[_-]?key\s*:\s*['\"]",
)
for pattern in secret_patterns:
    require(not re.search(pattern, router_text, re.IGNORECASE), f"router contains secret-like material: {pattern}")

workflow = ROOT / ".github" / "workflows" / "mediahub-openrouter-smoke.yml"
require(workflow.is_file(), "OpenRouter smoke workflow missing")
workflow_text = workflow.read_text(encoding="utf-8")

for needle in (
    "permissions:\n  contents: read",
    "OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}",
    "OPENROUTER_ENDPOINT: https://openrouter.ai/api/v1",
    "OPENROUTER_MODEL: openrouter/free",
):
    require(needle in workflow_text, f"workflow: missing required security contract: {needle}")

require("inputs:" not in workflow_text, "workflow must not accept arbitrary inputs")
require("inputs.endpoint" not in workflow_text, "workflow endpoint must not be operator-controlled")
require("set -x" not in workflow_text, "workflow must not enable shell tracing")
require("echo $OPENROUTER_API_KEY" not in workflow_text, "workflow must not print API key")
require("echo \"$OPENROUTER_API_KEY\"" not in workflow_text, "workflow must not print API key")

# Keep the probe intentionally bounded and avoid logging model output.
require('"max_tokens":4' in workflow_text, "inference probe must remain bounded")
require("content = (message.get('content') or '').strip()" in workflow_text, "probe must inspect response content without logging it")

print(f"AI_FACTORY_CHECK=PASS router={router.relative_to(ROOT)} agents={len(REQUIRED_AGENTS)}")
