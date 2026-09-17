#!/usr/bin/env python3
"""Static, dependency-free verification of the MediaHub ECC dispatcher policy."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "oss" / "adapters" / "ecc" / "dispatcher-policy.yaml"


def fail(message: str) -> None:
    print(f"ECC_DISPATCHER_CHECK=FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


require(POLICY.is_file(), f"dispatcher policy missing: {POLICY}")
text = POLICY.read_text(encoding="utf-8")

for needle in (
    "status: target-gated",
    "fail_closed: true",
    "unknown_agent: blocked",
    "unlisted_agent: blocked",
    "missing_authorization: blocked",
    "missing_constraints: blocked",
    "ecc_unavailable: degraded",
    "successful_result_is_advisory: true",
    "evidence_required: true",
    "verification_required_before_mutation: true",
    "state_authority_mutation_from_agent: false",
    "provider_selection_authority_from_agent: false",
    "release_authorization_from_agent: false",
    "production_authorization_from_agent: false",
    "direct_repository_mutation: false",
    "mutation_requires_reviewable_mediahub_change: true",
    "mutation_requires_verification: true",
    "mutation_requires_existing_release_gates: true",
    "production_authorization: human",
):
    require(needle in text, f"dispatcher policy: missing required contract: {needle}")

for agent in (
    "planner",
    "architect",
    "spec-miner",
    "tdd-guide",
    "code-reviewer",
    "security-reviewer",
    "agent-architecture-audit",
):
    require(f"  {agent}:" in text, f"dispatcher policy: missing allowlisted agent: {agent}")

require(text.count("authority: advisory") == 7, "dispatcher policy: every initial agent must be advisory")
print("ECC_DISPATCHER_CHECK=PASS policy=fail-closed allowlist=7")
