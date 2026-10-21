# Wave 316 — ambiguous dispatch reconciliation and automation readiness (2026-10-21)

## Executive result

Wave 316 corrected a second controller failure mode in Draft PR #432: a GitHub API/network exception during a dispatch POST does not prove that the child workflow was not accepted. The controller now marks that outcome `UNKNOWN` and reconciles the correlation ID alongside every other intended child. It still fails closed unless all three dispatches were explicitly accepted and every child run succeeded.

The exact-head CI initially caught a stale contract assertion expecting `FAILED`; the assertion was updated to the new `UNKNOWN` state. All five required PR checks subsequently completed successfully on the latest head. This is implementation and CI verification only, not independent qualification or acceptance.

## Canonical sources and governance

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governance issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Draft controller PR #432: https://github.com/VlDMlNSh/mediahub-os/pull/432

Observed refs:
- `main` HEAD: `f16e5bae202a78584f273132e7f88c6e25d3142e`.
- Latest PR #432 HEAD: `2b53167a48a04c5ec83c86b730a8513504e51ee5`, base remains the main SHA above; PR is OPEN/DRAFT/unmerged.
- Canonical documentation branch before this report: `a00bdfcb448eb508027c68237516bef2418727a8`.
- Formal PR #432 reviews: none observed.
- Issue #301: OPEN.

## Controller and test changes

PR branch: `fix/gemini-controller-api-dispatch-wave312-final`.

- `.github/workflows/gemini-batch-dispatch-controller.yml`
  - Latest blob SHA: `14681c8b0b8acb6c52568d49aeb53eb32cfd53fd`.
  - Commit: `39b00c0d8acee3e2b74c3e69cfd1c065d534aa60`.
  - Every intended child is recorded before the POST.
  - API/network exceptions are classified as `UNKNOWN` without printing exception bodies.
  - Reconciliation monitors every correlation ID, not only POSTs with an observed 204 response.
  - An unknown dispatch outcome cannot satisfy the final success predicate, even if a child run is found and succeeds.
  - Full batch summary and nonzero fail-closed outcome remain required on any dispatch/run failure or timeout.
- `tests/test_gemini_transport_controller_contract.py`
  - Latest blob SHA: `3dea2dee06fea903167155925d3b8338f513d719`.
  - Commit: `2b53167a48a04c5ec83c86b730a8513504e51ee5`.
  - Static contract now checks that ambiguous dispatches are reconciled and recorded as `UNKNOWN`.

## Exact-head CI

All five checks below refer to `2b53167a48a04c5ec83c86b730a8513504e51ee5` and completed successfully:

- [Workflow contract validation #39644795091](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39644795091) — SUCCESS.
- [Astra Verify #39644795075](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39644795075) — SUCCESS.
- [Astra Cloud Runtime Validation #39644795068](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39644795068) — SUCCESS.
- [Controller PR-context probe #39644795115](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39644795115) — SUCCESS; `dispatch_and_monitor` was SKIPPED.
- [Reusable workflow caller-context probe #39644795211](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39644795211) — SUCCESS; PR caller denied.

Prior attempt at head `48ab99c9b56cf778ee7c6e82381b424e68945506` failed because the new contract test still expected the prior `FAILED` marker. The failure was inspected in the workflow logs, the assertion was corrected, and all five checks passed on the subsequent exact head.

## Requested per-/next orchestration readiness

The requested end state requires both the GitHub controller and an event bridge that maps a ChatGPT `/next` turn to a trusted GitHub dispatch. A ChatGPT message is not itself a GitHub Actions event. The available GitHub connector tools in this session can inspect and update repository resources but do not expose a workflow-dispatch operation. No bridge from ChatGPT turn events to GitHub was observed or configured in this pass. Therefore do not claim that a chat `/next` currently triggers the controller automatically.

A future bridge must be owner-only, replay-resistant, scoped to Issue #301 or an explicitly approved integration, use a common immutable target SHA, pass only fixed bounded tasks, and remain fail-closed until all gates are accepted. It must not put `MEDIAHUB_GITHUB_TOKEN` into child workflows, prompts, logs, or artifacts, and must not use `secrets: inherit`.

## Local executor and browser readiness

- Desktop Commander device inventory showed `Voktors-Mini.Dlink` online; `mh-dev-01` and `mh-dev-02` offline.
- SentinelX showed only `Voktors-Mini.Dlink` operational; `mh-dev-01` and `mh-dev-02` are disabled. No host identified as Alamo/server 3 was available.
- Therefore the mandated local Claude Code on Alamo and @SentinelX/agent-browser checks were NOT RUN. Do not substitute Voktors or another server for Alamo.
- The Wave 272 binding requirement remains: Claude on Alamo must prove a permitted non-paid authorization route, no paid Anthropic API fallback, known upstream/terms/cost class and documented egress before qualification.

## Gates still open

- Independent security review of exact PR #432 head: NOT VERIFIED (no formal review).
- Effective `MEDIAHUB_GITHUB_TOKEN` permissions/scope: NOT VERIFIED.
- Presence and separation of `MEDIAHUB_DISPATCH_HMAC_KEY`, without reading its value: NOT VERIFIED.
- Branch protection / organization Actions governance: NOT VERIFIED by the available inspection response.
- Trusted-main no-secret probe: NOT VERIFIED; PR-context probe is not equivalent.
- ChatGPT `/next` to GitHub dispatch bridge: NOT IMPLEMENTED/NOT VERIFIED.
- Gemini Agents 1–3: NOT RUN; no controller run ID or child run IDs for Wave 316.
- Alamo Claude and browser: NOT RUN; host identity/capabilities not verified.

## Next bounded acceptance sequence

1. Obtain an independent security review of exact head `2b53167a48a04c5ec83c86b730a8513504e51ee5`.
2. Verify effective token scope, HMAC-secret configuration/separation and repository/organization governance without exposing secret values.
3. Design and review an owner-only, replay-resistant `/next` bridge; do not treat an issue comment as equivalent to a ChatGPT event unless the integration explicitly posts it.
4. Positively identify Alamo and validate the approved non-paid Claude route and browser capabilities independently of Gemini transport.
5. Only after the gates above are VERIFIED/ACCEPTED, authorize the first real batch and record controller run ID, all three child run IDs, common target SHA, result/artifact digests and independent verification.

## Provenance limits

Controller and test files were re-read from the PR branch after the final edits; their blob SHAs are recorded above. The exact-head CI statuses were queried from GitHub. No agent-mode workflow was dispatched, no secret values were read, no PR was merged, and no local executor was run. This report does not claim qualification, deployment, or acceptance.
