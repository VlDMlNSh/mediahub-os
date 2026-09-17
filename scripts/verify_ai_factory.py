#!/usr/bin/env python3
"""Static, dependency-free verification for the MediaHub AI engineering layer."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_AGENTS = {
    "mediahub-architect.md": ("State Authority", "machine-checkable acceptance criteria"),
    "mediahub-implementer.md": ("State Authority", "regression"),
    "mediahub-verifier.md": ("independent verifier", "PASS / FAIL / BLOCKED"),
    "mediahub-security.md": ("secrets", "privilege"),
    "mediahub-release.md": ("human production authorization", "rollback"),
}
ROUTER = ROOT / ".github" / "ai" / "model-router.yml"
WORKFLOW = ROOT / ".github" / "workflows" / "mediahub-openrouter-smoke.yml"
ECC_DOC = ROOT / "docs" / "ai" / "ECC-INTEGRATION.md"
ECC_MANIFEST = ROOT / "oss" / "manifests" / "ecc.yaml"


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

require(ROUTER.is_file(), f"AI router configuration missing: {ROUTER}")
router_text = ROUTER.read_text(encoding="utf-8")
for needle in (
    "fallback_must_be_free: true",
    "production_use_requires_review: true",
    "never_store_credentials_in_repo: true",
    "required_before_merge: true",
    "independent_review_required: true",
    "production_authorization: human",
    "model: openrouter/free",
    "endpoint: https://openrouter.ai/api/v1",
):
    require(needle in router_text, f"router: missing required contract: {needle}")

for pattern in (
    r"sk-[A-Za-z0-9_-]{12,}",
    r"OPENROUTER_API_KEY\s*:",
    r"Authorization\s*:\s*Bearer",
    r"api[_-]?key\s*:\s*['\"]",
):
    require(not re.search(pattern, router_text, re.IGNORECASE), f"router contains secret-like material: {pattern}")

require(WORKFLOW.is_file(), "OpenRouter smoke workflow missing")
workflow_text = WORKFLOW.read_text(encoding="utf-8")
for needle in (
    "permissions:\n  contents: read",
    "OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}",
    "OPENROUTER_ENDPOINT: https://openrouter.ai/api/v1",
    "OPENROUTER_MODEL: openrouter/free",
    '"max_tokens":4',
    "content = (message.get('content') or '').strip()",
):
    require(needle in workflow_text, f"workflow: missing required security contract: {needle}")

require("inputs:" not in workflow_text, "workflow must not accept arbitrary inputs")
require("inputs.endpoint" not in workflow_text, "workflow endpoint must not be operator-controlled")
require("set -x" not in workflow_text, "workflow must not enable shell tracing")
require("echo $OPENROUTER_API_KEY" not in workflow_text, "workflow must not print API key")
require("echo \"$OPENROUTER_API_KEY\"" not in workflow_text, "workflow must not print API key")

require(ECC_DOC.is_file(), "ECC integration document missing")
ecc_doc = ECC_DOC.read_text(encoding="utf-8")
for needle in (
    "Pinned upstream release: `v2.2.1`",
    "MediaHub remains authoritative",
    "ECC agents MUST NOT mutate State Authority directly.",
    "Provider credentials remain outside the repository and outside agent prompts.",
    "initial integration is deliberately documentation and policy only",
):
    require(needle in ecc_doc, f"ECC document: missing required contract: {needle}")
for secret_name in ("OPENAI_API_KEY", "OPENROUTER_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY"):
    require(secret_name not in ecc_doc, f"ECC document contains provider secret name: {secret_name}")

require(ECC_MANIFEST.is_file(), "ECC manifest missing")
ecc_manifest = ECC_MANIFEST.read_text(encoding="utf-8")
for needle in (
    "version: v2.2.1",
    "ref: v2.2.1",
    "status: target-gated",
    "class: agent-harness",
    "direct_state_authority_mutation: false",
    "hidden_network_egress: false",
    "unbounded_subprocesses: false",
    "bypass_authorization: false",
    "bypass_release_gates: false",
    "production_authorization: human",
    "fail_closed: true",
    "release_blocking: true",
    "independent-review",
    "wholesale_source_import: false",
    "hooks_enabled_by_default: false",
    "commands_enabled_by_default: false",
):
    require(needle in ecc_manifest, f"ECC manifest: missing required contract: {needle}")

print(f"AI_FACTORY_CHECK=PASS router={ROUTER.relative_to(ROOT)} agents={len(REQUIRED_AGENTS)} ecc=target-gated")
