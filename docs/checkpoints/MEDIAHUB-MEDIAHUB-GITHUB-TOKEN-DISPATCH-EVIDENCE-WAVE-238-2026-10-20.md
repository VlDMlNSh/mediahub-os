# Wave 238 — MEDIAHUB_GITHUB_TOKEN workflow-dispatch evidence and Contour A state

Date: 2026-10-20
Status: evidence recorded; Contour A remains **NOT PROVEN / BLOCKED**.

## Objective
Record the verified successful GitHub Actions workflow dispatch using the repository Actions secret `MEDIAHUB_GITHUB_TOKEN`, and refresh the relevant repository refs and governance status without promoting unaccepted code.

## Verified dispatch evidence
- Caller workflow run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39383103249
  - Run ID: `39383103249`
  - Caller job ID: `118496508757`
  - Job conclusion: `success`
  - Job log reported `workflow_dispatch_http_status=204` and `PASS: MEDIAHUB_GITHUB_TOKEN dispatched the temporary smoke target`.
- Target workflow run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39383110978
  - Run ID: `39383110978`
  - Target job ID: `118496536978`
  - Event: `workflow_dispatch`
  - Job conclusion: `success`.
- Triggering commit for the temporary caller: `48cd45187a3a7c52368204577ab7857e85b44606`.
- Temporary caller and target workflow files were deleted after the probe; both paths were re-read and returned 404.
- `main` after cleanup: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical documentation branch `docs/mediahub-chat-tree-map-20261012` at start of this pass: `1c30ecbc0f9b2ae650c3d72980847e083916dece`.

## Interpretation and limits
This proves that the named secret was sufficient for this narrow temporary REST workflow-dispatch smoke test. It does **not** prove that Gemini dispatch queues are healthy, that three Gemini agents are running, that the distributed worker admission path is secure, or that Contour A is qualified, deployed, or accepted. Do not expose this token to model-execution jobs or worker processes. A broad classic PAT is a high-impact credential; migrate to least privilege or a narrowly scoped GitHub App, separate worker execution from trusted publication, and rotate/revoke the broad token after migration.

The earlier fine-grained `PAT_DISPATCH` test could read the large roadmap/checkpoint and create/delete a ref, but workflow dispatch returned HTTP 403. Do not conflate that failed fine-grained-token test with the successful `MEDIAHUB_GITHUB_TOKEN` classic-token smoke test.

## Ref and governance audit
- `main`: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical docs branch: `docs/mediahub-chat-tree-map-20261012`, `1c30ecbc0f9b2ae650c3d72980847e083916dece`.
- Branches diverge; the latest comparison in this pass reported `main` 39 commits ahead and 2,558 behind the docs branch (merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`). Do not merge these branches as incidental documentation maintenance.
- Bootstrap blob SHA: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`.
- Checkpoint blob SHA: `e0ac08c2ab8578ff76c859ba43ff9f81adff9d8f`.
- Master Roadmap blob SHA: `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Canonical map blob read via Git Database API SHA `59973971096b716664e7c6cb6286af6fe84e4a1a`; complete content was retrieved. The map records Wave 237 and the current open trust-boundary gaps; this pass does not rewrite the large map.
- Issue #301 remains OPEN.
- PR #375, #388 and #404 remain open Draft/unmerged based on current PR metadata read. CI successes previously recorded for #388/#404 are not equivalent to acceptance; no merge was performed.
- Worker source `ops/qualification/run_distributed_local_worker.py` blob SHA `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`; the worker source does not itself implement issuer/capability/signature/replay/revocation validation, and it contains worker-side `git push` publication. This remains a blocking trust-boundary defect to address before qualification.

## Canonical references
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Wave 237 classic PAT dispatch verification](MEDIAHUB-CLASSIC-PAT-DISPATCH-VERIFICATION-WAVE-237-2026-10-20.md)

## Next bounded action
Trace the current Gemini/A0 workflow admission path and prove where `MEDIAHUB_GITHUB_TOKEN` is referenced or not referenced. If no safe, available dispatch tool can trigger the three mandated agent workflows from this session, record that limitation and continue with read-only source tracing rather than passing the broad token to workers. Define and test an artifact-only worker plus separate trusted publisher only after the issuer/capability and target-manifest contracts are established through the required governance process.
