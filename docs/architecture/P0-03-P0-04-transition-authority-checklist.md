# P0-03 → P0-04 Transition Authority Checklist v1.0

## Status

**PREPARED — FAIL-CLOSED — NO TRANSITION AUTHORIZED**

This checklist is an execution-control artifact. It does not record a governance decision and does not authorize implementation by itself.

## Gate 1 — P0-03 decision validity

All must be true before transition:

- [ ] One and only one decision is recorded: `ACCEPT`, `ACCEPT WITH CONDITIONS`, or `RETURN FOR REVISION`.
- [ ] Decision authority is identified.
- [ ] UTC timestamp is recorded.
- [ ] Exact P0-03 contract baseline is recorded as `9ae82f9e45bcb9c330ab283b13a482fbeea6b546` or an explicitly superseding accepted revision.
- [ ] Conditions are explicit and testable, if applicable.
- [ ] P0-04 implementation authorization status is explicit.
- [ ] Persistence authorization status is explicit.

Any unchecked item blocks transition.

## Gate 2 — P0-04 entry validity

Before implementation:

- [ ] P0-03 formal acceptance is recorded.
- [ ] Separate P0-04 implementation authorization is recorded.
- [ ] Authorized scope is deterministic in-memory State Authority only.
- [ ] Implementation baseline is a new immutable commit derived from the accepted P0-03 baseline.
- [ ] P0-04 scope lock is attached to the implementation baseline.
- [ ] SA-001..SA-014 traceability is carried into implementation verification.
- [ ] Security/privacy verification matrix is active.
- [ ] Stop conditions are active.
- [ ] Evidence integrity protocol is active.

## Gate 3 — Mandatory prohibited-capability check

Implementation must stop if it introduces any of:

- SQLite/ZFS/filesystem/cloud/hardware persistence;
- subprocess or arbitrary command execution;
- network sockets, HTTP clients, telemetry or mTLS transport;
- bootloader/systemd appliance behavior;
- installer/recovery media;
- update/rollback engine;
- unsafe deserialization;
- dynamic code execution;
- direct AI/external mutation authority;
- real user/private data in fixtures or evidence.

## Gate 4 — Evidence identity

Every verification result must identify the exact implementation commit, execution environment, exact command, exit code, and applicable test counts. Evidence from another commit cannot retroactively validate the implementation under review.

## Gate 5 — Security/privacy exit

P0-04 cannot be accepted until required functional, adversarial, security and privacy evidence exists, all blocking findings are resolved or formally dispositioned, and acceptance authority explicitly records the outcome.

## Fail-closed transition rule

If any field, authorization, baseline, scope, evidence identity, or acceptance authority is missing or ambiguous, the state remains `BLOCKED`. No emergency or informal bypass exists.

## Current state

- P0-03 formal decision: **PENDING**.
- P0-04 implementation authorization: **NOT GRANTED**.
- P0-04 implementation: **NOT STARTED**.
- Persistence authorization: **NOT GRANTED**.

## Historical boundary

This checklist does not infer or reconstruct MH-02…MH-16 responsibilities.
