# MH-06 — Dependency Model

Status: ACCEPTED for Health/Readiness semantics; full dependency graph remains unresolved.
ADR: `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md`

Dependencies must have explicit classification and bounded failure semantics. Relationship semantics include control and data dependencies. Dependency readiness does not imply authorization or trust.

## Readiness classification

- CRITICAL — failure or UNKNOWN means the operation is NOT_READY.
- OPTIONAL — failure yields DEGRADED only when the operation contract explicitly permits degraded execution; otherwise NOT_READY.
- FORBIDDEN / INCOMPATIBLE — yields NOT_READY or QUARANTINED according to supervisory condition; never READY.
- UNKNOWN CLASSIFICATION — fail-closed to NOT_READY until classification is explicitly established.

No optimistic dependency assumption is permitted.

## Aggregation precedence

1. QUARANTINED
2. invalid/incompatible generation or integrity
3. unavailable State Authority
4. lifecycle incompatible with operation
5. failed/unknown critical dependency
6. operation-specific resource constraint
7. optional dependency degradation
8. all required observations healthy

Critical dependency cycles require explicit ADR/evidence. The complete dependency graph, exact operation-to-dependency mapping and concrete resource policy remain UNKNOWN.

## Boundary

Dependency observation is non-authoritative. It cannot mutate canonical state, issue capability, grant authorization or bypass P0-05/P0-04.
