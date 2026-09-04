# MH-14 — ACCEPTANCE CRITERIA

Status: NOT YET ACCEPTED / FROZEN

MH-14 may transition to ACCEPTED/FROZEN only when all of the following are satisfied:

- [ ] Persistence boundary is explicit and subordinate to State Authority.
- [ ] P0-03…P0-06 frozen contracts remain compatible.
- [ ] P0-07 is not silently altered.
- [ ] Persistence contract and failure semantics are specified.
- [ ] Canonical vs persisted state distinction is testable.
- [ ] Consistency/version rules reject stale overwrite.
- [ ] Atomicity semantics are demonstrated by implementation evidence.
- [ ] Crash/power-loss behavior is demonstrated.
- [ ] WAL/journal or alternative atomicity mechanism has an ADR if needed.
- [ ] Snapshot semantics are explicit.
- [ ] Restore authorization and State Authority mediation are tested.
- [ ] Backup consistency and verification procedure are tested.
- [ ] At least one real restore test demonstrates recovery capability.
- [ ] RPO/RTO are explicitly decided or formally left TBD by governance.
- [ ] Corruption detection/quarantine/recovery behavior is tested.
- [ ] Integrity controls are selected from the threat model.
- [ ] Encryption and key lifecycle satisfy MH-12.
- [ ] Retention/deletion satisfy MH-13, including durable copies.
- [ ] Schema/version/migration/rollback compatibility is tested.
- [ ] Persistence isolation prevents unauthorized execution and access paths.
- [ ] UI/AI/plugin/configuration boundaries are preserved.
- [ ] Observability is bounded and privacy-aware.
- [ ] Resource/capacity limits are evidenced.
- [ ] Offline-first behavior is defined.
- [ ] Cloud persistence, if any, has explicit external-boundary governance.
- [ ] Hardware/OS/filesystem assumptions are evidenced.
- [ ] Security tests pass.
- [ ] Privacy tests pass.
- [ ] Dependency/contradiction/evidence registers are current.
- [ ] Physical persistence implementation receives separate governance authorization.

Until all mandatory gates are satisfied: `Physical persistence implementation = NOT AUTHORIZED`.
