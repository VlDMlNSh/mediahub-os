# MediaHub Contour A — default-deny trusted caller-context probe (Wave 292)

**Date:** 2026-10-20  
**Status:** implemented on an unmerged Draft PR branch; exact-head static/CI checks pass; trusted positive runtime remains pending.  
**Execution scope:** source change and GitHub-hosted PR validation only. No provider/model invocation, secret inspection, direct dispatch of a trusted workflow, merge, deployment, qualification or acceptance.

## Implementation

Updated PR #421 controller on branch `contour-a/workflow-call-controller-governance-wave243`.

- Added `mode` input with `probe` as the default and `agents` as the explicit alternative. The existing `confirm: yes` remains required for agent mode.
- Added a `probe` reusable-workflow job calling only `gemini-reusable-context-probe-wave284.yml`, a read-only observer with workflow/job `permissions: {}`, no secrets mapping, no checkout, no model action, and no external action.
- Added `assert_probe_context`, which checks both expected branches: a trusted `workflow_dispatch` from the exact `main` controller ref must report `trusted_controller=true`; a PR run must report `trusted_controller=false` and the merge ref.
- All three model jobs require `event_name == workflow_dispatch`, `mode == agents`, and `confirm == yes`. In probe mode they are skipped; the aggregate summary is also restricted to agent mode.
- Added static contract tests and updated existing reusable-workflow/transport contracts for the new job graph.
- Important repair during implementation: the first probe draft called the engineering child with empty permissions, conflicting with the child's workflow-level `contents: read` declaration. GitHub started no jobs (`startup_failure`). Replaced that call with the existing least-privilege observer and verified the resulting PR-triggered probe. This correction is captured here rather than treating the failed attempt as success.

## Exact-head verification

Final candidate commit: [`d7721ab3c15da3655ac2a2d71f07558c4b5f7845`](https://github.com/VlDMlNSh/mediahub-os/commit/d7721ab3c15da3655ac2a2d71f07558c4b5f7845).

| Check | Run | Result | Evidence |
|---|---:|---|---|
| Astra Verify | [39474954350](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39474954350) | PASS | 453 unit tests passed in 3.680 s |
| Gemini workflow contract validation | [39474954348](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39474954348) | PASS | actionlint step ran; 5 focused Wave 284 tests passed; contract validator passed |
| Astra Cloud Runtime Validation | [39474954173](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39474954173) | PASS | Exact-head run completed successfully |
| Existing negative caller-context probe | [39474954143](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39474954143) | PASS | Existing PR context rejected as untrusted |
| Wave 292 controller probe | [39474954081](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39474954081) | PASS | Probe and assertion succeeded; all three agent jobs and summary skipped |

Observed in the new PR run: `event_name=pull_request`, `workflow_ref=VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/pull/421/merge`, `trusted_controller=false`. The run executed the read-only reusable observer; agent1/agent2/agent3 and summary were skipped. No provider secret was mapped to the probe.

An earlier candidate commit `436ab7b613aa6e84a44db992e567ba89549f024d` failed two static assertions because PyYAML BaseLoader represents a single-item `needs: probe` as a scalar rather than a list. The assertions were corrected; the final exact-head run above passed. Earlier draft commit `4a7b2a7c44ae5064de9952a521f561aa9e597977` had contract failures and a startup failure; that probe implementation was replaced before final verification.

## What is not yet proven

- The **trusted positive path has not been executed**. This candidate is in PR #421, not `main`; dispatching a trusted positive probe is safe only after this reviewed controller implementation is merged into `main`, then using the default `mode=probe`.
- No model/provider was called, no provider key was accessed or logged, no agent execution occurred, and no write-capable probe permissions were granted.
- PR #421 remains OPEN/DRAFT/UNMERGED and has zero submitted reviews. PR #426 remains OPEN/DRAFT/UNMERGED and has zero submitted reviews. CI passing is not independent review, merge authorization, qualification, or acceptance.
- Repository rulesets endpoint returned `[]`; classic `main` branch protection endpoint returned 403 `Resource not accessible by integration`. These responses do not establish that protection is absent. Effective Actions/org policy remains unverified.
- `main` remains `80be45a70732b1d568164571d4273a6397792c3b`. Canonical documentation branch before this report: `28589282e93ff8c37b5910872e88ade2bf8fc306`.

## Disposition and next step

Wave 292 implements and validates the **non-launching negative PR path**. It does not yet establish trusted positive context. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

Next: obtain effective repository/org Actions and branch-protection policy evidence, independent review of PR #421, and only after merge dispatch the controller with `mode=probe` and `confirm=no`. Capture the positive observer output; do not choose `mode=agents` for this qualification probe. Keep PR #426 separate and unmerged until its own review/gates pass.

## Source links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) · [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426)