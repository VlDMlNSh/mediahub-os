# Wave 312 — Gemini controller transport correction (2026-10-21)

**State: IMPLEMENTED ON DRAFT PR #432; NOT MERGED, NOT QUALIFIED.**

- Primary evidence: [Wave 312 controller correction report](../checkpoints/MEDIAHUB-GEMINI-CONTROLLER-GITHUB-API-DISPATCH-FIX-WAVE-312-2026-10-21.md).
- Code PR: [#432](https://github.com/VlDMlNSh/mediahub-os/pull/432).
- Governance: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md).

## Contract correction

The controller must use the repository secret `MEDIAHUB_GITHUB_TOKEN` only inside the trusted controller to call GitHub's workflow-dispatch and run-monitoring API. The token must not enter child workflows, Gemini, prompts, logs, summaries or artifacts. The three child workflows are independent `workflow_dispatch` runs and must receive one identical immutable target SHA.

A separate `MEDIAHUB_DISPATCH_HMAC_KEY` authorizes the controller-generated child input envelope. Each child verifies the canonical HMAC payload and fixed allowlist before any provider/model step. It is not the transport token and must not be sent to a model. The controller's dispatch job is main-ref-only, requires explicit agent-mode confirmation, and the default path remains a no-secret probe.

## Gates still open

- PR #432 remains Draft and unmerged at exact head `ea637eb55c87d44f0ce22730588e744c7470ee1d`.
- Exact-head CI is now terminal SUCCESS: workflow contract validation #39604609734, Astra Verify #39604609752, caller-context probe #39604609755, controller probe #39604609766 (dispatch job SKIPPED), and Astra Cloud Runtime Validation #39604609921. Initial failures exposed stale `workflow_call` test assumptions and were corrected.
- Formal independent security review and effective repository token/governance evidence are not yet recorded.
- `MEDIAHUB_DISPATCH_HMAC_KEY` must be configured as a separate repository secret before future signed dispatch.
- No Gemini child was dispatched; no qualification or acceptance claim is made.
