# P0-04 — State Authority Security Verification Matrix

Status: security verification evidence complete for hardened remediation head; final governance acceptance pending.

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

## Final execution evidence

Evidence was executed on the approved validation environment `mh-dev-01` against exact hardened remediation commit `1279024fc7c20a2eb291c1f5bc5dbf807e2350b0`.

Environment:

- Python 3.12.3
- Linux kernel 6.8.0-138-generic
- x86_64

### Targeted P0-04 regression

Command:

`python3 -m unittest tests.runtime.test_in_memory_state -v`

Result:

- 16 tests
- 16 passed
- 0 failures
- 0 errors
- exit code 0

The targeted suite explicitly verifies the hardened read boundary (`test_read_is_immutable_and_authority_owned_version`) and checkpoint payload immutability (`test_checkpoint_identity_and_payload_are_immutable`), in addition to authorization, isolation, stale-writer, integrity, restore self-test, failure preservation, malformed-input, and terminal-transaction controls.

### Full repository regression

Command:

`python3 -m unittest discover -s tests -t . -p 'test_*.py' -v`

Result:

- 126 tests
- 126 passed
- 0 failures
- 0 errors
- exit code 0

The `-t .` top-level parameter is required for this repository layout because `tests/runtime` is itself a package named `runtime`; without an explicit top-level directory, unittest discovery shadows the implementation package `runtime/` and produces a false import failure.

### Capability inspection

Command:

`grep -RInE 'subprocess|os\\.system|os\\.popen|eval\\(|exec\\(|pickle\\.loads|marshal\\.loads|socket\\.|requests\\.|urllib\\.request|http\\.client|pathlib\\.Path\\.write|shutil\\.' runtime || true`

Result:

- no matches
- read-only inspection
- no prohibited execution, network, unsafe-deserialization, or filesystem-mutation capability detected by this scan

### Repository state integrity

`git rev-parse HEAD` returned:

`1279024fc7c20a2eb291c1f5bc5dbf807e2350b0`

`git status --short --branch` returned the branch synchronized with `origin/remediation/p0-04-security-gates` and no working-tree changes.

## Evidence interpretation

The evidence demonstrates the declared P0-04 implementation/test slice on the exact hardened commit above. It does not by itself constitute governance acceptance.

All 18 SEC-SA controls have implementation/test or capability-inspection mappings in the threat-to-test traceability record. Controls requiring source/capability evidence are treated as passed only for this exact reviewed state.

## Acceptance rule

P0-04 cannot be accepted solely from source inspection or test results. Final acceptance requires security/privacy review, threat-to-test traceability review, residual-risk disposition, evidence-integrity verification, and explicit governance acceptance.

Persistence remains NOT AUTHORIZED.
