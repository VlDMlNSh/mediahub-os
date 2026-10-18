# Contour A CI provenance and PR #338 divergence review — Wave 151 — 2026-10-18

## Summary
Confirmed two separate CI results and tightened the evidence boundary around what they prove. PR #358's worker-run correlation regression step passed on its observed head. PR #338's schema/semantic validator steps passed on a GitHub pull-request merge ref, not on the PR head SHA itself; its branch is now 20 commits ahead and 184 behind the current canonical documentation ref and must not be integrated mechanically.

## 1. PR #358 regression CI
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/358
- Observed PR head: `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; base/main observed SHA `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Workflow run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39117896120
- Job `verify` ID `117647309406`: success.
- Step `Worker run correlation regression tests`: success; `Signed command smoke test`: success.
- This proves the CI steps passed for the observed PR validation run. It does not prove signed A0 issuer lifecycle, full evidence provenance, real dispatch, or Contour A qualification.

## 2. PR #338 schema candidate
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/338
- Head branch: `contour-a-schema-validation-consolidation-wave98-20261017`.
- Head SHA: `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`.
- Current canonical docs branch SHA reported by compare: `51bd196d29c3bbac2902034ecc3d05c341b19e1f`.
- Compare: **DIVERGED, 20 commits ahead / 184 behind**, merge base `2bd41b5f71006597a7669a4b7154abc58f87af5d`. PR metadata's base SHA is stale relative to the current canonical ref.
- Changed files: 13; additions 1,773; deletions 0.
- Workflow run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058425661; job `validate` ID `117471084337`, conclusion success.
- Steps passed: immutable event-commit checkout, hash-locked dependency install, environment/source revision check, Draft 2020-12 schema validation, cross-artifact semantic fixtures, machine-readable report verification, evidence upload.
- Provenance from actual job log: event `pull_request`; ref `refs/pull/338/merge`; tested `github.sha` / merge ref SHA `dce0bc01c04020560b2842de6ab5cf190348f0fa`, not PR head SHA `fd12ee...`. Therefore report this as **successful PR merge-ref CI**, not exact-head CI.
- Artifact ID `12110676230`; digest `sha256:7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`; retention expiry shown by GitHub: 2026-10-31T18:31:02Z.
- Schema validator blob SHA `02c326da8cf90d2e5253dff3c1a5b90d72f6e18d`; source includes concrete array-index traversal for nested required properties.
- Semantic validator blob SHA `7c69f478301360930e9e2ff341692cf2676b16cd`.
- The synthetic fixture reports explicitly disclaim that field/digest consistency does not establish issuer identity, grant authority, policy validity, route eligibility or revocation.

## 3. Supply-chain and integration gate
- Bootstrap lock blob SHA `2cb89e822dabbe54a11e6b718ec8443b8891c926`; it pins exact versions and hashes, including `setuptools==84.0.0`.
- The lock's own comments correctly state that hashes verify downloaded bytes, not publisher identity. Independent provenance review for the bootstrap toolchain remains open; no independent PyPI publisher-provenance check was performed in this wave.
- Keep PR #338 Draft/open/non-mergeable. Do not rebase/cherry-pick/merge until its full diff is reviewed against the current docs branch and the 184-commit divergence is reconciled without duplication/loss. After any refresh, run CI on the new merge ref and capture the new source SHA/artifact digest.

## 4. Canonical provider registry search
Targeted GitHub code searches for provider registry/model ID/secret-reference and schema terms returned no results. Because code search is scoped to default branch and indexing may be incomplete, this is **inconclusive**, not evidence that no registry exists. Continue with repository tree/path inventory or targeted source references; do not create a second source of truth.

## 5. Authority and current status
- Issue #301 remains open and is the governing tracker.
- The Wave 149 issuer governance matrix reports options unselected and implementation blocked pending GOV-CAP-01…07 and R-06 dispositions.
- Jarvis mission coordination, ASTRA A0 queue authority and MediaHub Product State Authority remain distinct. CI passing does not satisfy these governance decisions.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains blocked.

## Next bounded step
1. Reconcile PR #338 against the current docs branch only after a full file/tree overlap review; do not mechanically rebase its 184-commit lag.
2. Independently verify or disposition bootstrap publisher provenance; retain the open risk until evidence is recorded.
3. Continue canonical provider registry consumer census and signed A0 ingress/provenance work that does not require inventing unapproved issuer policy.
4. Obtain explicit owner/governance decisions for GOV-CAP-01…07 and R-06 before encoding the trusted-context contract.

## Evidence boundary
Source/CI evidence review and documentation only. No tests were run in this chat; no workflow was dispatched; no provider was called; no credentials were inspected; no dependency or workflow source was changed; no branch was rebased/merged; no deployment or qualification occurred.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md


## Follow-up: changed-file overlap census against current canonical documentation ref
Compared all 13 paths in PR #338's changed-file list against `docs/mediahub-chat-tree-map-20261012` at the current observed ref:
- All 13 candidate paths are absent on the canonical branch: both new workflow files, candidate report, two lock/input files, two validator scripts and six fixture files. No same-path overwrite conflict was found in this bounded inventory.
- The three source schemas referenced by the candidate are present and match the recorded expected blob SHAs:
  - Task Envelope schema: `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a`.
  - Agent Registry schema: `b49b89b8fbdfc180862e3dc78f8198f35e486035`.
  - Evidence Manifest schema: `40c402432fd0f3899d45fde0fa0a8af4d34c593a`.
- This reduces direct path-collision risk for the 13 listed files; it does not make the 184-commit history divergence safe to integrate automatically. Keep PR #338 Draft/non-mergeable pending independent supply-chain disposition, review of the complete tree/history, and fresh CI against a reconciled base.
- No rebase, cherry-pick or merge was performed.
