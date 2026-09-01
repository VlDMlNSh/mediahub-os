# P0-03 — Governance Decision Record v1.0

## Purpose

Controlled record for the explicit project-authority decision on P0-03 State Authority Contract v1.0.

This document is a decision record, not a decision itself. Until the decision fields below are completed by the project authority, P0-03 remains formally pending and P0-04 implementation remains unauthorized.

## Decision target

**P0-03 State Authority Contract v1.0**

## Evidence baseline

- P0-02 design: technical/adversarial review PASS with residual implementation obligations.
- P0-03 contract: technical review PASS.
- P0-03 adversarial review: PASS with residual implementation obligations.
- P0-03 acceptance gate: technical/design criteria satisfied; formal acceptance pending.
- P0-04 gate, workplan, security matrix, abuse-case register, evidence template and traceability preparation available.

## Decision options

### Option A — ACCEPT

Accept P0-03 as the governing contract and authorize P0-04 implementation strictly within the approved deterministic in-memory State Authority boundary.

### Option B — ACCEPT WITH CONDITIONS

Accept P0-03 subject to explicitly recorded conditions. Conditions must identify an owner/acceptance criterion and must not silently expand P0-04 scope.

### Option C — RETURN FOR REVISION

Reject the current transition to P0-04 and identify the required contract/design revisions.

## Explicit P0-04 boundary if authorized

Allowed only:

- deterministic in-memory State Authority;
- canonical/candidate/transaction/checkpoint model;
- transaction lifecycle and stale rejection;
- generation compatibility plus independent integrity validation;
- operation-specific default-deny authorization;
- restore through candidate state and publication as a new canonical revision;
- adversarial/security/privacy tests and exact-commit execution evidence.

Still prohibited:

- SQLite/ZFS/filesystem persistence;
- subprocess or arbitrary command execution;
- network transport;
- bootloader/systemd appliance behavior;
- installer/recovery media;
- update engine;
- cloud persistence;
- hardware persistence.

## Decision fields

- Decision: `PENDING`
- Authority: `PENDING`
- Date/time: `PENDING`
- Conditions: `NONE RECORDED`
- Authorization scope: `NOT GRANTED`
- Effective implementation boundary: `P0-04 IN-MEMORY ONLY`

## Governance invariant

Technical PASS, adversarial PASS, documentation completeness, or issue/PR existence do not constitute formal acceptance. Authorization must be explicit and traceable to the project-authority decision.

## Security and privacy invariant

The decision must preserve default-deny authorization, State Authority as the sole canonical mutation authority, untrusted-state validation boundaries, sanitized diagnostics, and prohibition of direct AI/external mutation. No personal or production-sensitive data is required for this decision.

## Historical responsibility boundary

No semantic responsibility for MH-02…MH-16 is inferred from this decision record. Historical mapping remains unresolved unless supported by authoritative evidence.

## Post-decision action

If `ACCEPT` or `ACCEPT WITH CONDITIONS` is explicitly recorded, update Issue #9 and the P0-04 gate with the exact decision and scope before implementation begins. If `RETURN FOR REVISION` is recorded, implementation remains blocked and the required revision work must be opened explicitly.
