#!/usr/bin/env python3
"""Static, dependency-free verification for the MediaHub AI engineering layer."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / ".github" / "agents"
ROUTER = ROOT / ".github" / "ai" / "model-router.yml"
CONTROLLER = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"
FORBIDDEN_DIRECT_WORKFLOWS = (
    ".github/workflows/mediahub-openai-smoke.yml",
    ".github/workflows/mediahub-anthropic-smoke.yml",
    ".github/workflows/mediahub-gemini-smoke.yml",
    ".github/workflows/mediahub-openrouter-smoke.yml",
)
REQUIRED_AGENTS = {
    "mediahub-architect.md": ("State Authority", "machine-checkable acceptance criteria"),
    "mediahub-implementer.md": ("State Authority", "regression"),
    "mediahub-verifier.md": ("independent verifier", "PASS / FAIL / BLOCKED"),
    "mediahub-security.md": ("secrets", "privilege"),
    "mediahub-release.md": ("human production authorization", "rollback"),
}


def fail(message: str) -> None:
    print(f"AI_FACTORY_CHECK=FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


for filename, needles in REQUIRED_AGENTS.items():
    path = AGENTS / filename
    require(path.is_file(), f"missing agent file: {path}")
    text = path.read_text(encoding="utf-8")
    for needle in needles:
        require(needle in text, f"{filename}: missing required contract text: {needle}")

require(ROUTER.is_file(), f"AI router policy missing: {ROUTER}")
router_text = ROUTER.read_text(encoding="utf-8")
for needle in (
    "mode: policy_only",
    "direct_provider_api_calls: false",
    "permitted_cloud_agent_transport: .github/workflows/gemini-batch-dispatch-controller.yml",
    "permitted_cloud_agent_transport_only: true",
    "local_claude_runtime: ollama",
    "local_claude_host: Alamo",
    "local_claude_only: true",
    "paid_fallback: false",
    "unknown_route_behavior: fail_closed",
    "independent_review_required: true",
    "runtime_qualification_required: true",
    "production_authorization: human",
):
    require(needle in router_text, f"router: missing required policy: {needle}")

for forbidden in (
    "api.openai.com",
    "api.anthropic.com",
    "generativelanguage.googleapis.com",
    "openrouter.ai",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "OPENROUTER_API_KEY",
    "TABITOKEN_API_KEY",
):
    require(forbidden not in router_text, f"router contains unadmitted provider route or credential name: {forbidden}")

require(CONTROLLER.is_file(), "approved Gemini controller workflow missing")
controller_text = CONTROLLER.read_text(encoding="utf-8")
require("secrets.MEDIAHUB_GITHUB_TOKEN" in controller_text, "controller transport credential binding missing")
require("secrets.MEDIAHUB_DISPATCH_HMAC_KEY" in controller_text, "controller HMAC binding missing")

for relative in FORBIDDEN_DIRECT_WORKFLOWS:
    require(not (ROOT / relative).exists(), f"unapproved direct-provider workflow still exists: {relative}")

for pattern in (
    r"sk-[A-Za-z0-9_-]{12,}",
    r"Authorization\s*:\s*Bearer",
):
    require(not re.search(pattern, router_text, re.IGNORECASE), f"router contains secret-like material: {pattern}")

print(f"AI_FACTORY_CHECK=PASS agents={len(REQUIRED_AGENTS)} approved_controller_only=true")
