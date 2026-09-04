# MediaHub OS / MediaHub iOS — Implementation Rebaseline Gate

**Status:** PROPOSED / GOVERNANCE REVIEW REQUIRED / NO IMPLEMENTATION AUTHORIZATION
**Date:** 2026-09-04
**Repository:** `VlDMlNSh/mediahub-os`
**Purpose:** establish the review packet for a non-destructive implementation rebaseline derived from canonical architecture.

## 1. Decision boundary

This document does **not** modify canonical architecture and does not authorize implementation, deletion, merge, acceptance, freeze, production qualification, or production deployment.

The existing P0-P8 implementation lineage remains historical evidence. Git history must not be rewritten or deleted merely to obtain a cleaner baseline.

## 2. Canonical source hierarchy

Implementation authority is derived from the architecture custody chain MH-01..MH-23 and its Git-synchronized records, not from the current P0-P8 implementation tree.

Relevant repository evidence includes architecture-chat governance, master/reverse-master prompt records, decision/evidence/contradiction/unknown registers, and architecture packages for MH-13 through MH-22. The repository architecture tree confirms this custody structure.

For every implementation authorization, the exact architecture-source SHA set must be recorded before coding begins. If an architecture package is missing, contradictory, UNKNOWN, or marked forensic-recovery-only, implementation scope depending on it is BLOCKED pending architecture decision.

## 3. Current governance baseline

- P0-03: ACCEPTED / FROZEN.
- P0-04: ACCEPTED / FROZEN.
- P0-05: ACCEPTED / FROZEN.
- P0-06: ACCEPTED / FROZEN.
- P0-07: implementation work exists but execution verification and mutation/publication governance remain incomplete; NOT ACCEPTED / NOT FROZEN.
- P0-08: existing implementation/security verification does not expand State Authority; current production state remains NO-GO.
- MH-13: governance accepted, not frozen; reconstructed-proposed artifact, historical original not recovered.
- MH-14..MH-23: architecture packages remain subject to their recorded WIP / acceptance / forensic / qualification states; implementation must not silently upgrade their status.

## 4. Non-negotiable architectural kernel

The first implementation proof must preserve:

`Input -> Boundary -> Authorization -> State Authority -> Canonical State -> Observation -> Evidence`

### Authority rules

1. State Authority is the sole canonical mutation authority.
2. Persistence is not State Authority.
3. Device, Media, AI, Cloud, Plugin, Automation, Audit, Migration, and Observability do not acquire canonical mutation authority by implication.
4. AI is not authorization.
5. Network presence is not authorization or trust.
6. Device discovery is not trust.
7. Restore/recovery is not automatically canonical state mutation.
8. Audit/evidence/telemetry are observers and evidence producers, not mutation authorities.
9. Validation, authorization, publication, application, and persistence remain distinct lifecycle concepts.
10. UNKNOWN cannot become VERIFIED without new evidence.

## 5. P0-P8 carry-forward policy

| Legacy area | Default disposition | Rule |
|---|---|---|
| P0-03 | RETAIN / FROZEN REFERENCE | Do not alter semantics. |
| P0-04 | RETAIN / FROZEN REFERENCE | Sole State Authority boundary remains authoritative. |
| P0-05 | RETAIN / FROZEN REFERENCE | Integration boundary only; do not infer extra authority. |
| P0-06 | RETAIN / FROZEN REFERENCE | Reuse only after component conformance review. |
| P0-07 | REFERENCE-ONLY / QUARANTINE PENDING VERIFICATION | Do not treat implementation as accepted architecture. |
| P0-08 | REFERENCE-ONLY / QUARANTINE | Reuse only where explicit contract and evidence permit. |
| Any additional P0-P8 artifact | REFERENCE-ONLY by default | Promote to RETAIN only after conformance review. |

Legacy code is not automatically deleted. A later implementation decision may replace or quarantine it without destroying historical lineage.

## 6. New implementation baseline

The preferred baseline is a clean implementation branch created from an explicitly selected canonical starting point, rather than from the latest P0-07/P0-08 implementation branch.

Suggested branch naming: `implementation/rebaseline-2026`.

The branch must be created only after governance authorization. Until then, this name is a proposal, not an instruction to create the branch.

## 7. Minimal first vertical slice

The first slice should be deliberately narrow and prove the authority chain without persistence, cloud, plugin, automation, media, device execution, or AI mutation.

Required proof:

1. bounded input enters through an explicit boundary;
2. authorization is explicit and fail-closed;
3. an authorized mutation reaches the sole State Authority;
4. canonical state changes exactly once under the defined contract;
5. observation exposes the resulting state without becoming authoritative;
6. evidence records what was actually observed;
7. denied/invalid input produces no canonical mutation;
8. tests prove the authority boundary and absence of shadow mutation paths.

## 8. Required verification before expansion

No domain expansion until the first slice has evidence for:

- targeted unit/integration tests;
- negative authorization tests;
- forbidden direct canonical-write/import scans;
- persistence-boundary checks;
- security invariants;
- privacy/data-flow constraints;
- deterministic failure behavior;
- exact Git SHA and clean worktree;
- CI execution on the intended verification environment;
- evidence packet linked to the exact commit.

Local success alone is not production qualification.

## 9. Mandatory legacy mapping

Every reused or referenced P0-P8 component must receive one of four dispositions:

- **RETAIN** — explicitly conforms and is authorized for reuse.
- **REFERENCE-ONLY** — useful as historical/technical evidence but not imported into the new runtime.
- **QUARANTINE** — retained for investigation because its authority, security, or contract assumptions are unresolved.
- **REPLACE** — deliberately superseded by a new implementation derived from canonical contracts.

No component may be marked RETAIN solely because its existing tests pass.

## 10. Unknowns and contradictions

The rebaseline carries forward all unresolved contradictions and UNKNOWN states. In particular, implementation must not silently resolve architectural gaps around mutation/publication, defaults, Published-versus-Applied semantics, atomic publication/partial application, restart recovery, or forensic reconstruction domains.

Where MH-19/MH-20/MH-23 forensic recovery is required, implementation is BLOCKED unless an already-authoritative contract supplies sufficient scope.

## 11. Gate result

**CURRENT RESULT: BLOCKED / GOVERNANCE REVIEW REQUIRED.**

The repository now has a durable proposal record in Issue #26 and this review packet. Neither artifact authorizes destructive cleanup or implementation.

The next approval point is an explicit architecture/governance decision accepting the non-destructive rebaseline and approving the exact canonical source set and first vertical slice. Only after that decision may a new implementation branch be created.
