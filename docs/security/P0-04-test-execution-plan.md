# P0-04 Test Execution Plan v1.0

Status: PREPARED / BLOCKED ON GOVERNANCE AUTHORIZATION

## Purpose

Define the executable verification sequence for the deterministic in-memory State Authority before implementation begins. This document is a test plan, not implementation authorization.

## Preconditions

1. P0-03 formal governance decision is recorded.
2. P0-04 implementation authorization is explicit.
3. Implementation baseline is an immutable commit derived from the authorized P0-03 baseline.
4. No prohibited capability is introduced.

## Test layers

### Layer 1 — Contract and lifecycle

- canonical read is non-mutating;
- begin creates an isolated active transaction;
- abort preserves canonical state;
- commit transitions the transaction to terminal state;
- terminal transactions cannot be reused;
- malformed transaction handles fail closed.

### Layer 2 — Publication and revision safety

- candidate changes remain invisible before commit;
- successful commit publishes one complete revision;
- failed commit leaves canonical state and state version unchanged;
- state version is authority-owned and monotonic;
- caller-supplied revision numbers cannot control publication.

### Layer 3 — Concurrency and stale writers

- two transactions may observe the same baseline;
- first valid commit succeeds;
- stale second commit is rejected;
- rejected stale commit cannot modify canonical state;
- no implicit last-writer-wins behavior exists.

### Layer 4 — Generation and integrity

- matching generation succeeds;
- generation mismatch fails closed;
- binary/schema/state compatibility is checked independently from integrity;
- integrity failure rejects otherwise compatible state;
- integrity metadata cannot be supplied by an untrusted caller as an unconditional authority.

### Layer 5 — Authorization

Each operation is checked independently:

- read;
- begin/mutate/commit;
- abort;
- snapshot/checkpoint;
- restore.

Missing grants, malformed contexts, and unsupported operations must deny by default.

### Layer 6 — Checkpoint and restore

- snapshot originates only from canonical state;
- checkpoint identity is immutable;
- checkpoint material is untrusted until validation;
- unauthorized restore is rejected;
- invalid restore preserves canonical state;
- successful restore publishes a new canonical revision;
- restore does not rewrite checkpoint identity.

### Layer 7 — Hostile input and privacy

- hostile strings remain data and never become commands;
- malformed structures are rejected without side effects;
- bounded inputs prevent uncontrolled resource growth;
- errors and diagnostics contain no secrets, credentials, tokens, or unnecessary personal data;
- nested sensitive diagnostic fields are redacted.

### Layer 8 — Capability/security inspection

The implementation and tests must be inspected for absence of:

- subprocess/shell execution;
- network transport;
- arbitrary filesystem mutation;
- dynamic code execution;
- unsafe deserialization;
- AI-controlled canonical mutation.

## Evidence requirements

For each execution gate capture:

- exact commit SHA;
- branch;
- environment and toolchain;
- exact command;
- exit code;
- test count and failures/errors;
- relevant stdout/stderr summary;
- security capability scan result;
- timestamp.

Evidence must be captured from execution, not reconstructed afterward.

## Acceptance rule

P0-04 cannot be accepted if any required invariant fails, if execution evidence is missing, if a high/critical security finding remains unresolved, or if prohibited capabilities are present.

## Explicit exclusions

This plan does not authorize or test SQLite, ZFS, filesystem persistence, cloud persistence, network transport, subprocesses, bootloader/systemd appliance behavior, installer/recovery media, update engine, or hardware persistence.
