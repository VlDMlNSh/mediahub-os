# Wave 131 — deduplicate schema-validation candidates

Date: 2026-10-18  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Primary tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Objective

Reduce duplicate review surface without losing implementation or validation evidence. Keep one active schema-validation candidate and preserve the independent Contour A acceptance gates.

## Live refs and candidate status

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Canonical documentation branch HEAD: `e869232ae5018a24bd1450a5c9ea4fa36e5b6b8a`.
- Active candidate: [Draft PR #350](https://github.com/VlDMlNSh/mediahub-os/pull/350), branch `contour-a-schema-clean-integration-wave129-20261018`, head `b3b730ea061faf9c975b63fa8019541df4578a96`; GitHub reports mergeable=true, OPEN / DRAFT / UNMERGED.
- PR #350 has 12 additive schema-validation files and zero deletions. PR #351 has the same exact 12 changed paths, so it duplicated the candidate's review surface.
- Closed duplicate [PR #351](https://github.com/VlDMlNSh/mediahub-os/pull/351) without merging or deleting its branch. Its implementation remains represented in active PR #350.
- PR #350 currently has no submitted review records. No independent approval is evidenced.

## Exact-head CI evidence

- [Run #39078628962](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39078628962) completed `success` on exact PR head `b3b730ea061faf9c975b63fa8019541df4578a96`.
- Job `validate` passed all substantive steps: immutable event checkout, Python setup, hash-locked dependency install, source-revision/environment provenance, Draft 2020-12 schema and regression-fixture validation, cross-artifact semantic fixtures, machine-readable report checks, and artifact upload.
- This is CI validation evidence only. It does not establish independent review, integration, Contour A qualification, or deployment.

## Safety and acceptance boundaries

No provider invocation, credential read, queue admission, agent dispatch, merge, deployment, or Product State Authority mutation occurred. Keep PR #350 Draft pending independent review and the remaining Issue #301 gates: A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, and acceptance of the runner/workspace/network target manifest. Historical exact-head runs are not substitutes for fresh checks after any new commit.

## Next

Continue the open Issue #301 gates with a bounded primary-contract audit, prioritizing the A0 issuer/ingress/lease/cancel/recovery path and R-06 authority/privacy. Keep PR #350 as the sole active schema-validation candidate; do not merge on CI alone.


## Post-write reconciliation addendum (same pass)

The documentation branch advanced while recording this report, making the PR temporarily non-mergeable. To avoid leaving the candidate stale, rebuilt its tree from the latest canonical docs tree and re-applied only the same 12 candidate blobs. The reconciliation commit is `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`, with the previous candidate head `b3b730ea061faf9c975b63fa8019541df4578a96` as first parent and docs head `801d7d212fc114919bcec84faddd153548ec5d14` as second parent. No force update was used; the compare is 17 ahead / 0 behind and shows 12 added files, zero deletions.

- Fresh exact-head run [#39078844123](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39078844123) passed on `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`; all schema, semantic, report/provenance and artifact-upload steps passed.
- GitHub now reports PR #350 OPEN / DRAFT / UNMERGED and `mergeable=true`; no independent review submissions are present.
- The reconciliation restores candidate freshness but does not authorize merge or acceptance.
