# MH-14 — GAPS REGISTER / ETALON RECONCILIATION

Status: QUALIFICATION-READY / IMPLEMENTATION-NOT-AUTHORIZED

## Closed at architecture level

- State Authority remains sole canonical mutation authority.
- Persisted representation is not automatically canonical.
- Recovery is Physical Storage → Validation/Integrity/Schema/Compatibility → Candidate State → State Authority.
- Transaction, versioning, concurrency and stale-write boundaries are explicit.
- Snapshot/journal semantics are explicit.
- Strong, distributed-transactional, eventual and rebuildable consistency classes are separated.
- Persistence domains are logically separated.
- UI, AI, plugins and integrations cannot obtain unrestricted persistence access.
- MH-12 security and MH-13 privacy requirements remain mandatory.
- Backup is not HA and is not authority.
- Local First is preserved.
- Migration is versioned, validated, recoverable and provenance-preserving.

## Open evidence/governance gaps

| Gap | Status | Closure evidence |
|---|---|---|
| Physical persistence technology | OPEN | ADR + benchmark + crash/recovery evidence |
| Filesystem/storage semantics | OPEN | physical host/OS evidence |
| WAL/journal or equivalent | OPEN | atomicity + crash/power-loss tests |
| Exact durability semantics | OPEN | implementation contract + failure evidence |
| RPO | TBD | governance/workload decision |
| RTO | TBD | governance/workload decision |
| Backup destination/frequency | OPEN | MH-20 governance + capacity evidence |
| Restore-test cadence | OPEN | operations policy |
| Storage topology/health | OPEN | physical inspection |
| Encryption/key lifecycle | OPEN | MH-12 implementation evidence |
| Migration framework | OPEN | ADR + migration/rollback tests |
| Corruption recovery | OPEN | fault-injection evidence |
| Power-loss behavior / UPS | OPEN | appliance evidence |
| Replication / HA | OPEN | explicit governance decision |
| Cloud persistence | OPEN | privacy/security/network governance |
| Archival policy | OPEN | retention/data-governance decision |
| Resource/capacity thresholds | OPEN | workload + hardware benchmarks |
| Full qualification execution | QUEUED | autonomous qualification package |

## Non-gaps

The following must not be reopened as architecture questions:

- Persistence is not State Authority.
- Storage backend does not gain mutation authority.
- Recovery does not directly promote state.
- Backup does not imply HA.
- Database choice is not required to define the persistence boundary.
- Vector DB is not a mandatory dependency.
- Cloud persistence is not a prerequisite for Local First.
- P0-03…P0-06 remain frozen.
- P0-07 is not repaired by MH-14.

## Contradiction rule

Any future artifact that makes persistence, database, cache, backup, recovery worker, graph, vector index, AI memory or cloud replica a competing canonical authority is invalid and must be rejected during reconciliation.

## Qualification disposition

MH-14 is not yet ACCEPTED/FROZEN. It is QUALIFICATION-READY with explicit evidence/governance gates. Physical persistence remains NOT AUTHORIZED.
