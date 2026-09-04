# MH-5 — Dependency Map

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

```text
MH-1 Product / Governance
        ↓
MH-2 Reference Architecture / Boundaries
        ↓
MH-3 Runtime Foundation
        ↓
MH-4 State Authority / Security / Trust
        ↓
MH-5 Consumer / Integration Boundary
        ↓
P0-03 State Authority Contract
        ↓
P0-04 In-Memory State Authority
        ↓
P0-05 Consumer Boundary
        ↓
P0-06 Core Runtime Services
        ↓
P0-07 Configuration / Policy (implementation in progress; production not qualified)
```

MH-5 is constrained by the frozen P0-03–P0-06 authority/security boundaries. It does not authorize implementation or reopen frozen contracts. P0-07 remains a dependent, governance-controlled consumer of the boundary and retains its own unresolved authorization/API gap.

No transport, database, broker, container platform, orchestration system, or API framework is selected by this document.
