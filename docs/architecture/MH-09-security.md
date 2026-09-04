# MH-09 — Presentation Security

**Status:** PROPOSED

Security invariants:

1. UI is not authority.
2. UI visibility is not authorization.
3. Disabled controls are not security controls.
4. Hidden routes/deep links do not grant capability.
5. Read models are not mutation primitives.
6. Raw State Authority and raw transactions are never exposed.
7. Direct canonical persistence, unrestricted filesystem/network and shell access are forbidden.
8. AI recommendation/proposal is not authorization or command execution.
9. Plugin UI does not inherit authority through rendering.
10. Sensitive data is disclosed only according to authorization and least disclosure.
11. Security failures fail closed.
12. Emergency UX remains explicit and minimally dependent on AI/cloud.

All privileged actions must re-enter the canonical authorization and Consumer Boundary path.
