# MediaHub Hybrid Autonomous Development 24/7

Status: `target-gated` / `qualification-gated`

## Objective

Provide a continuous operating model for MediaHub engineering in which deterministic repository checks, specialist-agent analysis, provider fallback, and human authorization form one bounded control loop.

This document defines orchestration policy. It does not grant any agent authority over State Authority, release, production, or security decisions.

## Operating lanes

1. **Astra / coordinator** — decomposes work, correlates evidence, selects the next bounded task.
2. **Architect** — checks architecture, contracts, dependencies, and acceptance criteria.
3. **Implementer** — performs only reviewable repository changes.
4. **Verifier** — runs deterministic tests and qualification checks independently of implementation reasoning.
5. **Security** — checks secrets, permissions, network, supply-chain, and authority boundaries.
6. **Release** — assembles qualification evidence; it cannot authorize production.
7. **ECC specialist lane** — advisory support only through the seven allowlisted roles in `oss/adapters/ecc/dispatcher-policy.yaml`.

## Hybrid provider policy

The controlled AI router remains the provider boundary. Provider credentials are repository-external. The preferred sequence is GitHub Copilot agent, OpenAI, Anthropic, Gemini, Tabi, then the free OpenRouter fallback where the applicable workflow permits it.

Provider fallback is an availability/degradation mechanism, not a permission escalation. A provider cannot grant itself repository, release, or production authority.

## Continuous control loop

Each cycle follows this order:

`observe -> plan -> bounded task -> implement -> verify -> security/qualification -> evidence -> next task`

A failed verification returns the cycle to diagnosis. Missing evidence blocks progression. A degraded provider causes a bounded fallback or an explicit degraded result; it must not trigger an unsafe alternative.

## 24/7 execution boundary

The repository may host scheduled orchestration and machine-checkable gates, but unattended execution MUST remain bounded. No workflow may enable ECC hooks/commands, arbitrary upstream automation, unrestricted subprocesses, secret extraction, direct State Authority mutation, release authorization, or production deployment merely because an agent produced a successful result.

Long-running development requires an external runner/agent host with least-privilege credentials and explicit lifecycle controls. GitHub Actions scheduling alone is not treated as a perpetual agent runtime.

## Human gates

The following remain human-controlled:

- production authorization;
- release authorization where required by the baseline;
- enabling new agent roles beyond the allowlist;
- enabling ECC hooks or commands;
- granting new provider/tool permissions;
- changing State Authority authority boundaries.

## Evidence requirements

Every autonomous cycle must leave machine-checkable evidence: commit SHA, changed paths, tests, verification result, security/qualification result, provider/degraded state where applicable, and unresolved blockers. An unverified assertion is never converted into `PASS`.

## Initial activation

The initial activation is policy-level only. The ECC integration remains target-gated and the seven-role dispatcher remains advisory. Runtime execution must be separately qualified before being enabled.
