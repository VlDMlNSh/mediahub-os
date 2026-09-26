# MH-05 — Consumer Boundary Implementation Readiness v1.0

**Status:** READY FOR GOVERNANCE REVIEW / IMPLEMENTATION NOT AUTHORIZED
**Owner:** `consumer_boundary`
**Dependency:** MH-04 State Authority / CTR-001

## Purpose

Define the exact implementation and qualification entry conditions for the single governed ingress to the canonical State Authority without changing MH-04 semantics.

## Required implementation invariants

1. There is exactly one canonical State Authority.
2. Consumer Boundary owns routing/validation only; it does not own canonical state.
3. Every mutation request has consumer/source identity and correlation identity.
4. Authorization is explicit and deny-by-default.
5. Presence, discovery, health, readiness, liveness, physical connection and network reachability never imply authorization.
6. Rejection is non-mutating.
7. Event-triggered mutations re-enter through the same governed command path.
8. UI, AI, plugin, device, cloud, telemetry, persistence and recovery cannot bypass the boundary.
9. Boundary uncertainty fails closed.
10. No persistence or recovery semantics are introduced by MH-05.

## Verification matrix

| ID | Requirement | Evidence required | Current status |
|---|---|---|---|
| MH05-V01 | Positive governed ingress | executed runtime test + SHA | NOT_STARTED |
| MH05-V02 | Missing identity rejected | executed negative test | NOT_STARTED |
| MH05-V03 | Missing authorization rejected | executed negative test | NOT_STARTED |
| MH05-V04 | Forged source identity rejected | executed negative test | NOT_STARTED |
| MH05-V05 | Readiness/health cannot authorize | executed negative test | NOT_STARTED |
| MH05-V06 | Direct State Authority bypass rejected | executed negative test | NOT_STARTED |
| MH05-V07 | Event re-entry enforced | executed runtime test | NOT_STARTED |
| MH05-V08 | Consumer cannot become shadow authority | executed architectural/runtime test | NOT_STARTED |
| MH05-V09 | Remote access cannot elevate privilege | executed security test | NOT_STARTED |
| MH05-V10 | Rejection is non-mutating | executed state/evidence comparison | NOT_STARTED |
| MH05-V11 | Fail-closed uncertainty | executed failure test | NOT_STARTED |
| MH05-V12 | Persistence/recovery remain outside scope | static contract test | READY |

## Implementation boundary

The implementation must delegate accepted commands to the existing MH-04 State Authority. It must not duplicate generation, canonical state, event sequencing, persistence, checkpoint authority, or recovery authority.

## Qualification rule

`TEST_EXISTS` is not `TESTED`. `TESTED` is not `QUALIFIED`. Qualification requires current-SHA execution, attributable evidence, independent security review, and governance acceptance.

## Explicit blockers

- MH-05 implementation authorization is not recorded.
- System-wide negative verification cannot be claimed before the consumer surfaces exist.
- Persistence and restart recovery remain separate future scopes.
- Production release remains unauthorized.
