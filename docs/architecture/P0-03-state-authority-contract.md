# P0-03 — State Authority Contract v1.0

**Status:** Contract Draft / Controlled Implementation Gate  
**Depends on:** P0-02 State Authority Design

## Purpose
Convert P0-02 into a precise, persistence-neutral contract for a deterministic in-memory implementation and adversarial test suite.

The current `StateAuthority` boundary exposes `read`, `begin`, `commit`, `abort`, `snapshot`, and `restore`; P0-03 gives those operations explicit semantics without introducing persistence.

## Contract objects

### CanonicalState
Immutable-at-read-boundary logical revision containing payload, `generation_id`, `binary_version`, `schema_version`, authoritative `state_version`, and integrity reference/status. Callers cannot mutate canonical state in place.

### Transaction
Opaque handle bound at `begin` to transaction identity, authorization context, observed canonical generation, observed canonical state version, isolated candidate state, and lifecycle status.

### Checkpoint
Immutable identity for an accepted canonical recovery point, with generation/state/integrity metadata. Checkpoint material is untrusted at the persistence/read boundary until validated.

## Operation contract

### `read`
Observes canonical state only. Must return one complete internally consistent revision and must not grant mutation authority.

### `begin`
Creates an isolated candidate transaction. Must authorize the requested operation, bind to current generation/state version, and reject malformed or unauthorized requests fail-closed.

### `commit`
Atomically publishes a validated candidate. Preconditions: active transaction, valid authorization, matching generation/state-version preconditions, schema/type/bounds validation, generation compatibility, and integrity validation. Success publishes one complete revision and advances `state_version` according to State Authority sequencing. Failure leaves canonical state and version unchanged. Commit after abort/commit fails closed.

### `abort`
Invalidates an active candidate without changing canonical state or advancing state version. Repeated abort is deterministic and never resurrects a transaction.

### `snapshot`
Creates an accepted checkpoint only from canonical state. Preserves complete generation/state/integrity metadata. Does not mutate canonical state.

### `restore(snapshot_reference)`
Treats restore as a distinct authorized State Authority operation. Validates checkpoint authenticity/integrity and generation/schema compatibility, creates a candidate, validates/self-tests it, then publishes a new canonical revision. It never rewrites checkpoint identity and failed restore preserves prior canonical state.

## Transaction state machine

```text
             begin
               |
               v
             ACTIVE
            /      \
         abort     commit
           |         |
           v         v
        ABORTED   COMMITTED
```

Forbidden: `ABORTED -> ACTIVE`, `ABORTED -> COMMITTED`, `COMMITTED -> ACTIVE`, `COMMITTED -> COMMITTED`, `COMMITTED -> ABORTED`. Stale ACTIVE transactions are not implicitly rebased.

## Invariants

- **SA-001 Single authority:** canonical mutation occurs only through State Authority.
- **SA-002 Isolation:** candidate changes are not canonical before commit.
- **SA-003 Atomic publication:** readers see either the previous complete revision or the new complete revision.
- **SA-004 Monotonic version:** successful canonical mutation advances version; abort/failure does not.
- **SA-005 No caller-selected revision:** candidate payload cannot manufacture resulting canonical version.
- **SA-006 Generation binding:** active transactions bind to generation/state version; stale commits fail closed.
- **SA-007 Integrity gate:** compatibility does not imply integrity.
- **SA-008 Restore isolation:** restore enters candidate state before publication.
- **SA-009 Checkpoint immutability:** accepted checkpoint identity is never rewritten by restore.
- **SA-010 Default deny:** unauthorized or ambiguous mutation requests are rejected.
- **SA-011 No external mutation primitive:** AI/network/UI/plugin/diagnostic input remains data/request until explicitly authorized.
- **SA-012 Failure preservation:** unsafe failure preserves the last valid canonical revision.
- **SA-013 Untrusted persistence boundary:** serialized state/checkpoint material is untrusted until validation completes.
- **SA-014 Operation-specific authorization:** begin, commit, snapshot, and restore are independently authorization-sensitive.

## Error contract

Expected deterministic failure classes include invalid transaction state, stale transaction, generation mismatch, authorization denied, malformed candidate, integrity failure, invalid checkpoint, unsupported schema/version, and invalid restore target. Errors must not expose secrets or sensitive state.

## Security and privacy

The implementation must default-deny authorization; avoid raw state/sensitive payloads in logs and exceptions; reject unsafe deserialization; enforce structural and size bounds; expose no arbitrary filesystem/network execution through this API; keep AI output non-executable/non-authoritative; minimize retained sensitive state; and use the existing sanitized diagnostics boundary.

## Deterministic in-memory gate

Before persistence, demonstrate the contract with an in-memory implementation and tests for transaction lifecycle, isolation, atomic publication, monotonic versioning, stale rejection, generation mismatch, separate integrity gate, per-operation authorization, abort, restore-as-new-revision, checkpoint immutability, malformed/untrusted state, hostile input as data, and diagnostic privacy.

This gate does not authorize SQLite, ZFS, filesystem persistence, subprocesses, network transport, bootloader/systemd appliance behavior, installer/recovery media, or update engines.

## Acceptance criteria

- [ ] explicit pre/postconditions for every operation;
- [ ] deterministic transaction state machine;
- [ ] testable candidate/canonical isolation;
- [ ] testable atomic publication semantics;
- [ ] authority-owned version sequencing;
- [ ] fail-closed stale handling;
- [ ] distinct generation/integrity gates;
- [ ] restore creates a new revision;
- [ ] immutable checkpoint identity;
- [ ] operation-specific default-deny authorization;
- [ ] untrusted serialized-state boundary;
- [ ] testable security/privacy constraints;
- [ ] persistence-neutral implementation.

## Implementation gate

Approval authorizes only the contract implementation, in-memory State Authority, deterministic unit/adversarial tests, and related architecture/test documentation. Concrete persistence and appliance infrastructure remain unauthorized.
