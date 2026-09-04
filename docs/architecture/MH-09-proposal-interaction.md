# MH-09 — Proposal Interaction

**Status:** PROPOSED / REQUIRES VERIFICATION

Proposals are inert bounded data representing a suggested action or desired change. A proposal has no execution authority.

Canonical path:
`UI → Proposal → Validation → Policy → Authorization → Command → Consumer Boundary → State Authority`

Rules: proposal contents are untrusted input; capability is never inferred from proposal origin or UI visibility; proposals cannot execute, self-authorize, grant capability, bypass policy, or mutate canonical state. AI and plugins use the same boundary.

Verification must prove inertness and rejection of unauthorized, malformed, over-broad, or stale proposals.
