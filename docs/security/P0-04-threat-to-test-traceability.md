# P0-04 — Threat-to-Test Traceability v1.0

Status: execution-backed security traceability complete for hardened remediation head; final governance acceptance pending.

## Scope

This matrix covers only the deterministic in-memory State Authority authorized by P0-03/P0-04. It does not authorize persistence, network transport, subprocess execution, filesystem mutation, appliance integration, installer/recovery media, update engine, cloud persistence, or hardware persistence.

The matrix distinguishes implementation intent from executed evidence. A mapped test is execution evidence only when it has run successfully against the exact implementation commit under review.

## Traceability

| Control | Threat / abuse case | Contract / invariant | Verification | Current disposition |
|---|---|---|---|---|
| SEC-SA-01 | Bypass State Authority and mutate canonical state directly | SA-001 Single authority | read/commit boundary inspection; `test_read_is_immutable_and_authority_owned_version` | PASS for reviewed in-memory implementation |
| SEC-SA-02 | Candidate mutation becomes visible before commit | SA-002 Isolation | `test_read_is_immutable_and_authority_owned_version`, `test_stale_transaction_rejected_and_canonical_preserved` | PASS |
| SEC-SA-03 | Partial publication exposes mixed revision | SA-003 Atomic publication | `test_concurrent_commits_are_serialized_and_one_stales`, commit revision assertions | PASS for in-memory atomic publication; persistence crash atomicity out of scope |
| SEC-SA-04 | Failed mutation corrupts canonical state | SA-004/012 | abort, integrity, invalid-checkpoint and self-test failure tests | PASS |
| SEC-SA-05 | Stale writer overwrites newer state | SA-006 | `test_stale_transaction_rejected_and_canonical_preserved`, `test_concurrent_commits_are_serialized_and_one_stales` | PASS |
| SEC-SA-06 | Transaction or checkpoint crosses generation boundary | SA-006 | transaction generation checks and restore generation validation | PASS for implemented generation gate |
| SEC-SA-07 | Compatible state bypasses integrity validation | SA-007 | `test_integrity_is_independent_gate`, invalid checkpoint integrity test | PASS |
| SEC-SA-08 | Unauthorized operation changes state | SA-010/014 | `test_default_deny_is_preserved_per_operation` | PASS |
| SEC-SA-09 | Restore mutates canonical before validation/self-test | SA-008/012 | `test_restore_requires_self_test_and_preserves_canonical_on_failure`, `test_restore_self_test_exception_fails_closed` | PASS |
| SEC-SA-10 | Checkpoint identity or payload is altered after snapshot | SA-009 | `test_checkpoint_identity_and_payload_are_immutable` | PASS; hardened read/checkpoint boundary executed |
| SEC-SA-11 | Malformed/untrusted state reaches canonical storage | SA-013 | `test_malformed_and_oversized_state_is_rejected`, forged checkpoint test | PASS |
| SEC-SA-12 | Resource exhaustion through oversized/deep state | SA-012 | `test_malformed_and_oversized_state_is_rejected` | PASS for declared structural bounds |
| SEC-SA-13 | State or internal failure details leak through read/errors | Security/privacy boundary | `test_restore_self_test_exception_fails_closed`, hostile-data test; foundation diagnostics tests | PASS for demonstrated boundaries |
| SEC-SA-14 | State layer gains command/subprocess execution | SA-011 | read-only capability scan over `runtime/` plus hostile-string test | PASS for reviewed source tree; scan returned no matches |
| SEC-SA-15 | State layer gains network capability | SA-011 | read-only capability scan over `runtime/` | PASS for reviewed source tree; scan returned no matches |
| SEC-SA-16 | State layer mutates arbitrary filesystem | SA-011 | read-only capability scan over `runtime/` plus hostile-string test | PASS for reviewed source tree; scan returned no matches |
| SEC-SA-17 | Unsafe deserialization becomes mutation path | SA-013 | read-only capability scan; no deserialization primitive in implementation | PASS for reviewed source tree; scan returned no matches |
| SEC-SA-18 | AI/external input gains direct mutation authority | SA-011 | AI contract suites + State Authority boundary inspection | PASS for reviewed boundary; AI tests remain distinct from State Authority mutation evidence |

## Exact execution evidence

Executed on approved validation environment `mh-dev-01` against exact commit `1279024fc7c20a2eb291c1f5bc5dbf807e2350b0`.

Environment:

- Python 3.12.3
- Linux kernel 6.8.0-138-generic
- x86_64

Targeted P0-04:

- `python3 -m unittest tests.runtime.test_in_memory_state -v`
- 16/16 passed
- 0 failures
- 0 errors
- exit code 0

Full repository:

- `python3 -m unittest discover -s tests -t . -p 'test_*.py' -v`
- 126/126 passed
- 0 failures
- 0 errors
- exit code 0

Capability scan:

- exact prescribed read-only grep over `runtime/`
- no matches

Repository integrity:

- HEAD exactly `1279024fc7c20a2eb291c1f5bc5dbf807e2350b0`
- branch synchronized with `origin/remediation/p0-04-security-gates`
- no working-tree changes

## Security disposition

All SEC-SA-01 through SEC-SA-18 controls now have implementation mappings and exact-commit execution evidence or explicit source/capability evidence where the control is negative-capability based.

The following are **not** claimed by this disposition:

- durable/cryptographic checkpoint authenticity;
- crash-consistent persistent atomicity;
- durable retention/deletion/export controls;
- appliance/boot/update/recovery guarantees;
- persistent personal-data protection.

Those properties require future controlled phases and remain unauthorized here.

## Governance rule

Security traceability completion is not P0-04 governance acceptance. Final acceptance still requires evidence-integrity verification, residual-risk disposition, and explicit governance approval.

Persistence remains NOT AUTHORIZED.
