# MH-09 — Threat Model

**Status:** PROPOSED / REQUIRES VERIFICATION

Primary threats: UI privilege escalation, hidden/deep-link authorization bypass, stale-data mutation, forged or replayed interaction state, raw transaction exposure, plugin capability inheritance, notification-triggered bypass, AI recommendation auto-execution, sensitive-data disclosure, unrestricted network/filesystem access and false success after unknown outcomes.

Controls: deny-by-default authorization, operation-specific capabilities, Consumer Boundary enforcement, bounded immutable read models, explicit freshness/outcome states, inert proposals, least disclosure, fail-closed errors and independent subsystem verification.

Threat-model acceptance requires evidence from implementation and security testing; this document does not itself grant production qualification.
