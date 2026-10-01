# MH-25 — Dual Local Executor Blueprint 1.0

Status: IMPLEMENTATION DEFINED / RUNTIME LAUNCH BLOCKED
Date: 2026-10-02
Scope: CODEX_LOCAL + CLAUDE_LOCAL provider backends for Astra

## Objective
Provide two independent local executor providers under one Astra orchestration contract.

## Topology
A0 Astra -> provider adapter -> local executor process
                         -> A3 independent verifier

Providers:
- CODEX_LOCAL
- CLAUDE_LOCAL

## Invariants
- Provider is executor-only; no MediaHub authority.
- Each task has exactly one claim owner.
- Concurrent execution requires disjoint claims and isolated workspaces.
- Shared contracts, generated outputs, release metadata and authority surfaces are serialized.
- Missing provider runtime is BLOCKED, never silently replaced.
- Non-zero exit is FAILED.
- Timeout is FAILED.
- Malformed result is REJECTED.
- Credentials are never created or exposed by the fabric.
- Historical execution evidence cannot qualify a new provider build.

## Provider configuration
Canonical provider IDs:
- CODEX_LOCAL
- CLAUDE_LOCAL

Environment bindings:
- MEDIAHUB_CODEX_EXECUTOR
- MEDIAHUB_CLAUDE_EXECUTOR

Defaults are provider-local CLI names only; actual availability must be proven on the target node.

## Launch protocol
1. Astra creates two disjoint tasks.
2. ClaimStore records independent claims.
3. Each provider receives only its own task/workspace.
4. Both processes may start concurrently.
5. Each emits an executor result.
6. A3 verifies each result independently.
7. Commit/evidence/manifest are recorded only after verification.
8. Any provider absence blocks that provider without affecting authority or fabric state.

## Current truth
- Codex Tasks service exposes 0 registered execution environments.
- No Claude/Anthropic executor endpoint is exposed in the current tool inventory.
- Therefore this chat cannot truthfully report a successful local dual-process launch.
- The configuration has been created on branch `astra/dual-local-executors-20261002`, but runtime qualification and launch remain blocked pending an accessible local execution environment with both provider runtimes installed.

## Qualification gates
D1 provider identity
D2 local binary/runtime availability
D3 isolated workspace execution
D4 concurrent disjoint-task execution
D5 timeout/failure handling
D6 result contract
D7 independent A3 verification
D8 evidence chain
D9 restart/recovery
D10 exact-SHA qualification

No promotion to GOLD before D1-D10 PASS.
