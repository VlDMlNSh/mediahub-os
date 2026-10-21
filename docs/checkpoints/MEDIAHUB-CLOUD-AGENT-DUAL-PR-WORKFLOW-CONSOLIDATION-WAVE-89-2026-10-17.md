# MediaHub OS — dual-PR workflow consolidation review, Wave 89 (2026-10-17)

## Status

**Both schema-validation candidates have successful historical/current-head CI evidence; consolidation is still required. No PR was merged.**

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #335 — script/fixture-based validator: https://github.com/VlDMlNSh/mediahub-os/pull/335
- PR #337 — hash-locked inline validator: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Accepted Functional Baseline 2.0: https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/checkpoints/mediahub-functional-baseline-2.0.md

## Exact refs and CI observed

- PR #335 head: `44e2bc7c735ad7f70294d66de8e08eb1da612e0d`; workflow blob `880b9b5fef9b70b149299b7125d6cf7403d9afe1`; run [39044583119](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39044583119) succeeded.
- PR #337 head: `1bc17e3d5a52975e988d50789ca8de291c55d590`; validator workflow blob `31aaa4f2a35df446bae0b49e1bf4dc4f2daaed10); lock-generation workflow blob `951631787208740daf7999e71df24beb625b9910); lock blob `6a232e27c644ec1a46ddebc21a4a27c1d26ca781`.
- PR #337 validation runs [39047378737](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047378737) and [39047374968](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047374968) both succeeded on exact head `1bc17e3d5a52975e988d50789ca8de291c55d590`.
- PR #337's lock-generation run [39046901040](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39046901040) succeeded; artifact ID `12106331705`, digest `sha256:fa5a99df325011844a8998a8f9db848cc691ebd69f2ff55fde4dfe2ba9ece599`. The current lock header explicitly uses `env -u PIP_NO_INDEX`, `PIP_CONFIG_FILE=/dev/null`, and `PIP_INDEX_URL=https://pypi.org/simple`; the previously observed `--no-index` ambiguity is resolved in this file.
- Both PRs remain OPEN / DRAFT / unmerged, with zero submitted review records observed for PR #335 and PR #337.

## File-level comparison

| Dimension | PR #335 | PR #337 | Consolidation decision |
|---|---|---|---|
| Validator implementation | Separate Python scripts: schema/meta-validation and semantic cross-artifact validator | Large inline Python program embedded in workflow YAML | Prefer reviewable, testable scripts, but re-run them against exact target schema blobs before selection |
| Test inputs | Checked-in valid JSON fixtures plus explicit negative-case fixture data | Programmatically synthesized positive cases and generated negative mutations | Preserve named, checked-in regression fixtures; retain useful generated edge cases only as additional tests |
| Cross-artifact semantics | Dedicated semantic validator, with an explicit disclaimer that it is not an accepted admission/authority service | Embedded cross-artifact consistency and mismatch checks | Preserve explicit semantic checks while keeping them strictly test-only |
| Dependency installation | Exact package versions in `requirements-cloud-agent-schema-validation.txt`, without hashes | `--require-hashes` with generated transitive hashes | Prefer PR #337's hash-locked dependency model; move it to a dedicated requirements path and verify the selected scripts against it |
| Provenance | Immutable event-SHA checkout, source SHA assertion, workflow blob SHA in summary, machine-readable reports | Immutable event-SHA checkout and pinned dependency installation; fixture summary is in job logs | Preserve both source-provenance assertions and machine-readable evidence artifacts |
| Actions and permissions | Full-SHA action pins; `contents: read`; artifact upload pinned by SHA | Full-SHA action pins; `contents: read` | Keep least privilege and full-SHA pins |
| Path filters | Covers validator scripts and fixture tree as well as schemas, requirements, workflow | Covers schemas, requirements input/lock, and workflow files; no checked-in fixtures currently drive validation | Ensure every input actually used by the consolidated workflow is in PR path filters |
| Runtime authority | Scripts explicitly disclaim production admission, issuer, scheduler, provider, and qualification authority | Validation is CI-only; no provider call or credential required | Neither implementation qualifies Contour A or grants authority |

## Main finding

The two PRs add the same path, `.github/workflows/cloud-agent-schema-validation.yml`, with materially different designs. Merging both independently would create an unresolved workflow ownership/content collision. PR #335 offers a clearer separation of validation logic and machine-readable evidence; PR #337 offers stronger dependency reproducibility. The recommended direction is **one consolidated workflow** combining the strongest verified properties, not a blind merge of both PRs.

## Required consolidation plan

1. Keep both PRs Draft while a reviewer chooses the consolidated design.
2. Use PR #335's script/fixture structure as the maintainable validation harness, after independently reviewing its hard-coded schema blob SHA checks and running it against the exact schema blobs selected for the consolidated PR.
3. Port the hash-locked dependency strategy from PR #337 into one canonical requirements file; regenerate with the controlled PyPI workflow, compare output byte-for-byte, and test a clean `pip install --require-hashes`.
4. Consolidate event triggers/path filters so changes to schemas, lock input/lock, scripts, fixtures, workflow, and report-generation logic all schedule the required checks. Checkout must remain pinned to the immutable event SHA.
5. Run positive, negative, format, semantic cross-artifact, source SHA, and artifact-report checks on the consolidated head; inspect logs for leaked values (no provider credentials should be needed).
6. Compare both PRs against the canonical docs branch and review all files/conflicts. Branch comparison for PR #337 currently reports **53 ahead / 18 behind**, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`; this divergence is not merge approval.
7. Require independent schema/authority review and keep the workflow explicitly test-only. Issue #301 gates remain open: A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema review, and bounded worker/queue qualification.

## Boundaries

This review did not merge or rebase branches, access secrets, invoke model providers, dispatch workers, deploy Contour A, or start Contour B. Passing CI demonstrates only the tested schema-validation workflow on the exact cited commits. It does not constitute schema acceptance, authority approval, qualification, deployment, or product acceptance.

## Next step

Create one reviewed consolidation PR or a narrowly scoped successor branch that owns the single canonical schema-validation workflow. Before integration, verify all source/blob SHAs, lock reproducibility, all CI checks, independent review, and branch divergence. Keep PR #335 and PR #337 unmerged until that review is complete.


## Final branch-head revalidation (2026-10-17)

- The report commit moved PR #337 to head `9fa4134a4d59599789a9e86fd4f11732672085d8`.
- Exact-head schema-validation runs [39047869086](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047869086) and [39047864279](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39047864279) both completed successfully.
- PR #337 remains OPEN / DRAFT / unmerged; GitHub reports `mergeable=false`.
- Fresh comparison after the canonical map/checkpoint updates and the report commit: **54 commits ahead / 20 behind**, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This is an evolving compare snapshot, not merge permission.
- Canonical map blob after Wave 89 entry: `9a8add794ae4b9124d06444de7761a5152f63d67`. Canonical checkpoint blob after Wave 89 entry: `6a2e8b04c2957827996597b74b42877da6b8f97d`.
- Consolidation remains a design/review task. Neither PR has independent review, and Issue #301 gates remain open. Do not merge both workflow candidates.
