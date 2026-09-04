# MH-14 — ALL ARCHITECTURE PASSES

Date: 2026-09-04
Status: ARCHITECTURE WORK IN PROGRESS
Physical persistence implementation: NOT AUTHORIZED

## Pass 1 — Authority / Boundary

PASS: ACCEPTED AT ARCHITECTURAL LEVEL.

State Authority remains the sole canonical mutation authority. Persistence is subordinate storage. Persisted representations are candidates for recovery, never canonical merely because they exist on disk. Persistence has no authorization, capability-granting, command-execution, plugin, AI, UI, device-control or Consumer-Boundary bypass authority.

## Pass 2 — Contract / Lifecycle

PASS: DEFINED, implementation-neutral.

Required abstract capabilities: open, close, read, write, append where justified, begin, commit, abort, checkpoint, snapshot, restore, verify, recover, migrate, compact, delete/expire where applicable. Every operation must expose explicit success/failure semantics and must not imply canonical mutation authority.

## Pass 3 — Consistency / Versioning

PASS: DEFINED.

Persisted records require sufficient metadata to distinguish state version/generation, transaction/commit identity, schema identity/version, persistence format version, snapshot/checkpoint provenance and integrity status. Stale representations must not silently overwrite newer canonical state.

## Pass 4 — Durability / Atomicity

PASS: DEFINED; physical guarantees TBD.

Volatile, buffered, flushed, synchronized, committed, durable and recoverable are distinct states. `commit acknowledged` is not equivalent to durable persistence unless the selected implementation and evidence explicitly establish that contract. Partial writes/commits must never be accepted as complete canonical state.

Candidate mechanisms remain open: transactional storage, WAL/journal, copy-on-write, atomic replacement, snapshot-based recovery and hybrids. No mechanism is selected by this pass.

## Pass 5 — Crash / Power-Loss Consistency

PASS: ARCHITECTURALLY DEFINED.

Recovery must handle process crash, OS crash, sudden power loss, interrupted writes, partial metadata updates, stale checkpoints, incomplete migration, storage disappearance and filesystem/storage corruption. The last physical artifact is not automatically the last valid committed state.

## Pass 6 — Recovery / Restore

PASS: DEFINED.

Recovery flow:

Physical Storage -> Validation -> Integrity -> Schema/Compatibility -> Candidate State -> State Authority -> Runtime Verification.

Restore is privileged and requires identity, authorization, validation, integrity verification and State Authority mediation.

## Pass 7 — Snapshot / Backup

PASS: DEFINED.

State Authority snapshot and persistence snapshot are distinct. Persistence snapshots need state/schema/provenance/integrity/compatibility metadata. Backup is separate from persistence and is not HA. A backup is not verified recovery capability until restore succeeds and the resulting state/runtime is validated.

Current Recovery Capability: UNVERIFIED.

## Pass 8 — RPO / RTO

PASS: GOVERNANCE SLOT DEFINED; VALUES TBD.

RPO and RTO cannot be invented. Required decisions include acceptable data loss, acceptable downtime, recovery ordering, automation level, backup frequency and restore-test frequency. Numerical values require workload/business evidence.

## Pass 9 — Failure / Corruption

PASS: DEFINED.

Corruption classes: detectable, recoverable, partially recoverable, unrecoverable, metadata corruption, schema corruption and cryptographic integrity failure. Required responses: detect, quarantine where appropriate, prevent promotion to canonical state, preserve evidence, recover from verified source, and require operator/governance action where automatic recovery is unsafe.

Storage-full, permission failure, read-only filesystem, I/O timeout and device disappearance must not produce false successful canonical commits.

## Pass 10 — Integrity / Security

PASS: DEFINED; implementation controls TBD.

Integrity mechanisms may include hashes/checksums and authenticated records; stronger mechanisms are selected only from the threat model and evidence. Encryption at rest, key lifecycle, least privilege and secret separation follow MH-12. Encryption does not replace authorization.

Threats include unauthorized read/write, tampering, rollback/replay, deletion abuse, backup disclosure, key compromise, malicious migration, storage substitution and restore privilege escalation.

## Pass 11 — Privacy / Data Lifecycle

PASS: DEFINED.

Persistence obeys MH-13 data classification, purpose limitation, retention, deletion and export requirements. Durable copies include primary storage, journals/WAL, snapshots, backups, caches, replicas and derived data where applicable. Deleted state must not silently reappear after restore when policy forbids it.

