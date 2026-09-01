# P0-04 Governance Continuation Protocol v1.0

## Status

Prepared. This artifact does not grant implementation authorization.

## Purpose

Define the automatic continuation behavior for MediaHub OS while the P0-03 formal governance decision remains pending, without converting technical readiness into authorization.

## Current gate rule

P0-03 formal acceptance is the controlling prerequisite for P0-04 implementation. Until an explicit governance decision is recorded, implementation of the in-memory State Authority remains blocked.

## Allowed work while blocked

- architecture clarification;
- security and privacy threat analysis;
- test oracle refinement;
- evidence-template refinement;
- traceability maintenance;
- governance consistency checks;
- repository/history inspection;
- documentation of residual implementation obligations.

## Prohibited work while blocked

- implementation or mutation of P0-04 runtime code;
- persistence implementation;
- SQLite/ZFS/filesystem integration;
- subprocess or arbitrary command execution capability;
- network transport implementation;
- bootloader/systemd appliance work;
- installer/recovery media;
- update/rollback engine implementation;
- cloud or hardware persistence;
- changing P0-03 decision state implicitly;
- treating technical PASS as formal acceptance.

## Automatic transition after explicit acceptance

When and only when an explicit governance decision records P0-03 as ACCEPT or ACCEPT WITH CONDITIONS with authority, timestamp, and applicable conditions:

1. freeze the accepted P0-03 baseline SHA;
2. verify P0-04 implementation-entry prerequisites against that immutable baseline;
3. create/continue the dedicated P0-04 implementation branch from the authorized baseline;
4. implement only the deterministic in-memory State Authority contract surface;
5. execute the prescribed functional, adversarial, security, privacy, and capability tests;
6. capture exact-commit execution evidence;
7. perform adversarial/security review before any acceptance decision;
8. keep persistence and production topology outside the gate.

## Conditions handling

For ACCEPT WITH CONDITIONS, every condition must be explicit, testable, scoped, and traceable. No condition may silently authorize a prohibited capability or broaden P0-04 into persistence, networking, appliance, installer, recovery, update, cloud, or hardware work.

## Evidence integrity

Evidence must identify the exact immutable implementation commit, environment/toolchain, commands, exit codes, test counts, security inspection results, and timestamp. Evidence must not be reconstructed from memory or inferred from source inspection.

## Security and privacy invariants

The continuation protocol preserves:

- default-deny authorization;
- separation of generation compatibility from integrity validation;
- candidate isolation from canonical state;
- atomic publication semantics;
- failure preservation of the last valid canonical state;
- checkpoint identity immutability;
- restore-as-new-revision semantics;
- non-executable AI/external input boundary;
- sanitized diagnostics and errors;
- no unnecessary sensitive or personal data in test/evidence artifacts.

## Historical boundary

This protocol does not assign or infer historical responsibilities for MH-02…MH-16. Any such mapping requires authoritative historical evidence.

## Exit condition

This protocol remains active until the P0-03 governance decision is explicitly recorded. It then becomes the transition checklist for the authorized branch and does not itself constitute acceptance of implementation.
