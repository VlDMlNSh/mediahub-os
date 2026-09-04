# MH-14 — PERSISTENCE ARCHITECTURE

**MediaHub OS 11.x LTS / MediaHub iOS**

Status: **ARCHITECTURE WORK IN PROGRESS**
Physical persistence implementation: **NOT AUTHORIZED**
Canonical mutation authority: **State Authority**

## Governing principle

> Persistence stores canonical state; it does not become canonical authority.

Persistence is a storage mechanism. It may store, retrieve, verify and recover representations of state, but it never decides what the canonical runtime state is.

## Authority boundary

```text
Consumer/Input
  -> Authorization
  -> Consumer Boundary
  -> State Authority
  -> Canonical Runtime State
  -> Persistence Contract
  -> Persistence Implementation
  -> Physical Storage
```

Recovery is explicitly subordinate to State Authority:

```text
Physical Storage
  -> Persistence Implementation
  -> Validation / Integrity / Schema Checks
  -> Candidate State
  -> State Authority
  -> Canonical Runtime State
```

A persisted representation is not automatically canonical.

## Frozen dependencies

MH-14 does not modify:

- P0-03 State Authority Contract v1.0 — ACCEPTED / FROZEN
- P0-04 In-Memory State Authority v1.0 — ACCEPTED / FROZEN
- P0-05 Consumer / Integration Boundary — ACCEPTED / FROZEN
- P0-06 Core Runtime Services — ACCEPTED / FROZEN
- P0-07 Mutation publication — BLOCKED — GOVERNANCE/API GAP

MH-14 does not independently repair the P0-07 gap.

## Contract scope

The abstract persistence contract may expose:

- open / close
- read / write
- append where justified
- begin / commit / abort
- checkpoint
- snapshot / restore
- verify / recover
- migrate / compact
- delete / expire where applicable

These are storage operations, not a second State Authority.

## Durability

The architecture distinguishes volatile, buffered, flushed, committed, durable and recoverable semantics. `commit acknowledged` must not be silently treated as `durably persisted`.

Exact durability guarantees remain **REQUIRES VERIFICATION** until a physical implementation is selected and tested.

## Consistency and atomicity

Persisted records must carry sufficient versioning/provenance metadata to detect stale state and incomplete transactions. A partial persisted commit must never be accepted as a complete canonical state. Persistence must not silently overwrite newer canonical state.

Technology choices such as WAL, journal, copy-on-write, transactional database or snapshot replacement remain candidates pending ADR and evidence.

## Recovery

Recovery must identify and verify the last valid committed representation, detect incomplete transactions, validate integrity/schema/compatibility, and submit a candidate state to State Authority. Persistence cannot directly promote recovered data to canonical state.

## Snapshots and restore

State Authority snapshots and persistence snapshots are distinct concepts. Persistence snapshots require version, schema, provenance, integrity and compatibility metadata.

Restore is security-sensitive:

```text
Restore Request
  -> Identity
  -> Authorization
  -> Validation
  -> Integrity Check
  -> Compatibility Check
  -> Candidate State
  -> State Authority Restore
  -> Runtime Verification
```

## Backup

Backup is separate from persistence and is not HA. Backup is not canonical authority. A backup is not considered verified recovery capability until a restore has succeeded and the resulting state/runtime has been validated.

`Recovery Capability = UNVERIFIED` until then.

Current reliability baseline: **SINGLE NODE / NO HA**.

## Security and privacy

MH-12 security requirements and MH-13 privacy/data-governance requirements apply to persistence, snapshots, backups, recovery, migration and deletion. Encryption at rest does not replace authorization. Secrets require dedicated controls. Retention is not indefinite by default. Deletion semantics must account for WAL, snapshots, backups, caches and derived copies where applicable.

## Isolation

Persistence must not directly execute commands, call plugins, invoke AI, control devices, access arbitrary shell facilities, or bypass the Consumer Boundary. UI, AI and plugins do not receive arbitrary core persistence access.

## Failure and degradation

Persistence subsystem health may include `STARTING`, `READY`, `DEGRADED`, `READ_ONLY`, `UNAVAILABLE`, `CORRUPTED`, `RECOVERING`, `MIGRATING`, `FAILED` and `QUARANTINED`. These are subsystem health states and do not replace State Authority lifecycle authority.

On persistence failure, the system must avoid false success, prevent unsafe durable commits, expose degraded durability, and preserve current in-memory canonical state where safe.

Storage-full handling must never silently delete canonical state.

## Technology and hardware

Candidate classes include embedded DB, relational DB, KV/document store, filesystem, object store, append-only log and hybrid approaches. No concrete technology is selected by MH-14.

The Apple Mac mini Server 2011 is only a candidate hardware baseline. Exact storage, filesystem, RAM, device health, topology, power-loss behavior, firmware, OS, kernel and drivers require physical evidence.

## RPO / RTO

RPO: **TBD**

RTO: **TBD**

No numerical values are canonical without workload/business evidence.

## Implementation gate

```text
MH-14 Architecture
  -> Architecture Acceptance
  -> Persistence Implementation Authorization
  -> ADR / Technology Selection
  -> Implementation
  -> Functional + Security + Privacy + Recovery Verification
  -> Governance Acceptance
```

Database/filesystem code is not evidence of architecture approval.

## Immutable invariants

1. State Authority remains sole canonical mutation authority.
2. Persistence is storage, not authority.
3. Persisted state is not automatically canonical.
4. Persistence cannot authorize mutations or grant capabilities.
5. Persistence cannot execute commands or bypass Consumer Boundary.
6. Partial commits cannot appear as valid committed state.
7. Stale persisted data cannot silently overwrite newer state.
8. Restore requires explicit authorization and State Authority mediation.
9. Backup is not HA and is not canonical authority.
10. Persistence failure must not produce false success.
11. Corruption must be detected or conservatively handled.
12. Migration is explicit and versioned; destructive migration requires verified recovery.
13. Deletion accounts for durable copies where applicable.
14. Secrets require dedicated security controls.
15. MH-12 security and MH-13 privacy requirements apply.
16. Observability cannot become persistence control authority.
17. AI/plugins/UI cannot directly mutate core persistence.
18. Physical persistence implementation requires separate governance authorization.

## Open items

Technology, filesystem, database, WAL/journal strategy, durability guarantees, RPO/RTO, backup destination/frequency, storage topology/health, encryption/key management, migration framework, corruption recovery, power-loss characteristics, UPS, cloud persistence and replication remain **REQUIRES VERIFICATION**.

## Transition

MH-15 — OS / APPLIANCE ARCHITECTURE consumes this boundary and may establish physical execution-environment facts only through evidence. OS, hardware, filesystem and drivers do not become State Authority.
