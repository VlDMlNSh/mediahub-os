# P0-05 — State Authority Integration Boundary v1.0

## Status

DRAFT ARCHITECTURE — GOVERNANCE REVIEW REQUIRED

P0-04 In-Memory State Authority remains ACCEPTED/FROZEN. This document defines the next integration boundary only; it does not modify P0-04 semantics or authorize persistence.

## Objective

Define how runtime consumers interact with the frozen State Authority without bypassing its authority boundary or acquiring implicit mutation rights.

## Core rule

**All canonical state mutation remains exclusively owned by State Authority.**

Consumers may read canonical state through the contract, request an authorized transaction, operate on an isolated candidate, and commit through State Authority. No consumer receives a direct canonical-state mutation primitive.

## Consumer classes

- Runtime services: may read and request explicitly authorized state operations.
- UI/presentation: read-only with respect to canonical state; user intent must become an authorized operation request.
- Plugins/extensions: capability-scoped and default-deny; no direct authority over canonical state.
- AI/proposal systems: proposal/data only; never executable authority and never direct State Authority mutation.
- Diagnostics/telemetry: observational only; no state mutation path.
- Future persistence adapters: architectural boundary only; inactive and unimplemented in P0-05.

## Operation boundary

Consumer → operation request → authorization decision → State Authority transaction → candidate mutation → validation → generation/integrity checks → commit → canonical revision.

A rejected authorization, validation, generation, integrity, or commit condition fails closed and preserves canonical state.

## Read boundary

Reads expose a consistent canonical revision through an immutable read boundary. Consumers must not receive mutable aliases to authority-owned structures.

## Proposal boundary

An AI or external proposal is inert data. It may be inspected, validated and transformed into an explicit user/system operation request, but it cannot execute, commit, select a revision, bypass authorization, or mutate canonical state.

## Error/privacy boundary

Consumer-visible failures must be sanitized and must not disclose secrets, sensitive state, internal authorization material, or filesystem/network details. Internal diagnostic detail remains subject to the existing diagnostics security boundary.

## Concurrency

Consumers must treat transactions as isolated and generation/version-bound. Stale transactions are rejected; last-writer-wins behavior is prohibited.

## Explicit non-goals

P0-05 does not implement or authorize:

- SQLite, ZFS, filesystem persistence, or durable state;
- cryptographic/durable checkpoint authenticity;
- bootloader/systemd/appliance integration;
- installer/recovery media;
- update engine;
- network transport or remote mutation;
- cloud or hardware persistence;
- production deployment qualification.

## Security and privacy requirements

1. Default-deny authorization is preserved at every consumer boundary.
2. No consumer may construct or forge an authoritative transaction/checkpoint accepted by State Authority.
3. Consumer APIs must preserve immutable read boundaries and candidate isolation.
4. External/AI input is treated as untrusted data.
5. Resource limits apply before expensive processing.
6. No arbitrary command execution, network initiation, filesystem mutation, or unsafe deserialization is introduced by integration APIs.
7. Personal-data-bearing inputs require classification and minimization before any future durable boundary is considered.

## Acceptance criteria

P0-05 may not proceed to implementation acceptance until governance approves this boundary and its threat/test traceability. Any implementation must have exact-commit execution evidence, targeted and full regression, capability inspection, privacy/security negative tests, and explicit governance disposition.

## Change control

Any change that expands consumer authority, introduces persistence, or weakens State Authority exclusivity requires a new controlled architecture/security/governance decision. P0-04 remains frozen independently of P0-05.
