# MH-06 — Health / Readiness

Status: ACCEPTED / GOVERNANCE ACCEPTED
ADR: `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md`
Implementation authorization: NO

## Semantic separation

Liveness is the ability of a process/service to perform its basic runtime loop. Health is observation. Readiness is an operation-scoped derived verdict. Neither health nor readiness implies trust, authorization, capability or mutation authority.

`P0-06 LifecycleState.READY != MH-06 Readiness.READY`.

## Health results

- UNKNOWN
- HEALTHY
- DEGRADED
- FAILED
- QUARANTINED

Health is bounded, immutable/value-semantic and observation-only. It cannot mutate canonical state, grant capability, grant authorization, establish trust, or create persistence authority.

## Readiness results

- UNKNOWN
- NOT_READY
- READY
- DEGRADED
- QUARANTINED

Readiness is evaluated as `Readiness(operation, observations) -> verdict`. UNKNOWN never becomes READY automatically. READY requires all mandatory prerequisites for the specified operation. DEGRADED is valid only where the operation contract explicitly permits degraded execution. QUARANTINED blocks normal-operation readiness.

## Bounded observations

The semantic input set is limited to lifecycle state/transition validity, runtime/service health, dependency health/classification, State Authority availability, generation tuple/compatibility, integrity result/reference, operation-relevant resource constraints, explicit operation requirements, supervision/quarantine state and bounded diagnostic observations. Unbounded external input is not readiness evidence merely because it is observable.

## Dependency rules

- CRITICAL: failure or UNKNOWN => NOT_READY.
- OPTIONAL: failure => DEGRADED only when the operation permits degradation; otherwise NOT_READY.
- FORBIDDEN / INCOMPATIBLE: => NOT_READY or QUARANTINED according to supervisory condition; never READY.
- UNKNOWN CLASSIFICATION: fail-closed => NOT_READY until explicitly classified.

## Precedence

1. QUARANTINED
2. invalid/incompatible generation or integrity
3. unavailable State Authority
4. lifecycle incompatible with operation
5. failed/unknown critical dependency
6. operation-specific resource constraint
7. optional dependency degradation
8. all required observations healthy

A positive liveness signal or P0-06 lifecycle READY cannot override a stronger negative condition.

## Lifecycle relation

P0-06 remains unchanged: PROVISIONING, INITIALIZING, SELF_TEST => NOT_READY; READY => candidate only; DEGRADED => READY or DEGRADED only when operation permits; SAFE_MODE/RECOVERY => NOT_READY for normal operations.

STOPPING, STOPPED, FAILED and QUARANTINED are not added to the P0-06 lifecycle by this decision.

## Quarantine

Quarantine is a supervisory/health condition. It does not become a P0-06 lifecycle state, acquire State Authority, issue capability, grant authorization, mutate canonical state, or automatically change P0-06 lifecycle. It blocks normal readiness. Entry/exit thresholds, attempt counts and detailed recovery transitions remain implementation/topology evidence questions and require explicit governance before becoming concrete runtime policy.

## Authority and security

P0-04 remains the sole canonical mutation authority. P0-05 remains the mandatory controlled consumer/integration boundary. The normal path remains:

Readiness → Authorization → P0-05 Consumer Boundary → P0-04 State Authority

Health ≠ Trust; Readiness ≠ Trust; Readiness ≠ Authorization; Readiness ≠ Capability; Liveness ≠ Trust.

## Governance

This semantic contract is GOVERNANCE ACCEPTED. This does not authorize implementation, testing claims, CI verification, deployment or production qualification. Any implementation requires a separate scoped implementation authorization.
