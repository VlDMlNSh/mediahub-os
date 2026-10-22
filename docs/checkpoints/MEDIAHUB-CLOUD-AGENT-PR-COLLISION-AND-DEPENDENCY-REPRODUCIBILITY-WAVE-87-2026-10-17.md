# MediaHub OS — PR collision and dependency reproducibility, Wave 87

- Date: 2026-10-17
- Status: **EXACT-HEAD CI CONFIRMED ON BOTH CANDIDATE BRANCHES; WORKFLOW COLLISION / REVIEW / INTEGRATION OPEN**
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Consolidated-validator candidate: https://github.com/VlDMlNSh/mediahub-os/pull/335
- Inline-validator candidate: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Baseline 2.0: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md

## Verified current refs and CI

- `main` HEAD: `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`; branch API reports `protected=false`.
- Canonical documentation branch HEAD: `e2bfa62adeac1c2b563130870481389d31820355`; branch API reports `protected=false`.
- PR #337 head: `c8390ca94c991ab013985d29b4d70d6dd628166b`; base `docs/mediahub-chat-tree-map-20261012`; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. Current compare: diverged, 16 commits ahead / 18 behind. This supersedes earlier 13-ahead snapshots because the compare endpoint now counts 16 commits on the branch.
- PR #337 run [39043810272](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39043810272), job `117428432389`: **success** on exact head `c8390ca...`; checkout, Python setup, pinned validator install and schema/fixture validation all succeeded.
- A second exact-head push run [39043813654](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39043813654) also completed successfully on `c8390ca...`.
- PR #335 head: `d8d7ae270034967476e55a5d410e691e4738e2ac`; base is the same canonical docs branch; compare reported diverged, 23 ahead / 18 behind in the latest Wave 86 report, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- PR #335 run [39043807900](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39043807900): **success** on `d8d7ae...`.
- Submitted PR reviews: none were returned for PR #337; Wave 86 reports none for PR #335. Both PRs remain OPEN / DRAFT / UNMERGED. The API's `mergeable=true` is not acceptance evidence and does not remove the branch-drift risk.

## Workflow collision and test coverage

Both PRs add `.github/workflows/cloud-agent-schema-validation.yml`, so they are competing implementations and must not be merged independently.

- PR #335 uses a reusable validator and authored fixtures. It has a version-pinned requirements file at blob `8ea0f2250efeea118f435b41bb77fda9de06633e`, validator blobs `a6a7ff3b91602268424972d6f98a040fc411542e` and `7c69f478301360930e9e2ff341692cf2676b16cd`, and fixed positive/negative fixture blobs listed by PR #335's changed-files API.
- PR #337 workflow blob: `c0bca0c1994e9888b223c316f1bc3e7b50f5097e`. Its generic nested-required mutation helper removes each present nested required property from isolated fixture copies and requires validator rejection. This is useful coverage, but bounded by fields present in the generated sample; it is not exhaustive schema mutation testing.
- PR #335's authored negative fixtures already include nested cases such as registry lifecycle expiry and manifest execution, plus semantic cross-artifact mutations. Independent review must establish which unique checks each implementation contributes and port the nested-required mutation behavior into the single reusable validator if equivalent coverage is not demonstrated.
- Current workflow source blob on PR #335: `880b9b5fef9b70b149299b7125d6cf7403d9afe1`. It checks out the immutable event SHA, disables checkout credential persistence, grants read-only contents, pins actions by full SHA, and installs the pinned requirements file.

## Dependency reproducibility finding

PR #335's `requirements-cloud-agent-schema-validation.txt` pins eight package versions:
`attrs==26.1.0`, `jsonschema==4.26.0`, `jsonschema-specifications==2025.9.1`, `referencing==0.37.0`, `rpds-py==0.30.0`, `rfc3339-validator==0.1.4`, `six==1.17.0`, and `typing-extensions==4.16.0`.

This is materially better than a single direct pin because the known runtime package versions are explicit. It is **not yet a hash-locked, resolver-generated artifact**: the workflow installs with `pip install -r`, without `--require-hashes`; package artifacts are not bound to hashes/platform markers in this file. PR #337 separately pins `jsonschema[format]==4.23.0`, creating a validator-version difference that must be resolved deliberately rather than silently combined.

All three v0.2 schemas inspected on PR #335 declare `date-time` as their only JSON Schema format. The pinned `rfc3339-validator` dependency is relevant to that format, but reviewers must confirm that every format actually relied on by the validator is supported under the chosen dependency set. Do not change versions only to make the two PRs look alike; pick one reviewed version and prove it on the exact merge candidate.

## Canonical documentation read-back

The canonical map remains on `docs/mediahub-chat-tree-map-20261012`. Its Contents API response was empty despite returning blob SHA `e1eb74740b2429b10a6025fcb1a8289f5958316d`; the current pass did not obtain a reliable ranged content read. No map/checkpoint/roadmap files were changed in this pass. Do not infer that the map is empty or overwrite it on the basis of the empty response.

## Disposition and next step

1. Keep PR #335 and #337 Draft and unmerged until an independent reviewer compares the actual validator implementations and records a single-workflow consolidation decision.
2. Prefer the reusable validator structure as the consolidation candidate, subject to review; port and test any unique nested-required checks and cross-artifact assertions from the competing implementation.
3. Decide whether the dependency contract is version-pinned-only or requires artifact-hash locking. If hash locking is selected, generate it in a controlled Python 3.12/Linux environment and validate installation with `pip install --require-hashes` on the exact candidate.
4. Reconcile the 18-commit base drift without losing either branch's unique tests, run CI on the exact final merge candidate, and verify review/branch rules before integration.
5. Continue tracking A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, and the accepted runner/workspace/network target manifest under Issue #301. Schema fixture CI is not runtime qualification or Contour A acceptance.

No merge, deployment, provider call, credential access, or product-state mutation was performed in this pass.
