# MH-14 — UNKNOWN REGISTER

Status: OPEN

| ID | Unknown | Status | Required evidence/decision |
|---|---|---|---|
| U01 | Physical persistence technology | REQUIRES VERIFICATION | ADR + benchmark/test evidence |
| U02 | Filesystem | REQUIRES VERIFICATION | Host/OS evidence |
| U03 | WAL/journal mechanism | REQUIRES VERIFICATION | Atomicity/crash tests |
| U04 | Exact durability guarantee | REQUIRES VERIFICATION | Implementation + power-loss evidence |
| U05 | RPO | TBD | Business/workload decision |
| U06 | RTO | TBD | Business/workload decision |
| U07 | Backup destination/frequency | REQUIRES VERIFICATION | Governance + capacity analysis |
| U08 | Restore-test frequency | REQUIRES VERIFICATION | Operational policy |
| U09 | Storage topology/health | REQUIRES VERIFICATION | Physical inspection |
| U10 | Encryption/key management | REQUIRES VERIFICATION | MH-12 implementation decision |
| U11 | Migration framework | REQUIRES VERIFICATION | Technology ADR |
| U12 | Corruption recovery implementation | REQUIRES VERIFICATION | Fault-injection tests |
| U13 | Power-loss characteristics | REQUIRES VERIFICATION | Hardware/filesystem evidence |
| U14 | UPS | REQUIRES VERIFICATION | Appliance operations decision |
| U15 | Replication/HA | OPEN | Separate governance decision |
| U16 | Cloud persistence | OPEN | Privacy/security/network governance |
| U17 | Archival | OPEN | Retention/data-governance decision |

Rule: no unknown may be silently converted into an architecture fact by implementation convenience.
