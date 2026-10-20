# MediaHub OS Contour A — immutable action-ref hardening (Wave 255)

Date: 2026-10-20
Status: PATCHED / EXACT-HEAD CI PASSED / CONTROLLER NOT INTEGRATED

## Scope
Bounded continuation on Draft PR #421 to remove mutable GitHub Action references from Gemini Agent 3 and prevent recurrence through contract tests. No agent dispatch, merge, deployment, or qualification.

## Evidence
- PR [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421) remains Draft/open.
- Exact head: `3ab7258ab69353f7327266fc0508f02fc38716da`.
- Base `main`: `80be45a70732b1d568164571d4273a6397792c3b`; branch compare: 23 ahead / 0 behind.
- [Astra Cloud Runtime Validation #39416070256](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416070256): SUCCESS on exact head.
- [Astra Verify #39416070449](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39416070449): SUCCESS on exact head. Steps confirm actionlint, compile, reusable-workflow contract tests, cloud admission tests and signed-command smoke test passed.
- Agent 3 now pins `actions/checkout` to `11d5960a326750d5838078e36cf38b85af677262` and `google-github-actions/run-gemini-cli` to `f77273f4c914e4bf38440cf36a0369cb64a37489`, matching sibling workflows. Child file blob SHA: `3b8d71636575a8746f0391ebee795450bca9b031`.
- Contract tests now validate external `uses:` refs against full 40-character commit SHAs and reject a mutable action ref fixture. Test blob SHA: `c491d8e94f0e3a5715e9ff32357b4c6ddced8818`; commit: `3ab7258ab69353f7327266fc0508f02fc38716da`.

## Remaining blockers
1. The `ghcr.io/github/github-mcp-server:v0.27.0` container reference is still a mutable tag. Pin to a verified digest for the intended release or conduct a reviewed version upgrade; do not guess a digest or silently change versions.
2. PR #421 has no independent review recorded; the connected identity is the PR author and GitHub rejected its formal REQUEST_CHANGES review.
3. The controlled negative caller-context runtime test has not been executed. The available connector exposes no workflow-dispatch action, and no direct-child or alternate transport was used.
4. Governance-approved integration/branch protection review remains open.

## Dispatch posture
Routine three-agent work is an intended Contour A capability. The temporary hold applies only to the not-yet-integrated controller transport and the remaining security gates; it is not a project-wide ban. No Gemini agent was launched in Wave 255. No provider secret was read or changed.

## Next bounded action
Verify the exact `v0.27.0` OCI manifest digest through an authoritative package record or reviewed release metadata, pin it with a test enforcing digest use, rerun exact-head CI, and obtain a genuine independent review. Then run the approved controlled negative caller-context test before integration. After governance integration, the first bounded three-agent batch can be launched through the controller using `confirm: yes`, with run IDs and artifacts inspected.

## Navigation
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 253 caller-ref review](MEDIAHUB-CLOUD-AGENT-CALLER-REF-GUARD-REVIEW-WAVE-253-2026-10-20.md)
- [Wave 254 autonomous-use gate](MEDIAHUB-CLOUD-AGENT-AUTONOMOUS-USE-GATE-WAVE-254-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
