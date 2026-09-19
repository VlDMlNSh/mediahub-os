# MH-07 — Security Invariants

Status: CANDIDATE.

1. Configuration is not authority.
2. Policy is not authority.
3. Policy Engine is not State Authority.
4. Policy cannot self-grant authorization.
5. AI/plugin/external proposals cannot self-publish.
6. P0-05 remains controlled ingress.
7. P0-04 remains sole canonical mutation authority.
8. Wildcards, inheritance, hidden merge and LWW are forbidden.
9. Ambiguity, malformed and unsupported policy fail closed.
10. Stale revision fails closed.
11. Configuration/policy are bounded, immutable at read/evaluation boundaries and non-executable.
12. Credentials are rejected; opaque references are inert.
13. No hidden persistence, network execution or plugin execution.
14. Critical execution requires explicit authorization and stronger audit; AI-only approval is insufficient.

Verification status: architecture-defined; implementation verification pending.
