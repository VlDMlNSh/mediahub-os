# MediaHub OS Contour A — truth-ranked audit and readiness (Wave 206)

- Date: 2026-10-19
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Disposition: evidence audit and documentation synchronization; no gate promotion.

## Current repository truth

- PR #375 head is `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`, OPEN / Draft / unmerged.
- PR metadata reports `mergeable: true`, but this is not a review approval or permission to merge.
- Comparison snapshot during initial Wave 206 inspection: 12 commits ahead, 2 behind; merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. The branch is now diverged, so the previous Wave 205 statement of 11 ahead / 0 behind is historical and must not be reused.
- Changed files: `.github/workflows/astra-distributed-local-worker.yml`, `.github/workflows/astra-verify.yml`, `ops/qualification/test_worker_workflow_credential_policy.py`.
- Review submissions: none returned. Review threads: zero returned. Issue #301 remains OPEN (last updated 2026-10-19T10:37:13Z); its last inspected comments still state that branch protection/review settings could not be verified because the API returned 403.
- Generated current truth on `main`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`: G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED.

## Exact-head CI

For head `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`:
- [Astra Verify run 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907): completed SUCCESS.
- [Astra Cloud Runtime Validation run 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833): completed SUCCESS.

These runs verify only the workflow checks at that exact head; they do not establish governance acceptance, branch protection, production credential availability, or qualification.

## Worker publication path — confirmed gap

The workflow file at blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c` sets workflow-level `contents: read` and each of its three checkout steps has `persist-credentials: false`. It does not itself contain a literal `git push` command. However, its execution step calls `python3 ops/qualification/run_distributed_local_worker.py`.

The called worker script at blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` contains a direct publication path:
- creates a task-specific branch;
- runs `git add -A` and `git commit`;
- runs `git push origin HEAD:refs/heads/{branch}`;
- then uses `git ls-remote` to compare remote SHA with local HEAD.

Thus the precise gap is not that the workflow YAML contains a literal push, but that the worker program attempts to publish directly. `persist-credentials: false` reduces checkout credential persistence, yet the full credential chain and repository-wide git configuration have not been independently audited here. Do not infer either that the push can succeed or that it is impossible. Keep PR Draft and do not restore write credentials to the worker. Preferred design remains worker artifact output plus an isolated, independently validating publisher.

## YAML oracle status and limitation

The test file at blob `2c5fae2d431ca765bb548f4a2b5d70874961a438` uses a safe PyYAML loader rejecting duplicate mapping keys and has two negative tests for duplicate workflow-level and job-level permission keys. Exact-head CI is green. Remaining semantic review includes GitHub-specific schema/permission inheritance, reusable workflows, composite actions, expression contexts, action pinning and test-fixture mutation assumptions. This is a bounded static oracle, not a formal proof of GitHub Actions authorization.

## Ranked gaps

### P0
1. Issuer/capability contract and lifecycle (issuer, resource/operation binding, expiry, revocation, replay protection) must be resolved through governance, not guessed in code.
2. Worker-to-publisher boundary and output provenance: worker should emit an artifact; separate publisher validates immutable base SHA, repository/ref/path/diff and obtains narrow, auditable write authority.
3. Independent security review and evidence of branch protection/required reviews. No review submissions are present; API 403 leaves settings unverified.

### P1
4. Full semantic YAML policy coverage and supply-chain pinning.
5. Runner/workspace/network isolation and FCC propagation evidence.
6. Agent/provider availability and identity must be evidenced per run; workflow existence is not persistent autonomous readiness.

### P2
7. Reconcile diverged branch only after fresh ancestry/diff review and confirmation of branch protection. Do not perform broad merge/rebase while governance and publication path remain unresolved.

## Architecture options (ranked)

1. **Preferred:** isolated worker produces a quarantined patch/artifact; independent publisher reconstructs from immutable base and validates capability, diff, path allowlist and destination before publication.
2. **Conditional:** publisher uses a GitHub App or equivalent short-lived credential after governance approves issuer/capability semantics, key lifecycle, revocation and audit.
3. **Not acceptable as default:** model-controlled worker performs direct `git push` with ambient write authority.

## Readiness and next action

- YAML oracle: exact-head CI verified, limited scope.
- PR #375 integration: NOT READY; Draft, no review submissions, branch divergence 12 ahead / 2 behind, branch-protection state unverified.
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.
- Contour B: GATED.

No worker, Gemini or provider dispatch; no secret access, host command, merge, deployment or qualification was performed.

Next: (1) independently review worker script and credential chain, including repository-level git config and any ambient token sources; (2) specify artifact-only worker contract and publisher trust boundary; (3) resolve issuer/capability decisions in governance; (4) recheck exact PR head, CI, ancestry, branch protections and review state before any integration. Adversarial cases must include wrong repo/ref/SHA, expired/revoked/replayed grants, forbidden paths, symlinks/binary/oversized patches, forged Git metadata, cancellation races, audit outage and remote-SHA mismatch.


## Final read-back drift note

A fresh comparison after documentation writes returned 12 commits ahead / 3 behind `main`, with the same merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. The base advanced during this pass; use 12 ahead / 3 behind as the latest observed value and refresh again before any integration action. Map/checkpoint cross-links were read back by SHA; the canonical map content was retrieved via blob because the file endpoint returned empty content for this large file.
