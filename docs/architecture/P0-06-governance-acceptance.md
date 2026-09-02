# P0-06 — Governance Acceptance v1.1

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED

## Scope

This acceptance reconfirms the P0-06 Core Runtime Services architecture and implementation entry gate after clarification of authoritative lifecycle state handling.

It supersedes the prior P0-06 governance acceptance only with respect to the P0-06 service contract version and lifecycle-state contract explicitly named below. P0-04 and P0-05 remain ACCEPTED / FROZEN and are not modified.

## Accepted baseline

- P0-04 State Authority: ACCEPTED / FROZEN.
- P0-05 Consumer Boundary: ACCEPTED / FROZEN.
- P0-06 architecture boundary: ACCEPTED.
- P0-06 service contract: v1.1 ACCEPTED.
- P0-06 lifecycle state contract: v1.0 ACCEPTED.
- P0-06 threat model: ACCEPTED.
- P0-06 threat-to-test traceability: ACCEPTED.
- P0-06 implementation entry gate: ACCEPTED.
- P0-06 governance decision packet: ACCEPTED.

## Lifecycle clarification

The authoritative lifecycle state is represented inside P0-04 State Authority state as the bounded lifecycle field defined by the accepted lifecycle state contract.

The existing `LifecycleStateMachine` is a deterministic transition validator/compatibility primitive only. Its mutable local state is not authoritative and must not be used as a publication source.

Lifecycle publication must follow:

```text
Lifecycle request
      |
      v
P0-05 Consumer Boundary
      |
      v
P0-04 State Authority
```

The accepted lifecycle transition relation is closed, deterministic, and fail-closed. Invalid, stale, unauthorized, or otherwise rejected transitions must not partially publish state.

## Acceptance findings

1. P0-06 preserves P0-04 as the sole canonical mutation authority.
2. P0-06 preserves P0-05 as the mandatory consumer authorization/integration boundary.
3. Lifecycle state has an explicit bounded schema and deterministic transition relation.
4. Local lifecycle validation does not create a second canonical lifecycle store.
5. Health/readiness and diagnostics remain observation-oriented and bounded.
6. AI proposals remain inert until explicit authorization.
7. Plugin interaction remains capability-scoped; the full plugin subsystem is not authorized.
8. Stale/freshness and generation semantics remain inherited from P0-04/P0-05.
9. Persistence and external execution capabilities remain excluded.
10. Required security threats retain explicit verification paths.
11. The clarified contract does not modify P0-04/P0-05 semantics.
12. Controlled implementation is authorized within this exact scope.

## Lifecycle authorization capability

The lifecycle service MUST require an explicit capability identified as:

`runtime.lifecycle.transition`

Possession of this capability does not bypass P0-05 authorization. The request remains subject to the existing explicit authorization policy and State Authority transaction semantics.

## Decision

**IMPLEMENTATION AUTHORIZED.**

Authorization is limited to the exact accepted P0-06 documents and exclusions. Any authority-boundary change, persistence introduction, external execution, network/filesystem mutation, autonomous AI mutation, or P0-04/P0-05 semantic change requires a new governance decision.

## Implementation acceptance remains separate

This document does not approve implementation quality. After implementation, a separate P0-06 implementation acceptance must establish targeted tests, full regression, negative security evidence, capability scans, persistence scans, exact commit identity, clean state, and remote synchronization.

## Production status

**PRODUCTION QUALIFICATION: NOT GRANTED.**
