# MediaHub Contour A — selective schema-validation integration candidate (Wave 155, 2026-10-18)

## Disposition

**Selective additive candidate prepared; Draft PR only. No merge, acceptance, deployment, or Contour A qualification.**

## Current refs and canonical sources

- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`, observed base SHA `28816f6b523c8cbc878ebd0575b17bc419669889`.
- Bootstrap blob SHA: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical map blob SHA observed through Contents API: `5cb5818b827c80875dd95f710a5cc8abb207379f`. Contents API returned empty text for this large file; the prior verified blob read-back showed the document content. Do not interpret the empty response as an empty map.
- Master Roadmap blob SHA: `bf74e0aa5a8f049e22ab4730bf666a43a28ec053`.
- Issue #301 remains open: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Previous candidate PR #350 remains open/Draft/unmerged at `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`. Its old branch is 17 commits ahead / 106 behind the canonical docs ref (merge base `801d7d212fc114919bcec84faddd153548ec5d14`). No rebase or merge was performed.

## What changed

Instead of merging the divergent PR #350 history, a new branch was created from the current canonical documentation branch and the candidate's 12 additive files were carried over as a selective patch:
- two GitHub Actions workflows (schema validation and dependency lock generation);
- two requirement inputs/locks;
- two Python validators;
- README, negative-case matrix, and three synthetic valid fixtures.

Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/363

- Head branch: `integration/wave155-schema-validation-on-current-docs`
- Head SHA: `dec977fc40fb1b5b6dacc9efa24121ee3a1c3016`
- Base SHA: `28816f6b523c8cbc878ebd0575b17bc419669889`
- GitHub compare: 12 commits ahead / 0 behind; merge base equals the canonical base; exactly 12 added files, 1,713 additions, zero deletions. No existing canonical file was modified.
- All 12 files were fetched from PR #350's candidate branch, created on the fresh branch, and read back. The three canonical schema files referenced by the validators were verified to exist on the canonical base and their Git blob SHAs match the validator pins:
  - task envelope: `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a`
  - agent registry: `b49b89b8fbdfc180862e3dc78f8198f35e486035`
  - evidence manifest: `40c402432fd0f3899d45fde0fa0a8af4d34c593a`

## Exact-head CI

- New PR #363 exact-head schema workflow run `39126487850` was observed as **queued** at the time of the final check. No test result is claimed yet.
- PR #350's earlier schema run `39078844123` passed on its old head only; it is not a substitute for fresh CI on PR #363.
- PR #363 is Draft/open/unmerged. A mergeability snapshot of `true` is not an approval or acceptance decision.

## Security and qualification boundaries

- The schemas and semantic fixtures are proposed, synthetic validation artifacts. Their issuer/grant/policy/route/revocation references are inert strings; the validators explicitly do not resolve or prove authority.
- Green schema CI would validate the candidate's declared checks only. It would not qualify worker ingress, signed A0 authorization, freshness/replay protection, provider routing, artifact provenance, or isolation.
- Workflows use GitHub-hosted `ubuntu-24.04` for these validation jobs and read-only repository permissions; this does not establish isolation for the separate worker execution route, which still has self-hosted runner concerns.
- The canonical provider registry remains `ops/qualification/provider_model_registry.json`; no duplicate registry was created.
- WB-05 Option C remains a governance proposal only.

## Actions not performed

No workflow was manually dispatched, no tests were locally run, no provider/model calls or secret reads occurred, and no dependency installation, production runner change, deployment, merge, or qualification occurred.

## Next bounded step

Observe workflow run `39126487850` for the exact PR #363 head. If it passes, review its artifacts and inspect the semantic validator/lock-generation workflow independently; retain Draft status until independent review and all Contour A authority/provenance gates are satisfied. If it fails, diagnose only from the exact run/job logs and make the smallest targeted correction.

**Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.**
