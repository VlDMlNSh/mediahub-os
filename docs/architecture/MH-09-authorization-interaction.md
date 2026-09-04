# MH-09 — Authorization Interaction

**Status:** PROPOSED / REQUIRES VERIFICATION

Authentication establishes identity; authorization determines permitted operations. Presentation must treat authorization as an external decision.

Flow: `identity/auth context → capability check → policy decision → authorized command → Consumer Boundary`.

UI may display authorized/denied outcomes, but cannot authorize by enabling, hiding, routing, deep-linking, caching credentials, or changing presentation state. Denials fail closed and reveal only information permitted by the privacy policy.
