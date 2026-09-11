# MediaHub OS — State / HA Integration Contract

Date: 2026-09-11
Status: ACCEPTED ARCHITECTURAL BASELINE

## Decision

PostgreSQL is the durable transactional state store. etcd is the coordination substrate. NATS/JetStream is the asynchronous transport. MediaHub State Authority is the only domain authority.

No component is allowed to infer authority from infrastructure leadership alone.

## Write path

```text
Client / Agent
    -> Command API
    -> State Authority validation
    -> PostgreSQL transaction
    -> durable state + outbox record
    -> commit
    -> event publication
    -> consumers
```

The transaction boundary must guarantee that an accepted state mutation and its publication intent cannot diverge silently. Event publication is asynchronous and consumers must be idempotent.

## Coordination path

```text
State Authority instances
    -> etcd lease / membership
    -> leadership/coordination decision
    -> active writer role
```

etcd loss must not manufacture domain state. If required quorum/lease state cannot be established, mutating operations fail closed or enter explicitly defined degraded mode.

## Event path

```text
PostgreSQL committed state
    -> outbox dispatcher
    -> NATS/JetStream
    -> versioned MediaHub event
    -> idempotent consumers
```

NATS is not the authoritative source. Consumers must tolerate duplicate delivery, reconnects and bounded redelivery.

## Read path

Read models may be cached or asynchronously projected, but authoritative reads for correctness-sensitive operations must resolve against MediaHub State Authority / PostgreSQL.

## HA invariants

- exactly one authoritative mutation path at a time;
- split-brain protection is mandatory;
- leadership expiration is fail-closed;
- stale writers cannot commit authoritative state;
- every state mutation has a monotonic version/revision;
- events carry entity identity, revision, event identity and schema version;
- replay must be safe;
- recovery must reconcile persisted state before accepting normal writes.

## Replication decision

PostgreSQL native physical replication remains the default database HA mechanism to be evaluated first. Logical replication is permitted for explicitly justified projections, migration, integration or cross-version use cases, but is not automatically the State Authority HA mechanism. PostgreSQL documents logical replication as publish/subscribe change replication with transactional ordering within a subscription.

## Failure matrix

| Failure | Required behavior |
|---|---|
| PostgreSQL unavailable | no authoritative writes; controlled degraded mode |
| etcd unavailable | no quorum-sensitive leadership changes; fail closed where required |
| NATS unavailable | committed state remains authoritative; events queue/retry via durable outbox |
| consumer unavailable | state remains valid; consumer catches up |
| network partition | prevent split-brain authoritative writes |
| process crash after DB commit | replay publication from outbox |
| duplicate event | idempotent consumer ignores/reconciles duplicate |
| stale leader | rejected authoritative write |
| restore | verify state, reconcile revisions, then reopen writes |

## Acceptance gates

1. crash between DB commit and event publish;
2. duplicate event delivery;
3. leader loss and lease expiry;
4. network partition / split-brain attempt;
5. PostgreSQL restart;
6. NATS restart;
7. etcd restart;
8. full node loss;
9. restore from backup;
10. deterministic recovery to a single authoritative state.
