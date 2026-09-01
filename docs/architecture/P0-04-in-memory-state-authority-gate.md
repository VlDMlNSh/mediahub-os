# P0-04 — In-Memory State Authority Implementation Gate v1.0

**Status:** Preparation only — implementation authorization pending P0-03 acceptance  
**Depends on:** P0-02 State Authority Design; P0-03 State Authority Contract

## Purpose

Define the controlled implementation boundary before any code mutation is authorized.

## Authorized only after P0-03 acceptance

The implementation phase may introduce only a deterministic in-memory State Authority and its unit/adversarial tests. It must not introduce SQLite, ZFS, filesystem persistence, subprocess execution, network transport, bootloader/systemd appliance behavior, installer/recovery media, update engines, or cloud persistence.

## Required implementation surfaces

1. Canonical state container with immutable read-boundary semantics.
2. Opaque transaction object with explicit lifecycle.
3. Candidate-state isolation.
4. State Authority-owned revision sequencing.
5. Generation compatibility plus independent integrity validation.
6. Operation-specific default-deny authorization.
7. Checkpoint creation from canonical state only.
8. Restore through candidate validation and new-revision publication.
9. Fail-closed stale transaction handling.
10. Sanitized diagnostics and privacy-safe errors.

## Required adversarial tests

- read cannot mutate canonical state;
- candidate mutation is invisible before commit;
- commit publishes one complete revision;
- failed commit preserves canonical state and version;
- abort preserves canonical state and invalidates the transaction;
- terminal transactions cannot be reused;
- caller cannot select resulting state version;
- stale transaction cannot overwrite newer canonical state;
- generation mismatch is rejected;
- integrity failure is rejected independently of compatibility;
- unauthorized begin/commit/snapshot/restore are rejected;
- checkpoint identity remains immutable;
- restore failure preserves prior canonical state;
- successful restore creates a new canonical revision;
- malformed/untrusted state is rejected before acceptance;
- hostile strings remain data and cannot become execution;
- errors/diagnostics do not expose sensitive state.

## Evidence gate

Acceptance requires executed tests against the exact implementation commit, including the full regression suite and targeted P0-04 adversarial tests. Static capability inspection must confirm no newly introduced subprocess, network, arbitrary filesystem-write, dynamic-code-execution, unsafe-deserialization, or AI-direct-mutation capability.

No implementation may be merged into the runtime foundation until P0-04 evidence is complete and separately reviewed.

## Security and privacy boundary

The implementation must preserve least privilege, default-deny authorization, fail-closed behavior, generation binding, integrity validation, untrusted-input handling, sanitized diagnostics, and minimization of sensitive state. It must not create a covert persistence or execution path.

## Exit criteria

- P0-03 formally accepted.
- In-memory implementation passes contract invariants SA-001..SA-014.
- Adversarial suite passes with execution evidence.
- No unresolved high/critical security findings.
- Capability scan shows no prohibited execution/network/persistence capability.
- Architecture traceability updated from contract requirements to executable evidence.
