# MH-5 — Security Invariants

**Status:** PROPOSED — GOVERNANCE REVIEW REQUIRED

1. No direct consumer mutation.
2. No hidden authority escalation.
3. No implicit capability inheritance.
4. No wildcard authority.
5. No self-grant.
6. No trust from reachability alone.
7. No mutation from observation.
8. No execution from proposal alone.
9. No authority from identity alone.
10. No authority from authentication alone.
11. Authorization is operation-specific.
12. P0-04 remains the sole canonical mutation authority.
13. Boundary violations fail closed.
14. Malformed input is rejected.
15. Bounds are enforced before processing/publication.
16. Unknown capability is denied.
17. Unknown caller is denied.
18. Unknown device is untrusted.
19. External services remain outside Core authority.
20. Persistence cannot be smuggled through Consumer Boundary.

These invariants are architectural constraints. Passing a test does not itself change their governance status; acceptance requires evidence plus explicit decision.
