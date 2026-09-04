# MH-09 — Decision Log

**Status:** PROPOSED

### D-09-01 — UI has no authority
Presentation is explicitly a consumer/presentation layer. Canonical mutation remains with P0-04.

### D-09-02 — Read model isolation
UI consumes bounded immutable/value-semantic read models rather than internal runtime state.

### D-09-03 — Explicit interaction path
All mutations use explicit command/proposal contracts and the existing authorization/Consumer Boundary path.

### D-09-04 — Honest freshness
Current, stale, cached, unavailable, estimated, predicted and recommended states are distinct presentation semantics.

### D-09-05 — No frozen-foundation changes
MH-09 will not alter P0-03…P0-06 to unblock P0-07 or any UI feature.

### D-09-06 — Technology neutrality
No UI framework is selected until an ADR with evidence is reviewed.

All decisions remain PROPOSED until the MH-09 governance gate is completed.
