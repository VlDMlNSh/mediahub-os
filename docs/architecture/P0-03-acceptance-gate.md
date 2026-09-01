# P0-03 — State Authority Contract Acceptance Gate v1.0

## Status

**Technical review: PASS**  
**Adversarial review: PASS with residual implementation obligations**  
**Formal governance acceptance: PENDING**  
**Implementation authorization: NOT GRANTED**

## Decision boundary

This artifact records the acceptance decision point without making that governance decision on behalf of the project authority.

P0-03 defines the persistence-neutral State Authority contract for `read`, `begin`, `commit`, `abort`, `snapshot`, and `restore`, including canonical/candidate/transaction/checkpoint boundaries and the deterministic transaction state machine.

## Acceptance checklist

- [x] Single authoritative canonical-state boundary defined.
- [x] Candidate state is isolated from canonical state.
- [x] Transaction lifecycle and terminal states defined.
- [x] Atomic publication requirement defined.
- [x] State-version advancement belongs to State Authority.
- [x] Caller-selected canonical revision is prohibited.
- [x] Transactions bind to observed generation/state version.
- [x] Stale transaction rejection is fail-closed.
- [x] Generation compatibility and integrity validation are separate gates.
- [x] Restore is an authorized State Authority operation.
- [x] Restore uses candidate isolation and creates a new canonical revision.
- [x] Accepted checkpoint identity is immutable.
- [x] Operation-specific default-deny authorization is required.
- [x] External/AI/UI/network mutation primitives are prohibited.
- [x] Serialized state/checkpoint material is untrusted until validated.
- [x] Failure preserves the last known valid canonical state.
- [x] Security/privacy requirements are explicit.
- [x] Concrete persistence remains deferred.

## Residual implementation obligations

1. Prove atomic publication and reader consistency in the in-memory implementation.
2. Prove deterministic isolation and stale rejection under concurrency.
3. Implement checkpoint authenticity/integrity where cryptographic protection is required.
4. Use a safe serialization/deserialization boundary when persistence is introduced.
5. Enforce resource and size bounds against denial-of-service conditions.
6. Preserve privacy-safe diagnostics and exceptions.
7. Test failure behavior without exposing partial canonical state.
8. Re-run adversarial security review against concrete implementation and later persistence layers.

## Explicit non-goals

No SQLite, ZFS, filesystem persistence, subprocesses, network transport, bootloader/systemd appliance behavior, installer/recovery media, update engine, cloud persistence, hardware persistence, or production deployment topology is authorized by this gate.

## Governance rule

Only an explicit project-authority acceptance decision may change **Formal governance acceptance** to `ACCEPTED` and authorize P0-04 implementation. Technical PASS alone is insufficient.

## Traceability

- P0-02: State Authority Design v1.0
- P0-03: State Authority Contract v1.0
- P0-03 adversarial review: PASS with residual implementation obligations
- P0-04: In-Memory State Authority Implementation Gate v1.0
