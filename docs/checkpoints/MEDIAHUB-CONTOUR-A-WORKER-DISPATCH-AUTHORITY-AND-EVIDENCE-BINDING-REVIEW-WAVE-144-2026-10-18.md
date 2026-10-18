# MediaHub OS — Contour A Worker Dispatch Authority and Evidence Binding Review — Wave 144

Date: 2026-10-18
Repository: VlDMlNSh/mediahub-os
Status: SOURCE-LEVEL SECURITY FINDINGS; FIX NOT IMPLEMENTED; RUNTIME NOT QUALIFIED.
Scope: bounded review of the canonical main queue dispatcher, distributed worker workflow, worker admission code, and A0 signed-command contract.

## Sources inspected

- Main `runtime/mediahub_runtime/autonomous_queue.py`, blob `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`.
- Main `ops/qualification/run_distributed_local_worker.py`, blob `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`.
- Main `.github/workflows/astra-distributed-local-worker.yml`, blob `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- Main `astra_github_agent.py`, blob `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`.
- Main `tests/test_autonomous_queue_contract.py`, blob `e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7`.
- A0 command contract source has HMAC-SHA256, freshness window, node binding, target-SHA/current-HEAD binding and replay marker in `astra_github_agent.py`; see `_command_auth_valid`, `read_command`, and `_command_already_executed`.

## Findings

### F-144-01 — Distributed worker dispatch does not enforce the A0 signed-command envelope (HIGH / acceptance blocker)

The queue dispatches the worker workflow with individual inputs `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and serialized `task_json`. The worker workflow exposes `workflow_dispatch` inputs and the worker admission code validates the task shape, node, executor, and target SHA, but the reviewed worker code does not verify an A0 HMAC signature or freshness/replay policy for the task payload. `command_id` is carried as an identifier, not proof of issuer authorization. In contrast, `astra_github_agent.py` defines a signed control-command envelope and checks its HMAC, timestamp, node, target SHA and replay state.

Impact: this code path does not itself demonstrate that every distributed execution is authorized by the canonical A0 issuer/capability contract. GitHub workflow dispatch permission is a separate authorization layer; it must not silently substitute for issuer-level authorization. This finding is a source-level admission gap, not proof that an unauthenticated actor can dispatch in the current repository configuration.

Required disposition: BLOCKED until the governing contract explicitly defines this workflow's issuer/capability envelope and the implementation validates it before executing model-controlled code. Reuse the canonical verifier or an approved signed, short-lived, node-bound task envelope; bind task payload digest, command ID, target SHA, node, executor/verifier, allowed paths/actions and expiry; reject replay; add negative tests. Do not introduce a second divergent signing protocol.

### F-144-02 — Workflow run discovery is title-substring based (HIGH / correlation gap)

After dispatch, the controller polls the latest 30 workflow runs and selects the newest display title containing each of the command ID, task ID, node ID and executor strings. The dispatch response is not captured as a unique run identifier. The command ID defaults to an empty string if absent; substring matching with an empty component matches every title. Duplicate/retried dispatches for the same task and command may therefore be correlated to the wrong run unless additional unreviewed controls prevent it.

Required disposition: require a non-empty validated command ID before dispatch, capture and verify the exact run identity using an unambiguous run correlation mechanism, and assert the run's workflow path, event, inputs, target SHA and created-after-dispatch timestamp before accepting its artifact. Add concurrency/replay tests for overlapping dispatches.

### F-144-03 — Worker evidence schema checks are not equivalent to provenance authentication

The controller checks returned evidence fields against expected values and compares reported worker/remote branch SHAs. This is useful consistency validation, but values inside a downloadable JSON artifact are not by themselves a cryptographic attestation of the workflow run, producing job, artifact digest, or trusted runner identity. Qualification evidence should bind the artifact to the exact workflow run/job and source revision and record the GitHub artifact digest and run metadata independently.

Required disposition: add run/job/attempt/source-ref metadata and artifact digest to the controller evidence record; verify these through GitHub's API before marking a task VERIFIED. Keep untrusted artifact claims distinct from host- or GitHub-derived facts.

## Validation status

This pass inspected source only. No tests, workflow dispatch, provider calls, credentials, installation, deployment, or branch integration were performed. No runtime exploit was attempted. Findings are high-priority design/implementation gaps requiring tests and governance-aligned repair; they are not claims of a demonstrated external compromise.

## Next bounded step

1. Trace the authoritative issuer/capability contract and existing signed command schema; define one approved envelope for queue-launched workers.
2. Add unit-level negative tests for missing/empty/expired/wrong-node/wrong-target/bad-signature/replayed command envelopes and task-payload digest mismatch.
3. Add a pure correlation helper with tests for duplicate dispatches, empty command IDs, wrong workflow, stale runs and mismatched inputs; require exact artifact-to-run binding.
4. Only then implement the smallest fail-closed fix on a dedicated branch, run focused tests on the exact head, and review the diff. Do not dispatch real workers as part of parser tests.

## Current disposition

Contour A remains NOT READY FOR DEPLOYMENT / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. PRs #355–#357 are separate documentation candidates and do not resolve these findings.

Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
