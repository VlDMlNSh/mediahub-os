# MH-09 — Diagnostic UI

**Status:** PROPOSED / REQUIRES VERIFICATION

Diagnostic presentation is read-first, observer-oriented, bounded and privacy-aware. Diagnostic data must be classified by sensitivity and authorization.

Any diagnostic mutation requires an explicit operation, capability, authorization and Consumer Boundary path. Diagnostic screens cannot access raw authority internals, execute arbitrary shell/network/filesystem operations, or treat telemetry as canonical state.
