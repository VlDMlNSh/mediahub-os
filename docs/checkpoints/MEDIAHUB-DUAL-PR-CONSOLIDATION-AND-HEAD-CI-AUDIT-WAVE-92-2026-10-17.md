# MediaHub OS — dual-PR consolidation and current-head CI audit, Wave 92

- Date: 2026-10-17
- Scope: read-only audit of schema-validation PRs #335 and #337, their workflow collision, current-head CI evidence, and branch divergence.
- Working branch: `contour-a-schema-validation-wave81-20261017`
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #335: https://github.com/VlDMlNSh/mediahub-os/pull/335
- PR #337: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Prior consolidation review: [Wave 89](MEDIAHUB-CLOUD-AGENT-DUAL-PR-WORKFLOW-CONSOLIDATION-WAVE-89-2026-10-17.md)

## Source-of-truth reads

- Bootstrap instruction read from canonical branch; blob SHA `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical map fetched by blob SHA after the Contents endpoint returned an empty body; blob SHA `e1eb74740b2429b10a6025fcb1a8289f5958316d`, content length 1,028,034 bytes. The map identifies itself as an inventory, not full acceptance.
- Accepted Functional Baseline 2.0 read from `main`; blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Current checkpoint read from the working branch before this report; blob SHA `032919eb5b879e0abf09b8617b6c21420996e663`.
- Governing Issue #301 confirms the schemas and documentary queue are candidates, not a live scheduler/agent dispatch system, and leaves authority/runtime acceptance gates open.

## Exact refs and CI

| Item | PR #335 | PR #337 |
|---|---|---|
| Current head SHA | `44e2bc7c735ad7f70294d66de8e08eb1da612e0d` | `4e9ecc102c60402a9733539debe142d7e486c5d8` |
| Base SHA | `8083cd61dbe348e18ab7db3e09b2769529bdcfda` | `8083cd61dbe348e18ab7db3e09b2769529bdcfda` |
| State | Open / Draft / unmerged | Open / Draft / unmerged |
| Current-head CI evidence | [Run 39044583119](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39044583119) — success on exact head | [Run 39048595408](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048595408) and [39048589712](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39048589712) — success on exact head |
| Compare with canonical docs branch | 25 ahead / 20 behind | 68 ahead / 20 behind |
| Merge base | `8083cd61dbe348e18ab7db3e09b2769529bdcfda` | `8083cd61dbe348e18ab7db3e09b2769529bdcfda` |
| Submitted review records observed | 0 | 0 |

Main branch HEAD observed: `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. No branch merge, rebase, or cherry-pick was performed.

## File-level finding

Both PRs add `.github/workflows/cloud-agent-schema-validation.yml`; these are competing implementations, not independent changes that can safely be merged as-is.

- PR #335 workflow blob at its current head: `880b9b5fef9b70b149299b7125d6cf7403d9afe1`. It uses reviewable Python scripts, checked-in positive fixtures, explicit negative cases, semantic cross-artifact checks, schema blob SHA assertions and machine-readable report artifacts. Its dependency file `requirements-cloud-agent-schema-validation.txt` pins versions but does not use pip's `--require-hashes`.
- PR #337 schema workflow blob at its current head: `87db0e3fcfba9cf7373b7ba673325fc01eec6216`; lock-generator workflow blob: `c22d820ccb59bcbdbaf4bfa40125063f2c68d8e0`; hash lock blob: `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`. It uses `--require-hashes` and generates deterministic positive/negative cases inline, but duplicates a large validator inside workflow YAML and does not use PR #335's checked-in fixture tree as its primary test input.
- Wave 91 correction is confirmed in the current generator workflow: the generated lock is an output, not a generator trigger input. Its push path filter includes the direct input and generator workflow; manual dispatch remains available. The schema-validation workflow separately watches the lock.
- PR #337's current successful CI establishes only that this candidate's tests passed. It does not select the canonical design or satisfy independent review.

## Consolidation recommendation

Do not merge either PR independently. Produce one reviewed implementation that:
1. Keeps PR #335's maintainable scripts and named regression fixtures, including semantic cross-artifact checks strictly in test scope.
2. Ports PR #337's hash-locked dependency strategy into one canonical requirements/lock path, with controlled generation and a clean `pip install --require-hashes` check.
3. Retains immutable event-SHA checkout, full-SHA Actions pins, read-only `GITHUB_TOKEN`, schema blob SHA checks, and machine-readable evidence with artifact digests.
4. Ensures path filters cover every actual input: schemas, lock input and lock, scripts, fixtures, workflow and report logic.
5. Re-runs the consolidated suite on its exact final head and obtains independent schema/authority review before branch reconciliation.

## Governance boundaries and blockers

- Issue #301 remains open. A0 issuer/ingress/lease/cancel/recovery; R-06 audit/privacy authority; accepted runner/workspace/network manifest; independent schema review; and bounded worker/queue qualification remain open.
- Both PRs remain Draft and unmerged. CI green is not approval, qualification, deployment or acceptance.
- No secrets were accessed; no provider/model was invoked; no workflow was dispatched by this pass; no live agent was admitted; no merge/deployment occurred.
- No claim is made that the canonical map or Functional Baseline was changed.

## Next step

Create one consolidation candidate on a dedicated branch, reusing the reviewed scripts/fixtures and the hash-lock model. Avoid parallel edits to the same workflow and preserve both PRs as evidence until the consolidated head passes CI and independent review. Reconcile the 20-commit base lag deliberately rather than bulk-merging either branch.
