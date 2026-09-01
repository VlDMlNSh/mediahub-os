# P0-04 — In-Memory State Authority Implementation Workplan v1.0

**Status:** Prepared / blocked on formal P0-03 acceptance  
**Branch:** `architecture/p0-04-in-memory-state-authority`

## Purpose

Translate the accepted P0-03 contract into a bounded implementation sequence without granting implementation authorization prematurely.

## Phase sequence

### P0-04.1 Contract model
- Define immutable canonical-state representation.
- Define opaque transaction lifecycle representation.
- Define checkpoint representation with immutable identity.
- Keep payloads structurally bounded and validation-oriented.

### P0-04.2 Read / begin / abort
- `read` exposes one complete canonical revision.
- `begin` captures observed generation/state version and creates an isolated candidate.
- `abort` invalidates the candidate and leaves canonical state/version unchanged.

### P0-04.3 Commit
- Validate transaction lifecycle and authorization.
- Reject stale generation/state version.
- Validate schema, structure, bounds, compatibility and independent integrity.
- Publish exactly one complete canonical revision.
- Advance state version only under State Authority control.

### P0-04.4 Snapshot / restore
- Snapshot only from canonical state.
- Preserve immutable checkpoint identity.
- Restore through authorization, authenticity/integrity, generation/schema validation, candidate isolation and self-test.
- Successful restore publishes a new canonical revision.
- Failed restore never replaces canonical state.

### P0-04.5 Adversarial verification
- Transaction reuse and terminal-state attacks.
- Stale writer and concurrent transaction attacks.
- Caller-controlled revision attacks.
- Candidate leakage / partial publication attacks.
- Generation/integrity confusion attacks.
- Checkpoint substitution/tampering boundary tests.
- Unauthorized operation tests.
- Malformed/untrusted state and resource-bound tests.
- Sensitive diagnostic/error leakage tests.

## Evidence requirements

Execution evidence must identify the exact implementation commit and environment. Minimum evidence:

1. Full existing regression suite.
2. Complete P0-04 targeted/adversarial suite.
3. Capability inspection for subprocess/network/arbitrary filesystem writes/dynamic execution/unsafe deserialization/direct AI mutation.
4. Failure-path tests demonstrating canonical-state preservation.
5. Concurrency/stale-transaction evidence where applicable.
6. Privacy/security review of diagnostics and exceptions.

## Hard boundaries

This workplan does not authorize implementation. Until P0-03 is formally accepted, no runtime implementation changes are permitted under this gate.

Even after authorization, this phase excludes SQLite, ZFS, filesystem persistence, cloud persistence, subprocesses, network transport, bootloader/systemd appliance behavior, installer/recovery media, update engine and production deployment topology.

## Exit condition

P0-04 may exit only when implementation evidence and adversarial review demonstrate the P0-03 contract invariants without introducing prohibited capabilities or unresolved high/critical security findings.
