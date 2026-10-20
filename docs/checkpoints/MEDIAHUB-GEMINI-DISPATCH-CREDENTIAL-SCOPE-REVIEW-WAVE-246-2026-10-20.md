# Wave 246 — Gemini dispatch boundary and workflow credential-scope review

- Date: 2026-10-20
- Status: **SOURCE REVIEW COMPLETE; NEW A1/A2/A3 DISPATCH NOT PERFORMED; CONTOUR A NOT PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Ref and governance snapshot

- `main`: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical docs branch before this update: `ae45f7af63c9f7d8023cf0109a69029f82175fe5`.
- Merge base: `f0f406feb9f9816b009f4e6e756813541e53b9bc`; comparison is diverged (main 39 ahead, docs branch 2,561 ahead). No branch merge/rebase was performed.
- Bootstrap blob: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`.
- Checkpoint blob before this update: `1eff0ee249fa24d2471308f5adda53cead926b41` (861,488 characters).
- Master Roadmap blob: `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Canonical map blob before this update: `e928866157448038c040b63ec4bc4231ad44821b` (1,098,767 characters), retrieved completely by Git blob SHA because the Contents wrapper returns an empty body.
- Issue #301 remains OPEN. PR #375, #388 and #404 remain OPEN/Draft/unmerged in the current metadata read. Main's combined status endpoint returned no status entries; that is not a pass signal. No merge, deployment or qualification was performed.

## 2. A1/A2/A3 workflow definitions — source evidence

All three workflow files exist on `main` and accept `workflow_dispatch` with required task, base_ref constrained to `main`, and scope constrained to `contour-a`.

| Agent | File | Blob SHA | Model credential reference |
|---|---|---|---|
| A1 engineering/governance | `.github/workflows/gemini-autonomous-engineering.yml` | `09523d809530ae5b7bf528eab5fa53bc5deaf92d` | `secrets.GEMINI_API_KEY` |
| A2 research/architecture | `.github/workflows/gemini-agent-2.yml` | `259c8c82b8d90a39e1c90e65390e469b241b5581` | `secrets.GEMINI_API_KEY_2` |
| A3 security/verification | `.github/workflows/gemini-agent-3.yml` | `91b5397001e088dfae2f450ee77c9c23118b5601` | `secrets.GEMINI_API_KEY_3` |

Each workflow sets job permissions to `contents: write`, `pull-requests: write`, `issues: read`; checkout uses `persist-credentials: false`. The Gemini CLI action receives the per-run `github.token` as `GITHUB_TOKEN`, and the configured Docker GitHub MCP server receives it as `GITHUB_PERSONAL_ACCESS_TOKEN`. Thus the classic `MEDIAHUB_GITHUB_TOKEN` is not referenced by these workflow files. The token available to Gemini is instead the GitHub Actions job token with the permissions above; it can create branches/files/PRs through the allowlisted MCP tools. This is a real write-capable model boundary, not a read-only review workflow.

The prompt in each workflow mandates one bounded documentation/evidence pass and explicitly prohibits merge/deploy, installation, testing/qualification, additional provider calls, host/runtime inspection, infrastructure changes, migrations and secret changes. The post-step validates a non-empty JSON response, at least one successful tool call, and a successful PR tool call. These checks do not independently review the resulting patch or prove that claims in the PR are true.

## 3. Dispatch result and blocker

- This pass did not submit A1/A2/A3 dispatches; no new run IDs are claimed.
- The available GitHub connector supports reads and selected repository writes but exposes no workflow-dispatch operation.
- The available TinyFish browser profiles (`Default`, `MediaHub Freebuff`) both have an empty `signed_in_sites` list. Per browser integration rules, no authenticated Actions UI automation was attempted without a profile known to be signed in.
- No credential-bearing temporary push-triggered dispatch workflow was created. No token value was read or printed.
- Recent repository runs include the previously proven token smoke target, which has since been removed; that evidence remains limited to the temporary target and is not evidence that A1/A2/A3 have been launched in this pass.

## 4. Security interpretation

1. **Verified:** A1/A2/A3 use separate Gemini API secret names and do not reference `MEDIAHUB_GITHUB_TOKEN` in their workflow source.
2. **Verified:** Each workflow grants a write-capable job token to the Gemini MCP server. The exposed tools are limited to repository file read, branch creation, file create/update and PR creation; the model is not given merge/deploy tools in this configuration.
3. **Verified:** `persist-credentials: false` prevents checkout from persisting credentials in Git configuration, but does not make the whole job tokenless because the workflow explicitly passes `github.token` to the MCP server.
4. **Unknown:** Current secret presence/validity, successful provider authentication, quota availability, actual A1/A2/A3 run completion, and resulting artifact quality. Secrets APIs are not accessed.
5. **Open P0:** The distributed local worker source and workflow remain a separate issue: worker-side Git publication and missing issuer/capability/replay/revocation validation are not resolved by these Gemini workflows. Keep worker and trusted publisher separated.

## 5. Required next step

Obtain an authenticated GitHub Actions dispatch path using a browser profile that is confirmed signed in or a supported authorized API action. Dispatch A1/A2/A3 in parallel with distinct bounded tasks and capture the exact run IDs and conclusions. Do not place `MEDIAHUB_GITHUB_TOKEN` into model prompts, worker environments, task JSON or repository files. Then review resulting PRs against current `main`, verify their diffs and exact-head CI, and keep them Draft until required security/governance gates pass.

Contour A remains **NOT PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.
