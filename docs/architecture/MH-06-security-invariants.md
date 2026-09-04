# MH-06 — Security Invariants

Status: PROPOSED / REQUIRES VERIFICATION

1. P0-04 is sole canonical mutation authority.
2. Runtime services are not State Authority.
3. Supervisor cannot bypass authorization.
4. Scheduler cannot bypass authorization.
5. Health cannot grant capability.
6. Readiness does not imply trust.
7. Restart cannot silently mutate canonical state.
8. Recovery is bounded.
9. Critical recovery is gated.
10. Failed services fail closed.
11. Unknown service state is not healthy.
12. Internal IPC has explicit trust/auth semantics.
13. Least privilege applies to runtime services.
14. No hidden persistence.
15. No hidden external network authority.
16. AI is non-authoritative.
17. Observability is non-authoritative.
18. Cancellation does not automatically imply rollback.
19. Retry cannot silently duplicate unsafe operations.
20. Single-node is not represented as HA.

Any violation is an architecture/security contradiction requiring governance review.
