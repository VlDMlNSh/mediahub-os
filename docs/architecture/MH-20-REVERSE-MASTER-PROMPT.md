# MH-20 Reverse Master Prompt

Input to MH-20 from the development workspace.

Report only architecture-impacting implementation evidence. Include exact branch, commit SHA, files/paths, tests and CI evidence where available.

Required report:
1. Implemented contracts and their evidence.
2. Actual mutation paths and whether each reaches Policy → Authorization → Consumer Boundary → State Authority.
3. Any bypass, duplicate authority, hidden privilege, hidden retry/rebase/merge/LWW behavior or unsafe automation path.
4. Scheduler/time/idempotency/retry/rate-limit behavior actually implemented.
5. Safety, critical-action, manual-override and self-healing behavior actually implemented.
6. Energy control path and actuator boundaries.
7. AI/plugin/device/media/KG integrations.
8. Security/privacy/observability evidence.
9. Tests and verification results, distinguishing existence from PASS evidence.
10. Contradictions, unknowns and architecture decisions requiring governance.

Do not declare architecture accepted or frozen. MH-20 performs the architecture review and governance decision.