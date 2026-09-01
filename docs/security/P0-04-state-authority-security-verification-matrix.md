# P0-04 — State Authority Security Verification Matrix v1.0

**Status:** Prepared / non-authorizing
**Scope:** deterministic in-memory State Authority only
**Governance dependency:** P0-03 formal acceptance is still required before runtime implementation.

## Purpose

Provide a security/privacy verification matrix for P0-04 so implementation evidence can be collected without expanding the approved boundary.

## Verification matrix

| ID | Property | Required evidence | Failure disposition |
|---|---|---|---|
| SEC-SA-01 | Single authority | No alternate canonical mutation path in implementation | Block P0-04 |
| SEC-SA-02 | Candidate isolation | Pre-commit reads never expose candidate state | Block P0-04 |
| SEC-SA-03 | Atomic publication | Readers observe complete revisions only | Block P0-04 |
| SEC-SA-04 | Failure preservation | Failed commit/restore leaves prior canonical state unchanged | Block P0-04 |
| SEC-SA-05 | Stale writer rejection | Stale generation/state version cannot overwrite canonical state | Block P0-04 |
| SEC-SA-06 | Generation binding | Caller cannot select or bypass authoritative generation | Block P0-04 |
| SEC-SA-07 | Independent integrity gate | Integrity failure cannot be converted into compatibility success | Block P0-04 |
| SEC-SA-08 | Default-deny authorization | Unauthorized operation is rejected for every State Authority operation | Block P0-04 |
| SEC-SA-09 | Restore isolation | Restore validates before publication and creates a new revision | Block P0-04 |
| SEC-SA-10 | Checkpoint identity | Accepted checkpoint identity cannot be mutated by restore/commit | Block P0-04 |
| SEC-SA-11 | Untrusted input | Malformed/untrusted state remains data and is rejected safely | Block P0-04 |
| SEC-SA-12 | Resource bounds | Oversized/deep/hostile structures are bounded or rejected | Block P0-04 |
| SEC-SA-13 | Diagnostic privacy | Sensitive state is not emitted through errors/diagnostics | Block P0-04 |
| SEC-SA-14 | No execution primitive | No subprocess, shell, dynamic execution, or arbitrary command path | Block P0-04 |
| SEC-SA-15 | No network primitive | No network transport or externally controlled mutation path | Block P0-04 |
| SEC-SA-16 | No arbitrary filesystem mutation | State Authority cannot write arbitrary filesystem paths | Block P0-04 |
| SEC-SA-17 | No unsafe deserialization | No unsafe object reconstruction/deserialization primitive | Block P0-04 |
| SEC-SA-18 | No AI mutation | AI/proposal inputs cannot directly mutate canonical state | Block P0-04 |

## Evidence package

The implementation gate must record:

1. exact implementation commit;
2. environment and toolchain;
3. full regression result;
4. complete targeted/adversarial result;
5. capability inspection result;
6. failure-path evidence;
7. stale/concurrency evidence;
8. privacy/security inspection;
9. unresolved findings and disposition.

## Explicit exclusions

This matrix does not authorize SQLite, ZFS, filesystem persistence, cloud persistence, subprocesses, network transport, bootloader/systemd appliance behavior, installer/recovery media, update engine, or production deployment topology.

## Governance rule

A completed matrix is evidence preparation, not implementation authorization and not formal acceptance of P0-03 or P0-04.
