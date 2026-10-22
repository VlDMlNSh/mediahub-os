# MH-04 — State Authority Implementation Gate

**Status:** PROPOSED / NOT ACCEPTED
**Purpose:** materialize the State Authority implementation gate without granting production authorization.

## 1. Canonical authority

State Authority is the sole canonical mutation authority. Runtime, UI, AI, plugins, integrations, cloud services, telemetry, health/readiness and recovery components MUST NOT maintain or mutate a shadow canonical state.

## 2. Governed mutation path

`INPUT → BOUNDARY → AUTHORIZATION/POLICY → COMMAND → CONSUMER CONTRACT → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

A proposal/recommendation is not a command. An event is a fact, not a mutation request. Any event-driven mutation MUST re-enter the governed command path.

## 3. Required State Authority semantics

Before implementation authorization, the following must be explicitly specified and verified:

- canonical state model and ownership;
- valid state transitions and rejection semantics;
- command identity and correlation identity;
- authorization context propagation;
- optimistic/concurrency semantics;
- ordering guarantees;
- idempotency and duplicate-command handling;
- conflict detection and resolution;
- atomicity boundary;
- event emission semantics;
- failure and partial-failure behavior;
- restart/recovery behavior;
- degraded/non-mutating behavior when State Authority is unavailable;
- persistence boundary, if and when separately authorized;
- migration/version compatibility;
- audit/evidence requirements.

## 4. Non-negotiable invariants

- Discovery does not imply trust.
- Presence does not imply authentication.
- Authentication does not imply authorization.
- Physical connection does not imply authorization.
- Health/readiness/liveness do not grant authorization.
- Remote access does not increase authorization.
- Cloud does not become canonical authority.
- Persistence does not become a hidden authority.
- Recovery does not create a fallback authority.
- Cache does not become canonical state.

## 5. Implementation boundary

This gate authorizes **no production implementation by itself**. It is an engineering/governance artifact used to make the remaining authorization evidence explicit.

A production implementation may begin only after:

1. Master Architecture acceptance;
2. MH-03 acceptance where applicable;
3. MH-04 contract approval;
4. all architecture-impacting decisions are explicitly accepted;
5. verification criteria are executable;
6. implementation authorization is explicitly recorded.

## 6. Verification matrix

| Area | Required evidence | Status |
|---|---|---|
| State transitions | executable positive/negative tests | NOT VERIFIED |
| Authorization boundary | deny/allow tests for every consumer class | NOT VERIFIED |
| Concurrency | race/conflict tests | NOT VERIFIED |
| Idempotency | duplicate/retry tests | NOT VERIFIED |
| Ordering | deterministic ordering tests | NOT VERIFIED |
| Event semantics | command→mutation→event trace | NOT VERIFIED |
| Failure | State Authority failure tests | NOT VERIFIED |
| Recovery | restart/recovery evidence | NOT VERIFIED |
| Offline-first | no-cloud deterministic tests | NOT VERIFIED |
| Persistence | separately authorized durability evidence | NOT VERIFIED |
| Security | authenticated/authorized mutation evidence | NOT VERIFIED |
| CI | reproducible workflow evidence | NOT VERIFIED |

## 7. Current gate result

**IMPLEMENTATION AUTHORIZATION: BLOCKED**

Reason: the canonical architecture is still DRAFT/NOT ACCEPTED and the required implementation evidence does not yet exist. This document MUST NOT be interpreted as acceptance or production authorization.
