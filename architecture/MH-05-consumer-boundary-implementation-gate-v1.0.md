# MH-05 — Consumer Boundary Implementation Gate v1.0

**Status:** PROPOSED — IMPLEMENTATION NOT AUTHORIZED
**Owner:** Consumer / Integration Boundary
**Dependency:** MH-04 State Authority
**Contract dependency:** CTR-001 and applicable consumer-contract families

## 1. Purpose

Define the governance and verification gate required before implementing the system-wide Consumer / Integration Boundary that fronts the canonical State Authority.

This document does not authorize implementation, persistence, HA, production release, or any unrelated capability.

## 2. Required mutation path

All state-changing consumers MUST enter through:

`INPUT → CONSUMER BOUNDARY → AUTHORIZATION/POLICY → COMMAND → STATE AUTHORITY → CANONICAL STATE → EVENT → OBSERVATION → EVIDENCE`

The boundary MUST prevent direct mutation by UI, AI, cloud, plugin, device integration, automation, telemetry, health/readiness, cache, persistence/storage, recovery, or other observers.

## 3. Required properties

- explicit consumer/source identity;
- authenticated identity where required;
- authorization context;
- operation and target validation;
- deterministic command identity and correlation identity;
- contract selection and compatibility validation;
- deny-by-default behavior;
- fail-closed behavior when State Authority is unavailable;
- no shadow state authority;
- no direct canonical-state mutation API exposed to consumers;
- observational events cannot mutate state;
- event-triggered mutation must re-enter the governed command path;
- evidence must be attributable without becoming mutation authority.

## 4. Verification gate

Before implementation acceptance, evidence MUST demonstrate at minimum:

1. authorized command reaches exactly one canonical State Authority;
2. unauthorized consumer cannot mutate canonical state;
3. readiness/health/liveness cannot authorize mutation;
4. UI/AI/cloud/plugin/device/automation paths cannot bypass the boundary;
5. duplicate command handling is preserved;
6. stale-generation handling is preserved;
7. malformed commands are non-mutating;
8. State Authority outage is fail-closed;
9. event observers remain observational;
10. event-triggered mutation re-enters authorization and command validation;
11. source identity is preserved through the execution trace;
12. system-wide negative-path evidence is reproducible.

## 5. Acceptance dependencies

Implementation MUST STOP until the following are explicit and accepted for the relevant scope:

- canonical owner and interface contract;
- consumer contract registry mapping;
- invariant impact assessment;
- dependency readiness;
- security threat model and negative tests;
- persistence semantics where the consumer depends on durable state;
- recovery semantics where restart affects command processing;
- reproducible verification criteria;
- implementation authorization from the applicable governance authority.

## 6. Non-goals

This gate does not authorize:

- physical persistence;
- database/journal as canonical authority;
- HA or replication;
- cloud authority;
- production release;
- implementation of MH-06 or later domains;
- changes to frozen architecture decisions without a contradiction/governance process.

## 7. Current decision

**STOPPED / NOT AUTHORIZED.**

The current MH-04 implementation remains the accepted deterministic in-memory State Authority foundation. P0-05/MH-05 implementation requires explicit implementation authorization after contract, invariant, security, persistence-boundary and verification prerequisites are accepted.

**Production release: NOT AUTHORIZED.**
