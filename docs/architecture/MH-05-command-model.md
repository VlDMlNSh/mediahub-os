# MH-5 — Command Model

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

## Definition

A **Command** is an explicit request to perform a governed operation. It is not authorization and does not itself contain mutation authority.

```text
Consumer Input
 → classification
 → deterministic validation/bounds
 → identity/context
 → capability
 → authorization
 → Command
 → P0-05
 → P0-04 when canonical mutation is required
```

## Required semantics

A command has an explicit operation, target, bounded immutable payload, authorized context, correlation identity, and governed lifecycle. Its execution result is value-semantic and sanitized.

A command MUST NOT:

- mutate State Authority directly;
- embed executable payloads or callbacks;
- bypass policy or authorization;
- select or manufacture a canonical state version;
- create persistence;
- obtain unrestricted filesystem/network/subprocess access;
- smuggle credentials into the core boundary.

## Validation

Validation occurs before execution and before publication. Unknown operations, unknown capabilities, malformed targets, unsupported payload types, bound violations, stale transaction context, and ambiguous authorization fail closed.

## Retry and delivery

The command model does not claim exactly-once delivery. Duplicate detection may use command identity/idempotency where explicitly supported. Retry, replay, merge, rebase, and last-writer-wins behavior require operation-specific governance; none is implicit.
