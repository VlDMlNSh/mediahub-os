# Contour A worker admission and run-correlation audit — Wave 159

Date: 2026-10-19
Status: **SOURCE-LEVEL BLOCKERS CONFIRMED / NO RUNTIME QUALIFICATION**

## Scope and source refs

Repository: `VlDMlNSh/mediahub-os`.
Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`.
Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301), still open.
Relevant PRs: [#358 run correlation](https://github.com/VlDMlNSh/mediahub-os/pull/358), [#361 WB-05 Option C governance proposal](https://github.com/VlDMlNSh/mediahub-os/pull/361), [#363 schema-validation candidate](https://github.com/VlDMlNSh/mediahub-os/pull/363), [#367 Wave 158 evidence](https://github.com/VlDMlNSh/mediahub-os/pull/367).

Read-back source SHAs on `main`:
- `astra_github_agent.py`: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`.
- `ops/qualification/run_distributed_local_worker.py`: `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`.
- `.github/workflows/astra-distributed-local-worker.yml`: `f650f2416c19dc75b4b0eeec037661c0c6169910`.
- `runtime/mediahub_runtime/autonomous_queue.py`: `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`.
- `tests/test_autonomous_queue_contract.py`: `e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7`.

## Finding A — A0 signed command and distributed worker are separate admission paths

The canonical A0 transport in `astra_github_agent.py` implements:
- canonical JSON serialization excluding the signature field;
- HMAC-SHA256 comparison;
- `issued_at` age validation;
- node/operation/target SHA/current HEAD checks;
- a persistent command-ID replay marker.

But the distributed local worker path does not call this verifier. `load_task()` in `ops/qualification/run_distributed_local_worker.py` only parses JSON and requires task shape fields. `main()` checks configured node, task/node binding, executor, 40-hex target SHA, current checkout HEAD, clean workspace, and local model presence, then creates a task branch. It does not authenticate the task JSON signature, issuer/capability, freshness or replay marker before branch creation/execution.

The workflow `.github/workflows/astra-distributed-local-worker.yml` calls the input “Full signed task payload” and “Signed Astra command id”, but those names do not establish signature verification. It passes `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and `task_json` as independent workflow inputs. Workflow-level dispatch permission is not a substitute for issuer/capability authorization.

Severity: **HIGH / Contour A acceptance blocker**. This is a source-level gap, not evidence of a live exploit.

## Finding B — run-correlation candidate exists, but is not canonical

On `main`, `runtime/mediahub_runtime/autonomous_queue.py` still polls the latest 30 workflow runs and selects the newest display title containing the command ID, task ID, node ID and executor strings. The empty command ID case can degenerate into overly broad matching.

PR #358 proposes exact full-title matching, a non-empty command ID, dispatch-time freshness, rejection of duplicate exact matches, and seven focused regression tests. Its patch also correctly states that a run title is correlation metadata, not authorization. At the time of this review, PR #358 remained open/Draft/unmerged and had no submitted PR reviews. Workflow runs associated with its head were reported successful, but this pass did not independently read back their event/head SHA provenance; therefore they are not recorded here as exact-head proof.

## Required safe disposition

1. Keep worker admission blocked for trusted autonomous qualification until the approved issuer/capability envelope is explicitly defined by the applicable governance authority.
2. Reuse the canonical A0 verifier or an approved shared verifier. Do not invent a second HMAC protocol, key source, token format, or issuer identity in the worker.
3. Bind the verified authorization to command ID, task-payload digest, target SHA, node, executor/verifier, allowed paths/actions, issue/expiry time and replay state; validate before model-controlled execution and before branch creation.
4. Add negative tests for absent/bad signature, wrong node, stale/future issue time, replay, task digest mismatch, target SHA mismatch, unsupported capability and malformed payload. Tests must use an approved contract, not define it by themselves.
5. Review PR #358 separately: verify its exact-head CI provenance and test results, then obtain independent review before any promotion/integration. Even when merged, correlation is not authorization.
6. Preserve the WB-05 Option C governance proposal as **PROPOSED / NOT ACCEPTED / NOT IMPLEMENTED** until the required process records acceptance.

## Explicit non-claims

No code change to worker admission was made in this wave because the signed ingress contract and issuer governance remain unresolved. No secret was read, no provider invoked, no worker dispatched, no merge or deployment occurred. The local-worker workflow still uses self-hosted runner labels; GitHub-hosted ephemeral worker isolation is not established by this audit.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.

## Next bounded step

Independently validate PR #358's exact-head CI provenance and regression behavior, and locate the accepted governance artifact (if any) that defines issuer/capability for distributed worker dispatch. If no accepted artifact exists, prepare a decision-ready contract delta for governance review without implementing a new token/signature format.
