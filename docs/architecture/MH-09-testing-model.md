# MH-09 — Testing Model

**Status:** PROPOSED / REQUIRES VERIFICATION

Testing layers:
- unit: view models, state transformations, validation, navigation and error mapping;
- contract: Consumer Boundary, capability, authorization, read model, command and proposal semantics;
- security: no direct authority, raw transactions, unauthorized persistence, capability escalation, hidden auth, unrestricted network/filesystem;
- integration: UI → Consumer Boundary → authorization → State Authority;
- failure: stale, timeout, reject, policy/auth denial, disconnect, restart, degraded and unknown outcome;
- accessibility: critical flows with assistive technologies and presentation adaptations.

No UI test may certify canonical state solely from visual output; authoritative verification must inspect the governed subsystem outcome.
