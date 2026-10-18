# Project map addendum — Wave 151 — 2026-10-18

## Latest verified continuation
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Master Roadmap: ../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Wave 151 evidence report: ../checkpoints/MEDIAHUB-CONTOUR-A-CI-PROVENANCE-AND-PR338-DIVERGENCE-REVIEW-WAVE-151-2026-10-18.md
- Wave 151 checkpoint: ../checkpoints/MEDIAHUB-CONTINUATION-CHECKPOINT-ADDENDUM-WAVE-151-2026-10-18.md
- Governing issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358
- PR #338: https://github.com/VlDMlNSh/mediahub-os/pull/338

## Wave 151 results
- PR #358 workflow run 39117896120, job 117647309406: `Worker run correlation regression tests` and `Signed command smoke test` passed for observed head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`. This does not qualify issuer lifecycle or Contour A.
- PR #338 workflow run 39058425661, job 117471084337: schema and semantic validation, report checks and artifact upload passed on merge ref `refs/pull/338/merge`, tested SHA `dce0bc01c04020560b2842de6ab5cf190348f0fa`; it did **not** prove exact PR-head execution at `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`.
- PR #338 now compares as divergent, 20 ahead / 184 behind the current docs branch (SHA `51bd196d29c3bbac2902034ecc3d05c341b19e1f`). Keep Draft and do not mechanically integrate.
- Artifact for PR #338 run: ID `12110676230`, digest `sha256:7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`.
- Bootstrap toolchain publisher provenance, canonical provider registry discovery, GOV-CAP-01…07 and R-06 remain open.
- Targeted code-search no-results are inconclusive; locate registry by repository tree/path census before creating or modifying any registry.

## Next actions
1. Review PR #338 full file/tree overlap against current canonical docs branch and reconcile only with explicit evidence of no content loss/duplication.
2. Independently verify/disposition the bootstrap publisher-provenance concern; keep it open until documented.
3. Continue provider-registry consumer census and signed A0 ingress/provenance work within already accepted policy.
4. Obtain governance dispositions for GOV-CAP-01…07 and R-06 before defining trusted-context token semantics.
5. Refresh all refs, issue/PR states and CI logs on next `/next`.

## Gate
Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains blocked. Documentation-only Wave 151; no code changes, provider calls, dispatch, credentials, merge, deployment or qualification.


## Wave 151 supplemental CI evidence
- PR #358 merge-ref CI: run `39117896120`, merge SHA `c8024b033e31b1be218921399feefb16edb915b5`; focused correlation tests and signed-command smoke test passed. Additional negative coverage remains open.
- PR #338 merge-ref CI: run `39058425661`, tested merge SHA `dce0bc01c04020560b2842de6ab5cf190348f0fa`, artifact ID `12110676230`, digest `sha256:7957517179ce91c469e851996d2141410640c008da90c6f0c35f879ac185bb3c`. PR head `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21` was not the tested commit.
- PR #338 current divergence: 20 ahead / 184 behind docs branch `51bd196d29c3bbac2902034ecc3d05c341b19e1f`. Do not integrate mechanically.
- Canonical provider registry path is already recorded in roadmap as `ops/qualification/provider_model_registry.json`; continue consumer census, do not create a duplicate.


## Wave 151 path-overlap census result
- PR #338 has 13 changed paths; all 13 are absent on the current canonical documentation branch, so no same-path overwrite conflict was found in that bounded list.
- Canonical schema pins match: task envelope `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a`, agent registry `b49b89b8fbdfc180862e3dc78f8198f35e486035`, evidence manifest `40c402432fd0f3899d45fde0fa0a8af4d34c593a`.
- Despite that clean path overlap, PR #338 remains Draft/non-mergeable: 20 ahead / 184 behind. Do not integrate until history/tree reconciliation, independent bootstrap publisher-provenance disposition and fresh CI after reconciliation.
- Master Roadmap and Wave 151 report/checkpoint contain the full evidence. Canonical registry remains `ops/qualification/provider_model_registry.json`; finish consumer census and do not create a parallel registry.


## Wave 152 — bootstrap publisher provenance
- [Wave 152 report](../checkpoints/MEDIAHUB-SETUPTOOLS-84-0-0-PUBLISHER-PROVENANCE-REVIEW-WAVE-152-2026-10-18.md), blob SHA `ec6e01ebb3d074087cd081df1f4e6748f9d24877`.
- PyPI metadata for the pinned setuptools 84.0.0 wheel says Trusted Publishing: No. The GitHub tag's verified signature is a separate signal and does not establish wheel-to-source/workflow binding. Keep provenance OPEN pending exact-digest PyPI attestation verification or explicit alternative trust decision.
- PR #338 currently diverges 20 ahead / 193 behind the canonical docs ref; open/Draft/unmerged. No mechanical integration.
- Next bounded step: inspect PyPI Integrity API attestation for the exact wheel digest, then reconcile PR #338 and rerun CI on the reconciled base. Canonical provider registry remains `ops/qualification/provider_model_registry.json`.
