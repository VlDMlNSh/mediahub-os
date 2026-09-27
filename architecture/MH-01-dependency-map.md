# MH-01 Dependency Map

Status: PROPOSED / REQUIRES VERIFICATION.

```text
MH-01 Product/Governance
        ↓
MH-02 Reference Architecture
        ↓
MH-03 Runtime → MH-04 State Authority → MH-05 Consumer Boundary → MH-06 Core Services
        ↓
MH-07 Policy / MH-08 Plugins / MH-09 UI / MH-10 AI / MH-11 Observability
        ↓
MH-12 Security / MH-13 Privacy / MH-14 Persistence
        ↓
MH-15 OS/Appliance / MH-16 Recovery/Update / MH-17 Device / MH-18 Media
        ↓
MH-19 Knowledge/Digital Twin / MH-20 Automation / MH-21 Hybrid Cloud
        ↓
MH-22 Production/Qualification → MH-23 Evolution/Migration
```

## Dependency rules

- Authority dependency flows toward State Authority, never around it.
- UI/AI/knowledge/persistence/cloud may consume contracts but cannot become canonical mutation authorities.
- Security and policy constrain all mutation-capable domains.
- MH-23 may define migration/evolution but cannot retroactively invalidate frozen contracts without governance.
- Development implementation is downstream of architecture and does not become an architectural dependency.

## Current reliability boundary

Current baseline remains SINGLE NODE / NO HA. Distributed/cluster designs are candidates until independently verified and accepted.