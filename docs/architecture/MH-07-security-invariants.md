# MH-7 — Security Invariants

Status: CANDIDATE

1. Configuration is not authority.
2. Policy is not authority.
3. Policy Engine is not State Authority.
4. Policy cannot self-grant capability.
5. AI cannot publish without authorization.
6. Plugins cannot publish without authorization.
7. Configuration/policy cannot bypass P0-05.
8. Wildcard and capability inheritance are forbidden.
9. Hidden merge, LWW, retry and rebase are forbidden.
10. Ambiguous, malformed and unsupported policy fails closed.
11. Stale revisions fail closed.
12. Inputs are bounded and immutable.
13. Credentials are rejected.
14. Opaque references are inert and not dereferenced.
15. No hidden persistence, network access or arbitrary plugin execution.
16. P0-04 remains the sole canonical mutation authority.
