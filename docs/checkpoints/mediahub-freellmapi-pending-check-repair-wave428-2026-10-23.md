# Wave 428 — Repair the pending FreeLLMAPI check after PR #530

- Date: 2026-10-23
- Status: **IMPLEMENTED ON WORKING BRANCH / EXACT-HEAD CI PENDING / NOT MERGED**
- Main base SHA: `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`
- Working branch: `fix/freellmapi-main-pending-check-20261023`
- Prior merged change: [PR #530](https://github.com/VlDMlNSh/mediahub-os/pull/530), merge commit `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- Canonical checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Master Roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)

## Exact diagnosis

PR #530 itself merged at `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`. The PR-head workflow runs are green apart from the two intentionally skipped live-dispatch jobs. The incomplete post-merge main status comes from [FreeLLMAPI Live Qualification run #39959271970](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39959271970):

- event `push`, head SHA equal to the #530 merge commit;
- run status `pending`, no conclusion;
- GitHub Actions jobs endpoint reports `total_count=0`;
- merge-commit status API reports `state=pending` with zero status contexts.

The source workflow blob before repair was `708ddeffc4664fd03f5ca6475a117348cf3666dc`. Its `push` path filter starts a live qualification workflow for main changes, and its only job uses `[self-hosted, linux, x64, mediahub-control]`. Since there is no GitHub-hosted job boundary, an unavailable/unmatched runner leaves the entire post-merge check pending. This is a queue/trigger architecture defect, not a failing adapter test. Current availability of a matching live runner was not independently queried; the zero-job pending evidence is verified.

## Bounded repair

- Split deterministic adapter/workflow-contract tests onto `ubuntu-latest` for matching `push` and `pull_request` events. That hosted job does not receive FreeLLMAPI endpoint/key-file settings and makes no live provider request.
- Preserve the live model-list and inference qualification on the existing self-hosted node, but run it only via explicit `workflow_dispatch`, with `confirm=true`, repository-owner dispatch, `refs/heads/main`, and the full `target_sha` matching `github.sha`. The self-hosted node/identity/key-file assertions remain intact.
- Separate PR contract runs, main push contract runs and explicitly dispatched live qualification concurrency. The first post-merge main push after this change uses the previous live-run concurrency key with cancellation enabled so it can retire the known stale pre-fix pending run; an explicit live run uses its own non-canceling group.
- Pin `actions/checkout` and `actions/setup-python` to full commit SHAs.
- Add `tests/test_freellmapi_qualification_workflow_contract.py` to prevent regression: hosted push/PR checks, no secrets in the hosted job, owner/SHA gate, and live-provider confinement to self-hosted qualification.

## Safety and verification

- No provider key value was read or logged.
- No FreeLLMAPI live request or model inference was made.
- No local or self-hosted executor was used to transport Gemini.
- First exact-head CI (code SHA `d9f43c4d7715e5da5c5f00eb566d914f73099514`) completed successfully: [hosted FreeLLMAPI adapter and workflow contract tests](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961121209/job/120439068618) **SUCCESS**; [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961121224/job/120439065674) **SUCCESS**; [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961121040/job/120439066441) **SUCCESS**. On this PR event, the owner-confirmation gate (job `120439071136`) and live self-hosted qualification (job `120439071269`) were **SKIPPED** by design. Formal PR reviews remain **NONE**. The report-only follow-up head `35fec91413f01238222ef9b6c68a78980aaeeb94` also completed exact-head CI successfully: FreeLLMAPI workflow run [39961494821](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961494821) (hosted contract tests job `120440337056` SUCCESS; dispatch gate `120440339180` and live qualify `120440340787` SKIPPED), Astra Verify [39961494799](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961494799) job `120440335735` SUCCESS, and Cloud Runtime Validation [39961494731](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39961494731) job `120440335541` SUCCESS. The two skipped live jobs are expected on PR events. This establishes no live qualification.
- The existing run #39959271970 remains pending on the old SHA until a new main push applies the workflow's stale-run cancellation policy; it must not be relabeled success manually.
- No merge, deployment, provider qualification or Contour A acceptance is claimed.

## Next step

Open the repair PR, inspect exact-head CI and ensure the `ubuntu-latest` contract job runs while the live self-hosted job is skipped on PR/push events. After independent review and permitted integration, verify that the next main push cancels old run #39959271970 and that the new main SHA has green hosted checks. Keep live provider qualification **NOT RUN** until an owner explicitly dispatches it from main after verifying the self-hosted runner readiness.
