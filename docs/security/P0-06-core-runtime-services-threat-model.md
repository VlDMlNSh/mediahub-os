# P0-06 — Core Runtime Services Threat Model v1.0

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED
**Depends on:** P0-06 Core Runtime Services Boundary v1.0; P0-06 Service Contract v1.0

## Security boundary

```text
External / UI / AI / Plugin inputs
              |
              v
     Core Runtime Services
              |
              v
       P0-05 Consumer Boundary
              |
              v
       P0-04 State Authority
```

## Threats and required controls

| ID | Threat | Required control |
|---|---|---|
| P06-T01 | Service bypasses P0-05 | CRT-002; mandatory delegation path |
| P06-T02 | Service creates second canonical state | CRT-001; no service-owned canonical store |
| P06-T03 | Service self-grants capability | CRT-003; explicit authorization/default deny |
| P06-T04 | Invalid lifecycle transition | CRT-004; deterministic transition validation |
| P06-T05 | Partial lifecycle transition | CRT-005; atomic/fail-closed publication |
| P06-T06 | Stale transaction accepted | P0-04/P0-05 freshness and generation checks |
| P06-T07 | Implicit rebase or last-writer-wins | Explicit prohibition; preserve stale rejection |
| P06-T08 | Health API gains mutation capability | CRT-006; observation-only contract |
| P06-T09 | Diagnostics gain mutation capability | CRT-006; observation-only integration |
| P06-T10 | Diagnostic information leakage | CRT-009; existing sanitization boundary |
| P06-T11 | Oversized/malformed request | CRT-008; structural and size bounds |
| P06-T12 | Mutable alias escapes service boundary | CRT-008; value-semantic/immutable results |
| P06-T13 | AI proposal becomes executable | Inert proposal contract; no execution primitive |
| P06-T14 | Plugin capability escalation | Explicit capability-scoped authorization |
| P06-T15 | Arbitrary execution | No subprocess/shell/arbitrary execution capability |
| P06-T16 | Network side effect | No network capability in P0-06 |
| P06-T17 | Filesystem mutation | No arbitrary filesystem mutation |
| P06-T18 | Implicit persistence | CRT-010; no durable storage |
| P06-T19 | Error leaks internal information | CRT-009; sanitized stable errors |
| P06-T20 | Service failure corrupts canonical state | CRT-005; failure preservation tests |

## Security invariants

- **CRT-001 Single state authority**
- **CRT-002 Boundary preservation**
- **CRT-003 Default deny**
- **CRT-004 Lifecycle determinism**
- **CRT-005 Failure preservation**
- **CRT-006 Observation isolation**
- **CRT-007 No implicit execution**
- **CRT-008 Bounded inputs/outputs**
- **CRT-009 Sanitized failures**
- **CRT-010 Persistence exclusion**

## Negative-security requirements

Implementation MUST include negative verification for authority bypass, authorization bypass, stale operations, invalid lifecycle transitions, failure preservation, mutable aliases, oversized/malformed inputs, diagnostic leakage, AI execution paths, plugin capability expansion, arbitrary execution, network/filesystem access, and persistence.

## Stop conditions

Discovery of a direct State Authority mutation path, capability escalation, autonomous AI execution, persistence, network/external execution, or semantic change to P0-04/P0-05 immediately invalidates the P0-06 authorization and requires governance review.
