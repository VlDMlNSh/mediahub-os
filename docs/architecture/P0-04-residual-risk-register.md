# P0-04 Residual Risk Register v1.0

## Status

Prepared for controlled implementation planning. This register does not authorize implementation or acceptance.

## Risk rating convention

- **HIGH:** may compromise canonical-state integrity, authorization, recovery correctness, or confidentiality if not controlled.
- **MEDIUM:** meaningful security, reliability, or privacy impact requiring explicit verification.
- **LOW:** bounded concern with documented mitigation or deferred controlled scope.

## Register

| ID | Risk | Rating | P0-04 treatment | Evidence required |
|---|---|---|---|---|
| RR-01 | Partial canonical publication | HIGH | Atomic in-memory publication; readers observe complete revisions only | Concurrency/publication tests |
| RR-02 | Stale transaction overwrites newer state | HIGH | Compare-and-reject generation/state version at commit | Stale-writer adversarial tests |
| RR-03 | Caller controls revision number | HIGH | Authority-owned monotonic state_version | Negative test oracle |
| RR-04 | Generation accepted without integrity validation | HIGH | Compatibility and integrity are separate gates | Independent integrity-failure test |
| RR-05 | Unauthorized restore/checkpoint operation | HIGH | Operation-specific default-deny authorization | Authorization adversarial suite |
| RR-06 | Checkpoint identity substituted or mutated | HIGH | Immutable checkpoint identity and metadata | Checkpoint immutability tests |
| RR-07 | Candidate state visible before commit | HIGH | Isolated transaction candidate | Isolation tests |
| RR-08 | Failed commit/restore corrupts canonical state | HIGH | Failure preserves last known valid canonical revision | Failure-path tests |
| RR-09 | Unsafe/malformed state accepted | HIGH | Structural, schema, bounds, generation and integrity validation | Malformed/untrusted-state tests |
| RR-10 | Sensitive state exposed in diagnostics | MEDIUM | Recursive sanitization and minimal diagnostic payloads | Privacy regression + log inspection |
| RR-11 | Resource exhaustion through oversized input | MEDIUM | Explicit bounded payloads and transaction resources | Boundary/DoS-oriented tests |
| RR-12 | Unsafe deserialization introduced during implementation | HIGH | No unsafe deserialization in P0-04; future persistence is separate | Capability/source inspection |
| RR-13 | Command execution primitive introduced accidentally | HIGH | No subprocess/system execution in P0-04 | Capability scan + source inspection |
| RR-14 | Network mutation/telemetry path introduced | HIGH | No network capability in P0-04 | Capability scan |
| RR-15 | AI/external actor gains state mutation authority | HIGH | Proposal/data boundary; only authorized SA operations mutate state | Interface + adversarial tests |
| RR-16 | Personal data enters evidence artifacts | MEDIUM | Synthetic-by-default test/evidence data | Evidence/privacy inspection |
| RR-17 | Transaction lifecycle resurrection | HIGH | Terminal transaction states cannot return to ACTIVE | Lifecycle negative tests |
| RR-18 | Security assumptions become coupled to future persistence | HIGH | Persistence-neutral contract; later storage gets separate security gate | Architecture traceability |

## Deferred systemic risks

The following are intentionally deferred and must not be treated as resolved by P0-04:

- crash consistency and durable atomicity;
- cryptographic checkpoint authenticity and key lifecycle;
- SQLite/ZFS/filesystem security;
- recovery media and storage corruption;
- update/rollback interactions;
- production privilege boundaries;
- network/mTLS security;
- hardware-backed integrity and entropy;
- long-term retention/deletion and audit integrity.

## Acceptance rule

No HIGH risk may be marked closed merely because the implementation is plausible. Closure requires the prescribed test or inspection evidence on the exact implementation commit and explicit security review. MEDIUM risks require evidence and disposition before implementation acceptance.

## Privacy rule

P0-04 verification uses synthetic data unless a separately authorized need exists. Real credentials, authentication material, private content, raw voice/audio, or unnecessary personal data must not be copied into source, tests, logs, issues, or evidence.

## Historical boundary

This register does not infer historical MH-02…MH-16 responsibilities.
