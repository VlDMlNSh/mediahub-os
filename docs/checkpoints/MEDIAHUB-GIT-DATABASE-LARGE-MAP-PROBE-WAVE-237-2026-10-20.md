# MediaHub OS — Git Database API large-map update and live PR reconciliation (Wave 237)

- Date: 2026-10-20
- Scope: verify a safe Git Database API path for the >1 MiB canonical architecture map; refresh branch/PR state; record evidence without merging Draft PRs or changing Contour A gates.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governance issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Status: Git Database API accepted the complete map payload; a content-preserving blob round-trip returned the exact original SHA. This validates payload acceptance, not yet a distinct-content write until the actual documented map update is committed and read back.

## Live refs and divergence

- `main`: `8761f734031ef0b880b974cea24c2463e7a22046`
- `docs/mediahub-chat-tree-map-20261012`: `1e9d62ffcbd6e7d66ef21ad2c500d13523f7d938`
- Compare `main...docs`: diverged; docs is 2,551 commits ahead and 35 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge the documentation branch into main as part of this pass.

## Large-file read and Git Database API probe

The canonical map's Contents wrapper returned an empty body, but the Git blob endpoint successfully returned the full file:

- Path: `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`
- Original blob SHA: `2187b4ca50792fe073f0979442c0f73432a2f6f9`
- Complete payload length returned by the connector: 1,094,624 characters
- `POST /git/blobs` through the GitHub connector with the complete UTF-8 payload returned the same blob SHA `2187b4ca50792fe073f0979442c0f73432a2f6f9`.
- SHA equality confirms byte-for-byte content identity under Git object hashing. No branch ref moved during this probe.

The Contents wrapper's empty body is a wrapper/representation limitation for this file, not evidence that the Git object is unavailable. Git Database API is the preferred route for an atomic, history-preserving update of this existing >1 MiB map. Git LFS is not justified by this evidence; do not migrate the canonical map to LFS.

## Canonical source read-back

- Bootstrap blob: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`, 26,325 characters.
- Canonical map blob: `2187b4ca50792fe073f0979442c0f73432a2f6f9`, 1,094,624 characters via Git blob endpoint.
- Continuation checkpoint blob: `b9978ca997f966c1d3fc0c9baa2520a0c5366826`, 858,660 characters.
- Master Roadmap blob: `beef785c787702dc174cf9a5515bac8c9f4b292f`, 317,131 characters.
- The map contains extensive historical references to A0, issuer/capability, worker/publisher and Baseline 2.0; preserve historical IDs and do not rewrite or renumber the existing history.

## Current Draft PRs and CI

- PR #388: OPEN / Draft / unmerged; head `815fa4af497a593f321ee692f64f53a12dcad061`, base `main`. Exact-head runs: Astra Verify `39375449122` SUCCESS; Astra Cloud Runtime Validation `39375449153` SUCCESS.
- PR #404: OPEN / Draft / unmerged; head `75ce935bd54003b63086bb990496cee1ddc96d3b`, base `main`. Exact-head runs: Astra Verify `39371237195` SUCCESS; Astra Cloud Runtime Validation `39371237182` SUCCESS.
- Empty combined-status arrays are not treated as evidence of failure or success when explicit workflow-run records exist. No PR merged in this pass.
- Issue #301 remains OPEN.

## Security and workflow dispatch context

The preceding PAT_DISPATCH probe proved large Contents API reads and a bounded Git ref create/delete. A REST workflow-dispatch request returned HTTP 403, so dispatch authority remains unproven. Do not put PATs in chat, worker task JSON, command-line arguments or logs. Recheck fine-grained token Actions: write and repository/org policy separately; do not grant broader permissions merely to silence a 403.

## Next actions and boundaries

1. Update the canonical map by appending a dated, linked Wave 237 entry through Git Database API: fetch current branch ref and commit/tree, create a new full-content blob, create a tree from the exact base tree, create a commit with the current branch head as its only parent, then move the documentation ref fast-forward-only after checking the expected head.
2. Re-read the map by the new blob SHA and verify the appended entry and exact blob SHA.
3. Append a concise checkpoint addendum through Contents API if the updated checkpoint stays within its supported size; read it back and verify the new blob SHA.
4. Keep PR #388/#404 Draft; no merge, deployment, qualification or acceptance is authorized by this probe.
5. Continue issuer/capability/replay/revocation, accepted manifest, R-06 audit/privacy, worker artifact-only output, separate trusted publisher and independent acceptance work.

Contour A remains **NOT PROVEN / BLOCKED**. Contour B remains gated on Contour A deployment and independent acceptance.
