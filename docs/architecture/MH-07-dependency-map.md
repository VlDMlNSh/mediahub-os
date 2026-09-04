# MH-7 — Dependency Map

Status: CANDIDATE

## Frozen dependencies
- P0-03 State Authority Contract v1.0 — sole canonical mutation authority.
- P0-04 In-Memory State Authority — current frozen implementation baseline.
- P0-05 Consumer/Integration Boundary — controlled consumer ingress.
- P0-06 Core Runtime Services — frozen runtime-services baseline.

## MH-7 dependencies
Configuration model, Policy model, validation, evaluation and authorization compose above P0-05 and P0-04. Runtime application consumes the resulting authorized representation.

## Non-dependency guarantees
MH-7 does not own physical persistence, alternate state authority, capability issuance, arbitrary execution or direct runtime mutation.

The P0-07→P0-05 authorization composition gap is an explicit governance blocker, not permission to modify frozen lower layers.
