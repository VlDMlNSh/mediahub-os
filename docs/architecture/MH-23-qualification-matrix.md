# MH-23 Qualification Matrix

| Domain | Requirement | Evidence | Status | Risk | Owner | Gate |
|---|---|---|---|---|---|---|
| Authority | sole State Authority | P0-03/P0-04 lineage | REQUIRES VERIFICATION | HIGH | Governance | no split |
| Security | secure migration/rollback | security scans + artifacts | REQUIRES VERIFICATION | HIGH | Security | signed/verified |
| Privacy | derived/cloud data handling | inventory/evidence | UNKNOWN | HIGH | Privacy | privacy gate |
| Runtime | lifecycle/state compatibility | tests | REQUIRES VERIFICATION | HIGH | Runtime | health gate |
| API/Schema | contract compatibility | matrix/tests | PROPOSED | HIGH | Architecture | compatibility |
| Persistence | contract only; no physical implementation | ADR/evidence | NOT AUTHORIZED | HIGH | Architecture | separate authorization |
| Configuration/Policy | semantic preservation | P0-07 evidence | BLOCKED | HIGH | Governance | close API gap |
| Plugins/Devices | security/identity compatibility | qualification | UNKNOWN | HIGH | Integration | quarantine on fail |
| Media/KG/Automation | semantic migration | domain evaluations | UNKNOWN | MEDIUM/HIGH | Domain owners | qualification |
| AI/Cloud | behavior/boundary qualification | eval/provider evidence | UNKNOWN | HIGH | AI/Cloud | promotion gate |
| Hardware/OS | operational compatibility | hardware/OS evidence | UNKNOWN | HIGH | Operations | qualification |
| Installer/Update/Recovery | lifecycle/recovery proof | MH-16 evidence | REQUIRES VERIFICATION | HIGH | Operations | recovery gate |
| Operations/Evidence | runbooks/evidence/incident handling | current records | UNKNOWN | HIGH | Operations | governance |
| Governance | ADR/owner/approval | decision records | REQUIRES VERIFICATION | HIGH | Governance | acceptance |