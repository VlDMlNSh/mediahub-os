# MH-04 — State Authority Contract v1.0

**Status:** PROPOSED / NOT ACCEPTED  
**Owner:** `state_authority`  
**Contract:** CTR-001  
**Purpose:** make the canonical State Authority semantics executable and reviewable without granting production implementation authorization.

## 1. Scope

State Authority is the sole canonical mutation authority for MediaHub state. This contract defines the semantic boundary between governed commands, canonical state mutation, events, observation, and evidence.

This document does **not** authorize production implementation, persistence, HA, or a technology-specific architecture.

## 2. Canonical mutation path

`INPUT → BOUNDARY → AUTHORIZATION/POLICY → COMMAND → CONSUMER CONTRACT → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

A proposal, recommendation, telemetry observation, health result, readiness result, cache value, database record, AI output, cloud result, plugin request, or device report is not canonical mutation authority.

## 3. Command contract

Every state-changing request MUST have:

- command identity;
- correlation identity;
- source/consumer identity;
- authenticated identity where required;
- authorization context;
- target canonical entity/function;
- requested operation;
- expected/current-version or equivalent concurrency context where applicable;
- deterministic validation result;
- explicit lifecycle and expiry semantics where applicable.

Malformed, ambiguous, unauthenticated, unauthorized, stale, incompatible, or quarantined requests MUST be rejected without canonical mutation.

## 4. State transition contract

For each canonical state field/domain the implementation specification MUST define:

- owner;
- admissible values/types;
- legal transitions;
- illegal transitions;
- preconditions;
- postconditions;
- invariant checks;
- version/concurrency semantics;
- failure semantics.

A rejected transition MUST leave canonical state unchanged.

## 5. Concurrency and ordering

The implementation MUST provide a deterministic, testable policy for:

- concurrent commands targeting the same state;
- stale command detection;
- ordering/correlation;
- conflict classification;
- retry behavior;
- duplicate command handling.

The specific concurrency technology remains a candidate until architecture/governance acceptance.

## 6. Idempotency

Commands classified as retryable MUST define an idempotency identity and duplicate semantics. A duplicate MUST NOT create an unintended additional state transition or duplicate externally visible side effect.

Idempotency does not authorize bypassing validation or authorization.

## 7. Atomicity and failure

Each mutation operation MUST define its atomicity boundary. Partial failure MUST NOT silently produce an invalid canonical state.

If the State Authority cannot safely determine or commit the requested transition, it MUST fail closed and report a deterministic failure/evidence state rather than delegating authority to another component.

## 8. Event contract

A successful canonical mutation produces an event according to the event contract. Events MUST represent facts about accepted canonical state changes; they MUST NOT themselves be mutation authority.

Event-triggered changes MUST re-enter the governed command path.

The event MUST preserve enough identity/correlation/causality information to reconstruct the command-to-mutation-to-event trace.

## 9. Persistence boundary

CTR-001 requires persistence semantics, but the current MH-03 foundation freezes the current State Authority as in-memory and does not authorize physical persistence. Therefore this contract defines the **semantic boundary only**.

No database, cache, journal, filesystem, cloud store, or replica may become a second canonical authority without an explicit accepted architecture decision and contract update.

## 10. Restart and recovery

After restart/recovery the system MUST re-establish a valid lifecycle state before accepting mutations. Recovery MUST NOT create a shadow authority or silently reconstruct authority from an unqualified source.

If canonical authority cannot be safely established, mutation MUST remain stopped.

## 11. Offline-first

The deterministic local core MUST NOT require cloud, external AI, RAG, paid APIs, or Internet connectivity for its core state-authority semantics.

Loss of optional cloud/AI dependencies MUST NOT grant them authority and MUST NOT automatically invalidate safe local deterministic operation.

## 12. Security boundary

The State Authority trusts only governed authorization context. Discovery, physical connection, presence, health, readiness, liveness, or network reachability MUST NOT be treated as authorization.

Remote access MUST NOT increase authorization.

## 13. Evidence requirements

A qualified implementation must be able to produce evidence for at least:

1. accepted command identity and correlation;
2. authorization decision;
3. validation result;
4. pre-state/version;
5. canonical mutation result;
6. post-state/version;
7. emitted event and causality;
8. rejection/failure reason where applicable;
9. duplicate/retry handling;
10. recovery/non-mutating behavior.

Evidence collection is observational and MUST NOT mutate canonical state.

## 14. Required negative properties

Verification MUST demonstrate absence of unauthorized mutation paths for at least:

- UI;
- AI;
- cloud;
- plugin;
- device integration;
- automation/event reaction;
- telemetry;
- health/readiness;
- cache;
- persistence/storage;
- recovery subsystem.

## 15. Acceptance status

This contract is **PROPOSED / NOT ACCEPTED**. Acceptance requires governance review, compatibility with frozen P0-03/P0-04/P0-05/P0-06 semantics, executable verification criteria, contradiction review, and explicit acceptance authority.

**Implementation authorization remains BLOCKED.**
