# MediaHub OS — worker issuer and publisher boundary audit (Wave 235, 2026-10-20)

## Scope and status

This is a source-bound, read-only continuation after Wave 234. It examines the current distributed worker implementation and the credential-minimization candidate PR #375. The objective is to determine whether the current worker/publisher boundary is sufficiently established to implement or accept the candidate.

**Disposition: BLOCKED / NOT ACCEPTED.** No code was changed, no worker was dispatched, no secret was accessed, no test was run locally, and no merge/deployment/qualification was performed.

## Current refs and source evidence

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Current `main` HEAD: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- Worker source: `ops/qualification/run_distributed_local_worker.py@main`, blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`, 715 lines.
- Worker workflow: `.github/workflows/astra-distributed-local-worker.yml@main`, blob `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- PR #375: https://github.com/VlDMlNSh/mediahub-os/pull/375
  - State: OPEN / DRAFT / unmerged.
  - Head SHA: `6fb078aad7e8e1bb41916168fdd038dfa4e1022b`.
  - Candidate workflow blob reported by PR: `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`.
  - Candidate test blob reported by PR: `4b3787368758f2dba4abd85325025cfbfbe59e9b`.
  - Exact-head CI: Astra Verify run `39295373907` SUCCESS; Astra Cloud Runtime Validation run `39295373833` SUCCESS.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Related security assignment: https://github.com/VlDMlNSh/mediahub-os/issues/378

## Verified source findings

### 1. Task envelope is parsed but not cryptographically authenticated inside the worker

In `load_task()` (worker source lines 64–76), the process reads `ASTRA_MICRO_TASK_JSON`, JSON-decodes it, checks that the value is a dictionary, and checks for required fields:
`task_id`, `node_id`, `executor`, `verifier`, `mission`, `boundary`, `acceptance`.

A full text scan of the 715-line worker source found no references to `signature`, `issuer`, `capability`, or `hmac`. The function therefore does not verify a cryptographic signature or issuer/capability. This finding is limited to this worker file; it does not assert that no upstream caller exists. Any upstream admission check must be traced and shown to authenticate the exact task payload and bind its authorization to the selected node, executor, target SHA and permitted actions. A signed-looking field or workflow input label is not evidence of verification.

### 2. Target binding exists, but it is not issuer authorization

In `main()` (around lines 385–410), the worker requires a 40-character lowercase hexadecimal target SHA and checks it against the current checkout HEAD. It then constructs a branch name using task ID, the target SHA prefix and wall-clock time. These checks help bind execution to a checkout but do not authenticate the task issuer, enforce capability scope, establish revocation/expiry, or prove the worker was authorized to publish a particular change.

### 3. Worker directly commits and pushes

In the worker source around lines 660–679, a non-empty worktree leads to:
- `git add -A`;
- `git commit`;
- `git push origin HEAD:refs/heads/{branch}`;
- `git ls-remote` and comparison of the remote branch SHA with the local commit SHA.

The code also records a PASS when the remote SHA matches. This proves only that the worker observed the pushed branch pointing to its own commit; it does not independently validate the patch against a trusted policy or prove the task's publisher authority. Because the worker itself is the producer and publisher, there is no separately trusted publication boundary in this path.

### 4. PR #375 reduces checkout credentials but leaves a publication dependency unresolved

The PR changes workflow-level `contents: write` to `contents: read` and sets `persist-credentials: false` on all three checkout steps. It adds static YAML-policy tests and wires the focused test into CI. The exact-head Astra Verify and Cloud Runtime Validation runs passed.

Those checks do not demonstrate a successful authorized worker publication. The current worker still invokes `git push`; the candidate no longer retains the checkout-provided write credential. An ambient credential helper might exist in some runner environments, so this is an unresolved compatibility/security dependency, not an observed runtime failure. Do not restore broad write credentials in the model-execution job merely to make the push path work.

## Risk and acceptance matrix

| Control | Evidence | Disposition |
|---|---|---|
| Immutable target checkout | Target SHA syntax and HEAD equality in worker | PARTIAL; does not authorize issuer or publisher |
| Cryptographic task issuer verification | No signature/issuer/capability/HMAC logic found in worker source | NOT PROVEN; upstream admission boundary must be traced |
| Capability scoping and expiry/revocation | Not enforced in the worker file | NOT PROVEN |
| Worker cannot publish | Worker performs commit and push itself | FAILS CURRENT BOUNDARY REQUIREMENT |
| Narrow publisher credential | No separate publisher in PR #375 diff | NOT IMPLEMENTED |
| Patch validation independent of worker worktree | Current checks run before worker commit; no separate trusted reconstruction shown | NOT PROVEN |
| Remote SHA readback | Worker compares remote branch SHA to its own commit SHA | PARTIAL provenance only |
| PR #375 CI | Exact-head Verify and Runtime Validation passed | PASS for the checks only; no worker publication or security acceptance |

## Required next implementation gate

Do not merge PR #375 or claim the publisher boundary is solved. The smallest safe sequence is:

1. Trace the actual workflow caller and canonical command-admission path. Record where issuer authentication, task integrity, target binding, expiry, revocation, replay protection and capability evaluation occur. If any control is absent, preserve the fail-closed blocker.
2. Define the worker output as an artifact/patch only. The worker must not have a GitHub write token, credential helper, or ability to publish the result.
3. Define a separate trusted publisher contract only after the issuer/capability authority is accepted. The publisher must independently reconstruct or inspect the patch against an immutable base; validate task/run identity, allowlisted paths, symlinks, file modes, size, duplicate/malformed manifest fields and diff policy; recompute hashes; enforce freshness/idempotency/revocation; then use a narrowly scoped write capability.
4. Add negative tests proving the worker cannot push, forged/stale/replayed task envelopes are rejected, untrusted branch/commit metadata is ignored, and the publisher rejects base-SHA mismatch, path escape, unapproved paths, malformed manifests, secret-bearing output and remote-SHA mismatch.
5. Exercise the actual authorized publication path in a disposable test repository, bind results to the exact PR head and run/job/artifact IDs, and have an independent reviewer inspect the boundary. Hosted CI success alone is insufficient.

The project still has unresolved GOV-CAP-01…07 and R-06/MH-12 authority/privacy decisions in prior governance records. This pass does not choose an issuer protocol, key store, authority owner, or product-state authority on behalf of governance.

## Verification limits and next step

- Re-read the current worker source and workflow from `main`; exact blob SHAs are recorded above.
- Re-read PR #375 metadata, diff, changed filenames, and exact-head workflow runs. The PR remains Draft and unmerged.
- This is static source review only; no local test execution, worker dispatch, credential access, remote publication, independent qualification or deployment occurred.
- The canonical map and large checkpoint were not rewritten in this pass because the map Contents response is empty and a safe Git-data tree update is not exposed in the current integration.
- Next: trace the canonical issuer/admission caller and the full workflow-to-worker input path, then update the source-bound control matrix. Keep PR #375 Draft/unmerged until the trusted publisher path and independent review are evidenced.
