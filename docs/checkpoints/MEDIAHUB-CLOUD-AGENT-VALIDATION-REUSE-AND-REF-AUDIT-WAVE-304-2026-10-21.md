# MediaHub OS — Cloud-agent validation reuse and ref audit (Wave 304)

- Date: 2026-10-21
- Status: **EXISTING VALIDATION EVIDENCE FOUND / REUSE AUDIT / CONTOUR A BLOCKED**
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working branch / evidence PR: `docs/contour-a-wave302-exact-head-gate-audit-20261021` / https://github.com/VlDMlNSh/mediahub-os/pull/430
- Prior report: [Wave 303 scaffold audit](MEDIAHUB-SCHEMA-VALIDATION-SCAFFOLD-AUDIT-WAVE-303-2026-10-21.md)

## Correction to Wave 303 probe

The previous pass's search of `main` at exact paths `pyproject.toml`, `requirements.txt`, and `.github/workflows/verify.yml` did not find those files, and the broad GitHub code-search queries returned no results. This was not a complete repository-tree inventory and did not establish that a schema-validation workflow did not already exist. Follow-up retrieval from exact historical/work branches and evidence recorded in the canonical roadmap found prior schema-validation implementations and successful runs. Do not create a duplicate validator or workflow on the strength of the earlier limited probe.

## Recovered prior evidence

### Wave 81 / PR #335

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/335 (OPEN; issue snapshot reports no merge; formal reviews list empty).
- Exact run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39038451255; job `117412908148`; success.
- Artifact ID `12102957938`; digest `sha256:633e1417aa41fc844b5d1c67c3ff2be417a98f72bcc6f055119023565d710e07`.
- PR description records 3/3 schemas Draft 2020-12 meta-validated, 3/3 synthetic positive fixtures accepted, 13/13 invalid mutations rejected. This is evidence for those immutable schema candidates and fixtures, not runtime payload qualification or authority acceptance.

### Wave 81 / PR #337

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337 (OPEN; issue snapshot reports no merge; formal reviews list empty).
- Exact run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39041807077; job `117422642538`; success, as recorded in PR body and the Wave 81 report.
- PR body records Draft 2020-12 meta-validation, representative positive fixtures, and negative cases including empty objects, unknown top-level properties, invalid enums and malformed date-time.
- The workflow source was re-fetched from branch `contour-a-schema-validation-wave81-20261017`; blob SHA `bbe4f7e975a7ceb2c9fa7d2901bd484d06cbefc6`. It uses `contents: read`, checkout credential persistence disabled, full-SHA pins for checkout/setup-python/upload-artifact, hash-locked dependencies, exact event SHA assertion, schema validation, semantic fixture validation and machine-readable report/provenance artifact upload.

### Clean-base consolidation / PR #374

- PR: https://github.com/VlDMlNSh/mediahub-os/pull/374 (OPEN/DRAFT/UNMERGED; formal reviews list empty).
- Exact tested head: `3b1fc96beeedcc6cb38c7beeb5809f0004c6ac8a`.
- Exact-head run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222111677; job `117959603249`; success.
- Artifact ID `12171314150`; digest `sha256:4aaf3dbe764f22fd4eb0288685d1e069e3e28407c26f37d2e6825a487c7ae675`; artifact remains unexpired at audit time.
- Compared refs show this candidate diverges substantially from both `main` and the canonical docs branch. Against `main`: 2,359 ahead / 44 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Against canonical docs: 14 ahead / 610 behind, merge base `7cb4c49f737d2c5199864f206e289bf60b40ac9a`. The ahead/behind totals include inherited history and are not a code diff. Do not merge or rebase the whole branch. PR #374 explicitly leaves setuptools 84.0.0 bootstrap wheel publisher provenance unverified and requires independent schema/semantic and supply-chain review.

### Main's different schema validator

- `tools/validate_contracts.py` exists on `main` at blob `61862cfc763e9bf239af8b19242bc11a21f08d70`. It validates the canonical `schemas/` tree and metadata envelope; it is not the dedicated CAF v0.2 fixture/provenance workflow and should not be mistaken for it.
- `.github/workflows/astra-verify.yml` exists on `main` at blob `ae59d954f1ca6569a8d047589a2a54fd03e47f5b`. It installs PyYAML in its current main version and runs repository unittest discovery; the separate PR #388 line proposed JSON Schema dependencies and targeted hardening, but that line remains a distinct draft.
- PR #388 has a recorded COMMENTED targeted review at head `815fa4af497a593f321ee692f64f53a12dcad061`; exact-head Astra Verify run `39375449122` and Astra Cloud Runtime Validation run `39375449153` are recorded as successful. The review is not an approval.

## Governance interpretation

- Existing successful validation evidence means the immediate next task is **reconciliation/reuse and provenance review**, not starting another schema implementation.
- These are separate branches and PRs; none of the listed PRs has a formal approving review in the current reviews API responses. Successful historical CI does not mean the workflow is merged or currently triggered on the canonical branch.
- Schema validation of exact candidate blobs does not close the other Issue #301 gates: A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network target manifest, independent supply-chain review, controlled dispatch authority, or Contour A qualification and acceptance.
- No provider credentials, model calls, dispatch, queue admission, merge, deployment, qualification or acceptance occurred in this pass.

## Decision / next step

Do not implement another validator. Independently review the source and provenance of PR #374's exact tested head and artifact; resolve the setuptools 84.0.0 bootstrap publisher provenance and transitive lock inputs; check its intended file set against the current target base. Then select a single clean, source-bound PR for independent review. Keep all current drafts unmerged until branch-diff scope, CI at exact head, review and governance gates are satisfied.

**Disposition: CONTOUR A BLOCKED / NOT_PROVEN.**
