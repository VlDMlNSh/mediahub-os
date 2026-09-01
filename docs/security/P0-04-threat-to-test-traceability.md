# P0-04 — Threat-to-Test Traceability v1.0

Status: controlled remediation traceability; execution re-validation pending after read-boundary hardening.

## Scope

This matrix covers only the deterministic in-memory State Authority authorized by P0-03/P0-04. It does not authorize persistence, network transport, subprocess execution, filesystem mutation, appliance integration, installer/recovery media, update engine, cloud persistence, or hardware persistence.

The matrix distinguishes implementation intent from executed evidence. A mapped test is not considered execution evidence until it has run successfully against the exact implementation commit under review.

## Traceability

| Control | Threat / abuse case | Contract / invariant | Verification | Current disposition |
|---|---|---|---|---|
| SEC-SA-01 | Bypass State Authority and mutate canonical state directly | SA-001 Single authority | `test_read_is_immutable_and_authority_owned_version`, commit/read behavior | Implementation review; execution pending on hardened commit |
| SEC-SA-02 | Candidate mutation becomes visible before commit | SA-002 Isolation | `test_read_is_immutable_and_authority_owned_version`, `test_stale_transaction_rejected_and_canonical_preserved` | Mapped |
| SEC-SA-03 | Partial publication exposes mixed revision | SA-003 Atomic publication | `test_concurrent_commits_are_serialized_and_one_stales`, commit revision assertions | Mapped; persistence-level crash atomicity out of scope |
| SEC-SA-04 | Failed mutation corrupts canonical state | SA-004/012 | `test_abort_preserves_state_and_is_terminal`, integrity/self-test/invalid-checkpoint failure tests | Mapped |
| SEC-SA-05 | Stale writer overwrites newer state | SA-006 | `test_stale_transaction_rejected_and_canonical_preserved`, `test_concurrent_commits_are_serialized_and_one_stales` | Mapped |
| SEC-SA-06 | Transaction or checkpoint crosses generation boundary | SA-006 | `test_stale_transaction_rejected_and_canonical_preserved`, restore generation checks | Mapped; explicit generation mismatch preservation should be added if needed |
| SEC-SA-07 | Compatible state bypasses integrity validation | SA-007 | `test_integrity_is_independent_gate`, invalid checkpoint integrity test | Mapped |
| SEC-SA-08 | Unauthorized operation changes state | SA-010/014 | `test_default_deny_is_preserved_per_operation` | Mapped |
| SEC-SA-09 | Restore mutates canonical before validation/self-test | SA-008/012 | `test_restore_requires_self_test_and_preserves_canonical_on_failure`, self-test exception test | Mapped |
| SEC-SA-10 | Checkpoint identity or payload is altered after snapshot | SA-009 | `test_checkpoint_identity_and_payload_are_immutable` | New hardened verification; execution pending |
| SEC-SA-11 | Malformed/untrusted state reaches canonical storage | SA-013 | `test_malformed_and_oversized_state_is_rejected`, forged checkpoint test | Mapped |
| SEC-SA-12 | Resource exhaustion through oversized/deep state | SA-012 | `test_malformed_and_oversized_state_is_rejected` | Mapped for declared structural bounds |
| SEC-SA-13 | State or internal failure details leak through read/errors | Security/privacy boundary | `test_restore_self_test_exception_fails_closed`, hostile-data test; foundation diagnostics tests | Mapped; no sensitive fixture required |
| SEC-SA-14 | State layer gains command/subprocess execution | SA-011 | Read-only capability scan over `runtime/` plus hostile-string test | Scan evidence must be re-run on hardened commit |
| SEC-SA-15 | State layer gains network capability | SA-011 | Read-only capability scan over `runtime/` | Scan evidence must be re-run on hardened commit |
| SEC-SA-16 | State layer mutates arbitrary filesystem | SA-011 | Read-only capability scan over `runtime/` plus hostile-string test | Scan evidence must be re-run on hardened commit |
| SEC-SA-17 | Unsafe deserialization becomes mutation path | SA-013 | Read-only capability scan; no deserialization primitive in implementation | Scan evidence must be re-run on hardened commit |
| SEC-SA-18 | AI/external input gains direct mutation authority | SA-011 | AI contract suites + State Authority boundary inspection | Mapped; execution evidence must remain separate from AI contract tests |

## Required execution evidence

After the current read-boundary hardening commit is present on `mh-dev-01`, execute:

1. targeted P0-04 suite;
2. full repository regression with `-t .`;
3. capability scan over `runtime/`;
4. exact `git rev-parse HEAD` and clean-tree verification.

The expected targeted count is 17 tests if the current test file is unchanged. The expected full count is the prior 126 plus the single added checkpoint/read-boundary test, subject to discovery and repository state; the observed result, not this expectation, is authoritative.

## Security acceptance rule

A control is **PASS** only when implementation mapping and execution evidence both exist for the exact reviewed commit. A source-only mapping is **NOT EXECUTION EVIDENCE**.

Any failure, missing trace, unexpected test-count change, capability-scan match, or dirty working tree blocks security exit until dispositioned.

## Residuals carried into governance

- Cryptographic/durable checkpoint authenticity is not implemented in P0-04 because persistence is not authorized.
- Crash consistency and durable atomic publication are not assessed in P0-04.
- Retention, deletion, export, and durable personal-data handling are outside the authorized scope.
- The in-memory implementation must not be represented as proving persistent or appliance-level guarantees.
