# MediaHub OS Contour A — truth-ranked audit and readiness (Wave 208)

- Date: 2026-10-19
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governance tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Scope: read-only source/evidence audit plus documentation sync. No runtime dispatch, secret access, host command, merge, deployment or qualification.

## Verified current state

- PR #375 is OPEN / Draft / unmerged at `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`. GitHub's computed `mergeable` field has fluctuated between reads; it is not a governance signal.
- Latest branch comparison: 12 commits ahead / 3 behind `main`; merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. Status is `diverged`. Do not merge or rebase from a stale comparison.
- Exact-head CI remains green: [Astra Verify run 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907) and [Astra Cloud Runtime Validation run 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833); jobs `verify` and `validate` completed SUCCESS.
- No review submissions and no review threads were returned for PR #375. Issue #301 remains OPEN. Branch protection / required-review settings remain unverified; a previous API attempt returned 403.
- Current truth on `main`, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`: G0–G11 BLOCKED, overall NOT_PROVEN / BLOCKED.

## Credential boundary — source-level findings

Inspected at the exact PR head:
- Workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`, `.github/workflows/astra-distributed-local-worker.yml`.
- Worker blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`, `ops/qualification/run_distributed_local_worker.py`.

The workflow grants `contents: read` and sets `persist-credentials: false` on all three checkout steps. The workflow YAML itself has no literal `git push`, but it invokes the worker program.

The worker program:
1. Uses `os.environ.copy()` when creating FCC/Claude and some test subprocess environments.
2. Has a generic subprocess helper that inherits the process environment unless an explicit environment is supplied.
3. Runs model execution with Bash-capable tooling in configured modes.
4. Creates a task-specific branch, stages all workspace changes via `git add -A`, commits, runs `git push origin HEAD:refs/heads/{branch}`, and verifies the remote SHA using `git ls-remote`.

This establishes a direct-push code path, not proof that a push currently succeeds. The workflow's read-only token permission and disabled checkout credential persistence do not establish the complete effective credential chain on the self-hosted runner. Ambient environment variables, runner service environment, Git credential helpers/configuration, remote URL configuration and OS-account access remain unverified.

No runner host or service configuration was inspected in this pass. No secret values, FCC env-file contents, or credential values were read. It would be incorrect to claim either that write credentials are available or that the current runner cannot publish.

## Ranked gaps

### P0 — blocks safe integration and qualification
1. **Worker/publisher separation:** worker code can attempt direct Git publication and stages all workspace changes. The worker should instead emit a quarantined artifact bound to immutable target SHA, task/command IDs and a content digest. A separate publisher should validate provenance, authorization, repository/ref/path allowlists and diff policy before obtaining narrowly scoped write authority.
2. **Credential-chain evidence:** verify runner service identity, inherited environment names (not values), Git configuration origins and credential-helper presence using approved read-only metadata. Do not dump environment contents or inspect secret files.
3. **Governance contract:** issuer/capability semantics, resource/operation binding, expiry, replay prevention, revocation and audit-failure behavior require an explicit governance decision before publisher credentials are implemented.
4. **Integration controls:** branch is diverged; review submissions are absent and branch-protection requirements remain unverified.

### P1
5. **Model-process environment:** replace broad inherited environments with explicit allowlists, but first enumerate documented runtime dependencies and prove provider execution still works without publisher authority.
6. **Artifact validation:** reject wrong repo/ref/SHA, unauthorized paths, symlinks, binary or oversized patches, forged metadata, cancellation races, stale bases, audit outages and remote-SHA mismatches.
7. **Independent YAML review:** duplicate-key rejection tests pass in exact-head CI, but the policy oracle is not a formal model of GitHub Actions permission inheritance, reusable workflows, expressions, composite actions or action supply-chain pinning.

### P2
8. Reconcile the branch only after a fresh diff/ancestry review, explicit conflict handling, verified protection state and exact-head CI. No integration is authorized by a green CI result alone.

## Architecture options, ranked

1. **Preferred:** artifact-only worker with no repository write authority; immutable-base patch validation; isolated trusted publisher with least privilege, auditable grants and revocation.
2. **Conditional:** short-lived GitHub App/publisher credential after governance acceptance, path/ref restrictions and adversarial tests.
3. **Rejected as default:** model-controlled worker uses ambient credentials to `git push` directly.

## Readiness

- Static workflow credential checks: exact-head CI PASS, limited claim only.
- Runner credential-chain qualification: NOT PROVEN.
- Trusted publisher and artifact provenance: NOT IMPLEMENTED / NOT QUALIFIED by this audit.
- PR #375 integration: NOT READY (Draft, 12 ahead / 3 behind, no review submissions, protection unverified).
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.
- Contour B: GATED.

## Next bounded action

Request/perform an authorized, read-only runner configuration inventory that returns only configuration source paths, relevant variable names and credential-helper metadata—never values. In parallel, define the versioned artifact-only worker contract and threat model. Do not alter runner credentials, create publisher credentials, dispatch agents or merge until governance authorizes the trust boundary. After any approved code change, add adversarial tests, run exact-head CI, recheck branch ancestry/protection and update the canonical map/checkpoint with verified SHAs.
