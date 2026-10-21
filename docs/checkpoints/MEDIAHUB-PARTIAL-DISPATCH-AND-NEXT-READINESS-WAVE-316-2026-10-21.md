# Wave 316 — ambiguous dispatch reconciliation and automation readiness (2026-10-21)

## Executive result

Wave 316 corrected a second controller failure mode in Draft PR #432: a GitHub API/network exception during a dispatch POST does not prove that the child workflow was not accepted. The controller marks ambiguous POST outcomes `UNKNOWN` and reconciles each correlation ID. A matching child run makes the attempt `RECONCILED`; an uncorrelated timeout remains failed. Final success requires each dispatch to be `ACCEPTED` or `RECONCILED` and every child run conclusion to be `success`.

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
- Latest PR #432 HEAD: `269b57b8b9c412261c97c4811bd49cbb4122ba03`, base remains the main SHA above; PR is OPEN/DRAFT/unmerged.
- Canonical documentation branch before this report: `a00bdfcb448eb508027c68237516bef2418727a8`.
- Formal PR #432 reviews: none observed.
- Issue #301: OPEN.

## Controller and test changes

PR branch: `fix/gemini-controller-api-dispatch-wave312-final`.

- `.github/workflows/gemini-batch-dispatch-controller.yml`
  - Latest blob SHA: `9453403bba899a2400ee3fb874d32badd034c704`.
  - Latest controller branch head: `269b57b8b9c412261c97c4811bd49cbb4122ba03`.
  - Records every intended child before POST; treats explicit non-408 4xx rejections as terminal failures and treats transport/5xx/408 outcomes as ambiguous `UNKNOWN` states.
  - Reconciles accepted and ambiguous correlation IDs; an unknown outcome never counts as successful dispatch.
  - Adds an Issue #301 `/next` bridge restricted to exact body `/next`, owner association, non-PR issue, and main ref; replay suppression keys on an exact `next-comment-<comment-id>` marker.
  - Adds a fail-closed `MEDIAHUB_GEMINI_BATCH_ENABLED` repository-variable admission gate before any controller token/secret mapping to the dispatch job.
  - Keeps full summary and nonzero fail-closed result for any incomplete batch.
- `tests/test_gemini_transport_controller_contract.py`
  - Latest blob SHA: `081ba101a1b56553577abd7b469b3c9bf6f31196`.
  - Adds contract checks for ambiguous dispatch reconciliation, exact comment replay marker, and closed-by-default admission gate.
- `tests/test_gemini_controller_positive_context_probe_wave292_contract.py`
  - Latest blob SHA: `84a92e514c930c55d411bf74ad390109b7ed0d4b`.
  - Updated legacy assertion to accept the expanded owner-only `/next` condition.

## Exact-head CI

All five checks below refer to `269b57b8b9c412261c97c4811bd49cbb4122ba03` and completed successfully:

- [Workflow contract validation #39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718) — SUCCESS.
- [Astra Verify #39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683) — SUCCESS.
- [Astra Cloud Runtime Validation #39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609) — SUCCESS.
- [Controller PR-context probe #39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682) — SUCCESS; `dispatch_and_monitor` was SKIPPED.
- [Reusable workflow caller-context probe #39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781) — SUCCESS; PR caller denied.

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


## Wave 317 role-task refinement (same Draft PR)

The controller task payloads now assign three distinct roadmap-driven roles per admitted /next batch: Agent 1 selects and performs one bounded implementation task; Agent 2 independently verifies contracts/tests without claiming review of concurrent Agent 1 work; Agent 3 audits security, least privilege, quota/fallback policy and provenance. Each is constrained to draft evidence/PR work, no merge/deployment/qualification and no nested dispatch. Latest branch head for this refinement is `269b57b8b9c412261c97c4811bd49cbb4122ba03`; controller blob `9453403bba899a2400ee3fb874d32badd034c704`; test blob `081ba101a1b56553577abd7b469b3c9bf6f31196`. Exact-head CI all SUCCESS: [contract validation #39647070718](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070718), [Astra Verify #39647070683](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070683), [Cloud Runtime Validation #39647070609](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070609), [controller probe #39647070682](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070682; child dispatch skipped), [caller-context probe #39647070781](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39647070781).


## Branch hygiene correction — documentation-only commits (2026-10-21)

During report reconciliation, four documentation-only commits were inadvertently written to `main` instead of the canonical documentation branch. The issue was detected by comparing refs and commit ancestry. The affected commits changed only these four files: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-316-2026-10-21.md`, `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`, `docs/checkpoints/MEDIAHUB-PARTIAL-DISPATCH-AND-NEXT-READINESS-WAVE-316-2026-10-21.md`, and `docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md`; compare showed four commits ahead and zero behind from the prior main SHA, with no non-doc files changed. Before repair, a recovery branch `recovery/wave316-docs-main-misroute-20261021` was created and verified at `1f9fe47f986376a733fb0ddfa5e3b567b2613d5c`. Then `main` was restored using force-with-lease from `1f9fe47f986376a733fb0ddfa5e3b567b2613d5c` to the previously observed `f16e5bae202a78584f273132e7f88c6e25d3142e`. Post-repair refs confirm main is back at `f16e5bae202a78584f273132e7f88c6e25d3142e`, and the recovery branch preserves the four commits. Canonical documentation remains on `docs/mediahub-chat-tree-map-20261012`. Recovery branch: https://github.com/VlDMlNSh/mediahub-os/tree/recovery/wave316-docs-main-misroute-20261021.


## Wave 320 follow-up — current PR head and branch integrity (2026-10-21)

- Latest observed PR #432 head: `8a6bc17180ff8027edb5c628f8092a4c527212b5` (OPEN/DRAFT/unmerged). Controller blob remains `9453403bba899a2400ee3fb874d32badd034c704`; transport contract test blob `081ba101a1b56553577abd7b469b3c9bf6f31196`; reusable workflow contract test blob `65bc0c4b9a7eb58a71bb1b8123cf1ff4305f52af`. All three child workflows now contain the canonical UUIDv4 dispatch-ID pattern, and the reusable workflow contract includes positive/negative UUID fixtures.
- Exact-head CI all SUCCESS: contract validation [#39648235554](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235554), Astra Verify [#39648235100](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235100), Cloud Runtime Validation [#39648235456](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235456), controller non-launching probe [#39648235821](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235821; dispatch skipped), caller-context probe [#39648235621](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39648235621).
- Branch integrity: current `main` was verified restored to `f16e5bae202a78584f273132e7f88c6e25d3142e`. Two accidental documentation-only main advances were preserved before repair: `recovery/wave316-docs-main-misroute-20261021` at `1f9fe47f986376a733fb0ddfa5e3b567b2613d5c` (four `docs/` files only) and `recovery/wave319-review-main-misroute-20261021` at `61b8ea4fa918f5e629cc9fee674673b525c5c6b5` (Wave 319 source-review report only). The Wave 319 report was copied to the canonical documentation branch at blob `3eaac1b7a3443ccabc080954ed6a2774e9e688e5`; canonical URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-PR432-SOURCE-SECURITY-REVIEW-WAVE-319-2026-10-21.md.
- These repairs preserved commits rather than discarding them. No agent-mode dispatch occurred. Formal independent PR review remains absent; the source-only Wave 319 review explicitly does not qualify PR #432.
