# MH-09 — Persistence Boundary

**Status:** PROPOSED / REQUIRES VERIFICATION

MH-09 introduces no persistence authority. UI storage is limited to presentation cache, drafts, session context or other explicitly non-canonical data.

Canonical runtime state remains owned by the State Authority. UI cache must identify freshness and cannot be treated as canonical after restart, disconnect, conflict or unknown outcome. Any future persistence integration requires its own accepted architecture and governance decision.
