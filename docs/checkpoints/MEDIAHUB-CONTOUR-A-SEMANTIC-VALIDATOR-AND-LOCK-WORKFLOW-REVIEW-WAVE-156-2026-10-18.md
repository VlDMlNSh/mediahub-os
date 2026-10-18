# Contour A semantic-validator and lock-workflow review — Wave 156

Date: 2026-10-18
Status: **INDEPENDENT STATIC REVIEW / CANDIDATE ONLY / NOT QUALIFICATION**

## Scope and exact refs

- Repository: `VlDMlNSh/mediahub-os`
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`, base SHA observed `28816f6b523c8cbc878ebd0575b17bc419669889`.
- Candidate PR: [#363](https://github.com/VlDMlNSh/mediahub-os/pull/363), head `dec977fc40fb1b5b6dacc9efa24121ee3a1c3016`, open/Draft/unmerged.
- Evidence PR: [#364](https://github.com/VlDMlNSh/mediahub-os/pull/364), still open/Draft/unmerged at prior recorded head `5f38b961ccc0be9643d6d1284f2c73d7efe30c90`.
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301), open.
- Current candidate compare: 12 commits ahead / 0 behind; merge base equals base SHA; 12 added files, 0 deletions.
- Relevant blobs on candidate:
  - `scripts/validate_cloud_agent_semantics.py`: `7c69f478301360930e9e2ff341692cf2676b16cd`
  - `scripts/validate_cloud_agent_schemas.py`: `02c326da8cf90d2e5253dff1c3a5b90d72f6e18d`
  - `.github/workflows/cloud-agent-lock-generation.yml`: `22ed52a9252630bfa62b5fbb7d37ea79c84f8b82`
  - `.github/workflows/cloud-agent-schema-validation.yml`: `f58add06b86b9f816e641ca1aea7d343e9662765`

## Verification evidence

- Exact-head GitHub Actions run [39126487850](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39126487850) for candidate SHA `dec977fc40fb1b5b6dacc9efa24121ee3a1c3016`: completed `success`.
- Job `validate` completed the checkout-at-event-SHA, Python setup, hash-locked dependency installation, source revision/environment verification, Draft 2020-12 schema/fixture validation, semantic fixture validation, machine-readable report checks, and evidence upload steps.
- The prior PR description said exact-head CI had not yet been returned. That stale statement was corrected in PR #363's body after checking the run. No code changed; no fresh CI is claimed for a new code SHA.
- Three schema blob pins in the candidate match the canonical schema blobs recorded in Wave 155.
- No independent PR review submissions were present at time of inspection.

## Static review findings

1. **Scope is correctly labelled as fixture-only.** The semantic validator explicitly says it is not an accepted issuer/admission/scheduler/provider contract. Synthetic references for authorization, policy, routes and revocation are not resolved to live authority.
2. **Useful cross-artifact checks exist.** The code compares task/manifest identity, source provenance fields, schema references/digests, policy bundle references, lifecycle ordering, task capability, data class, path grants/denials, execution budgets, output effect, provider/model route labels, and execution/artifact metadata.
3. **A passing fixture suite is not an authorization proof.** The `authorized` status check only checks evidence-kind labels; it explicitly does not authenticate their source or authority. Time checks validate ordering and offsets but do not establish current-time freshness or a trusted revocation source.
4. **Lock-generation workflow is bounded.** It uses a GitHub-hosted `ubuntu-24.04` runner, read-only repository permissions, pinned action SHAs, an immutable event-SHA checkout, a hash-locked bootstrap toolchain, an explicit PyPI index, a generated lock diff artifact and a byte-for-byte reproducibility gate. The workflow itself has not been independently executed in this pass.
5. **Artifacts remain uninspected.** Run and job metadata prove a successful job result, not that the downloaded JSON reports and provenance artifact have independently been examined. Artifact ID/digest verification is still a follow-up.
6. **Artifact was downloaded and independently inspected.** GitHub artifact ID `12136710208`, size 8,799 bytes, digest `sha256:553177a7510912426e54d1c4ae3554749c2f88bddd134bd2ba871eec175d8151`; locally calculated ZIP SHA-256 matches the GitHub artifact digest exactly. ZIP contains three JSON files. Schema report: PASS, 3/3 schemas meta-validated, 3/3 positive fixtures passed, 179/179 negative cases rejected, 0 failures. Semantic report: PASS, 1/1 positive bundle passed, 26/26 semantic negative cases rejected, 0 failures. Both reports and the provenance JSON bind to run `39126487850`, attempt `1`, repository `VlDMlNSh/mediahub-os`, and event merge SHA `cb2b5851eac94f27ab7da447c261d18d670ff8b0`; the GitHub run metadata identifies PR head `dec977fc40fb1b5b6dacc9efa24121ee3a1c3016` and branch `integration/wave155-schema-validation-on-current-docs`. This distinction is expected for the `pull_request` merge ref (`refs/pull/363/merge`), but the report must not describe the synthetic merge SHA as the PR head SHA.
7. **No runtime/issuer proof.** The candidate does not close signed A0 ingress, issuer/capability lifecycle, freshness/replay, target-manifest acceptance, source-bound job/attempt/artifact provenance, self-hosted worker isolation, or bootstrap publisher identity.

## Decision

- Keep PR #363 Draft/open/unmerged pending independent code review and artifact read-back.
- Keep PR #364 Draft/open/unmerged; this report records review evidence but is not a merge/acceptance decision.
- Do not claim Contour A qualified, deployed, or independently accepted. Contour B remains blocked by the Contour A gate.
- No provider calls, secret reads, production dispatch, worker changes, deployment, merge/rebase/cherry-pick or qualification were performed.

## Next bounded step

Next: independently review the signed A0 ingress and worker dispatch contracts, including source-bound workflow/event/SHA/job/attempt/artifact provenance, freshness/replay and fail-closed behavior. Keep PR #363 Draft until independent review and authority/security gates are satisfied.
