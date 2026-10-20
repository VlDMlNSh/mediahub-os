# Wave 247 — PR exact-head CI and autonomous-dispatch readiness

Date: 2026-10-20
Status: bounded verification complete; Contour A remains **NOT PROVEN / BLOCKED**.

## Canonical references and current refs
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- `main` HEAD: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Docs branch HEAD before this wave: `577501f8954376b0044de350d6d67e949dfb0fc2`.
- Branches are diverged: docs branch 2,562 commits ahead, main 39 commits ahead; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No merge/rebase.
- Bootstrap blob SHA `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`; checkpoint blob before this wave `03b5791ddb814c2eacda95858ffcd50668106f14`; Master Roadmap blob SHA `beef785c787702dc174cf9a5515bac8c9f4b292f`; map blob before this wave `3e71ed85a6bdfd730111452cfc8ad081372a8f6b`. Map and checkpoint were retrieved by exact blob SHA and length-checked before append; empty Contents-wrapper output was not treated as an empty document.

## 1. Open PR status and exact-head CI read-back

| PR | Exact head SHA | State | Current CI evidence |
|---|---|---|---|
| [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375) worker checkout credential minimization | `6fb078aad7e8e1bb41916168fdd038dfa4e1022b` | OPEN, Draft, unmerged | [Astra Verify 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907) SUCCESS; [Cloud Runtime 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833) SUCCESS |
| [#388](https://github.com/VlDMlNSh/mediahub-os/pull/388) JSON Schema 2020-12 validation | `815fa4af497a593f321ee692f64f53a12dcad061` | OPEN, Draft, unmerged | [Astra Verify 39375449122](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39375449122) SUCCESS; [Cloud Runtime 39375449153](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39375449153) SUCCESS |
| [#404](https://github.com/VlDMlNSh/mediahub-os/pull/404) clean-room rebuild contract | `75ce935bd54003b63086bb990496cee1ddc96d3b` | OPEN, Draft, unmerged | [Cloud Runtime 39371237182](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39371237182) SUCCESS; [Astra Verify 39371237195](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39371237195) SUCCESS |
| [#401](https://github.com/VlDMlNSh/mediahub-os/pull/401) A2 OSS/architecture research | `0d492cd8998ed60be9b6cef2ad40d3e168907aba` | OPEN, Draft, unmerged | [Astra Verify 39370284376](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370284376) and [Cloud Runtime 39370284372](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370284372) both `action_required` |
| [#402](https://github.com/VlDMlNSh/mediahub-os/pull/402) A3 security review | `ccb26d0b65042e3b9d1d87604dc3223cb2a7f9bb` | OPEN, Draft, unmerged | [Cloud Runtime 39370303319](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370303319) and [Astra Verify 39370303391](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370303391) both `action_required` |
| [#403](https://github.com/VlDMlNSh/mediahub-os/pull/403) A1 authorization architecture | `7a939d8805d12b2b56d4c0edabcd63c15b4f3c9a` | OPEN, Draft, unmerged | [Astra Verify 39370356797](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370356797) and [Cloud Runtime 39370356910](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370356910) both `action_required` |

The combined-status API returned empty status arrays for these commits; workflow-run records above are the concrete evidence used. `action_required` is neither a test failure nor a pass: the checks did not execute to a successful conclusion. PRs #401–#403 remain research proposals, not accepted engineering changes.

## 2. Token and Gemini dispatch scope

The prior Wave 237/238 evidence remains valid but narrow:
- `MEDIAHUB_GITHUB_TOKEN` dispatched a temporary smoke target; caller run `39383103249` and target run `39383110978` succeeded; the temporary workflows were deleted after verification.
- The A1/A2/A3 workflow definitions use separate `GEMINI_API_KEY*` secrets, do not reference `MEDIAHUB_GITHUB_TOKEN`, and pass the per-job `github.token` to their configured GitHub MCP server. The job token is write-capable under workflow permissions. `persist-credentials: false` does not remove that explicit MCP token handoff.
- This pass did not dispatch A1/A2/A3 again. The connector exposes no workflow-dispatch action; the available browser profiles had no GitHub sign-in recorded. No push-triggered workaround was created, no token values were read, and no broad PAT was inserted into a worker.

## 3. Blocking interpretation

- PR #375 reduces checkout credential exposure but does not establish a replacement publisher boundary; current worker code still publishes directly. Do not merge until artifact-only worker and independent trusted publisher are designed, tested, and reviewed.
- Successful CI on #375/#388/#404 only confirms the named checks for those exact heads. It does not prove issuer/capability authentication, replay/revocation enforcement, secret isolation, production deployment, qualification, or independent acceptance.
- A1/A2/A3 PR checks remain `action_required`; their successful agent run output validators are not a substitute for PR CI.
- Issue #301 remains OPEN. Contour A remains **NOT PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.

## Next bounded action
Use an authorized authenticated dispatch mechanism (or ask the repository owner to enable/confirm a signed-in Actions UI profile) for new A1/A2/A3 runs, then inspect the exact run outputs and PR artifacts. In parallel, continue the read-only threat-model work on Issue #378 and draft an artifact-only worker/publisher contract without changing authority ownership or restoring ambient write credentials.
