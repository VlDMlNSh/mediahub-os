# ADR-002 — GitHub Prior-Art-First Engineering Rule

Status: ACCEPTED
Date: 2026-09-09
Scope: MediaHub Product and MediaHub Autonomous Development

## Decision

Before implementing any new MediaHub component, the engineering loop MUST first inspect existing mature implementations and relevant prior art on GitHub and other approved source repositories.

The purpose is not to copy a project wholesale. MediaHub uses prior art to reduce design errors, discover edge cases, compare stable implementation patterns, and identify proven test strategies.

## Mandatory sequence

1. Define the component contract and security constraints.
2. Search GitHub for existing implementations, libraries, standards, and tests.
3. Select the strongest candidates using maturity, maintenance, security history, test coverage, architecture, license, and operational evidence.
4. Inspect actual source code, not README claims alone.
5. Record reusable algorithms, interfaces, test cases, failure handling, and stable implementation patterns.
6. Decide for each candidate: USE, ADAPT, REIMPLEMENT, REFERENCE-ONLY, or REJECT.
7. Implement the MediaHub-native component independently unless an explicit dependency is approved.
8. Preserve MediaHub invariants: fail-closed, least privilege, provenance, deterministic behavior, R4 immutability, and provider independence.
9. Add regression tests derived from discovered edge cases.
10. Re-run qualification and record the decision in the component registry.

## Non-goals

- Do not blindly import a complete third-party architecture.
- Do not make MediaHub Product dependent on a single external project.
- Do not treat stars, README claims, or popularity as security qualification.
- Do not copy code without license/provenance review.

## Required evidence

Every new component proposal must contain:

- GitHub prior-art search record;
- selected repositories and exact revisions/files where relevant;
- strengths and known weaknesses;
- license/provenance assessment;
- security and maintenance assessment;
- implementation decision;
- tests derived from prior art;
- explicit MediaHub-specific improvements.

## Architecture principle

MediaHub Product owns the contracts, authority, security boundary, routing policy, provenance, and fail-closed behavior. GitHub projects are an engineering corpus from which stable ideas and, where legally and technically appropriate, narrowly selected code patterns may be learned or incorporated.

## Current qualified corpus

Initial references include OmniRoute, Bifrost, LiteLLM, Codex, MCP SDKs, OPA, Firecracker, OpenTelemetry Collector, Cosign, Gitleaks, Semgrep, OSS-Fuzz, LangGraph, PydanticAI, and Renovate. The authoritative component registry is maintained separately and must be updated as the corpus evolves.
