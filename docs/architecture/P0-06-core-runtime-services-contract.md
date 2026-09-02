# P0-06 — Core Runtime Services Contract v1.0

**Status:** ACCEPTED — IMPLEMENTATION AUTHORIZED
**Depends on:** P0-06 Core Runtime Services Boundary v1.0; P0-05 Consumer Contract (ACCEPTED / FROZEN)

## 1. Contract purpose

Define the logical service contract for Core Runtime Services. The service layer coordinates runtime operations but is not a second state authority.

The responsibilities below do not require separate processes, packages, or public APIs unless a later approved design explicitly chooses them.

## 2. Mandatory delegation path

```text
Service request
      |
      v
P0-05 Consumer Boundary
      |
      v
P0-04 State Authority
```

No P0-06 service may obtain a direct canonical-state mutation path.

## 3. Common service contract

Every P0-06 service operation MUST:

- accept an explicit operation/request type;
- identify the calling principal/capability where authorization is required;
- validate bounded input;
- preserve P0-05 authorization and transaction semantics;
- return bounded, immutable or value-semantic results;
- sanitize externally visible failures;
- fail closed when authorization, freshness, validation, or required state conditions are not satisfied.

Services MUST NOT self-grant capabilities or reinterpret P0-04 generation/version semantics.

## 4. Lifecycle Service

### Responsibility

Provide a controlled runtime lifecycle operation surface using the approved deterministic transition contract.

### Required behavior

- validate requested transition against the allowed transition relation;
- reject invalid transitions without partial state publication;
- construct only explicitly authorized P0-05 requests;
- preserve State Authority generation/version semantics;
- propagate failure without hidden retry or rebasing.

### Prohibited behavior

- second lifecycle canonical store;
- direct State Authority mutation;
- implicit transition recovery;
- last-writer-wins publication;
- hidden persistence.

## 5. Runtime Coordination Service

### Responsibility

Sequence and coordinate approved runtime operations.

### Required behavior

- use explicit operation requests;
- preserve transaction isolation and freshness;
- stop or fail closed when a required operation fails;
- never bypass P0-05.

### Prohibited behavior

- canonical state ownership;
- capability escalation;
- implicit transaction rebasing;
- arbitrary command execution;
- network or filesystem side effects.

## 6. Health / Readiness Service

### Responsibility

Expose deterministic, bounded observation of runtime health and readiness.

### Required behavior

- observation-only by default;
- bounded result size and structure;
- immutable/value-semantic response;
- sanitized diagnostic content.

### Prohibited behavior

The observation API MUST NOT expose a mutation primitive, transaction handle, executable callback, or mutable internal state alias.

## 7. Diagnostic Service integration

Diagnostic integration consumes the existing sanitized diagnostic boundary.

It MAY expose bounded observation/reporting data. It MUST NOT gain authority to mutate state, execute commands, access arbitrary files, or transmit data over a network.

New diagnostic data paths require privacy/security review.

## 8. AI and proposal handling

AI-originated proposals are inert data. Validation does not authorize execution.

```text
AI proposal -> validation -> inert request/data -> explicit authorization -> P0-05
```

No P0-06 service may provide a proposal-to-execution shortcut.

## 9. Plugin interaction

Plugin interaction remains capability-scoped. A plugin request is data until explicit authorization is established. P0-06 does not implement the full plugin subsystem.

## 10. Concurrency and freshness

P0-06 MUST preserve P0-05 transaction isolation, generation binding, freshness checks, and fail-closed stale handling.

There is no implicit rebasing and no last-writer-wins rule.

## 11. Resource bounds

Requests, identifiers, diagnostic payloads, lifecycle inputs, and service responses MUST have explicit structural and size limits appropriate to their contract.

Unbounded recursion, uncontrolled object copying, and arbitrary user-defined executable objects are prohibited at service boundaries.

## 12. Error contract

Externally visible errors MUST use stable sanitized categories. They MUST NOT expose secrets, credentials, sensitive state, internal filesystem paths, stack traces, or private implementation objects.

## 13. Persistence and external capability exclusion

This contract does not authorize:

- durable persistence;
- database/SQLite/ZFS storage;
- durable checkpoints;
- network transport or mutation;
- subprocess or shell execution;
- arbitrary filesystem mutation;
- bootloader/systemd/appliance integration;
- installer/recovery/update engine;
- cloud or hardware persistence;
- autonomous AI mutation.

## 14. Contract acceptance rule

Any implementation that violates this contract is outside P0-06 authorization and requires a new governance decision before acceptance.
