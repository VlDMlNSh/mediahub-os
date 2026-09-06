# MH-04 — State Authority Contract v1.0

**Status:** ACCEPTED FOR AUTHORIZED IN-MEMORY SCOPE  
**Owner:** `state_authority`  
**Contract:** CTR-001  
**Purpose:** make the canonical State Authority semantics executable and reviewable.

## 1. Scope

State Authority is the sole canonical mutation authority for MediaHub state. This contract defines the semantic boundary between governed commands, canonical state mutation, events, observation, and evidence.

This acceptance applies only to the current deterministic in-memory foundation. It does **not** authorize physical persistence, HA, production release, or unrelated capability implementation.

## 2. Canonical mutation path

`INPUT → BOUNDARY → AUTHORIZATION/POLICY → COMMAND → CONSUMER CONTRACT → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

A proposal, recommendation, telemetry observation, health result, readiness result, cache value, database record, AI output, cloud result, plugin request, or device report is not canonical mutation authority.

## 3. Command contract

Every state-changing request MUST have command identity, correlation identity, source/consumer identity, authenticated identity where required, authorization context, target canonical entity/function, requested operation, applicable concurrency context, and deterministic validation.

Malformed, ambiguous, unauthenticated, unauthorized, stale, incompatible, or quarantined requests MUST be rejected without canonical mutation.

## 4. State transition contract

Rejected transitions MUST leave canonical state unchanged. Legal transitions, invariants, version semantics and failure behavior remain domain-specific contract requirements.

## 5. Concurrency and ordering

The in-memory foundation uses serialized atomic publication under its authority lock and generation checks for stale writers. Concurrent same-generation writers are deterministic: one commits and later stale writers are rejected without mutation or event emission.

## 6. Idempotency

Command identity is the idempotency identity for the current foundation. A previously accepted command ID is rejected as a duplicate and MUST NOT create a second state transition or event. Retry semantics beyond this reject behavior require future contract qualification.

## 7. Atomicity and failure

Mutation is prepared against a detached candidate state and published atomically. Validation, authorization, stale-generation and authority-availability failures occur before publication. If State Authority cannot safely determine or commit a transition, it MUST fail closed.

## 8. Event contract

A successful canonical mutation produces an observational event containing command/correlation identity and canonical generation/version. Events MUST NOT themselves be mutation authority. Event-triggered changes MUST re-enter the governed command path.

Observer failures do not roll back an already-published canonical mutation; delivery/error semantics require separate event-system qualification.

## 9. Persistence boundary

CTR-001 requires persistence semantics, but current MH-03 freezes this foundation as in-memory. No database, cache, journal, filesystem, cloud store, or replica may become a second canonical authority without separate accepted architecture/contract authorization.

## 10. Restart and recovery

The current in-memory foundation does not provide process-restart durability. Recovery cannot silently reconstruct canonical authority from an unqualified source. Durable restart/recovery remains a future authorized scope.

## 11. Offline-first

The deterministic local State Authority semantics do not require cloud, external AI, RAG, paid APIs, or Internet connectivity.

## 12. Security boundary

The State Authority trusts only governed authorization context. Discovery, physical connection, presence, health, readiness, liveness, or network reachability MUST NOT be treated as authorization. Remote access MUST NOT increase authorization.

## 13. Evidence requirements

Qualification evidence must preserve command/correlation identity, authorization decision, validation result, pre/post state and versions, mutation result, emitted event/causality, rejection/failure reason, duplicate handling, and recovery behavior where applicable.

Evidence collection is observational and MUST NOT mutate canonical state.

## 14. Required negative properties

Verification must demonstrate absence of unauthorized mutation paths across UI, AI, cloud, plugin, device integration, automation/event reaction, telemetry, health/readiness, cache, persistence/storage and recovery boundaries. Current package-level security tests cover only the implemented foundation surface; system-wide negative verification remains open.

## 15. Acceptance status

This contract is **ACCEPTED FOR THE AUTHORIZED IN-MEMORY SCOPE** under `governance/MEDIAHUB-ARCHITECTURE-ACCEPTANCE-2026-09-06.md`.

**Production release: NOT AUTHORIZED.**
**Physical persistence / HA: NOT AUTHORIZED.**
**Architecture freeze: NOT REQUESTED.**
