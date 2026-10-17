# MediaHub OS — Wave 93: lock trigger and dual-PR reconciliation (2026-10-17)

## Scope

Bounded evidence pass after Wave 92. Re-read the canonical Bootstrap, map blob, Master Roadmap, Functional Baseline 2.0, current continuation checkpoint, PR #335, PR #337, Issue #301, and the current lock/validation workflows. This pass does not merge or qualify Contour A.

## Verified repository state

- Working branch: `contour-a-schema-validation-wave81-20261017`.
- Starting HEAD: `559700815424c58adc03c8f602c6fb6a985f5d5e` (Wave 92 checkpoint commit).
- PR #337 head: `559700815424c58adc03c8f602c6fb6a985f5d5e`, open, Draft, unmerged, mergeable according to the PR API at read time.
- PR #335 head: `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`, open, Draft, unmerged.
- Both PRs define `.github/workflows/cloud-agent-schema-validation.yml`; their designs are materially different. They must not be merged independently.
- PR #337 compare to canonical documentation branch `docs/mediahub-chat-tree-map-20261012`: 70 ahead / 20 behind; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This divergence is a review and reconciliation gate, not permission to bulk-rebase or merge.
- Current lock blob: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`. Its generated header explicitly uses `env -u PIP_NO_INDEX`, `PIP_CONFIG_FILE=/dev/null`, and `PIP_INDEX_URL=https://pypi.org/simple`; the earlier Wave 87 `--no-index` concern is resolved in the currently read lock.
- Current generator workflow blob: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`. Its path filter watches the direct requirements input and generator workflow, but not the generated lock. This is consistent with treating the lock as an output rather than an input: changing the lock itself should trigger the validation workflow, not regenerate and overwrite the output automatically. The Wave 87 follow-up saying the generator path filter included the lock is stale relative to current branch state and should not be used as current evidence.
- Current schema validation workflow blob: `87db0e3fcfba9cf7373b7ba673325fc01eec6216`. It installs dependencies using `pip install --require-hashes`, checks Draft 2020-12 schemas, positive/negative fixtures, and cross-artifact semantic invariants in test scope.
- Successful validation runs on current starting HEAD: [39048903303](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048903303) and [39048900960](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048900960). The latest inspected run's `validate` job and dependency installation step both succeeded.
- The map fetched through its blob SHA `e1eb74740b2429b10a6025fcb1a8289f5958316d` contains 1,028,034 characters and is explicitly an inventory, not full acceptance. Canonical map link: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Decision

Do not add the generated lock to the generator workflow's path filter merely to satisfy the stale Wave 87 note. The current separation is clearer:
1. Input or generator changes run the lock generator and publish an auditable artifact.
2. Lock changes run schema validation, which enforces hashes.
3. A deliberate generator run compares/reviews the generated output before the lock is committed.

The lock reproducibility evidence remains the successful generator run and byte-for-byte comparison recorded in prior Wave 87 evidence; it is not re-claimed as having run on this current HEAD.

## Consolidation recommendation

Preserve PR #335's named Python scripts, checked-in regression fixtures and maintainable semantic test coverage. Port only the dependency-lock, immutable checkout, full-SHA Action pinning, least-privilege permissions and provenance improvements needed from PR #337. Create a single consolidation candidate after comparing every overlapping file. Avoid importing the entire 70-commit PR #337 history into the canonical branch without file-level review.

## Governance and blockers

Issue #301 remains open. A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema/authority review, and bounded worker/queue qualification remain gates. Zero independent PR review submissions were observed on PR #337 at this pass. CI success does not equal review, qualification, deployment or acceptance.

No secrets were accessed. No model/provider was invoked. No task was dispatched. No branch was merged or deployed.

## Next step

Inspect PR #335 and #337 changed-file patches side-by-side and produce one minimal consolidation branch/candidate, preserving provenance and test coverage. Run CI on that candidate's exact final SHA, obtain independent review, then reconcile the canonical branch deliberately. Do not merge PR #335 or #337 independently.
