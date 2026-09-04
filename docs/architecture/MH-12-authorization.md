# MH-12 Authorization

Authorization is explicit, operation-specific, identity-bound, context-aware, policy-aware, auditable and fail-closed.

Forbidden: implicit grants, wildcard privileges, hidden inheritance, self-grant, privilege escalation, hidden admin paths, network-based authorization and token-only authorization where context is required.

Authorization must terminate at the approved Consumer Boundary and State Authority mutation contract; it cannot create an alternate mutation authority.
