# MH-02 — Master Traceability Matrix

| Boundary | Threat/Failure | Authority | Control | Verification | Governance |
|---|---|---|---|---|---|
| Presentation | direct mutation | State Authority | request-only API | negative bypass tests | MH-01/P0-03 |
| Intelligence | AI direct mutation | State Authority | proposal gate | AI boundary tests | MH-01/MH-10 |
| Integration | malicious/unknown device | State Authority | adapter + consumer contract + authorization | quarantine/negative tests | P0-05/MH-17 |
| Persistence | second authority | State Authority | persistence contract | mutation-path audit | P0-04/MH-14 |
| Observability | telemetry mutation | State Authority | observer-only interface | telemetry tests | MH-11 |
| Cloud | external compromise/control | State Authority | controlled authorized interface | network/capability tests | MH-12/MH-21 |
| Plugin | privilege escalation | State Authority | scoped capabilities | sandbox/capability tests | MH-08/MH-12 |
| OS/Hardware | host failure | Recovery authority | lifecycle/recovery boundary | failure injection | MH-15/MH-16 |

Fundamental rule: no subsystem may cross a boundary by implicit authority inheritance.
