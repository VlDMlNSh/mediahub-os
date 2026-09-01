# P0-04 — Negative Test Oracle v1.0

Status: PREPARED / NON-AUTHORIZING

## Purpose

Define expected fail-closed outcomes for the future P0-04 in-memory State Authority implementation. This is a test oracle, not implementation code and not authorization.

## Oracle rules

A negative test passes only when the attempted operation is rejected and the canonical state remains unchanged unless the contract explicitly defines a successful new revision.

Tests must assert both the rejection result and preservation/non-mutation properties.

## Required negative cases

| ID | Attempt | Expected result | Canonical-state expectation |
|---|---|---|---|
| NEG-01 | unauthorized read/mutation operation | authorization denied | unchanged |
| NEG-02 | stale transaction commit | stale rejection | unchanged |
| NEG-03 | generation mismatch | generation rejection | unchanged |
| NEG-04 | integrity validation failure | integrity rejection | unchanged |
| NEG-05 | malformed candidate | validation rejection | unchanged |
| NEG-06 | caller-selected state version | rejected | authority retains sequencing |
| NEG-07 | commit after abort | terminal-state rejection | unchanged |
| NEG-08 | repeated commit | terminal-state rejection | no duplicate revision |
| NEG-09 | restore without restore authorization | authorization denied | unchanged |
| NEG-10 | invalid checkpoint | checkpoint rejection | unchanged |
| NEG-11 | tampered/untrusted checkpoint material | authenticity/integrity rejection | unchanged |
| NEG-12 | candidate observed through canonical read before commit | candidate must be invisible | unchanged |
| NEG-13 | oversized/resource-bound input | bounded rejection | unchanged |
| NEG-14 | hostile string payload | treated as data, not executable input | unchanged |
| NEG-15 | unsafe serialized/object payload | rejected by safe validation boundary | unchanged |
| NEG-16 | diagnostic containing nested sensitive fields | sanitized output | no sensitive disclosure |
| NEG-17 | AI/external proposal presented as mutation command | no mutation primitive available | unchanged |
| NEG-18 | transaction reuse after terminal state | rejected | unchanged |

## Positive/negative pairing

Where possible, each negative test must be paired with a neighboring positive test proving that the rejection is not caused by an over-broad implementation failure. For example, a valid transaction should commit while a stale transaction is rejected.

## Concurrency oracle

For competing transactions bound to the same observed canonical revision, at most the contract-permitted successful publication may advance the canonical state. A transaction that becomes stale must fail closed and must not overwrite or partially alter the winner's revision.

## Privacy oracle

Negative-path assertions must inspect exceptions and diagnostics for secrets, credentials, tokens, raw voice/audio payloads, and unnecessary personal data. Fixtures use synthetic values only.

## Capability oracle

The implementation must not expose or introduce primitives for subprocess execution, arbitrary command execution, network transport, arbitrary filesystem mutation, unsafe deserialization, or AI-driven canonical mutation.

## Evidence requirement

Each executed oracle case must record the exact immutable implementation commit, command, exit code, environment/toolchain, test result, and relevant state-preservation assertion. A source-code statement alone is not execution evidence.

## Scope

P0-04 remains deterministic in-memory only. Persistence, SQLite, ZFS, filesystem durability, production privileges, network/mTLS, bootloader/systemd appliance integration, installer/recovery media, update engine, cloud persistence, and hardware persistence require later separately authorized gates.
