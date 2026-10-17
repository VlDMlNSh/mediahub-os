# MediaHub OS — Dual-PR exact-patch reconciliation, Wave 97

- Date: 2026-10-17
- Scope: Contour A / [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Status: **PATCH OVERLAP CONFIRMED / NO INTEGRATION PERFORMED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on `docs/mediahub-chat-tree-map-20261012`

## Live refs and state

- PR [#335](https://github.com/VlDMlNSh/mediahub-os/pull/335): Open, Draft, GitHub reports mergeable=true; head `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`; base/merge-base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- PR [#337](https://github.com/VlDMlNSh/mediahub-os/pull/337): Open, Draft, GitHub reports mergeable=true; head `5ff2dbcc32d4949f4ce045164d110233cef980ba`; base/merge-base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- Current compare of `contour-a-schema-validation-wave81-20261017` against canonical docs branch reports **diverged, 83 ahead / 23 behind**, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- PR #337 head has successful validation run [39050957165](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39050957165). No matching PR-triggered run was returned by the commit-run query for PR #335's reported head; historical success claims in prior reports are not treated as current-head evidence.

## Exact changed-file overlap

The fetched PR patches confirm eight overlapping paths:

- `.github/workflows/cloud-agent-schema-validation.yml`
- `scripts/validate_cloud_agent_schemas.py`
- `scripts/validate_cloud_agent_semantics.py`
- `tests/fixtures/cloud-agent-schemas/README.md`
- `tests/fixtures/cloud-agent-schemas/negative-cases.json`
- `tests/fixtures/cloud-agent-schemas/valid/agent-registry-v0.2.json`
- `tests/fixtures/cloud-agent-schemas/valid/evidence-manifest-v0.2.json`
- `tests/fixtures/cloud-agent-schemas/valid/task-envelope-v0.2.json`

PR #335 supplies separately reviewable Python validation scripts, checked-in fixtures, semantic validation and source-pinned schema checks. PR #337 supplies a generated hash-locked dependency set, `--require-hashes` installation, a controlled lock-generation workflow, and broader generated nested-required negative cases. Both define the same schema-validation workflow path, so merging their branches directly risks a workflow collision and accidental loss of controls.

## Integration decision

Do not merge either branch directly and do not force-update refs. GitHub's mergeable flag is only a point-in-time mechanical estimate; it does not resolve duplicate workflow design or establish architecture acceptance. Keep PRs Draft until a single candidate is assembled and reviewed.

Consolidation requirements:
1. Keep the Python validators and checked-in fixtures from #335, including cross-artifact semantic tests.
2. Use #337's hash-locked requirements and `pip install --require-hashes`; prove the checked-in lock reproduces from its declared input and generator toolchain.
3. Preserve #337's nested-required negative coverage for object properties and array items, source-commit assertions, least-privilege permissions, full-SHA action pins, and machine-readable reports.
4. Audit workflow triggers so changes to lock inputs, lock files, scripts, fixtures, schema sources and both workflows trigger the appropriate checks without creating a recursive lock-generation loop.
5. Build one reviewable consolidation branch from a fresh canonical base, port only verified files, run all tests, and inspect new commit/tree/blob SHAs and fresh CI before any integration decision.

## Gates and limitations

Issue #301 remains open. A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema/security review, and bounded worker/queue qualification remain open. This pass did not invoke providers, read secrets, dispatch cloud agents, deploy, merge, or qualify Contour A.

## Evidence provenance

- PR patches and changed-file lists fetched live from GitHub during Wave 97.
- Canonical map blob before this report: `ade6dacbe2878d96b66f334316cb8d6a1358beb7`.
- Compare result: `diverged`, 83 ahead / 23 behind; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
