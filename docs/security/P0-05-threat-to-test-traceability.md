# P0-05 — Threat-to-Test Traceability v1.0

## Status

DRAFT — GOVERNANCE REVIEW REQUIRED

This is an architecture/security traceability artifact. It does not constitute execution evidence or governance acceptance.

## Threat classes

| ID | Threat | Required control | Verification intent |
|---|---|---|---|
| P05-T01 | Consumer bypasses State Authority | Single mutation authority | Static/API inspection + negative test |
| P05-T02 | Mutable alias modifies canonical state | Immutable read boundary | Mutation-attempt negative test |
| P05-T03 | Consumer self-grants authorization | Default-deny authorization | Unauthorized operation test |
| P05-T04 | Stale consumer overwrites newer revision | Generation/version binding | Concurrent/stale transaction test |
| P05-T05 | AI proposal becomes executable authority | Inert proposal boundary | Capability/API inspection + negative test |
| P05-T06 | Plugin obtains broader capability than granted | Capability scoping | Authorization matrix + negative test |
| P05-T07 | Invalid external input reaches expensive/unsafe path | Bounds + validation | Malformed/oversized input tests |
| P05-T08 | Failure leaks sensitive internals | Sanitized error boundary | Error-output privacy tests |
| P05-T09 | Diagnostics become mutation channel | Observation-only boundary | API inspection + mutation negative test |
| P05-T10 | Integration introduces hidden execution/network/fs side effect | Capability prohibition | Static capability scan + negative tests |
| P05-T11 | Personal data crosses boundary unnecessarily | Minimization/classification | Privacy negative tests + data-flow review |
| P05-T12 | Future persistence becomes implicit through adapter interface | Inactive durable boundary | API/source inspection |

## Traceability rule

A control is execution-backed only when the corresponding test or inspection has run successfully against the exact reviewed commit. Architecture intent alone is never treated as evidence.

## Required evidence before implementation acceptance

- targeted P0-05 consumer-boundary tests;
- full repository regression;
- authorization negative-path coverage;
- immutable-read and candidate-isolation tests;
- AI/plugin capability negative tests;
- malformed/oversized input tests;
- sanitized error/privacy tests;
- prohibited-capability scan;
- exact commit identity;
- clean/synchronized repository state;
- explicit unresolved-risk disposition.

## Governance boundary

P0-04 remains accepted/frozen. P0-05 does not authorize persistence. SQLite/ZFS/filesystem, network mutation, subprocess execution, appliance integration, installer/recovery, update engine, cloud/hardware persistence, and production qualification remain excluded.
