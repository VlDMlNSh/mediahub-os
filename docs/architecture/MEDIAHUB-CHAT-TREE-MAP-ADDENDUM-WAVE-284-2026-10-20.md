# Canonical map addendum — Wave 284 (2026-10-20)

## Gemini caller-context probe triage

- Detailed report: [Wave 284 — exact-head probe startup-failure triage](../checkpoints/MEDIAHUB-GEMINI-CALLER-PROBE-STARTUP-FAILURE-TRIAGE-WAVE-284-2026-10-20.md).
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md); [continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); [governance Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Exact PR #421 head `abcfce3f70c4cc56335bf353a51a268d998f41b0`: Astra Verify #39459833610 and Astra Cloud Runtime Validation #39459833967 succeeded; non-launching probe #39459834572 ended `startup_failure`, with zero jobs and unavailable logs.
- Source-level leading hypothesis: the caller probe grants only read permissions but invokes a reusable child whose `engineer` job declares contents/pull-request write permissions. GitHub reusable-workflow token permissions cannot be elevated by the called workflow. Since startup logs were unavailable, keep this cause labeled probable, not confirmed.
- PR #421 and PR #426 both define `.github/workflows/gemini-caller-context-probe.yml` with incompatible roles (PR caller vs reusable sentinel). Resolve by distinct filenames and bounded security review before integration.
- PR #421 and #426 remain OPEN/DRAFT/UNMERGED and have no submitted independent review; branch-protection read remains blocked by API 403. No Gemini/provider invocation, dispatch, merge, deployment, qualification, or acceptance.
- Next bounded task: design the least-privilege, no-secret runtime probe with a distinct path while retaining static assertions that the actual child guard is unchanged. Do not enable write permissions on the probe just to bypass workflow startup.
