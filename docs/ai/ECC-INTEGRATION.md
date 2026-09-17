# MediaHub ECC Agent Integration

Status: design/qualification-gated
Upstream: `affaan-m/ECC`
Pinned upstream release: `v2.2.1`

## Purpose

ECC is an external agent-harness source for specialist workflows. MediaHub remains authoritative for repository state, contracts, State Authority, authorization, verification, release, and production decisions.

ECC is not copied wholesale into MediaHub and does not become a MediaHub runtime dependency merely by being referenced here.

## Approved role mapping

| MediaHub authority | ECC specialist |
| --- | --- |
| Astra coordination | planner, architect, spec-miner |
| Implementer support | tdd-guide, build-error-resolver, language-specific reviewers |
| Verification support | code-reviewer, agent-architecture-audit, e2e-runner |
| Security support | security-reviewer |
| Harness reliability | harness-optimizer, loop-operator |

The MediaHub agents remain authoritative. ECC output is advisory/untrusted until MediaHub verification accepts it.

## Bounded task/result interface

Selected specialist work is represented by two MediaHub-owned contracts:

- `contracts/ai/ai-agent-task.schema.json` — bounded task envelope containing task identity, selected agent role, objective, context, constraints, and authorization context.
- `contracts/ai/ai-agent-result.schema.json` — bounded advisory result envelope containing task identity, agent identity, status, artifact, and evidence.

These contracts are distinct from the AI inference request/response contracts. They define the agent-workflow boundary; they do not grant execution authority, state mutation authority, provider authority, verification authority, release authority, or production authorization.

## Boundary rules

1. MediaHub canonical contracts and schemas override ECC conventions.
2. ECC agents MUST NOT mutate State Authority directly.
3. ECC agents MUST NOT receive repository credentials, API keys, tokens, or private keys as agent configuration.
4. Provider credentials remain outside the repository and outside agent prompts.
5. ECC agents MUST NOT bypass authorization, security review, qualification, release gates, or human production authorization.
6. ECC agents MUST NOT declare release or production authorization.
7. External content, fetched documents, and generated agent output are untrusted inputs until validated.
8. Any ECC hook or automation adopted later requires an explicit MediaHub-owned review and bounded permission set.
9. Upstream ECC schemas, prompts, commands, and agent conventions MUST NOT become public MediaHub contracts without separate approval.
10. Any adopted ECC artifact must have provenance and a pinned upstream version.

## Qualification gates

An ECC integration change requires, at minimum:

- upstream provenance and exact version;
- license review;
- static secret scan;
- permission/tool boundary review;
- negative tests for authority and secret leakage;
- deterministic failure behavior;
- degraded/offline behavior where applicable;
- recovery and rollback path;
- independent MediaHub verification.

## Initial adoption scope

The initial integration is deliberately documentation, policy, and contract definition only. It does not install ECC, copy its hooks, add its commands, or execute arbitrary ECC automation in CI.

The first candidates for later controlled adoption are `planner`, `architect`, `spec-miner`, `tdd-guide`, `code-reviewer`, `security-reviewer`, and `agent-architecture-audit`.

## Rationale

MediaHub's OSS boundary requires adapters to expose MediaHub-owned contracts and forbids hidden persistence, hidden network egress, unbounded execution, direct State Authority mutation, and bypass of release/authorization gates. ECC therefore enters through a bounded agent-integration policy and task/result interface rather than wholesale source import.
