# MediaHub OS Contour A — worker environment inheritance audit (Wave 209)

- Date: 2026-10-19
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Scope: source-level review of environment inheritance and staging behavior. No host inspection, runtime dispatch, secret access, code change to the candidate PR, merge, deployment or gate promotion.

## Current state revalidated

- PR #375 remains OPEN / Draft / unmerged at `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
- Current compare against main: 12 commits ahead / 3 behind; status `diverged`; merge base `c06015e0b1526e0aaa6a522306052b077455aba5`. The comparison's base commit is currently `0897bd613c0c041794ec5ec4a72cd487b13a6944`. Refresh immediately before any integration.
- Exact-head CI remains SUCCESS: [Astra Verify 39295373907](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373907) and [Astra Cloud Runtime Validation 39295373833](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39295373833).
- No PR review submissions or review threads were returned. Issue #301 remains OPEN. Branch protection and required-review configuration remain unverified.
- Current truth on main, blob `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`: G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED.

## Source evidence

At PR head:
- Worker script `ops/qualification/run_distributed_local_worker.py`, blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`.
- Workflow `.github/workflows/astra-distributed-local-worker.yml`, blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`.
- Static policy tests `ops/qualification/test_worker_workflow_credential_policy.py`, blob `2c5fae2d431ca765bb548f4a2b5d70874961a438`.

Confirmed worker behaviors:
1. Generic helper `run(..., env=None)` passes `env` directly to `subprocess.run`; when omitted, Python inherits the parent process environment.
2. `start_fcc` copies `os.environ`, then overlays values parsed from the FCC env file and launches `fcc-server` with that combined environment.
3. `exec_claude` also copies `os.environ`, overlays FCC values and configures Claude transport. Its configured tool modes include Bash.
4. After verifier success, the worker stages the entire workspace with `git add -A`, commits and attempts `git push origin HEAD:refs/heads/{branch}`; it then compares the remote SHA to local HEAD.
5. Workflow YAML uses `contents: read` and `persist-credentials: false` on all three checkout steps. That does not by itself establish the effective environment, Git credential helper, remote URL, service-account or OS-level access on the self-hosted runner.

These are source-level findings only. They prove a direct publication attempt path and ambient-environment inheritance, but do **not** prove that a write credential exists, that a push succeeds, or which credential source is effective. No environment values, secret files, runner service configuration or host state were inspected.

## Test coverage boundary

The static policy test file has 11 tests at the inspected blob, including duplicate-key rejection and workflow/job permission checks. These tests inspect workflow YAML; they do not test the worker's environment allowlist, credential-helper behavior, staging allowlist, or publisher separation. Green CI is not evidence that those runtime boundaries are enforced.

## Truth-ranked findings

### P0
- Worker execution and publication are still in one trust domain.
- `os.environ.copy()` plus broad subprocess inheritance leaves ambient variables in the execution environment unless explicitly removed; model-controlled Bash increases the significance of that boundary.
- `git add -A` can stage every workspace change, not only explicitly authorized output paths.
- Issuer/capability authority, revocation/replay semantics, independent review and publisher provenance remain unresolved.

### P1
- Static workflow policy tests need complementary tests for environment allowlisting, forbidden Git credential configuration, permitted output paths, symlinks/binaries/oversized artifacts, and immutable base-SHA binding.
- Effective runner credential-chain evidence remains unavailable; use approved read-only metadata and never print environment values or read secret-file contents.

## Ranked architecture options

1. **Preferred:** worker gets no publication authority, runs with a minimal allowlisted environment, and emits a quarantined artifact bound to task/command IDs, immutable base SHA and content digest. A separate trusted publisher validates authorization and diff/path policy before using narrowly scoped credentials.
2. **Conditional:** publisher-side short-lived GitHub App credential only after governance approves issuer/capability contracts, key lifecycle, audit, revocation and recovery.
3. **Rejected as default:** model-controlled worker inherits broad environment and directly commits/pushes workspace state.

## Readiness and next action

- PR #375 integration: NOT READY — Draft, diverged 12/3, no review submissions, branch protection unverified.
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.
- Contour B: GATED.
- No worker/Gemini/provider dispatch, secret access, host command, merge, deployment, qualification or acceptance occurred.

Next bounded step: write a testable artifact-only worker contract and tests for allowlisted environment, output path allowlist, immutable target SHA, and no direct publication calls; obtain governance disposition before changing authority semantics or adding publisher credentials. Refresh head, CI, ancestry and protection evidence before any integration.
