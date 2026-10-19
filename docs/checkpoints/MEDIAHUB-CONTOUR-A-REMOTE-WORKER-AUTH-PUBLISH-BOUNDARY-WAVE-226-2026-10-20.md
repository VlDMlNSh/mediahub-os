# Contour A Wave 226 — remote worker authorization and publication seam

Date: 2026-10-20. Status: bounded source audit; no implementation, runtime dispatch, qualification, or acceptance.

## Navigation and governing references

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map ref: `docs/mediahub-chat-tree-map-20261012`; map blob reported by Contents API: `2187b4ca50792fe073f0979442c0f73432a2f6f9`. Contents API returned empty text; raw read through the connected desktop returned the map text and confirms it is an inventory, not full acceptance.
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Evidence PR (this report's noncanonical branch): https://github.com/VlDMlNSh/mediahub-os/pull/396
- Credential-minimization Draft PR: https://github.com/VlDMlNSh/mediahub-os/pull/397
- Prior Wave 225 report: https://github.com/VlDMlNSh/mediahub-os/blob/work/contour-a-wave216-continuous-qualification-2026-10-20/docs/checkpoints/MEDIAHUB-CONTOUR-A-SIGNED-CONTEXT-REUSE-BOUNDARY-WAVE-225-2026-10-20.md

## Exact source observations

1. `astra_github_agent.py`, main blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`, implements a local command-consumption path. `read_command()` checks the command schema, node/operation, target SHA, required fields, owned paths, freshness/HMAC through `_command_auth_valid()`, current HEAD equality, and a local replay marker. This is evidence that the local agent has command-authentication logic; it does not prove that every other execution path consumes the same signed command.
2. `ops/control/sign_command.py`, main blob `fc6943a79cefdf06e59d6e32771d2df551b2f0e9`, signs canonical JSON using node-specific HMAC-SHA256 and validates a bounded issue-time window. The existing tests in `tests/control/test_sign_command.py`, blob `af3b93c1ed482d1058873a1cea65237b79ca6b74`, cover signing, tamper sensitivity, missing required fields and stale timestamps. A valid HMAC is command integrity/authentication, not by itself an authorization grant to publish source.
3. `runtime/mediahub_runtime/autonomous_queue.py`, main blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`, builds a task payload and dispatches `.github/workflows/astra-distributed-local-worker.yml` with separate `command_id`, `target_sha`, task identity and task JSON. The inspected dispatch path does not pass the signed command body or a verifiable capability receipt as a workflow input.
4. `.github/workflows/astra-distributed-local-worker.yml`, main blob `f650f2416c19dc75b4a0eeec037661c0c6169910`, accepts `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and `task_json`; its inspected admission step checks host/user, executor and local model availability. It does not visibly verify the command HMAC, issuer/capability, or bind the task boundary to the signed command's `owned_paths`.
5. `ops/qualification/run_distributed_local_worker.py`, main blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`, checks task shape, node/executor binding, target SHA, clean workspace and changed-path scope. When changes exist, it commits them, runs `git push origin HEAD:refs/heads/{branch}`, and verifies the remote SHA. The result JSON includes an evidence digest, which provides integrity metadata but does not authorize publication.
6. PR #397 head `8ee730e2a5d9038d6f2764cf00e483bd3a5505e0` changes the worker workflow to `contents: read` and `persist-credentials: false` on checkout steps, with semantic YAML regression tests. Exact-head CI was read back as SUCCESS for Astra Verify (run 2146 / id 39332175846) and Astra Cloud Runtime Validation (run 972 / id 39332175994). PR #397 remains open and Draft, not merged.

## Findings

### F-226-1 — command-authentication coverage is not end-to-end (BLOCKER / NOT_PROVEN)

The local agent has signed-command validation, but the separately dispatched distributed worker path carries a command ID and task JSON without demonstrating validation of the signed command or a scoped capability at the worker admission boundary. Do not infer end-to-end issuer/capability enforcement from the existence of `read_command()` or the HMAC signer.

### F-226-2 — credential minimization conflicts with the current publication mechanism (BLOCKER / compatibility risk)

The current worker implementation explicitly pushes its own source branch. PR #397 disables persisted checkout credentials and removes workflow contents-write permission. This is a sensible reduction of ambient credentials, but the worker's current push step has no demonstrated alternative authorized publisher credential. Therefore the proposed permissions change may make source publication fail. The workflow CI passing does not exercise a live authorized source-publish operation and does not disprove this conflict.

### F-226-3 — task boundary and signed command scope are separate inputs (BLOCKER / NOT_PROVEN)

The worker validates changed paths against task-provided `boundary` / `forbidden` values, while the signed command schema contains `owned_paths`. The inspected dispatch path does not prove that task boundary is a subset of signed `owned_paths`, or that the issuer/capability authorizes this exact publication operation.

## Recommended bounded sequence

1. Keep PR #397 Draft/unmerged pending a compatible publication design and an independent security review.
2. Define a source-change artifact contract bound to exact `command_id`, issuer/principal, target SHA, task ID, declared boundary, changed-path manifest, patch/tree digest, test evidence, and expiry/replay policy.
3. Separate worker execution from publication: worker emits a quarantined artifact; a narrowly scoped trusted publisher validates signature/issuer/capability, exact target SHA, path containment, manifest/digests, freshness, replay protection and policy before creating a branch/PR. Do not give the general worker broad source-write authority as a shortcut.
4. Add negative tests for missing/invalid/stale command proof, wrong issuer or node, capability mismatch, task boundary exceeding signed `owned_paths`, path traversal, artifact tampering, replay, stale target SHA, and publication denial. Include a compatibility test proving that the worker can complete execution without a source-write token and that the publisher alone performs an authorized publication.
5. Re-run focused tests and exact-head CI, inspect workflow permissions/rulesets, then ask for independent security/governance review. Keep qualification, deployment and acceptance separate.

## Verification record

- Read back source and blob SHAs for the signer, agent, queue, worker, worker workflow, and credential-policy PR.
- Read back exact PR #397 head and two successful exact-head workflow runs.
- No worker dispatch, credential use, branch publication, merge, deployment, or qualification was performed by this pass.
- Local tests on a detached worktree at exact main SHA `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`: signer suite 5/5 passed; worker security-gate suite 4/4 passed. The distributed workflow contract suite could not run in this environment because `pytest` and PyYAML are absent (`ModuleNotFoundError`); this is an environment limitation, not a pass. CI results above belong to PR #397's exact head and are not tests of the proposed publisher boundary.
- Current truth remains **NOT_PROVEN / BLOCKED**. G0–G11 remain BLOCKED; G11 remains HUMAN_ONLY. Contour A is not accepted.

## Next step

Implement and test the smallest source-change artifact manifest plus trusted-publisher contract on a dedicated branch, after checking the map's Contour A navigation and the applicable security/authorization contract. Do not merge PR #397 until the publication compatibility and end-to-end authorization gaps are resolved or the architecture explicitly accepts a different safe mechanism.
