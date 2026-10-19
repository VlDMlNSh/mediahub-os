# MediaHub OS — schema-validation candidate exact-head review — Wave 165

- Date: 2026-10-19
- Status: **CANDIDATE CI EVIDENCE VERIFIED / SEMANTIC AUTHORITY GATES OPEN**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Scope: read-only source and workflow-run inspection of Draft PR #338; documentation/evidence only.

## 1. Exact candidate and CI evidence

- Candidate: [PR #338](https://github.com/VlDMlNSh/mediahub-os/pull/338), OPEN / DRAFT / UNMERGED.
- Head branch: `contour-a-schema-validation-consolidation-wave98-20261017`.
- Exact candidate HEAD: `fd12ee3272e64707fdbf9e0648bdbce3f7c5eb21`.
- Base ref: `docs/mediahub-chat-tree-map-20261012`, base SHA `2bd41f5b71006597a7669a4b7154abc58f87af5d`.
- Changed files: 13, including two validators, three synthetic positive fixtures, a negative-case mutation catalog, the schema-validation workflow and hash locks.
- Workflow run: [39058425661](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39058425661), workflow “Cloud-agent schema validation (Wave 94 consolidation candidate)”.
- Run artifact metadata ties this run to the exact candidate HEAD above. The single `validate` job completed successfully; the observed steps for immutable checkout, locked dependency install, source/environment verification, Draft 2020-12 schema/fixture validation, semantic fixture validation, machine-readable report checks and artifact upload all concluded `success`.
- Evidence artifact `cloud-agent-schema-validation-evidence-dce0bc01c04020560b2842de6ab5cf190348f0fa-run-39058425661` was reported present and unexpired at read time. This review inspected artifact metadata, not the artifact payload itself.

## 2. Source-bound implementation review

| Surface | Exact blob SHA | What the source does |
|---|---|---|
| `scripts/validate_cloud_agent_schemas.py` | `02c326da8cf90d2e5253dff3c1a5b90d72f6e18d` | Uses `Draft202012Validator.check_schema`, `FormatChecker`, explicit Git blob pins for three schemas, positive synthetic instances, 13 declared negative mutations, and generated missing-required mutations for required fields present in the fixtures. |
| `scripts/validate_cloud_agent_semantics.py` | `7c69f478301360930e9e2ff341692cf2676b16cd` | Checks proposed cross-document schema versions, immutable schema digests, canonical JSON digest bindings and synthetic semantic negative cases; explicitly records unresolved authority references as an open P0 finding. |
| `tests/fixtures/cloud-agent-schemas/negative-cases.json` | `88a2571fb92e7dc2dd825a649a42fb4b95827cc7` | Declares cases for missing required values, malformed date-time and SHA values, unexpected properties, duplicate paths, zero concurrency and incomplete schema references. |
| Task-envelope schema | `6f3cd3d40b2c5fe3f21bb6085536769fbef8322a` | Declares JSON Schema Draft 2020-12; candidate-only and not an accepted authorization contract. |
| Agent-registry schema | `b49b89b8fbdfc180862e3dc78f8198f35e486035` | Declares JSON Schema Draft 2020-12; explicitly requires external issuer/grant/policy/revocation resolution before runtime admission. |
| Evidence-manifest schema | `40c402432fd0f3899d45fde0fa0a8af4d34c593a` | Declares JSON Schema Draft 2020-12; states that execution, verification, qualification, release, deployment and acceptance are distinct. |
| `.github/workflows/cloud-agent-schema-validation.yml` | `f58add06b86b9f816e641ca1aea7d343e9662765` | Uses `ubuntu-24.04`, SHA-pinned checkout/setup-python/upload-artifact actions, checkout at `github.sha`, `persist-credentials: false`, `contents: read`, hash-locked install and evidence artifact upload. |

## 3. What the successful run establishes — and does not

**Established for this candidate HEAD:** the candidate workflow executed successfully with the pinned source revision; its declared schema and synthetic semantic fixture checks returned success; machine-readable report checks and artifact upload also succeeded.

**Not established:** trusted issuer identity, accepted capability issuance/delegation, revocation freshness, authorization at actual worker ingress, policy-reference validity, provider-route eligibility, secret isolation in the separate model-controlled worker path, independent artifact attestation, runtime admission, qualification, deployment or acceptance. The validators themselves describe these limits; the semantic validator deliberately emits `AUTHORITY_REFERENCES_UNRESOLVED` as P0 / OPEN.

A successful fixture-validation run is not a governance decision. It does not close the WB-05 / GOV-CAP-01…07 / R-06 gates, nor the separate worker-ingress and publication-credential isolation findings.

## 4. Adoption and integration disposition

- Keep PR #338 a candidate. Its current history/tree must be reconciled with the canonical documentation ref before integration; no automatic rebase, cherry-pick or merge was attempted.
- The setuptools 84.0.0 publisher-provenance gate remains specific to PR #338's bootstrap lock-generation workflow. This CI run does not create PyPI publisher provenance or replace an accountable supply-chain trust disposition.
- Preserve the three schema blob pins and exact-head evidence when review resumes. Any schema change requires explicit pin updates, regenerated reports and fresh exact-head CI.
- Next useful engineering gate: independently review schema semantics and cross-reference resolution against the accepted authority contracts once those contracts are approved; meanwhile continue the A0 ingress/authentication and model-execution credential-isolation tracks independently.

## 5. Evidence boundary

This pass read GitHub source, PR metadata, workflow run/job/artifact metadata and wrote this report plus navigation/checkpoint documentation. It did not execute the candidate locally, download the artifact, read secrets, call providers, dispatch workers, alter code/dependencies/workflows, change hosts, merge, deploy, qualify or independently accept Contour A.

**Disposition:** schema-validation candidate CI evidence is verified at the exact candidate HEAD; authorization and runtime qualification remain blocked. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains gated.
