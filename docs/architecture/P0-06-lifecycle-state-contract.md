# P0-06 — Lifecycle State Contract v1.0

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED
**Depends on:** P0-04 State Authority (ACCEPTED / FROZEN); P0-05 Consumer Boundary (ACCEPTED / FROZEN); P0-06 Core Runtime Services Contract v1.1
**Governance acceptance:** P0-06 Governance Acceptance v1.1

## 1. Purpose

Define the canonical representation and transition semantics for runtime lifecycle state without modifying P0-04 State Authority semantics.

This document is a P0-06 domain-state contract. It does not authorize implementation outside the accepted P0-06 scope or authorize persistence.

## 2. Canonical representation

Lifecycle state is represented inside the authoritative P0-04 `CanonicalState.payload` under the reserved key `lifecycle`:

```text
payload
└── lifecycle
    └── state: <LifecycleState value>
```

The lifecycle object is value data. It is not a second state store, transaction object, executable object, or mutable alias.

The canonical lifecycle state is therefore obtained only from P0-04 through P0-05.

## 3. Allowed values

The only lifecycle state values are:

- `PROVISIONING`
- `INITIALIZING`
- `SELF_TEST`
- `READY`
- `DEGRADED`
- `SAFE_MODE`
- `RECOVERY`

No free-form lifecycle strings are permitted.

## 4. Transition relation

The approved deterministic relation is:

```text
PROVISIONING -> INITIALIZING
INITIALIZING -> SELF_TEST
SELF_TEST -> READY
SELF_TEST -> DEGRADED
SELF_TEST -> SAFE_MODE
READY -> DEGRADED
READY -> SAFE_MODE
DEGRADED -> READY
DEGRADED -> SAFE_MODE
SAFE_MODE -> RECOVERY
RECOVERY -> INITIALIZING
```

A transition not listed above is invalid and MUST fail closed.

A transition from a state to itself is invalid as a lifecycle transition request.

## 5. Atomic publication

A lifecycle transition is a normal P0-05 transaction against the canonical P0-04 state.

Required sequence:

```text
read authoritative state
        ↓
validate transition relation
        ↓
begin authorized P0-05 transaction
        ↓
re-check the authoritative revision
        ↓
update candidate payload.lifecycle.state
        ↓
commit through P0-05 / P0-04
```

The transition MUST NOT publish a partially updated lifecycle object.

The service MUST NOT mutate a local `LifecycleStateMachine` and then copy its local state into canonical state.

## 6. Concurrency and freshness

The lifecycle transaction inherits P0-04/P0-05 generation and freshness semantics.

If the authoritative state changes after the transaction begins, commit MUST fail closed according to the existing stale-transaction contract. No implicit rebase or last-writer-wins behavior is permitted.

The service additionally rejects a revision change observed between its initial read and transaction establishment rather than rebasing the request onto newer state.

## 7. Authorization

Lifecycle mutation requires explicit authorization through the P0-05 boundary.

The accepted capability identifier is `runtime.lifecycle.transition`.

P0-06 MUST NOT create or self-grant a capability. The underlying P0-04 authorization policy remains the authority for operation grants.

Unauthenticated or insufficiently authorized lifecycle requests MUST be rejected without state mutation.

## 8. Validation boundaries

Lifecycle input MUST be bounded and value-semantic.

The accepted request consists only of:

- one allowed lifecycle target value;
- one explicit `AuthorizationContext` carrying the accepted capability identifier.

No callback, arbitrary object, executable proposal, transaction handle supplied by a caller, filesystem path, network target, or persistence instruction is part of this contract.

## 9. Failure behavior

Invalid transition, authorization failure, stale transaction, malformed state, or commit failure MUST leave canonical lifecycle state unchanged.

Externally visible failures use the existing sanitized P0-05 error contract.

## 10. Existing LifecycleStateMachine

The existing `LifecycleStateMachine` is a deterministic compatibility/validation primitive only.

Its mutable local `.state` MUST NOT be treated as canonical state and MUST NOT be used as an authoritative publication source.

P0-06 implementation MAY use an isolated validator instance initialized from the authoritative current state, provided validation does not mutate canonical state and does not introduce a second lifecycle store.

## 11. Persistence and external capability

This contract authorizes no persistence, network access, filesystem mutation, subprocess execution, boot/system integration, or autonomous AI action.

## 12. Acceptance rule

This document is authoritative for P0-06 lifecycle semantics within the accepted implementation scope. Any change to the transition relation or authorization contract requires a new governance decision before implementation.
