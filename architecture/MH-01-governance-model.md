# MH-01 Governance Model

Status: PROPOSED / REQUIRES VERIFICATION.

## Authority layers

1. Frozen foundation: P0-03…P0-06. Downstream MH cannot override it.
2. MH-01/governance: product mission, global principles, authority, safety hierarchy, cross-MH invariants and change policy.
3. Domain MH: domain architecture within MH-01 constraints.
4. Development: implementation only after architecture/implementation authorization.
5. Verification: evidence that implementation meets requirements.
6. Governance acceptance: formal acceptance.
7. Freeze: explicit stabilization point.

## Decision ownership

MH-01/governance owns global authority, safety, product scope, cross-domain constraints and change-control semantics. Domain decisions may be delegated only when they do not alter global authority/security/safety invariants.

## Required separation

Architecture chats are canonical architecture custodians, not development workspaces. Development chats are execution workspaces. Development findings return through a Reverse Master Prompt/evidence package. No development chat can silently promote an observation to architecture.

## Acceptance distinction

`IMPLEMENTED` ≠ `TESTED` ≠ `ACCEPTED` ≠ `FROZEN`.

Production qualification is a separate gate and is not implied by architecture acceptance.

## Frozen-contract changes

Any change to P0-03, P0-04, P0-05 or P0-06 requires a separate governance change record, impact analysis, verification plan and explicit acceptance. MH-01 does not silently amend these contracts.

## Evidence hierarchy

Repository evidence and explicit accepted decisions outrank recollection, draft notes, benchmarks, marketing claims, external examples or inferred mappings. Unknown remains Unknown until evidence changes its status.