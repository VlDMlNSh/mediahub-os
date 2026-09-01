# P0-03 — Governance Decision Record v1.0

## Purpose

Controlled record for the explicit project-authority decision on P0-03 State Authority Contract v1.0.

## Decision target

**P0-03 State Authority Contract v1.0**

## Evidence baseline

- P0-02 design: technical/adversarial review PASS with residual implementation obligations.
- P0-03 contract: technical review PASS.
- P0-03 adversarial review: PASS with residual implementation obligations.
- P0-03 acceptance gate: technical/design criteria satisfied.
- P0-04 gate, workplan, security matrix, abuse-case register, evidence template and traceability preparation available.

## Formal decision

**Decision: ACCEPT**

**Decision authority:** Project authority (explicit decision issued in the controlling project chat).

**Decision timestamp:** 2026-09-01T19:44Z

**Referenced P0-03 contract baseline:** `9ae82f9e45bcb9c330ab283b13a482fbeea6b546`

**Conditions:** None beyond the existing P0-04 scope and security/privacy controls.

## P0-04 implementation authorization

**Authorization: GRANTED** strictly for P0-04 In-Memory State Authority implementation derived from the accepted P0-03 baseline.

Allowed only:

- deterministic in-memory State Authority;
- canonical/candidate/transaction/checkpoint model;
- transaction lifecycle and stale rejection;
- authority-owned monotonic revision sequencing;
- generation compatibility plus independent integrity validation;
- operation-specific default-deny authorization;
- restore through candidate state and publication as a new canonical revision;
- bounded inputs and privacy-safe diagnostics;
- functional, adversarial, security and privacy verification.

## Persistence authorization

**NOT GRANTED.**

Still prohibited:

- SQLite/ZFS/filesystem persistence;
- subprocess or arbitrary command execution;
- network transport;
- bootloader/systemd appliance behavior;
- installer/recovery media;
- update engine;
- cloud persistence;
- hardware persistence;
- production deployment topology.

AI, UI, plugins, network and external inputs remain non-authoritative and cannot mutate canonical state directly.

## Governance invariant

This record supersedes the previous PENDING status for P0-03. It does not authorize any capability outside the explicitly stated P0-04 in-memory boundary.

P0-04 acceptance remains a separate evidence-based gate and is not implied by this authorization.

## Security and privacy invariant

The implementation must preserve default-deny authorization, State Authority as the sole canonical mutation authority, untrusted-state validation boundaries, sanitized diagnostics, resource bounds, and prohibition of direct AI/external mutation. Verification must use synthetic data by default and must not introduce credentials, secrets, raw voice/audio, private content, or unnecessary personal data into source, tests, logs, issues, or evidence.

## Historical responsibility boundary

No semantic responsibility for MH-02…MH-16 is inferred from this decision record. Historical mapping remains unresolved unless supported by authoritative evidence.

## Post-decision action

Create a new immutable P0-04 implementation baseline from the accepted P0-03 commit. Execute entry security checks before implementation, then proceed through implementation, adversarial verification, execution evidence, security/privacy review, and the separate P0-04 acceptance gate.
