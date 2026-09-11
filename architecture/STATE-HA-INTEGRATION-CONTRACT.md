# MediaHub OS — State / HA Integration Contract

Date: 2026-09-11
Status: PROPOSED FUTURE EXTENSION — NOT CURRENT RUNTIME AUTHORITY

## Governing constraint

This document does not override MH-03/P0-04. The current frozen runtime foundation remains single-node, in-memory State Authority, with no physical persistence authorized in the current foundation.

The contract below defines a future HA/persistence target only. It may become active only after an explicit governance change, compatibility review, acceptance and freeze. Until then it is not an implementation requirement and must not be used to introduce PostgreSQL, etcd or NATS as the current State Authority.

## Target architecture under governance review

PostgreSQL = durable transactional persistence candidate.
etcd = coordination candidate.
NATS/JetStream = asynchronous transport candidate.
MediaHub State Authority = the only domain authority.

No infrastructure component may infer domain authority from infrastructure leadership.

## Target write path

```text
Client / Agent
    -> Command API
    -> State Authority validation
    -> transactional persistence candidate
    -> durable state + outbox record
    -> commit
    -> event publication
    -> consumers
```

The target transaction boundary must prevent accepted state mutation and publication intent from diverging silently. Event publication remains asynchronous and consumers must be idempotent.

## Target coordination path

```text
State Authority instances
    -> coordination candidate lease / membership
    -> leadership decision
    -> single active writer role
```

Coordination loss must never manufacture domain state. If quorum/lease state cannot be established, authoritative mutation must fail closed.

## Target event path

```text
Committed authoritative state
    -> outbox dispatcher
    -> NATS/JetStream candidate
    -> versioned MediaHub event
    -> idempotent consumers
```

The message broker is not authoritative. Consumers must tolerate duplicate delivery, reconnects and bounded redelivery.

## Target invariants

- exactly one authoritative mutation path at a time;
- split-brain protection;
- leadership expiration is fail-closed;
- stale writers cannot commit authoritative state;
- state mutations have monotonic revision semantics;
- events carry entity identity, revision, event identity and schema version;
- replay is safe;
- recovery reconciles persisted state before normal writes reopen.

## Target replication

If persistence is later authorized, PostgreSQL native physical replication is the first mechanism to evaluate for database HA. Logical replication remains reserved for explicitly justified projection, migration, integration or cross-version cases and is not itself the State Authority.

## Failure acceptance gates for future activation

1. crash between persistence commit and event publish;
2. duplicate event delivery;
3. leader loss and lease expiry;
4. network partition / split-brain attempt;
5. database restart;
6. broker restart;
7. coordination restart;
8. full node loss;
9. restore from verified backup;
10. deterministic recovery to one authoritative state;
11. compatibility review against frozen P0-03/P0-04/P0-05/P0-06;
12. explicit governance approval before activation.
