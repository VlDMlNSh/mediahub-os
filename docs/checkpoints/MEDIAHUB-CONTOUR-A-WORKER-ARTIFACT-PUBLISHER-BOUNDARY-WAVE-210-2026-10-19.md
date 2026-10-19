# MediaHub OS Contour A — Wave 210 worker artifact/publisher boundary and candidate synchronization audit

Date: 2026-10-19
Status: source/CI audit; no worker dispatch, provider invocation, secret access, merge, deployment, qualification, or acceptance.

## Decision summary

Do not merge PR #375 or #376 yet. Keep both Draft. Preserve Baseline 2.0 and all authority boundaries. This pass confirms a concrete need to separate untrusted model execution from publication, and a live branch divergence that makes CI evidence insufficient for integration.

## Refs and CI evidence

- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
  - head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`, base `main`, base SHA recorded by PR `c06015e0b1526e0aaa6a522306052b077455aba5`.
  - Current compare against `main`: DIVERGED, 12 ahead / 3 behind; merge base `c06015e0b1526e0aaa6a522306052b077455aba5`; current base commit returned by compare `0897bd613c0c041794ec5ec4a72cd487b13a6944`.
  - Exact-head Astra Verify run 39295373907 and Astra Cloud Runtime Validation run 39295373833 both report SUCCESS. Verify job includes `Worker workflow credential policy regression tests`.
  - Candidate workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`: `contents: read`, all three checkout steps `persist-credentials: false`.
  - Worker script on main blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`: direct `git add -A` / commit / `git push origin HEAD:refs/heads/{branch}` publication path; subprocess helper defaults to ambient environment inheritance; FCC and Claude code paths copy `os.environ`. This proves a credential-boundary compatibility question, not that a real push fails or succeeds. The effective self-hosted runner credential helper/config remains unverified.
- PR #376: https://github.com/VlDMlNSh/mediahub-os/pull/376
  - head `1b6643d4dc3cbb27646e9dbfd27a6a763340cfbd`; compare against `main`: DIVERGED, 1 ahead / 3 behind, merge base `c06015e0b1526e0aaa6a522306052b077455aba5`; compare's current base commit `0897bd613c0c041794ec5ec4a72cd487b13a6944`.
  - Workflow runs 39231107074 and 39231107098 report SUCCESS, but the verify job step list does not contain the new Gemini parity test. The parity test path is `tests/test_gemini_workflow_parity.py`; the observed CI step list only shows compile, Cloud admission tests and signed-command smoke test. Thus successful CI does not establish execution of the newly added test.
  - Test candidate explicitly detects mutable action/container references and existing write permissions; it does not remediate those risks or prove that Gemini credentials/workflows work.

## Proposed trust boundary (design, not implementation or accepted governance)

1. **Worker output only:** the model executor must not publish branches or commits and must not receive repository write credentials. It emits a bounded result manifest plus patch/artifact files in a dedicated output directory. No blanket `git add -A`.
2. **Immutable binding:** manifest binds command/task/node/executor, issuer/capability decision ID, exact base/target commit SHA, expected branch namespace, schema version, artifact digests, and run identity. A hash or self-asserted field is not issuer authentication.
3. **Fail-closed output validation:** publisher rejects missing/extra files, path traversal, symlinks, submodules, unexpected modes, binary/oversized files outside explicit policy, changed base SHA, stale branch, malformed manifest, duplicate keys, and diff paths outside a task-specific allowlist. Recompute digests from downloaded bytes; never trust worker-provided hashes alone.
4. **Fresh trusted checkout:** publisher runs in a separate job with no shared writable workspace and a separately scoped write credential. It checks out the canonical base by immutable SHA, reconstructs the proposed change from validated patch data, verifies the resulting diff and policy independently, then performs a narrowly scoped branch update. Model-produced Git metadata, hooks, config, remotes and workspace state are not trusted.
5. **Credential non-propagation:** model, FCC server, verifier, test process, artifacts and logs receive no publisher token. Environment variables passed to subprocesses must be explicit allowlists; inherited environment is not an acceptable default for untrusted model execution. Secret values must never be logged.
6. **Provenance:** record run ID, workflow commit, source/base SHA, validated artifact digest, policy version, publisher identity, resulting remote SHA and verification result. A successful push is not acceptance of product changes.
7. **Tests before integration:** unit/negative tests for artifact allowlist, invalid target SHA, changed base, unapproved path, symlink/path traversal, credential-env absence, no direct worker push, publisher token unavailable to worker, and remote SHA mismatch. Add an integration test against a disposable test repository or mocked publisher boundary; do not use production credentials.
8. **Governance:** issuer/capability semantics, authority of task approval, and the Jarvis → ASTRA A0 → Product State Authority boundary must be accepted through the existing governance process before implementing publisher credential use. This document is a proposal only and does not accept WB-05 or any governance decision.

## Ranked gaps

- P0: untrusted worker directly stages and attempts to push a broad worktree diff; publication authority is not separated.
- P0: ambient process environment is copied into FCC/Claude execution paths; effective secret exposure and runner credential chain have not been inspected.
- P0: A0 issuer/verifier/ingress/lifecycle and GOV-CAP-01…07 remain BLOCKED/NOT_PROVEN; required fields are not proof of signature or authority.
- P1: PR #375 is 12 ahead / 3 behind current main; exact-head CI does not exercise real worker publication.
- P1: PR #376 is 1 ahead / 3 behind current main; new parity test is not visible in the recorded verify steps.
- P1: branch protection and required-review rules remain unverified; mergeability metadata is not authorization.
- P1: canonical map must be kept current; the Contents API returned empty map content, so this pass used the blob endpoint and must verify the updated blob after write.

## Work performed and limits

- Re-read current PR metadata, compare results, exact-head run summaries/job steps, worker source and candidate diffs.
- Posted a source-bound compatibility finding to PR #375. Existing discussion already contains more detailed publisher/environment findings.
- No source code or workflow was changed; no test was executed locally; no host configuration, secret, provider, or worker was touched.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.

## Next bounded action

Implement the worker-side artifact-only contract and regression tests on a fresh branch based on the current main SHA, without adding publisher credentials or enabling publication. In parallel, reconcile the two Draft PRs against current main and make the Gemini test step explicit. Only then design a separate trusted publisher under accepted issuer/capability semantics.
