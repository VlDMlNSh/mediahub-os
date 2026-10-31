# Wave 489 — Hosted runner manifest reconciliation

- Date: 2026-10-31
- Status: **DOCUMENTATION CANDIDATE CREATED / NOT ACCEPTED / NOT QUALIFIED**
- Work item: CAF-Q-012
- Contour: A — GitHub-hosted cloud execution pool
- Parent target: PR #601 head `02f0988cdeac2c6b360946c9a62b7a56f21c142d`
- Parent PR #595 head: `72a6725dbc7c38e37805e254377d293fcb141e7e`
- Runtime source snapshot: `main` at `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Canonical documentation base: `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`

## 1. Objective

Reconcile the Wave 478 v0.1 runner/workspace/network manifest candidate with the Wave 488 source-verified GitHub-hosted standard runner catalog. Preserve the distinction between hosted ephemeral jobs and self-hosted node identities. Keep the document explicitly non-authorizing.

## 2. Source reconciliation

Read back the following exact artifacts:

- Wave 478 manifest v0.1: blob `b2ee53f0f1caed379d0fc15172c1f3f52edacc37`.
- Wave 478 discovery report: blob `50ee83e097e42a54e2b2afbd7eab8d425439e118`.
- Wave 488 runner matrix: blob `1da1647b61cae396bb9cc1e29aeb26cee54b62da`.
- Wave 488 map addendum: blob `98cb2cacc3b4cceec1a37239ec3dc2913dfeff92`.
- Wave 488 continuation addendum: blob `217ca8b46632902a98735676e96ea7dc1a997dba`.
- A0 issuer/verifier contract candidate: blob `691b4b52cd6ba80bb822cf64ef5bea5e6e523c61`.

Wave 478 v0.1 described one Ubuntu 24.04 x64 baseline, job-local workspace, outbound-only egress, and explicit admission gates. Wave 488 expanded the source-backed standard runner catalog to Ubuntu x64/ARM64, Windows x64/ARM64, macOS ARM64 and Intel. It also clarified that standard hosted jobs are ephemeral, no runner-to-runner bandwidth SLA is documented, the standard Linux/Windows matrix has no documented GPU entitlement, and persistent desktop sessions are not supported by the job lifecycle.

## 3. Reconciliation decisions

1. Retain `ubuntu-24.04` x64 as the only default candidate profile.
2. Add ARM64, Windows and macOS profiles as secondary/specialist candidates, not as simultaneously reserved pool capacity.
3. Explicitly mark account plan, effective concurrency, artifact retention and deletion policy as NOT VERIFIED.
4. Preserve job-local workspace and bounded artifact relay; do not imply shared storage or direct peer networking.
5. Keep destination-level egress enforcement NOT VERIFIED and provider-connected jobs BLOCKED.
6. Exclude larger runners from the free-only baseline and exclude `ubuntu-slim` from the model-worker baseline.
7. Mark persistent GUI access as outside the ephemeral hosted-runner target; it requires a separate governed worker class.
8. Preserve all A0 issuer, R-06, schema validation, independent review, quota and provenance gates.

## 4. New artifact

Created `MEDIAHUB-RUNNER-WORKSPACE-NETWORK-TARGET-MANIFEST-WAVE-489-2026-10-31.json`, schema version `mediahub.runner-workspace-network-target.v0.2`.

It is a proposal only. It does not authorize workflow dispatch, model/provider calls, secret access, agent execution, runtime changes, merge, deployment or qualification.

## 5. Explicit unresolved gates

- PR #600 A0 issuer/verifier contract is OPEN/DRAFT/UNMERGED; independent A3 review and exact-head CI are NOT VERIFIED.
- R-06 audit/privacy acceptance remains open.
- Destination-level egress enforcement for standard hosted runners is NOT VERIFIED.
- JSON Schema Draft 2020-12 validation and positive/negative fixtures have not been run for this v0.2 artifact.
- Account-specific runner concurrency and artifact retention settings are NOT VERIFIED.
- Gemini controller task profiles do not accept this exact reconciliation packet; no agent dispatch was attempted.
- No runtime benchmark, provider call, secret read, host task, deployment or acceptance occurred.

## 6. Git and review state

- Working branch: `docs/wave489-hosted-runner-manifest-reconciliation-20261031`.
- Branch created from immutable PR #601 head `02f0988cdeac2c6b360946c9a62b7a56f21c142d`.
- This is a documentation-only child of PR #601, itself stacked on PR #595.
- No merge or rebase into the canonical documentation branch was attempted.
- Exact-head CI and formal independent review must be checked after PR creation; empty results are NOT VERIFIED.

## 7. Next

1. Independently review the A0 issuer/verifier contract and Wave 486 governance decisions.
2. Validate the v0.2 manifest against JSON Schema Draft 2020-12 with format assertions and positive/negative fixtures.
3. Close destination-level egress and artifact-retention policy gaps.
4. Obtain authority acceptance of the exact manifest before any read-only benchmark workflow is created.
5. Only after admission, pilot one immutable non-secret Ubuntu x64 job and a bounded artifact-relay measurement.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
PR #595 cloud-first priority: https://github.com/VlDMlNSh/mediahub-os/pull/595
PR #600 A0 issuer/verifier candidate: https://github.com/VlDMlNSh/mediahub-os/pull/600
PR #601 Wave 488 runner matrix: https://github.com/VlDMlNSh/mediahub-os/pull/601

## 8. Post-creation read-back and exact-head checks

- Manifest re-read from the PR branch; blob SHA: `515cf8fe8be353ade1fac83baac4dbf38f6127fc`.
- UTF-8 JSON parser check: **PASS**. Required top-level sections and all six runner profile IDs were present. This is syntax/shape inspection only, not JSON Schema Draft 2020-12 validation.
- Report blob SHA before this evidence update: `afab22b440d4a5d8e636cfa02156840095a67e15`.
- PR #603 exact head: `2693635c94f9d88a44a0ba27db48f25a3bf3039b`; PR base SHA: `02f0988cdeac2c6b360946c9a62b7a56f21c142d`; mergeable reported true; Draft/open/unmerged.
- PR #603 exact-head combined status: zero status contexts; associated workflow runs: zero; reviews: zero. Therefore CI and independent review are **NOT VERIFIED**, not PASS.
- PR #600 A0 issuer/verifier exact head `1e98fb9377e2103bdb6a70b1ca369596cea3a9fe`: zero status contexts, zero associated workflow runs and zero reviews. It remains Draft/open/unmerged; A0 admission remains blocked.
- No merge, dispatch, provider call, secret read, runtime benchmark or deployment was performed.
