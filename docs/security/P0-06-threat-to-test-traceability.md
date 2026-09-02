# P0-06 — Threat-to-Test Traceability v1.0

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED
**Depends on:** P0-06 Threat Model v1.0; P0-06 Service Contract v1.0

## Verification rule

Every P0-06 security threat MUST have a defined verification path. A threat without verification evidence remains open.

## Traceability matrix

| Threat | Control | Verification |
|---|---|---|
| P06-T01 | CRT-002 | Static boundary scan + negative test |
| P06-T02 | CRT-001 | Architecture/code inspection |
| P06-T03 | CRT-003 | Authorization negative tests |
| P06-T04 | CRT-004 | Lifecycle transition matrix tests |
| P06-T05 | CRT-005 | Failure-injection tests |
| P06-T06 | Freshness/generation preservation | Stale-generation negative tests |
| P06-T07 | No implicit rebase | Concurrent transaction tests |
| P06-T08 | CRT-006 | API inspection + negative capability test |
| P06-T09 | CRT-006 | API inspection + negative capability test |
| P06-T10 | CRT-009 | Diagnostic sanitization tests |
| P06-T11 | CRT-008 | Boundary/resource-limit tests |
| P06-T12 | CRT-008 | Mutation-after-return tests |
| P06-T13 | Inert AI proposal | API inspection + forbidden-call scan |
| P06-T14 | Capability-scoped authorization | Capability negative tests |
| P06-T15 | CRT-007 | Forbidden import/call scan |
| P06-T16 | CRT-007 | Forbidden import/call scan |
| P06-T17 | CRT-007 | Forbidden API scan + negative tests |
| P06-T18 | CRT-010 | Persistence/import/path scan |
| P06-T19 | CRT-009 | Sanitized-error tests |
| P06-T20 | CRT-005 | Failure-injection + state-integrity tests |

## Required implementation test surface

The implementation SHOULD provide focused tests for lifecycle service, runtime coordination, health/readiness, diagnostics, security boundaries, and common service boundaries. Exact filenames are implementation details and are not architecture requirements.

## Static scans

Implementation acceptance MUST inspect for forbidden capabilities including subprocess/shell execution, network mutation/transport, filesystem mutation, persistence/database paths, unsafe deserialization, dynamic execution, and direct State Authority mutation.

Scan results MUST distinguish implementation capabilities from intentional strings in documentation and hostile test fixtures.

## Acceptance evidence

Required evidence:

- exact implementation commit;
- targeted tests;
- full regression;
- negative security tests;
- forbidden capability scan;
- persistence scan;
- API/capability inspection;
- clean working tree;
- synchronized remote state.

All required evidence must pass before implementation can be frozen.
