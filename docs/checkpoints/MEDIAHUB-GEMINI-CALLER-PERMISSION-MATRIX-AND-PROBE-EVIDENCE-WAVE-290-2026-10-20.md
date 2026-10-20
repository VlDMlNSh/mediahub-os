# MediaHub Contour A — caller/child permission matrix and probe evidence (Wave 290)

**Date:** 2026-10-20  
**Execution class:** GitHub source, run-log and status inspection; documentation only. No workflow dispatch, model/provider invocation, secret inspection, test execution, merge or deployment.

## Source-to-runtime permissions matrix (PR #421 head)

| Caller job | Called workflow | Caller permissions | Child permissions | Finding |
|---|---|---|---|---|
| `agent1` | `gemini-autonomous-engineering.yml` | contents: write; pull-requests: write; issues: read | `engineer`: same; observer/rejector: `{}` | No source mismatch visible |
| `agent2` | `gemini-agent-2.yml` | contents: write; pull-requests: write; issues: read | `engineer`: same; observer/rejector: `{}` | No source mismatch visible |
| `agent3` | `gemini-agent-3.yml` | contents: write; pull-requests: write; issues: read | `engineer`: same; observer/rejector: `{}` | No source mismatch visible |
| `summarize` | local summary | `{}` | local summary only | Least privilege |

Controller blob `da1d0254a993adcc224d5859a9a97bf609abd710`; PR #421 head `3141a44370694d78f76779243adb548318a745d7`; child blobs: agent1 `f67d62b721bcd8b86ef3a9491db5db2f50de6b1d`, agent2 `9fced7999c0ab5a5a8b9666fd92791726b64fc66`, agent3 `460f69408e0429bf70e3f71c3281fe792cc0bdf2`. The workflow-level `permissions: {}` alone does not establish that explicitly permissioned caller jobs lack write scopes. Repository/org policy and successful write behavior remain unverified.

## Runtime evidence

- [Run 39459834572](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39459834572) reports `startup_failure`; jobs API returns zero jobs. No runner-step log exists in the returned evidence. Root cause remains **unknown**; do not attribute it to permissions.
- [Run 39462792657](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792657) succeeded. Logs from [job 118766311081](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792657/job/118766311081) and [job 118766347362](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39462792657/job/118766347362) show `event_name=pull_request`, workflow ref ending `gemini-controller-context-probe-wave284.yml@refs/pull/421/merge`, and `trusted_controller=false`; negative-path assertion passed. This does **not** prove the trusted positive caller path.
- PR #421 exact-head runs #39462792590 (Astra Verify), #39462792571 (workflow contract), #39462792657 (non-launching probe), #39462792548 (Cloud Runtime Validation) succeeded. PR #426 checks #39456720322 and #39456720748 succeeded. CI success is not qualification or acceptance.
- PR #421 remains OPEN/DRAFT/UNMERGED at `3141a44370694d78f76779243adb548318a745d7`; PR #426 remains OPEN/DRAFT/UNMERGED at `6caf55977260e808a055c8c4b9a04d68eb050d8c`. Both have zero submitted independent reviews. Keep separate and unmerged.

## Disposition and next step

No dispatch, provider/model invocation, secret/host access, tests, merge, deployment, qualification, or acceptance occurred. Issue #301 remains OPEN. Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated.

Next: obtain independently reviewable repository/org Actions-policy and branch-protection evidence; then design a separately named no-credential positive-context observer called by the actual controller, with model/provider jobs unreachable. Preserve the negative-path test. Do not rerun or diagnose the zero-job failure by inference.

## Source links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) · [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421) · [PR #426](https://github.com/VlDMlNSh/mediahub-os/pull/426)