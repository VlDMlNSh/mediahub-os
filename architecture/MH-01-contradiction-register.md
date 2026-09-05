# MH-01 Contradiction Register

Status: OPEN / REQUIRES VERIFICATION.

| ID | Source A | Source B | Conflict | Current authority | Proposed resolution | Status |
|---|---|---|---|---|---|---|
| C-001 | Proposed MH-01 identity | Historical corpus | Exact historical charter wording not proven | Evidence | Reconcile historical sources before freeze | OPEN |
| C-002 | Proposed MH-01…23 mapping | Existing corpus | Full historical mapping not proven | Evidence | Verify each domain mapping | OPEN |
| C-003 | Local cluster terminology | Current single-node/no-HA baseline | Cluster can be misread as HA | Current baseline | Keep distributed/HA as candidate | RESOLVED BY SCOPE |
| C-004 | Hybrid AI/cloud research | Local-first baseline | Candidate topology may be mistaken for frozen | Current authority model | Keep cloud external/non-authoritative | OPEN |
| C-005 | Persistence roadmap | P0-04 | Persistence could be mistaken for authority | P0-04 | Preserve persistence ≠ authority | RESOLVED |
| C-006 | AI/agent design | P0-03 | AI could be treated as mutation authority | P0-03 | Proposal→policy→authorization→command | RESOLVED |
| C-007 | Backup/recovery | HA assumptions | Backup/mirroring ≠ HA | Current baseline | Keep HA unknown | RESOLVED |
| C-008 | Historical hardware target | Production qualification | Target hardware ≠ qualified hardware | Qualification process | Defer to MH-15/MH-22 | OPEN |
| C-009 | P0-07 implementation | Production acceptance | Verification/implementation ≠ acceptance | Governance | Preserve P0-07 gap | OPEN |

## Rule

No contradiction is silently repaired. If sources cannot be reconciled, retain both evidence records and mark the disputed proposition UNKNOWN/REQUIRES VERIFICATION or PROPOSED.