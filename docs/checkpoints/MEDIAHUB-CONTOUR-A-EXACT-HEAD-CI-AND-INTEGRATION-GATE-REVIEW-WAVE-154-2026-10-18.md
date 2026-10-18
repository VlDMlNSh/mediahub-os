# MediaHub Contour A — exact-head CI and integration-gate review (Wave 154, 2026-10-18)

- Status: **REVIEW EVIDENCE ONLY**. No acceptance, merge, deployment, or qualification is implied.
- Canonical documentation ref reviewed: `docs/mediahub-chat-tree-map-20261012`.
- Bootstrap blob: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical map blob observed: `5cb5818b827c80875dd95f710a5cc8abb207379f`. Contents API returned empty content; the blob API read-back returned 1,063,436 characters and the latest section was Wave 151. This is treated as an API representation quirk, not an empty map.
- Checkpoint blob observed: `1e663836e6628b50b87148510fdb029f76307f02`.
- Master Roadmap blob observed: `bf74e0aa5a8f049e22ab4730bf666a43a28ec053`.
- Issue #301 remains open: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Exact-head CI evidence

### PR #358 — worker-run correlation
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/358
- State: open, Draft, unmerged; base `main`, head branch `fix/wave-146-fail-closed-worker-run-correlation`.
- Exact head SHA: `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; base SHA: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Compare: base `main` is the merge base; PR head is 5 commits ahead / 0 behind. Changed files: `.github/workflows/astra-verify.yml`, `runtime/mediahub_runtime/autonomous_queue.py`, `tests/test_worker_run_correlation.py`.
- Workflow run `39117896120` (Astra Verify): completed, conclusion **success**. The run's `validate` job passed contract validation, runtime tests and the Astra cloud runtime tests.
- Workflow run `39117895925` (Astra Cloud Runtime Validation): completed, conclusion **success**; job `validate` passed.
- Interpretation: exact-head CI is green for the current PR head. This verifies the tested correlation/hardening slice only. It does **not** prove signed A0 issuer verification, freshness/replay protection in the actual worker ingress, or workflow/event/source-SHA/job/attempt/artifact provenance. The PR description itself marks these as remaining gates. Keep Draft pending independent review and those gates.

### PR #350 — schema-validation candidate
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/350
- State: open, Draft, unmerged; base `docs/mediahub-chat-tree-map-20261012`, head branch `contour-a-schema-clean-integration-wave129-20261018`.
- Exact head SHA: `4c1ebafc5d33e8ae075a5bba85771d14aed4ac96`; observed base SHA: `801d7d212fc114919bcec84faddd153548ec5d14`.
- Workflow run `39078844123` (Cloud-agent schema validation, Wave 94 consolidation candidate): completed, conclusion **success**. The `validate` job passed immutable-event-checkout/source revision checks, Draft 2020-12 schema and regression fixtures, cross-artifact semantic fixtures, machine-readable report verification, and report/provenance upload.
- Current comparison to canonical docs ref: **DIVERGED**, 17 commits ahead / 106 behind, merge base `801d7d212fc114919bcec84faddd153548ec5d14`. The PR's reported mergeability was true at the snapshot, but divergence means CI evidence must not be treated as proof that the candidate is reconciled with the current canonical tree. No merge or rebase was attempted.
- Interpretation: the validator passed on this exact head; integration still requires fresh reconciliation, CI against the reconciled base, independent review, and separate ingress/issuer/lease/cancel/recovery, R-06 and target-manifest gates.

### PR #361 — Wave 153 governance proposal
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/361
- Exact head SHA: `a87acd6294fd9f8d9a7e49047dae071a566308e8`; open, Draft, unmerged.
- No PR-triggered workflow runs were returned for this SHA by the workflow-run query. This is **no CI evidence returned**, not a failed build.
- Option C remains a governance proposal only: NOT ACCEPTED / NOT IMPLEMENTED.

## Independent blockers retained
1. Signed A0 issuer envelope validation and replay/freshness enforcement at the actual worker ingress are not proven by PR #358 correlation tests.
2. GitHub-derived run/job/attempt/event/source SHA and artifact provenance must be bound to the result before worker execution is qualified.
3. The worker execution path currently relies on self-hosted runner labels; ephemeral GitHub-hosted isolation is not established.
4. PR #350 is divergent from the canonical documentation ref and needs safe reconciliation before integration.
5. Bootstrap publisher provenance for the pinned `setuptools==84.0.0` artifact remains open pending exact-digest attestation verification or an explicit alternative trust decision.
6. The canonical provider registry at `ops/qualification/provider_model_registry.json` is a routing inventory, not proof that credentials, free quotas, or live provider routes are available or qualified.
7. Wave 153 WB-05 Option C is still only a governance proposal; do not infer authority approval from documentation or CI.

## Actions and limitations
- Performed read-only GitHub inspection of refs, PR metadata, workflow runs/jobs, comparisons, issue #301, and canonical documents.
- Did not run new tests, dispatch workflows, invoke models/providers, read secrets, install dependencies, change runners, deploy, merge, or qualify Contour A.
- No integration operation was attempted. Branch divergence is preserved as a safety constraint.

## Next bounded step
Reconcile PR #350 against the current canonical docs branch on a dedicated branch, preserving its 12-file scope and auditing the diff for loss/overlap; then run exact-head schema CI on the reconciled candidate. In parallel, keep PR #358 Draft until a source-bound signed-ingress/provenance test slice is reviewed. Verify the exact-digest PyPI attestation before closing the bootstrap publisher-provenance gate.

**Disposition:** Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains blocked.
