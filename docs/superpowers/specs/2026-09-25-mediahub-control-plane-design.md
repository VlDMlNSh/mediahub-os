# MediaHub Control Plane — Reference-Grade Design

**Status:** DESIGN — implementation gated by existing persistence/governance contracts
**Date:** 2026-09-25
**Scope:** autonomous engineering orchestration only

## Goal

Build a durable, recoverable Control Plane that coordinates MediaHub engineering workers without making worker processes, terminals, or LLM context authoritative.

## Authority boundary

The Control Plane owns orchestration state only: nodes, agents, tasks, leases, executions, checkpoints, orchestration events and audit records. It does not replace MH-04 State Authority for product/domain state.

Existing MH-04 remains canonical for governed MediaHub product state. Any future durable orchestration store must be explicitly qualified so it does not become a second product State Authority.

## Architecture

The system is a modular service with API, state machine, scheduler, lease manager, reconciler, policy engine, event journal, audit sink and worker protocol. Production persistence is intended to be transactional and durable; the exact storage technology is selected during implementation planning subject to the existing persistence gate.

The first deployment is single-active-controller. Interfaces must permit later leader ownership without changing task or lease semantics.

## Domain aggregates

- Node: identity, platform, architecture, capabilities, health and lifecycle.
- Agent: worker protocol identity, version, session and observed execution state.
- Task: immutable creation identity plus validated lifecycle transitions, dependencies, requirements and retry policy.
- Lease: ownership, expiry and generation/fencing data.
- Execution: attempt-specific runtime and verification record.
- Checkpoint: versioned recovery point.
- Event: replay/debug record with causation and correlation identities.
- AuditRecord: append-only security/accountability record.

## State transitions

Agent: REGISTERING → ONLINE → IDLE → CLAIMING → BUSY → VERIFYING → IDLE, with DEGRADED, UNHEALTHY, DISCONNECTED, DRAINING and OFFLINE recovery paths.

Task: PENDING → READY → CLAIMED → RUNNING → VERIFYING → SUCCEEDED, with FAILED, RETRY_WAIT, BLOCKED, CANCELLED and EXPIRED paths.

Lease: ACTIVE → RENEWED → EXPIRING → EXPIRED, or RELEASED/REVOKED.

Every transition is validated and records actor, correlation and causation identity.

## Atomic ownership

Claim and lease creation are one governed transaction. A task can have at most one current owner/generation. Lease renewal requires matching owner and generation. Completion requires an unexpired/authorized generation or an explicit recovery transition; stale workers are rejected.

## Reconciliation

The reconciler compares desired and observed orchestration state. It handles offline agents, expired leases, orphaned tasks, missing checkpoints/artifacts, failed verification and incompatible workers. Actions are bounded, idempotent, policy-checked and auditable. Ambiguous ownership fails closed.

## Worker protocol

REGISTER → AUTHENTICATE → ONLINE/IDLE → CLAIM → LEASE → RECEIVED → STARTED → HEARTBEAT/RENEW → CHECKPOINT → RESULT → VERIFY → COMPLETE → IDLE.

Workers reconnect using stable identity and must reconcile before resuming uncertain work.

## Scheduler

Selection considers priority, dependencies, capabilities, health, resource capacity, affinity/anti-affinity, retry budget, age and concurrency. Scheduler never directly executes shell commands.

## Security boundary

API input is schema-validated and authorized before state mutation. Arbitrary task payload is never converted directly to shell execution. Worker execution uses a policy-controlled sandbox/worktree boundary with scoped credentials, allowed paths/commands/network, timeouts and resource limits.

## Events and audit

Events support replay/debugging and carry event_id, timestamp, source, entity, correlation_id and causation_id. Audit records are append-only to ordinary workers and cover administrative and critical state changes. Event delivery never becomes mutation authority.

## Recovery guarantees

Required scenarios: worker crash/reboot, network partition, stale lease, controller restart, database restart, duplicate request/event, GitHub outage, partial execution and failed verification. Recovery must avoid silent task loss and stale-worker completion; uncertain ownership is blocked until reconciled.

## External integrations

GitHub/CI are observation and execution integrations, not runtime source of truth. Their state is imported through validated adapters and represented as observations, events or tasks.

## Observability

Structured logs, metrics, liveness/readiness, correlation IDs, task/lease/agent metrics and audit evidence are first-class outputs. Health must distinguish process liveness from readiness and degraded dependencies.

## Verification strategy

TDD for each state transition and boundary. Integration tests cover API+store, registration+heartbeat, claim+lease, scheduler, worker protocol and events. E2E proves create→schedule→claim→execute→verify→record. Failure tests prove recovery and stale-writer rejection. Chaos and soak testing are release gates, not post-release aspirations.

## Governance gate

The repository currently contains an accepted MH-04 in-memory State Authority contract and a separate persistence implementation gate marked BLOCKED/NOT AUTHORIZED. This design does not override either. Before production durable implementation, the orchestration persistence boundary, transaction semantics, crash recovery, migration, backup/restore and authority relationship must receive the required governance acceptance.

## Definition of design completion

This design is complete when the implementation plan maps every requirement to a focused component and test, contains no unresolved authority contradiction, and explicitly marks governance-blocked work.
