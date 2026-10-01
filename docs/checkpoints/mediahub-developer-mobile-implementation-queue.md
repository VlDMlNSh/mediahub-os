# Developer Mobile — MH-25 Implementation Queue

Status: **Queued — implementation starts after Developer Mobile UX/UI closure**

Source functional baseline:
- docs/checkpoints/mediahub-developer-mobile-functional-baseline.md
- Commit: c8c66b778ae444c14c1190ad214fb284b632cbc4

## Required implementation order

1. Application shell and Project orchestration model.
2. Local Assistant hardware capability discovery and adaptive runtime.
3. Assistant/model registry and hybrid inference routing.
4. Coordination provider abstraction.
5. GitHub repository/issues/branches/commits/PR integration.
6. GitHub Actions build/test/sign/stage/publish/rollback control.
7. Development Workspace: terminal, files, processes, Git, builds, logs, jobs.
8. Three-level authorization with mandatory confirmation for MEDIUM and HIGH.
9. Credential references/capabilities without raw secret exposure.
10. Digital Clone.
11. Trusted Sources and Knowledge ingestion.
12. Media Studio.
13. Web Studio with Generated → Review → Approved → Published.
14. Release/update control surface.
15. Activity/Evidence.
16. Offline queue and reconnect revalidation.
17. Accessibility and qualification automation.

## Hard implementation constraints

- Developer Mobile is a control plane, not a MediaHub State Authority.
- AI and Local Assistant are not authorities.
- Coordination Chat is not an authority.
- Remote terminal is never unrestricted by default.
- MEDIUM actions always require explicit user confirmation.
- HIGH actions always require explicit user confirmation.
- Raw secrets are not exposed to Local Assistant or Developer Mobile merely to execute authorized work.
- Offline queued actions are revalidated before execution.
- Existing MediaHub authority boundaries remain unchanged.
- Functional completion must not be claimed as implementation or qualification completion.

## Transition gate

Before coding begins:
1. close Developer Mobile Visual / UX Baseline;
2. reconcile visual decisions with the functional baseline;
3. create MH-25 implementation plan;
4. map each functional requirement to implementation and qualification evidence.

MH-25 is the execution phase; this file is the queue/contract, not implementation evidence.
