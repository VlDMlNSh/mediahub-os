# MH-09 — Navigation Model

**Status:** PROPOSED / REQUIRES VERIFICATION

Navigation includes application shell, feature, modal, deep-link, guarded, privileged, recovery, offline and degraded states.

Navigation is presentation-only. Deep links, routes, hidden screens and guarded navigation cannot grant capability, authenticate, authorize, bypass policy, or mutate canonical state. Privileged destinations must independently enforce authorization through the canonical command path.
