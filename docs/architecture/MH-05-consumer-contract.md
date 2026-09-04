# MH-5 — Consumer Contract

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

## Canonical contract

A Consumer Request is a bounded, value-semantic request envelope. It carries only the information required to classify, authorize, execute, and audit one consumer operation.

```text
ConsumerRequest
├── identity
├── context
├── capability
├── operation
├── target
├── payload
├── bounds
├── authorization
├── transaction_context
├── correlation
└── idempotency
```

The execution result is separate:

```text
ConsumerResult
├── outcome
├── value
├── error
├── correlation
└── audit_context
```

## Field semantics

- **identity:** authenticated principal identity and principal type; identity alone grants no authority.
- **context:** caller/service/device/plugin/AI context needed for authorization; must be bounded and non-authoritative.
- **capability:** explicit requested capability; unknown or absent capability is denied for protected operations.
- **operation:** explicit operation identifier; no implicit operation inference from payload.
- **target:** explicit resource/object scope; wildcard authority is prohibited unless a separately governed capability explicitly defines it.
- **payload:** immutable/value-semantic bounded data; executable objects and hidden commands are prohibited.
- **bounds:** validation metadata/constraints applied before expensive processing; implementation must not let callers enlarge authoritative limits.
- **authorization:** result/context of the authorization decision; consumers cannot self-assert an accepted decision.
- **transaction_context:** opaque State Authority transaction reference where applicable; never an internal transaction object.
- **correlation:** bounded request correlation identifier for observability and causation tracing where needed.
- **idempotency:** bounded command identity/deduplication context where the operation supports it; no exactly-once promise is implied.

## Deliberately excluded fields

No consumer contract field grants shell, filesystem, network, database, credential, subprocess, plugin execution, persistence, or direct State Authority access.

Timeout and cancellation are execution-control concerns and may be attached by a governed transport/runtime adapter; they do not grant authority. The transport is not part of the canonical trust model.

## Contract rule

`identity → capability → operation → target → authorization` must be explicit before a mutation-capable command can reach P0-05/P0-04. Malformed, ambiguous, over-bound, stale, or unauthorized requests fail closed.
