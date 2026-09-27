# MH-04 — State Authority Implementation Gate

**Status:** ACCEPTED FOR AUTHORIZED IN-MEMORY IMPLEMENTATION / QUALIFICATION OPEN
**Purpose:** record the accepted implementation scope and preserve the separation between implementation authorization, qualification, persistence authorization, and production release.

## 1. Governance state

Master Architecture, MH-01, MH-03 and MH-04 have been accepted for the authorized scope. Explicit implementation authorization is recorded for the **in-memory State Authority foundation only**.

This gate does not authorize physical persistence, HA/failover, production release, or any capability outside the accepted MH-04 scope.

## 2. Canonical authority

State Authority is the sole canonical mutation authority. Runtime, UI, AI, plugins, integrations, cloud services, telemetry, health/readiness and recovery components MUST NOT maintain or mutate a shadow canonical state.

## 3. Governed mutation path

`INPUT → BOUNDARY → AUTHORIZATION/POLICY → COMMAND → CONSUMER CONTRACT → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

A proposal/recommendation is not a command. An event is a fact, not a mutation request. Any event-driven mutation MUST re-enter the governed command path.

## 4. Accepted in-memory semantics

The authorized implementation scope includes:

- command and correlation identity;
- source identity attribution;
- authenticated authorization context;
- deny-by-default mutation authorization;
- optimistic generation conflict detection;
- atomic candidate-state publication;
- deterministic canonical state digest;
- duplicate command rejection;
- event emission after canonical mutation;
- observational event delivery;
- fail-closed behavior when State Authority is unavailable;
- immutable read/checkpoint boundaries;
- checkpoint authority-token validation;
- concurrency conflict protection.

## 5. Explicitly outside this authorization

- physical persistence and durability;
- HA/failover State Authority;
- restart durability qualification;
- production release;
- system-wide Consumer Boundary qualification;
- full MediaHub capability qualification.

These remain separately governed work and must not be inferred from this implementation gate.

## 6. Verification status

| Area | Current status |
|---|---|
| State transitions | TESTED |
| Authorization boundary | TESTED |
| Concurrency | TESTED |
| Duplicate handling | TESTED |
| Event semantics | TESTED |
| Failure / unavailable authority | TESTED |
| Offline-first local execution | TESTED |
| Security negative suite | TESTED on recorded execution |
| Deterministic digest / source identity hardening | TESTED on recorded execution |
| Restart/recovery durability | NOT VERIFIED |
| Physical persistence | BLOCKED BY SCOPE |
| System-wide Consumer Boundary | NOT VERIFIED |
| Full V-01…V-15 qualification | OPEN |

## 7. Current gate result

**IMPLEMENTATION AUTHORIZATION: AUTHORIZED FOR IN-MEMORY SCOPE**

**QUALIFICATION: OPEN / REVIEW REQUIRED**

**PERSISTENCE AUTHORIZATION: NOT GRANTED**

**PRODUCTION RELEASE AUTHORIZATION: NOT GRANTED**

This document records governance state; it does not self-grant acceptance, qualification, or production authorization.