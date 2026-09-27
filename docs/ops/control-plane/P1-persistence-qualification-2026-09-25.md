# P1 Persistence Qualification — 2026-09-25

## Decision

`BLOCKED / NOT AUTHORIZED`

The existing `architecture/PERSISTENCE-IMPLEMENTATION-GATE-v1.0.md` remains authoritative for durable persistence authorization. No database implementation is introduced by this qualification record.

## Required invariants for a future adapter

1. Claim and lease creation are atomic.
2. A committed task cannot disappear silently across controller restart.
3. A stale lease generation cannot write completion state.
4. Replayed event and idempotency identities are harmless.
5. Recovery never promotes an unqualified cache, backup, replica, or event stream into canonical authority.
6. Schema migrations are versioned, validated, reversible where supported, and tested against restart/recovery scenarios.
7. Backup restore is verified before it is considered recoverable state.
8. Corruption is detected and fails closed rather than being silently repaired into authoritative state.

## Required evidence before implementation authorization

- transaction and crash-consistency design;
- recovery source-of-truth decision;
- migration compatibility matrix;
- backup/restore procedure and restore test;
- encryption/key lifecycle design;
- duplicate/replay tests;
- corruption/quarantine tests;
- authority-boundary tests;
- documented RPO/RTO;
- governance acceptance recorded against the existing gate.

Until these conditions are accepted, the in-memory repository remains test-only and must not be described as durable production persistence.
