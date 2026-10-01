# MH-25 — Dual Local Executor GitHub Transport Control Blueprint 1.0

Status: IMPLEMENTED / RUNTIME QUALIFICATION BLOCKED

## Objective

GitHub is the durable control/evidence transport for Astra. Local execution remains on mh-dev-01. GitHub commands must describe desired state; the local controller reconciles desired state into bounded executor processes.

## Control operations

Machine-readable operations:

- START — request a bounded executor session.
- STOP — request termination of an owned session.
- STATUS — report provider/session/claim/lease/target-SHA state.
- RECONCILE — reconcile unknown/interrupted outcomes.
- RUN — execute one claimed task.
- VERIFY — request independent A3 verification.
- CANCEL — invalidate an unstarted task claim.

## Provider identities

- CODEX_LOCAL → `MEDIAHUB_CODEX_EXECUTOR`, default `codex`
- CLAUDE_LOCAL → `MEDIAHUB_CLAUDE_EXECUTOR`, default `claude`

Provider selection is allowlisted and never inferred from model names.

## Mandatory fencing

Every execution carries:

`task_id + claim_id + owner_id + generation + target_sha + provider + workspace`

A result is accepted only when all identities match the current durable GitHub task state.

## GitHub Transport

GitHub carries:

`TASK → CLAIM → DISPATCH → WORKER → RESULT → VERIFY → EVIDENCE → COMMIT`

GitHub does not execute the local provider itself.

## Local control

The local controller owns:

- CLI discovery
- isolated worktree creation
- bounded subprocess launch
- timeout and process-group termination
- stdout/result bounds
- provider failure classification
- evidence emission
- recovery/reconciliation

## Concurrency

Maximum two local executors. Concurrent execution is allowed only for disjoint claims and isolated worktrees. Shared files/contracts/release metadata remain serialized.

## Provider failure

Missing binary, authentication failure, policy denial, malformed output, timeout, or transport uncertainty produces BLOCKED/FAILED/RECONCILIATION_REQUIRED. It never fabricates a result.

## Operator controls

No secret values are stored in GitHub task payloads. START/STOP/STATUS/RECONCILE are control intents only. Credentials remain broker-owned on the execution node.

## Qualification gates

D1 identity
D2 executable/provider availability
D3 isolated execution
D4 concurrent disjoint execution
D5 failure/timeout
D6 result contract
D7 independent verification
D8 evidence chain
D9 restart/recovery
D10 exact-SHA qualification

Current state: D1 PASS; D2 PARTIAL; D3-D10 blocked or gated by D2/runtime wiring.

## Hard prohibitions

No credential creation/exposure, quota bypass, production authorization, State Authority mutation, force-push, rebase, reset, history rewrite, or historical-SHA promotion.
