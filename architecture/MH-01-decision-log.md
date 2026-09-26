# MH-01 Decision Log

Status: PROPOSED / REQUIRES VERIFICATION.

| ID | Context | Decision | Status | Affected domains |
|---|---|---|---|---|
| MH1-D-001 | Product identity | MediaHub OS is an OS/runtime platform, not an AI wrapper | PROPOSED | MH-02, MH-10 |
| MH1-D-002 | Runtime mutation | State Authority is sole canonical mutation authority | ACCEPTED / inherited FROZEN | MH-03…MH-23 |
| MH1-D-003 | AI | AI is non-authoritative and may only propose through policy/authorization | PROPOSED | MH-10, MH-20 |
| MH1-D-004 | Cloud | Cloud is external/non-authoritative | PROPOSED | MH-21 |
| MH1-D-005 | Product posture | Local-first and offline-capable core | PROPOSED | MH-02, MH-22 |
| MH1-D-006 | Reliability | Current baseline is SINGLE NODE / NO HA | OBSERVED / CURRENT | MH-15, MH-22 |
| MH1-D-007 | Reliability | Backup/mirroring does not imply HA | ACCEPTED PRINCIPLE | MH-14…MH-23 |
| MH1-D-008 | Persistence | Persistence cannot replace State Authority | ACCEPTED PRINCIPLE | MH-04, MH-14 |
| MH1-D-009 | Series mapping | MH-01…MH-23 mapping is proposed until historical proof | PROPOSED | All |
| MH1-D-010 | Governance | P0-03…P0-06 cannot be changed by MH-01 implicitly | GOVERNANCE INVARIANT | All |
| MH1-D-011 | Hybrid compute | Local + external GPU/cloud remains candidate | CANDIDATE | MH-21 |
| MH1-D-012 | Hardware | Historical Mac mini target is not production qualification | DEFERRED | MH-15, MH-22 |

## Decision record rule

Every future decision must contain: ID, date, context, evidence, decision, alternatives, consequences, authority/owner, status and affected MH domains. Chat discussion alone is not a canonical decision record.