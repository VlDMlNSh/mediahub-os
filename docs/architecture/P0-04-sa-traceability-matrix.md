# P0-04 — SA-001..SA-014 Traceability Matrix v1.0

## Status

**Prepared — implementation and evidence pending authorization.**

This matrix translates the accepted-at-contract-level State Authority invariants into concrete implementation and verification obligations. It does not grant implementation authorization.

| Invariant | Required implementation property | Primary verification | Security/privacy evidence |
|---|---|---|---|
| SA-001 | Only State Authority can publish canonical state | authority-path test + code inspection | no external mutation primitive |
| SA-002 | Candidate state isolated before commit | pre-commit visibility test | no candidate leakage |
| SA-003 | Commit publishes one complete revision | atomic publication test | no partial state exposure |
| SA-004 | Revision/state version owned and advanced by authority | sequential commit test | caller cannot select version |
| SA-005 | Caller cannot choose canonical revision | adversarial input test | reject revision injection |
| SA-006 | Transaction bound to observed generation | generation mismatch test | stale generation fails closed |
| SA-007 | Integrity is independently validated | integrity-failure test | compatibility cannot bypass integrity |
| SA-008 | Restore uses isolated candidate and new revision | restore success/failure tests | failed restore preserves canonical |
| SA-009 | Accepted checkpoint identity remains immutable | checkpoint immutability test | tamper/substitution rejected |
| SA-010 | Operations default-deny without explicit grant | unauthorized-operation tests | no fail-open path |
| SA-011 | API exposes no external execution/mutation primitive | capability inspection | subprocess/network/fs mutation absent |
| SA-012 | Failed operation preserves last valid canonical state | failure-path tests | no partial corruption |
| SA-013 | External/serialized state treated as untrusted | malformed/boundary tests | unsafe deserialization rejected |
| SA-014 | Authorization is operation-specific | per-operation authorization tests | no generic transaction privilege |

## Mandatory cross-cutting evidence

Every row must ultimately reference:

1. implementation file/class/method;
2. deterministic test identifier;
3. adversarial test identifier where applicable;
4. exact immutable commit SHA;
5. execution result and exit code;
6. security/privacy disposition;
7. final acceptance disposition.

## Evidence state before authorization

All verification columns are intentionally `PENDING`. No implementation result may be backfilled from design review. Design-level PASS is not execution evidence.

## Scope controls

P0-04 remains strictly in-memory. The implementation must not introduce SQLite, ZFS, filesystem persistence, cloud persistence, network transport, subprocesses, arbitrary command execution, bootloader/systemd appliance behavior, installer/recovery media, update engine, or hardware persistence.

## Governance

Formal P0-03 acceptance remains a prerequisite. If acceptance is `ACCEPT WITH CONDITIONS`, each condition must be explicitly recorded and mapped to this matrix before implementation proceeds.
