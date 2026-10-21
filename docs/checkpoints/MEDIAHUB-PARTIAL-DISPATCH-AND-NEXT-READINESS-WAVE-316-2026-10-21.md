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
- Latest PR #432 HEAD: `87f2d416364e624ecb2b26f86b493c4d68735458`, base remains the main SHA above; PR is OPEN/DRAFT/unmerged.
- Canonical documentation branch before this report: `a00bdfcb448eb508027c68237516bef2418727a8`.
- Formal PR #432 reviews: none observed.
- Issue #301: OPEN.

## Controller and test changes

PR branch: `fix/gemini-controller-api-dispatch-wave312-final`.

- `.github/workflows/gemini-batch-dispatch-controller.yml`
  - Latest blob SHA: `24c37be6f46865aced634ea0b2d04952e9bdee3b`.
  - Latest controller branch head: `87f2d416364e624ecb2b26f86b493c4d68735458`.
  - Records every intended child before POST; treats explicit non-408 4xx rejections as terminal failures and treats transport/5xx/408 outcomes as ambiguous `UNKNOWN` states.
  - Reconciles accepted and ambiguous correlation IDs. If a matching child run is found by its unique dispatch ID, the controller records `RECONCILED`; if no run can be correlated before timeout, the outcome remains failed. Final success requires each child status to be `ACCEPTED` or `RECONCILED` and its run conclusion to be `success`.
  - Adds an Issue #301 `/next` bridge restricted to exact body `/next`, owner association, non-PR issue, and main ref; replay suppression keys on an exact `next-comment-<comment-id>` marker.
  - Adds a fail-closed `MEDIAHUB_GEMINI_BATCH_ENABLED` repository-variable admission gate before any controller token/secret mapping to the dispatch job.
  - Keeps full summary and nonzero fail-closed result for any incomplete batch.
- `tests/test_gemini_transport_controller_contract.py`
  - Latest blob SHA: `2806962ef90a892b49288cadf56925b60d39e224`.
  - Adds contract checks for ambiguous dispatch reconciliation, exact comment replay marker, and closed-by-default admission gate.
- `tests/test_gemini_controller_positive_context_probe_wave292_contract.py`
  - Latest blob SHA: `84a92e514c930c55d411bf74ad390109b7ed0d4b`.
  - Updated legacy assertion to accept the expanded owner-only `/next` condition.

## Exact-head CI

All five checks below refer to `87f2d416364e624ecb2b26f86b493c4d68735458` and completed successfully.

- [Workflow contract validation #39646172941](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39646172941) — SUCCESS.
- [Astra Verify #39646173254](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39646173254) — SUCCESS.
- [Astra Cloud Runtime Validation #39646173261](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39646173261) — SUCCESS.
- [Controller PR-context probe #39646173269](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39646173269) — SUCCESS; `dispatch_and_monitor` was SKIPPED.
- [Reusable workflow caller-context probe #39646173087](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39646173087) — SUCCESS; PR caller denied.

Prior attempt at head `48ab99c9b56cf778ee7c6e82381b424e68945506` failed because the new contract test still expected the prior `FAILED` marker. The failure was inspected in the workflow logs, the assertion was corrected, and all five checks passed on the subsequent exact head.

## Requested per-/next orchestration readiness

The requested end state requires both the GitHub controller and an event bridge that maps a ChatGPT `/next` turn to a trusted GitHub dispatch. A ChatGPT message is not itself a GitHub Actions event. The candidate bridge is implemented in Draft PR #432 as an owner-only Issue #301 comment trigger; it is not live until independently reviewed and merged. Once live, this ChatGPT workflow must post the matching owner-authored `/next` comment to Issue #301 for each chat request. The connector's actual comment author association and trusted-main issue-comment event context remain unverified, so automatic execution from a chat `/next` is not yet qualified.

A candidate bridge is now implemented on Draft PR #432: an exact `/next` comment on Issue #301 by an OWNER, on a non-PR issue, can enter the controller; it uses a comment-ID marker for replay suppression. A repository variable `MEDIAHUB_GEMINI_BATCH_ENABLED` must be `true` before the secret-bearing dispatch job can run; unset/false skips child dispatch. The bridge is not live until reviewed and merged. The ChatGPT message itself is not a GitHub event; when accepted, the assistant must create the corresponding owner-authored Issue #301 comment for each `/next`, and this comment-authorship/event path must be verified with a no-secret probe. The bridge must not put `MEDIAHUB_GITHUB_TOKEN` into child workflows, prompts, logs, or artifacts, and must not use `secrets: inherit`.

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
- Issue #301 owner-only `/next` bridge: IMPLEMENTED IN DRAFT PR, NOT LIVE/VERIFIED; ChatGPT connector comment authorship and trusted-main issue-comment event context still require a no-secret probe after merge.
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
