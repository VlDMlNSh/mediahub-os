# MH-5 — Unknowns

**Status:** OPEN — REQUIRES VERIFICATION

1. Exact canonical schemas for all consumer request/result/event envelopes.
2. Exact capability inventory and resource/scope qualifiers.
3. Final human/service/device/plugin/AI identity model and credential lifecycle.
4. Final policy precedence/conflict semantics, especially while P0-07 is not accepted.
5. Exact numerical bounds for MH-5-specific envelopes where not inherited from an accepted contract.
6. Transport-specific delivery semantics and retry/replay behavior.
7. Required streaming/event ordering guarantees.
8. Final external data-export policy for sensitive content.
9. Device enrollment and verification mechanism.
10. Full plugin lifecycle and grant/revocation model.
11. Administrative critical-action approval semantics.
12. Pagination/chunking requirements for large reads/events.
13. Hardware topology; MH-5 intentionally does not depend on hardware assumptions.
14. Final persistence contract and durable privacy model.
15. Whether additional governance artifacts are needed to close P0-07 mutation authorization/API gap.

Unknowns are not assumptions and must not be silently implemented.
