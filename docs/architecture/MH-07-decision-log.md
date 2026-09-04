# MH-7 Decision Log

Status: CANDIDATE — governance decisions pending

## D-01 — Separation of concerns
Configuration = desired behavior; Policy = admissibility conditions; Authorization = principal right; Runtime State = observed/effective state. P0-04 remains sole mutation authority.

Status: CANDIDATE.

## D-02 — Device-local v1
Configuration and policy scope remain device-local. Tenant, organization, project, fleet and cloud-canonical scopes are deferred.

Status: CANDIDATE.

## D-03 — Fail closed
Malformed, unsupported, ambiguous, conflicting and stale policy/configuration operations do not apply.

Status: CANDIDATE.

## D-04 — No implicit conflict resolution
No priority, inheritance, merge, LWW, hidden retry or rebase. Any precedence system requires a separate ADR and governance approval.

Status: CANDIDATE.

## D-05 — Persistence neutrality
Physical persistence is not authorized by MH-7. Future storage requires separate technology/security/compatibility review.

Status: CANDIDATE.

## D-06 — P0-07 mutation bridge
Three candidates remain open: existing independently authorized context; explicit governance-approved authorization bridge; revised P0-05 contract. P0-07 code must not invent a mapping.

Status: BLOCKED / REQUIRES GOVERNANCE DECISION.

## ADR candidates
- P0-07/P0-05 authorization composition.
- Configuration publication and authoritative-source contract.
- Policy mode transition authority.
- Critical-operation policy and audit contract.
- Runtime application/rollback semantics.
- Future persistence boundary.
- Future multi-scope policy architecture.
