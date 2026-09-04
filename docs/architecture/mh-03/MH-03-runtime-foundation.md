# MH-03 Runtime Foundation

Status: PROPOSED. Parent chain: MH-01 → MH-02 → MH-03.

## Canonical invariants
- State Authority is the sole canonical mutation authority.
- Runtime coordinates lifecycle and execution; it is not State Authority.
- Current State Authority is in-memory; physical persistence is not authorized here.
- Core Runtime Services operate through the P0-05 Consumer/Integration Boundary.
- No second mutation path, shadow authority, or fallback state authority is permitted.
- Command is a request to change; Event is a fact that something happened.
- Observability is non-mutating.
- Single node / no HA remains inherited.

## Reference runtime
Bootstrap → configuration validation → trust context → State Authority → Core Runtime Services → dependencies → readiness → READY.

Runtime services are logical boundaries, not mandatory processes or containers. Technology choices remain CANDIDATE until evidence, compatibility, security and architecture decision.

## Failure
Malformed/ambiguous/unauthorized/stale requests are rejected or denied. Optional cloud/AI failures permit deterministic local degraded operation where possible. State Authority failure never creates a fallback mutation authority.

## Shutdown
Stop admission of new work → finish/cancel bounded operations → publish required facts/diagnostics → stop dependent services → stop Runtime.

## Status
MH-03 remains PROPOSED until the acceptance gate in `MH-03-acceptance-criteria.md` is passed and governance approval is recorded.
