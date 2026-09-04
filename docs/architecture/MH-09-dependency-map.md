# MH-09 — Dependency Map

**Status:** PROPOSED

```text
MH-1 Governance
   ↓
MH-2 Reference / Boundaries
   ↓
MH-3 Runtime Foundation ── MH-6 Core Runtime
   ↓                         ↓
MH-4 Security / Trust ── MH-5 Consumer Boundary
   ↓                         ↓
MH-7 Configuration / Policy ─┤
   ↓                         ↓
MH-8 Plugin / Extension ─────┤
                             ↓
                    MH-9 Presentation / UI
                             ↓
                           MH-10 AI
```

P0 mapping:
- P0-03 State Authority: canonical mutation authority — VERIFIED by frozen governance context supplied to MH-9; repository presence on current main remains REQUIRES VERIFICATION.
- P0-04 In-memory authority: frozen implementation baseline — VERIFIED by prior acceptance evidence; current branch lineage requires repository verification.
- P0-05 Consumer Boundary: frozen canonical integration boundary — VERIFIED by prior acceptance evidence; exact current-main artifact presence requires verification.
- P0-06 Core Runtime: ACCEPTED/FROZEN implementation evidence exists; production qualification remains not granted.
- P0-07 Configuration/Policy: implementation in progress; mutation publication remains blocked.
- P0-08 Plugin/Extension: current repository contains verification workflow and draft integration candidates; final acceptance is not asserted here.

Dependency rule: presentation may depend on explicit contracts, never on authority internals.
