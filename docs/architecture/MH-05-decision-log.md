# MH-5 — Decision Log

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

| ID | Decision | Rationale | Evidence | Alternatives | Consequences | Dependencies | Status |
|---|---|---|---|---|---|---|---|
| D-001 | P0-04 remains the only canonical mutation authority | Preserves frozen State Authority invariant | E-001 | Secondary consumer store | All mutation paths terminate at P0-04 | P0-03/P0-04 | PROPOSED for MH-5 confirmation |
| D-002 | P0-05 remains mandatory consumer mediation | Existing accepted/frozen boundary | E-002 | Direct consumer→P0-04 path | No direct consumer mutation path | P0-05 | PROPOSED for MH-5 confirmation |
| D-003 | Proposal is inert until explicit command conversion/authorization | Prevents AI/plugin/automation authority leakage | E-002,E-005 | Autonomous proposal execution | Adds explicit conversion gate | P0-07, MH-4 | PROPOSED |
| D-004 | Transport is not canonical trust | Reachability/authenticated transport is not authority | E-002 plus MH-4 baseline | Transport-defined trust | Keeps security policy above transport | MH-2/MH-4 | PROPOSED |
| D-005 | Persistence remains outside MH-5 | Frozen restriction | E-001,E-002,E-003 | Consumer-side cache/store | Prevents hidden persistence side channel | Future Persistence Contract | PROPOSED |
| D-006 | Exactly-once is not claimed globally | Evidence does not justify global delivery guarantee | E-002,E-003 | Global exactly-once | Per-operation delivery semantics required | Future transport decisions | PROPOSED |

No technology selection is made by these decisions.