## Pass 12 — Schema / Migration / Rollback

PASS: DEFINED.

Schema identity/version and compatibility are explicit. Migration is versioned, testable, auditable and bounded. Destructive migration requires verified recovery. Migration failure must preserve the source where practical and quarantine the failed result. Application rollback does not automatically imply data rollback.

## Pass 13 — Isolation / Cross-Architecture Interaction

PASS: DEFINED.

Persistence is isolated from arbitrary network access, shell execution, plugin execution, AI execution and direct device control. UI consumes read models, not storage internals. AI memory and plugin persistence are separate governed namespaces. Configuration becomes active only through validation/policy/authorization/State Authority flow.

## Pass 14 — Observability / Operations

PASS: DEFINED.

Persistence health is observable through bounded operational metrics: read/write latency, errors, queue/backlog, capacity, corruption/recovery/migration state and durability state. Observability cannot become an independent mutation authority and must respect privacy minimization.

## Pass 15 — Resource / Capacity

PASS: DEFINED AT POLICY LEVEL.

Resource limits must cover write rate, queue depth, transaction size, snapshot size, backup size, temporary space, recovery work and migration work. Exact thresholds are REQUIRES VERIFICATION and must be established from hardware/workload evidence.

## Pass 16 — Offline-First / Cloud

PASS: DEFINED.

Core local persistence is not dependent on cloud availability unless explicitly authorized by a later architecture decision. Cloud persistence is external, encrypted, bounded, privacy-governed, observable and auditable. Cloud synchronization cannot create a second canonical authority.

## Pass 17 — Technology / Hardware Evaluation

PASS: EVALUATION FRAMEWORK DEFINED; SELECTION OPEN.

Candidate classes: embedded database, relational database, KV/document store, filesystem, object store, append-only log and hybrid. Evaluation criteria: atomicity, durability, crash recovery, corruption handling, migration, backup/restore, encryption, privacy, footprint, operations, maintenance, licensing, portability and hardware compatibility.

Apple Mac mini Server 2011 remains a candidate hardware baseline only. Exact hardware/storage/filesystem/OS/kernel/driver/power-loss facts require evidence.

## Pass 18 — Verification / Testing

PASS: DEFINED.

Required tests cover normal persistence, transactions, crash, power loss, partial writes, corruption, recovery, snapshots, restore, backup verification, migration, rollback, storage-full, permission errors, encryption/key rotation, deletion/retention, concurrency and stale-version rejection. Security and privacy test suites are mandatory.

## Pass 19 — Governance / Change Control

PASS: DEFINED.

Architecture changes follow: evidence -> contradiction/unknown update -> ADR where needed -> explicit governance decision -> baseline update -> implementation. Development success does not equal architecture approval. Physical persistence remains unauthorized until the separate implementation authorization gate passes.

## Pass 20 — Long-Term Architecture / GitHub Synchronization

PASS: ESTABLISHED.

GitHub repository `VlDMlNSh/mediahub-os` is the durable external architecture record. MH-14 architecture chat is the semantic guardian, not the only durable store. Development chat consumes `MH-14-master-prompt.md` and returns findings through `MH-14-reverse-master-prompt.md`.

Architecture chats MH-1…MH-23 are not development workspaces. Development, debugging and implementation iteration belong in the separate development track. Architecture-impacting findings return through the reverse master protocol.

## Final result

MH-14 is architecturally coherent at the abstract level and remains intentionally implementation-neutral.

ACCEPTED/FROZEN: authority boundary, persistence boundary, recovery authority model, security/privacy dependency model, development/architecture separation.

OPEN / REQUIRES VERIFICATION: physical technology, filesystem, WAL/journal choice, exact durability semantics, RPO/RTO, backup schedule/destination, restore-test schedule, hardware/storage facts, encryption/key-management implementation, migration framework, corruption-recovery implementation, power-loss characteristics, UPS, replication and cloud implementation.

GATE: MH-14 cannot be marked ACCEPTED/FROZEN until all mandatory evidence and acceptance criteria are satisfied. Until then physical persistence implementation remains NOT AUTHORIZED.

## Transition

MH-15 consumes the persistence boundary and defines OS/appliance execution-environment facts. MH-15 must not transfer canonical state authority to OS, filesystem, hardware, service manager or storage layer.
