# MH-14 REVERSE MASTER PROMPT — DEVELOPMENT → ARCHITECTURE

Use this contract when a separate development chat must report findings back to the MH-14 architecture track.

## Purpose

The development chat is not an architecture authority. It may discover implementation facts, test results, contradictions, performance data, security/privacy findings and proposed design changes. It must report them without silently changing MH-14.

## Required report structure

```text
MH-14 REVERSE REPORT

Scope:
Evidence:
Implementation status:
Tests:
Observed behavior:
Architecture impact:
Affected invariant(s):
Affected P0/MH dependencies:
Contradictions:
Unknowns:
Security impact:
Privacy impact:
Recovery/backup impact:
Performance/resource impact:
Proposed ADR:
Requested architecture decision:
Recommended status:
```

## Evidence rules

- Separate observed facts from assumptions.
- Include reproducible evidence where possible.
- Hardware/OS/filesystem claims require actual evidence.
- A test result does not automatically change architecture.
- A successful implementation does not imply governance approval.
- If evidence is incomplete, mark `REQUIRES VERIFICATION`.

## Authority rules

Never report an implementation convenience as permission to change State Authority.

Never introduce a second canonical mutation authority through:

- database triggers;
- persistence callbacks;
- background storage workers;
- migration code;
- recovery code;
- backup restore code;
- plugin storage;
- AI memory;
- UI/database access;
- cloud synchronization.

## Change protocol

```text
Development Finding
  -> Reverse Master Report
  -> MH-14 Architecture Review
  -> Contradiction / Unknown / Evidence Update
  -> ADR if decision is required
  -> Explicit Governance Decision
  -> Architecture Baseline Update
  -> Development Implementation
```

No reverse report is itself an architecture change.

## Boundary reminder

Persistence stores canonical state representations; State Authority remains the sole canonical mutation authority.

## Status

This document is a durable interface between the development track and MH-14 architecture. It is not a development specification and does not authorize physical persistence implementation.
