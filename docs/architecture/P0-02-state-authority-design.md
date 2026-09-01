# P0-02 — State Authority Design v1.0

**Status:** Architecture Draft / Controlled Design Phase  
**Branch:** `architecture/p0-02-state-authority-design`  
**Scope:** MediaHub OS Runtime Foundation  

## 1. Purpose

Define the authoritative state boundary for MediaHub OS before introducing concrete persistence or recovery infrastructure.

This document defines architecture and invariants only. It does **not** authorize or implement SQLite, ZFS, bootloader, systemd appliance behavior, installer/recovery media, update engines, network persistence, or hardware-specific storage.

## 2. Architectural Principle

`StateAuthority` is the sole authoritative boundary through which canonical runtime state may be created, mutated, committed, checkpointed, or restored.

External actors may propose, request, observe, or validate state, but must not bypass the State Authority boundary.

## 3. State Domains

The design distinguishes:

- **Canonical State** — currently authoritative runtime state.
- **Candidate State** — an isolated state under an active transaction and not yet authoritative.
- **Checkpoint** — an explicitly accepted recovery point representing a valid canonical state.
- **Generation** — compatibility identity for the binary/schema/state generation associated with state.
- **State Version** — versioned identity of the canonical state revision. For authoritative mutations it MUST advance monotonically.
- **Integrity Reference** — reference used by an integrity-validation mechanism; its concrete representation is implementation-specific and out of scope here.

Canonical state MUST NOT be replaced by an unvalidated candidate.

## 4. Mutation Boundary

The normative mutation path is:

```text
Caller
  |
  v
Authorization
  |
  v
State Authority
  |
  +--> begin transaction
  |        |
  |        v
  |     candidate state
  |        |
  |        +--> validation
  |        +--> generation compatibility
  |        +--> integrity validation
  |        |
  |        +---- failure ---> abort
  |        |
  |        +---- success ---> commit
  |                         |
  |                         v
  |                  canonical state
```

AI output, network input, UI input, plugins, diagnostics, or other untrusted/external content MUST NOT acquire a direct state mutation primitive merely by supplying a state-shaped payload.

## 5. Transaction Semantics

An implementation conforming to this design MUST provide the following semantic guarantees:

1. `begin` creates an isolated candidate transaction bound to the observed canonical generation and state version.
2. A candidate does not become canonical before `commit` succeeds.
3. Validation failure results in `abort` and leaves canonical state unchanged.
4. An aborted transaction cannot subsequently commit.
5. A committed transaction cannot be committed again.
6. A stale or generation-incompatible transaction is rejected closed/fail-closed.
7. A failed commit MUST NOT expose a partially applied canonical state.
8. Transaction ownership and authorization MUST be explicit; possession of a transaction identifier alone is not sufficient authority.
9. Error handling MUST preserve the previous valid canonical state whenever commit cannot be completed safely.
10. A successful authoritative commit MUST atomically publish one complete canonical state revision and its associated generation/state metadata.
11. State-version advancement MUST occur as part of successful authoritative publication; failed or aborted transactions MUST NOT advance the canonical state version.

### 5.1 Commit linearization point

The implementation MUST define one unambiguous commit linearization point: the point at which the candidate becomes the new canonical state.

Before that point, readers MUST continue to observe the previous canonical state. After that point, readers MUST observe the complete new canonical revision, never a mixture of old and new fields.

The concrete primitive used to provide this guarantee is implementation-specific.

## 6. Generation Binding

State operations are generation-bound.

The compatibility decision MUST account for:

- `generation_id`
- `binary_version`
- `schema_version`
- `state_version`

The existing runtime compatibility contract compares these four values.

`integrity_reference` is deliberately treated as a separate integrity-validation concern rather than silently folded into compatibility identity. P0-02 therefore requires two distinct gates:

```text
Generation Compatibility
          +
Integrity Validation
          =
State Acceptance
```

A future implementation MUST NOT infer that generation compatibility alone proves state integrity.

### 6.1 State-version ownership

The State Authority is the authoritative owner of accepted state-version advancement.

A caller MUST NOT select an arbitrary resulting canonical `state_version` merely by supplying a value in a candidate payload. The implementation MUST derive or validate the resulting version according to the State Authority's sequencing rule.

## 7. Checkpoint Semantics

A checkpoint is an accepted recovery point, not merely an arbitrary serialized snapshot.

A valid checkpoint MUST have sufficient metadata to establish, at minimum:

- generation identity;
- schema compatibility;
- state version;
- integrity reference;
- checkpoint identity;
- acceptance status.

Checkpoint creation MUST occur only from valid canonical state.

Checkpoint identity MUST be immutable once the checkpoint is accepted.

Checkpoint deletion/retention policy is implementation-specific and is outside this design phase.

## 8. Restore Semantics

Restore is a controlled state transition and MUST NOT bypass State Authority.

Normative flow:

```text
Requested Recovery Target
          |
          v
Generation validation
          |
          v
Schema compatibility
          |
          v
Integrity validation
          |
          v
Authorization
          |
          v
Candidate restore
          |
          v
Self-test / validation
       /       \
   reject       accept
     |             |
    abort        commit
```

