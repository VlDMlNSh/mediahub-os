# MediaHub OS — lock-generation evidence gap (Wave 101, 2026-10-17)

## Result

This pass verified the current candidate workflow and the exact-head schema-validation run, but did **not** establish that the separate lock-generation workflow executed. Reproducibility remains unverified.

## Sources and immutable references

- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Candidate PR: [#338](https://github.com/VlDMlNSh/mediahub-os/pull/338), open and Draft.
- Candidate workflow commit: [`29d72044ae77086df3380358816da2e15a940725`](https://github.com/VlDMlNSh/mediahub-os/commit/29d72044ae77086df3380358816da2e15a940725).
- Lock-generation workflow: [`.github/workflows/cloud-agent-lock-generation.yml`](https://github.com/VlDMlNSh/mediahub-os/blob/contour-a-schema-validation-consolidation-wave98-20261017/.github/workflows/cloud-agent-lock-generation.yml), blob SHA `bc6a50bb93ec8ba32aacc7e3b7f973a6311cb072`.
- Direct input: `requirements/cloud-agent-schema-validation.in`, blob SHA `46aa24e6ab56bc0bc1c69e29ffa778e7f2c74635`.
- Checked-in generated lock: `requirements/cloud-agent-schema-validation.lock`, blob SHA `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- Exact-head schema validation: [run 39053283811](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053283811), commit `29d72044ae77086df3380358816da2e15a940725`, conclusion `success`.
- That run's evidence artifact: [artifact 12108506417](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39053283811), digest `sha256:898ffd15cc92d639116f873a046de7a192adcd07a7d3e31165579f20bb235476`. It is **schema-validation evidence**, not regenerated-lock evidence.

## Findings

1. The lock-generation workflow has `workflow_dispatch` and a `push` trigger for changes to its workflow or the `.in` input. Its source contains diff capture, artifact upload and a byte-for-byte `git diff --exit-code` gate.
2. The available commit-run query only returns pull-request-triggered runs. It returned the schema-validation run above; it cannot enumerate the separate push/dispatch run. A public search for the lock-generation artifact name returned no result. The connected GitHub fetch endpoint did not accept the workflow-runs collection URL. Therefore this pass cannot conclude that the lock workflow did or did not run; no lock-generation run ID, job result, artifact digest or regenerated lock was verified.
3. The lock-generation workflow still bootstraps `pip==24.3.1` and `pip-tools==7.4.1` by version-only installation from PyPI. The runtime validator lock's hashes do not prove integrity of this separate bootstrap. No bootstrap hash lock was fabricated in this pass.
4. The schema-validation run succeeded, but that is not evidence of byte-for-byte lock reproducibility. No claim of reproducibility or bootstrap integrity is made.

## Verification and disposition

- Workflow source re-read: PASS; guard and artifact steps present.
- Exact-head schema-validation job: PASS.
- Lock-generation execution and artifact read-back: **NOT VERIFIED**.
- Bootstrap package integrity: **OPEN**.
- PR #338: remains Draft/open/unmerged.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301): remains open; A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent review and bounded worker/queue qualification remain open.
- No provider calls, secret access, agent dispatch, deployment, merge or Contour A acceptance occurred.

## Next bounded step

Use an authorized Actions run-list/dispatch interface to enumerate runs for workflow `cloud-agent-lock-generation.yml` on the candidate branch, dispatch it only if the same candidate SHA has not already been tested, and capture run/job/artifact IDs. Download and compare the regenerated lock and diff; only after that evidence exists, separately introduce and verify a hash-controlled bootstrap for pip and pip-tools. Do not update the lock file merely to make the comparison pass.
