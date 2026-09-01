# P0-04 — Implementation Evidence Template v1.0

## Status

**Prepared — evidence collection only.**

This artifact defines the evidence package that must accompany any authorized P0-04 implementation. It does not authorize implementation and does not change the P0-03 formal acceptance state.

## 1. Governance prerequisites

- P0-03 formal acceptance: `ACCEPTED` required before implementation.
- P0-04 implementation gate: `AUTHORIZED` required.
- Exact implementation commit: record immutable SHA.
- Scope review: confirm no persistence, network, subprocess, bootloader/systemd, installer/recovery, update-engine, cloud, or hardware-persistence capability.

## 2. Environment identity

Record:

- host identifier
- operating system/kernel
- Python/runtime version
- repository and branch
- exact commit SHA
- working-tree status
- relevant dependency/tool versions

## 3. Functional evidence

| ID | Invariant | Required evidence | Result |
|---|---|---|---|
| SA-001 | Single authority | API/code inspection + tests | PENDING |
| SA-002 | Candidate isolation | pre-commit visibility test | PENDING |
| SA-003 | Atomic publication | complete revision publication test | PENDING |
| SA-004 | Monotonic version | sequential commit tests | PENDING |
| SA-005 | No caller-selected revision | adversarial test | PENDING |
| SA-006 | Generation binding | mismatch tests | PENDING |
| SA-007 | Independent integrity gate | integrity failure tests | PENDING |
| SA-008 | Restore isolation | failed/successful restore tests | PENDING |
| SA-009 | Checkpoint immutability | identity/material immutability tests | PENDING |
| SA-010 | Default deny | unauthorized operation tests | PENDING |
| SA-011 | No external mutation primitive | capability/code inspection | PENDING |
| SA-012 | Failure preservation | failure-path tests | PENDING |
| SA-013 | Untrusted persistence boundary | malformed/untrusted input tests | PENDING |
| SA-014 | Operation-specific authorization | per-operation authorization tests | PENDING |

## 4. Security evidence

Required negative checks:

- subprocess / arbitrary command execution absent;
- network access absent;
- arbitrary filesystem mutation absent;
- path traversal capability absent;
- dynamic code execution absent;
- unsafe deserialization absent;
- AI/external input cannot directly mutate canonical state;
- authorization remains fail-closed;
- stale transactions cannot overwrite newer state;
- generation mismatch fails closed;
- integrity failure cannot be bypassed;
- diagnostics/errors do not expose sensitive state;
- resource/size bounds are enforced.

## 5. Concurrency evidence

At minimum record deterministic tests for:

- two transactions observing the same revision;
- first valid commit succeeding;
- stale second commit failing closed;
- canonical state remaining equal to the first committed complete revision;
- no partial candidate becoming visible.

If concurrency is not implemented in this phase, record the explicit limitation and corresponding contract boundary rather than claiming concurrency qualification.

## 6. Failure-path evidence

Demonstrate that failed operations preserve:

- canonical payload;
- canonical generation;
- canonical state version;
- integrity status/reference;
- accepted checkpoint identity.

Terminal transaction handles must not be reusable or resurrected.

## 7. Privacy evidence

Verify that:

- sensitive fields are excluded or sanitized from diagnostics;
- exceptions contain no secret/token/credential payloads;
- hostile input remains data and is not interpreted as executable content;
- tests do not require real personal data or production credentials.

## 8. Execution record

For every executed command record:

- exact command;
- working directory;
- exit code;
- relevant stdout/stderr summary;
- test count/result;
- environment identity;
- timestamp.

No evidence may be reconstructed from memory after the fact.

## 9. Acceptance rule

P0-04 is not accepted merely because implementation tests pass. Acceptance requires:

1. formal governance authorization;
2. exact-commit execution evidence;
3. functional and adversarial test evidence;
4. security/privacy inspection;
5. absence of unresolved high/critical findings;
6. confirmation that prohibited capabilities were not introduced;
7. traceability back to P0-03 SA-001..SA-014.

## 10. Explicit non-goals

This evidence package does not qualify:

- SQLite or other persistence;
- ZFS;
- filesystem durability;
- bootloader/systemd appliance behavior;
- installer/recovery media;
- update engine;
- network transport/mTLS;
- cloud persistence;
- hardware persistence;
- production deployment topology.