An invalid, incompatible, unauthenticated, or integrity-failed recovery target MUST be rejected without replacing canonical state.

A restore MUST create a new authoritative state revision rather than silently rewriting history or changing the identity of an existing checkpoint.

## 9. Concurrency and Staleness

The implementation MUST define a deterministic rule for concurrent transactions.

At minimum:

- transactions MUST be bound to the state version/generation from which they began;
- commit against a stale canonical state MUST fail closed;
- implicit last-writer-wins behavior MUST NOT be assumed for authoritative state;
- retry MUST require a newly validated transaction rather than silently rebasing an unsafe candidate.

The exact concurrency primitive is intentionally deferred.

## 10. Authorization

State Authority does not replace authorization.

Every mutating operation MUST be subject to the existing default-deny authorization boundary.

The effective security model is:

```text
identity
  + capability
  + operation
  + current generation/state context
  ------------------------------
          authorization
```

No caller may obtain authority by constructing a syntactically valid state object.

Authorization MUST be evaluated against the operation actually requested (including restore/checkpoint operations), not merely against the ability to open a generic transaction.

## 11. Failure and Safe-State Requirements

State Authority MUST prefer preservation of the last known valid canonical state over speculative recovery or partial mutation.

On uncertainty, integrity failure, generation mismatch, authorization failure, malformed state, or incomplete commit, the boundary MUST fail closed.

Recovery into `SAFE_MODE` or `RECOVERY` remains governed by the runtime lifecycle contract; this document does not redefine lifecycle transitions.

## 12. Security Requirements

The State Authority implementation MUST be designed to resist:

- unauthorized state mutation;
- confused-deputy mutation through trusted services;
- stale-generation commits;
- partial writes;
- corrupted checkpoints;
- malicious or malformed serialized state;
- path traversal or arbitrary filesystem access introduced by persistence implementation;
- unsafe deserialization;
- AI-controlled mutation without authorization;
- network-originated direct state mutation;
- rollback to incompatible or unauthenticated state;
- accidental exposure of sensitive state through diagnostics/logging.

Persistence implementations MUST treat serialized state as untrusted input at their deserialization boundary and MUST validate schema, types, bounds, generation, and integrity before candidate acceptance.

Concrete persistence mechanisms MUST undergo a separate security review before adoption.

## 13. Explicit Non-Goals

P0-02 v1.0 does not define or implement:

- SQLite schema or storage engine;
- ZFS datasets/snapshots;
- bootloader state handling;
- systemd appliance integration;
- installer or recovery media;
- update/rollback engine;
- mTLS/network transport;
- hardware entropy source;
- cloud persistence;
- production deployment topology.

## 14. Acceptance Criteria

P0-02 is architecturally accepted only when all of the following are true:

- [ ] canonical state ownership is explicit;
- [ ] candidate/canonical separation is explicit;
- [ ] transaction lifecycle semantics are explicit;
- [ ] commit/abort invariants are explicit;
- [ ] commit linearization point is explicit;
- [ ] state-version advancement is authoritative and atomic with publication;
- [ ] stale transaction behavior is explicit;
- [ ] generation compatibility and integrity validation are separate gates;
- [ ] state version cannot be caller-selected arbitrarily;
- [ ] restore cannot bypass State Authority;
- [ ] restore creates a new accepted state revision;
- [ ] authorization remains default-deny per operation;
- [ ] failure preserves last valid canonical state;
- [ ] deserialization is treated as an untrusted boundary;
- [ ] security boundaries and non-goals are documented;
- [ ] implementation scope is not expanded into concrete persistence infrastructure before architecture acceptance.

## 15. Traceability

| Requirement | P0-02 Design Boundary | Evidence Required Later |
|---|---|---|
| State ownership | Sections 2–3 | Contract + implementation tests |
| Transaction isolation | Section 5 | Runtime tests |
| Atomic commit semantics | Section 5.1 | Runtime/adversarial tests |
| State-version monotonicity | Sections 3, 5, 6.1 | Mutation/concurrency tests |
| Generation binding | Section 6 | Compatibility tests |
| Integrity gate | Section 6 | Integrity tests |
| Checkpoint validity | Section 7 | Checkpoint tests |
| Safe restore | Section 8 | Recovery/adversarial tests |
| Stale transaction rejection | Section 9 | Concurrency tests |
| Default-deny authorization | Section 10 | Authorization tests |
| Fail-closed behavior | Sections 5, 8, 11 | Failure-injection tests |
| Deserialization safety | Section 12 | Malformed-input/security tests |
| Security boundary | Section 12 | Security review + execution evidence |

## 16. Decision Record

**Decision:** establish State Authority as the sole authoritative mutation/recovery boundary and keep persistence technology out of the architecture gate.

**Rationale:** separates semantic authority from storage implementation, prevents premature coupling to SQLite/ZFS, and makes recovery subject to the same authorization, generation, integrity, validation, and atomic-publication boundaries as ordinary mutation.

**Adversarial hardening added in v1.0 draft:** explicit commit linearization, authoritative state-version advancement, immutable checkpoint identity, restore-as-new-revision, operation-specific authorization, and untrusted-deserialization boundary.

**Current state:** Draft. No implementation acceptance implied.
