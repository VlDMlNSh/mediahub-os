# P0-06 — Core Runtime Services Boundary v1.0

**Status:** DRAFT — GOVERNANCE REVIEW REQUIRED  
**Depends on:** P0-05 State Authority Integration Boundary & Consumer Contract (ACCEPTED / FROZEN)

## Purpose

Define the architectural boundary for the first Core Runtime Services layer without reopening frozen P0-04/P0-05 semantics or introducing persistence, external execution, networking, or appliance infrastructure.

This document is an architecture proposal only. It does not authorize implementation.

## Scope

P0-06 evaluates a minimal service layer around the frozen State Authority integration boundary:

- **Lifecycle Service** — owns runtime lifecycle coordination and validates lifecycle transitions against the existing deterministic lifecycle state machine.
- **Runtime Coordination Service** — coordinates authorized runtime operations without becoming a second state authority.
- **Health / Readiness Service** — exposes bounded observational health/readiness information; it does not mutate canonical state directly.
- **Diagnostic Service integration** — consumes the existing sanitized diagnostics boundary for observation/reporting; it does not gain mutation or execution authority.

These names describe architectural responsibilities, not a commitment that each must become a separate process, package, or public API.

## Boundary

```text
Core Runtime Services
        |
        v
P0-05 Consumer Boundary
        |
        v
Frozen P0-04 State Authority
```

Core Runtime Services MUST NOT create a parallel canonical-state mutation path. State reads, authorized state transactions, and canonical publication remain governed by P0-05 and P0-04.

## Authority model

1. State Authority remains the sole canonical mutation authority.
2. P0-05 remains the consumer authorization and integration boundary.
3. Core Runtime Services may coordinate operations but may not self-grant capabilities.
4. Lifecycle transitions must remain deterministic and fail-closed.
5. Health/readiness and diagnostics are observational unless a separately approved contract explicitly grants a bounded request capability.
6. Service identity, operation, and capability scope are explicit inputs to authorization.

## Required invariants

- **CRT-001 Single state authority:** no service owns a second canonical state store.
- **CRT-002 Boundary preservation:** services access State Authority through P0-05.
- **CRT-003 Default deny:** absent explicit authorization, service operations fail closed.
- **CRT-004 Lifecycle determinism:** invalid lifecycle transitions are rejected without partial transition.
- **CRT-005 Failure preservation:** service failure cannot corrupt canonical state.
- **CRT-006 Observation isolation:** health and diagnostics cannot mutate canonical state through observation APIs.
- **CRT-007 No implicit execution:** service coordination does not imply subprocess, filesystem mutation, network mutation, or arbitrary code execution.
- **CRT-008 Bounded inputs/outputs:** service requests, identifiers, diagnostics, and responses are structurally and size bounded.
- **CRT-009 Sanitized failures:** service-facing errors expose stable categories rather than secrets, sensitive state, credentials, private material, or internal paths.
- **CRT-010 Persistence exclusion:** P0-06 introduces no durable persistence or durable checkpoint implementation.

## Explicit exclusions

P0-06 does not authorize:

- SQLite, ZFS, database or filesystem persistence;
- durable checkpoint storage;
- network transport or network mutation;
- subprocess/process spawning;
- shell or command execution;
- bootloader, systemd, appliance integration;
- installer, recovery, update engine;
- cloud or hardware persistence;
- plugin subsystem implementation;
- AI execution or autonomous mutation;
- production qualification.

## Proposed service responsibilities

### Lifecycle Service

Responsible for presenting a controlled runtime lifecycle operation surface over the existing lifecycle state machine. It must not duplicate or reinterpret State Authority version/generation semantics.

### Runtime Coordination Service

Responsible for sequencing approved runtime operations and coordinating service boundaries. It may issue authorized requests through P0-05 but cannot bypass that boundary or mutate canonical state directly.

### Health / Readiness Service

Responsible for deterministic, bounded observation of runtime health/readiness. It must not expose mutable internal objects or grant a mutation primitive.

### Diagnostic Service integration

Responsible for collecting or exposing already-sanitized diagnostic information within the existing observation boundary. Any new diagnostic data path requires privacy/security review.

## Data-flow rule

External, UI, plugin, diagnostic, and AI-originated data remains data/request until explicitly authorized. AI proposals remain inert data. No P0-06 service may convert a proposal directly into an execution primitive.

## Concurrency

Services must preserve P0-05 transaction isolation, generation binding, freshness checks, and fail-closed stale handling. P0-06 must not introduce last-writer-wins behavior or implicit rebasing.

## Security and privacy

The P0-06 implementation gate must include negative tests for authority bypass, self-granted authorization, mutable aliases, stale operations, lifecycle invalid transitions, oversized/malformed inputs, diagnostic leakage, AI execution paths, plugin capability expansion, arbitrary execution/network/filesystem access, and implicit persistence.

Personal-data-bearing inputs must be minimized. P0-06 does not create a durable personal-data store.

## Governance gate

Implementation requires separate approval of:

1. this architecture boundary;
2. a precise service contract;
3. a threat model;
4. threat-to-test traceability;
5. an implementation entry gate.

Only after those artifacts are reviewed and governance-authorized may an implementation branch be created.

## Change control

Any proposal that changes P0-04 State Authority semantics, P0-05 consumer authority, authorization invariants, persistence scope, or security invariants stops P0-06 and requires a new controlled governance decision.
