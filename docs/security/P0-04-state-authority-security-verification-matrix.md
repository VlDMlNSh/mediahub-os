# P0-04 — State Authority Security Verification Matrix

Status: implementation verification in progress.

This matrix is governance/evidence guidance only. It does not authorize persistence or production deployment.

## Scope

Authorized scope is deterministic in-memory State Authority only.

Explicitly out of scope and unauthorized:

- SQLite or other persistence
- ZFS/filesystem persistence
- subprocess or arbitrary command execution
- network transport
- bootloader/systemd appliance integration
- installer/recovery media
- update engine
- cloud persistence
- hardware persistence

## Verification items

- SEC-SA-01 — single State Authority mutation path
- SEC-SA-02 — candidate isolation
- SEC-SA-03 — atomic publication
- SEC-SA-04 — failure preservation
- SEC-SA-05 — stale writer rejection
- SEC-SA-06 — generation binding
- SEC-SA-07 — independent integrity gate
- SEC-SA-08 — default-deny authorization
- SEC-SA-09 — restore isolation
- SEC-SA-10 — checkpoint identity protection
- SEC-SA-11 — malformed/untrusted input rejection
- SEC-SA-12 — structural/resource bounds
- SEC-SA-13 — diagnostic/privacy protection
- SEC-SA-14 — no execution primitive
- SEC-SA-15 — no network primitive
- SEC-SA-16 — no arbitrary filesystem mutation
- SEC-SA-17 — no unsafe deserialization
- SEC-SA-18 — no AI/external mutation authority

## Evidence status

Exact implementation commit: `d872196224affbfb3ef2dde21a896444e365c2f9`

Execution environment:

- Python 3.12.3
- Linux `mh-dev-01`, kernel 6.8.0-138-generic, x86_64

Full repository regression captured from the exact implementation branch:

- `python3 -m unittest discover -s tests -v`
- 99 tests
- 0 failures
- 0 errors
- exit code 0

The targeted P0-04 suite and focused adversarial execution remain required before final acceptance.

## Capability inspection note

A repository-wide read-only grep was executed. Its only match was a hostile-input test fixture containing the literal string `subprocess.run()`. This is test data, not an execution capability. The implementation itself must continue to be inspected independently for prohibited imports/capabilities.

## Acceptance rule

P0-04 cannot be accepted solely from source inspection or the full regression result. Final acceptance requires exact-commit targeted/adversarial execution evidence, security/privacy review, and explicit governance acceptance.
