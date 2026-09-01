# P0-04 Decision-Ready Index v1.0

## Status

**PREPARED — P0-03 FORMAL ACCEPTANCE PENDING — P0-04 IMPLEMENTATION NOT AUTHORIZED**

This index is a navigation and state-consolidation artifact. It does not replace the governing contract, does not make a governance decision, and does not authorize implementation.

## Authoritative hierarchy

1. P0-03 State Authority Contract v1.0 — technical contract and invariants.
2. P0-03 formal governance decision — sole boundary for changing P0-03 from pending to accepted and for authorizing the next phase.
3. P0-04 implementation gate — bounded in-memory implementation scope after authorization.
4. P0-04 workplan — implementation decomposition.
5. Security/privacy artifacts — threat model, verification matrix, negative-test catalogs, exit criteria.
6. Evidence artifacts — evidence template, integrity protocol, traceability matrix.
7. Execution evidence — exact implementation commit, environment, commands, exit codes, test results and capability inspection.
8. Adversarial/security review — assessment of concrete evidence and residual risk.
9. P0-04 acceptance decision — separate acceptance gate after implementation and evidence.

No lower-level artifact overrides a higher-level governance boundary.

## Current immutable baselines

- P0-03 contract baseline: `9ae82f9e45bcb9c330ab283b13a482fbeea6b546`.
- P0-04 preparation branch: `architecture/p0-04-in-memory-state-authority`.
- P0-04 preparation PR: #8.
- Current PR #8 head: `19eb003812b96b746723e3512d635429bb085add`.
- PR #8 remains Draft/Open and contains documentation/gate preparation only.

The P0-04 preparation head must not be treated as an implementation baseline. If implementation is later authorized, a new implementation commit must be explicitly identified and independently evidenced.

## Governance state

### P0-03

- Technical review: PASS.
- Adversarial review: PASS with residual implementation obligations.
- Governance readiness: PREPARED.
- Decision packet: READY.
- Formal decision: **PENDING**.
- P0-04 implementation authorization: **NOT GRANTED**.

### P0-04

- Gate: PREPARED.
- Workplan: PREPARED.
- Security/threat/privacy controls: PREPARED.
- Evidence and traceability controls: PREPARED.
- Implementation: **NOT STARTED**.
- Execution evidence: **NOT APPLICABLE YET**.
- Acceptance: **NOT REACHED**.

## Required decision path

The only valid governance choices for P0-03 are `ACCEPT`, `ACCEPT WITH CONDITIONS`, or `RETURN FOR REVISION`.

A valid decision must identify the authority, UTC timestamp, exact P0-03 baseline, conditions if applicable, explicit P0-04 implementation authorization status, and explicit persistence authorization status. Missing or contradictory fields keep the state `PENDING`.

Even after `ACCEPT`, P0-04 implementation requires a separate explicit implementation authorization recorded against the immutable P0-03 baseline.

## P0-04 scope lock

If authorized, P0-04 remains limited to deterministic in-memory State Authority behavior: canonical state; isolated candidate transactions; begin/commit/abort lifecycle; authority-owned monotonic revisions; generation compatibility; independent integrity validation seam; operation-specific default-deny authorization; immutable checkpoint identity; restore through candidate validation and publication as a new canonical revision; bounded inputs; privacy-safe diagnostics; functional, adversarial, security and privacy verification.

Still prohibited: SQLite/ZFS/filesystem/cloud/hardware persistence; subprocesses/arbitrary command execution; network transport/telemetry; bootloader/systemd appliance integration; installer/recovery media; update/rollback engine; production deployment topology; real user/private data in fixtures or evidence.

## Security and privacy gate

P0-04 cannot exit security review without evidence for authority, authorization, isolation, atomicity, versioning/stale rejection, generation, independent integrity, recovery, input safety, execution/network/filesystem/deserialization boundaries, AI boundary, privacy, failure preservation, and resource safety.

Evidence must be attributable to the exact immutable implementation commit and must contain no unnecessary credentials, secrets, raw voice/audio, private content, or personal data.

## Residual risks

High-risk implementation obligations remain open until concrete evidence closes them, including partial publication, stale overwrite, caller-controlled revision, integrity bypass, unauthorized recovery operations, checkpoint substitution, candidate leakage, failed-operation corruption, malformed state acceptance, unsafe deserialization, command/network mutation, AI mutation authority, and transaction resurrection.

Systemic risks intentionally deferred beyond P0-04 include durable crash consistency, cryptographic checkpoint key lifecycle, storage corruption/recovery media, persistence security, update/rollback interaction, production privilege boundaries, network/mTLS, hardware integrity/entropy, and retention/deletion/audit integrity.

## Governance linkage

- Formal P0-03 decision point: Issue #9.
- P0-04 evidence/traceability gate: Issue #10.
- P0-03 → P0-04 transition authority checklist: `P0-03-P0-04-transition-authority-checklist.md`.
- P0-03 governance decision packet: `P0-03-governance-decision-packet.md`.

## Historical boundary

This index does not infer or reconstruct MH-02…MH-16 responsibilities. Any such mapping requires authoritative historical evidence.

## Gate conclusion

**DECISION-READY / CONSISTENT / FAIL-CLOSED.**

The project is prepared for the explicit P0-03 governance decision. No implementation work should begin while the formal decision and separate P0-04 authorization remain absent.
