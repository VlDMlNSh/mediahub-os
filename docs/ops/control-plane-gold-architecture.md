# MediaHub Control Plane — GOLD architecture contract

## Authority
SQLite is the authoritative persistent state store. GitHub is transport/integration, not runtime truth.

## Runtime components
- tasks, executions, leases, generations, events and audit are durable state.
- scheduler selects only eligible tasks and dependencies.
- reconciler repairs expired, failed and ambiguous state deterministically.
- workers execute under fenced leases.
- provider gateway owns provider routing and failure classification.
- agent registry exposes host/agent capability state.
- command bus accepts only bounded control commands and is singleton-fenced.
- Astra supervisor observes and reconciles execution lanes; STOP does not destroy state authority.
- metrics/heartbeat expose queue, worker, lease, model and resource health.
- backup/recovery is fail-closed and never overwrites an existing restore target.

## Task lifecycle
DISCOVER → PLAN → READY → SELECT → CLAIM → EXECUTE → VERIFY → RECORD → COMMIT → PUSH → QUALIFY → CLOSE → GENERATE_NEXT

Every transition requires durable evidence. `DONE` is not a free-form status: it requires implementation evidence, verification, tests, required qualification, evidence and a durable record.

## External operations
External operation identity is `(operation_key)`. RESOLVED operations are executor-side deduplicated. Ambiguous transport is fail-closed unless replay is explicitly authorized.

## Fencing and recovery
Leases use generations. Expired ownership cannot complete a newer generation. Reconciliation is idempotent and must not manufacture attempts. Crash recovery restores durable state before resuming execution.

## Model qualification
A model is routable only when its registry record is qualified for the requested capability/task class. Discovery produces qualification work; it does not grant execution authority.

Qualification contract:
DISCOVER → DOWNLOAD → VERIFY → RESOURCE CHECK → HEALTH CHECK → GENERATION TEST → CODING TEST → PATCH TEST → TEST EXECUTION → QUALIFICATION → REGISTER

## Safety boundaries
AI output is untrusted. Model output cannot directly become unrestricted shell execution. Destructive, credential-bearing and irreversible operations remain behind explicit approval boundaries.

## GOLD evidence
A release claim requires fresh test evidence, qualification evidence, recovery evidence, independent verification and a durable acceptance record. Long-running soak, physical reboot and distributed-host gates remain open until actually executed.
