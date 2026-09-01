# P0-03 → P0-04 Transition Checklist v1.0

Status: PREPARED / BLOCKED ON FORMAL GOVERNANCE DECISION

## Purpose

Provide a deterministic transition checklist for moving from the accepted P0-03 State Authority contract to the separately authorized P0-04 in-memory implementation.

This document does not grant implementation authorization.

## Preconditions

- P0-03 technical review: PASS.
- P0-03 adversarial review: PASS with residual implementation obligations.
- P0-03 formal governance decision: PENDING until explicitly recorded.
- P0-04 implementation authorization: NOT GRANTED.
- No historical MH-02…MH-16 responsibility is inferred from this gate.

## Required governance transition

1. Record one explicit P0-03 decision: ACCEPT, ACCEPT WITH CONDITIONS, or RETURN FOR REVISION.
2. Record decision authority and timestamp.
3. If ACCEPT WITH CONDITIONS, record every condition as a testable implementation constraint.
4. Only after ACCEPT or an explicitly scoped ACCEPT WITH CONDITIONS may implementation authorization be issued.
5. Create the P0-04 implementation branch from the authorized P0-03 contract baseline, not from an unrelated or unreviewed working state.

## Implementation boundary after authorization

Allowed:

- deterministic in-memory State Authority;
- canonical state, candidate state, transaction and checkpoint contract types;
- transaction lifecycle and isolation;
- authority-owned state revision sequencing;
- generation compatibility plus independent integrity validation;
- operation-specific default-deny authorization;
- checkpoint and restore semantics;
- adversarial and regression tests;
- security/privacy evidence and exact-commit execution evidence.

Prohibited in P0-04:

- SQLite or other persistence;
- ZFS/filesystem persistence;
- subprocesses or arbitrary command execution;
- network transport;
- bootloader/systemd appliance integration;
- installer or recovery media;
- update engine;
- cloud persistence;
- hardware persistence;
- AI-driven canonical state mutation.

## Security/privacy transition controls

Before implementation starts, confirm that the implementation plan preserves:

- default-deny authorization;
- no caller-selected canonical revision;
- no stale transaction overwrite;
- no checkpoint identity mutation;
- no implicit trust in persisted/untrusted material;
- no unsafe deserialization;
- bounded inputs and resource use;
- no sensitive state in diagnostics/errors;
- no direct AI/external mutation path;
- test data that does not require real personal data or secrets.

## Exit from transition

The transition is complete only when:

- formal governance decision is recorded;
- implementation authorization is explicit and scoped;
- exact implementation commit is identified;
- SA-001…SA-014 traceability is populated;
- required tests and security checks are executed;
- execution evidence is captured from the exact commit;
- unresolved high/critical security findings are absent;
- prohibited capabilities are absent;
- final P0-04 acceptance is separately recorded.

Until those conditions are satisfied, P0-04 remains a prepared gate rather than an accepted implementation.
