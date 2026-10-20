# MediaHub Contour A — exact-head CI repair and revalidation (Wave 293)

**Date:** 2026-10-20  
**Status:** targeted controller-contract CI and repository verification passed at the current unmerged PR head; trusted positive runtime and governance remain unproven.  
**Scope:** repair failing static contract expectations, ensure CI actually runs the new Wave 292 contracts, and record exact-head evidence. No model/provider invocation, secret access, agent execution, trusted workflow dispatch, merge, deployment, qualification, or acceptance.

## Change and rationale

PR #421 remains on `contour-a/workflow-call-controller-governance-wave243`. The controller declares `needs: probe` as a scalar dependency, so the PyYAML BaseLoader contract must assert the scalar string rather than a one-element list. The two tests now match the source workflow syntax. The dedicated workflow contract-validation workflow was also updated to trigger for the new Wave 292 contract and the reusable-workflow/transport contract tests, then execute each targeted suite in CI instead of only the legacy Wave 284 test.

## Exact-head candidate

- Branch head: [`185f55b63121b1aece7e60f6c087ecfceab2721e`](https://github.com/VlDMlNSh/mediahub-os/commit/185f55b63121b1aece7e60f6c087ecfceab2721e)
- PR: [#421](https://github.com/VlDMlNSh/mediahub-os/pull/421), open / Draft / unmerged.
- Base `main`: `80be45a70732b1d568164571d4273a6397792c3b`.
- Current branch compare: 66 commits ahead, 0 behind, merge base `80be45a70732b1d568164571d4273a6397792c3b`.
- Parent sequence in this repair: `d7721ab3c15da3655ac2a2d71f07558c4b5f7845` → `01adf01f6a2436d67dc4acdd774f33597658e11c` → final `185f55b63121b1aece7e60f6c087ecfceab2721e`. The intermediate `01adf01` still failed the new scalar assertion and is not treated as passing.

## Verification evidence at final head

| Check | Run | Result | Evidence |
|---|---:|---|---|
| Astra Verify | [39475766199](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766199) | PASS | 453 unit tests passed in 4.198 s |
| Gemini workflow contract validation | [39475766192](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766192) | PASS | actionlint passed; focused suites passed: Wave 284 5, Wave 292 5, reusable workflow 12, transport 5 |
| Astra Cloud Runtime Validation | [39475766251](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766251) | PASS | Completed successfully at exact head |
| Existing negative caller-context probe | [39475766469](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766469) | PASS | PR context remains untrusted |
| Wave 292 controller probe | [39475766513](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39475766513) | PASS | Observer and assertion passed; agent1/agent2/agent3 and summary were skipped |

Observed runtime evidence remains only the negative PR path: `event_name=pull_request`, `workflow_ref=VlDMlNSh/mediahub-os/.github/workflows/gemini-batch-dispatch-controller.yml@refs/pull/421/merge`, `trusted_controller=false`. The probe maps no provider secret and has no write permissions. No trusted `workflow_dispatch` positive path has been executed.

## Governance and residual blockers

- PR #421 and PR #426 remain open, Draft, unmerged, with zero submitted independent reviews at this pass.
- PR #426 changes overlapping caller-context probe files; keep both candidates separate and resolve the path/ownership collision before integration.
- The repository rulesets endpoint returned an empty list and the classic `main` branch protection endpoint returned 403 to the available integration. Neither result proves protection is absent. Effective repository/organization Actions policy remains unverified.
- The successful checks are implementation/test evidence only. They are not independent review, merge approval, deployment, qualification, or acceptance.

## Disposition and next step

Wave 293 repairs the test contract and makes the dedicated CI workflow exercise the relevant suites. The final head is CI-green. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

Next: resolve PR #421/#426 overlap and obtain independent security review plus effective branch-protection/Actions policy evidence. Only after the reviewed controller is accepted on `main), run the controller with `mode=probe` and `confirm=no` to gather trusted positive-context evidence. Do not use `mode=agents` for qualification.

## Source links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Wave 292 report](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-DEFAULT-DENY-TRUSTED-CALLER-CONTEXT-PROBE-WAVE-292-2026-10-20.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) · [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426)
