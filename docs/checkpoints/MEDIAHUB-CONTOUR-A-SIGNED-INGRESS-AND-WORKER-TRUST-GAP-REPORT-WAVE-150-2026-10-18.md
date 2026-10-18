# Contour A signed-ingress and worker trust-gap report — Wave 150 — 2026-10-18

## Summary
A bounded read of the current `main` worker path found an important trust-boundary gap: the reviewed worker entry point parses the task JSON and checks required fields, but the inspected code does not validate a canonical signed A0 envelope before execution. This is a source-review finding, not evidence that a live exploit occurred.

## Exact source evidence
- `ops/qualification/run_distributed_local_worker.py`, blob SHA `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`, lines around 45–70: `load_task()` reads `ASTRA_MICRO_TASK_JSON`, JSON-decodes it, requires an object and checks for `task_id`, `node_id`, `executor`, `verifier`, `mission`, `boundary`, and `acceptance`. No signature/HMAC/issuer/capability/freshness/replay validation appears in this function.
- Same file, `main()` around lines 386–420: reads `ASTRA_COMMAND_ID`, `ASTRA_TARGET_SHA`, and `ASTRA_NODE_ID`; validates configured node, task/node binding, executor, target SHA/current HEAD and workspace cleanliness. The reviewed path does not bind the command ID to a verified signed envelope before branch creation.
- `.github/workflows/astra-distributed-local-worker.yml`, blob SHA `f650f2416c19dc75b4a0eeec037661c0c6169910`: workflow_dispatch accepts `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and `task_json`; its “Canonical admission” steps check host/user/executor/local model availability. The three worker jobs use self-hosted runner labels (`mediahub-control`, `mediahub-provider`, `astra-control`), not GitHub-hosted ephemeral runners.
- `runtime/mediahub_runtime/autonomous_queue.py`, blob SHA `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`: on `main`, run correlation still uses substring matching over a 30-run window and picks the newest title match. PR #358 contains a fail-closed fix, but remains open/Draft/unmerged, so its fix is not canonical on `main`.
- `ops/qualification/qualify_execution_backends.py`, blob SHA `acf092d5dd9d67ab187f1b67ab691ca730028306`, is a confirmed consumer of `ops/qualification/provider_model_registry.json`. The reviewed autonomous queue and agent_fabric files do not reference that registry; do not treat qualification-catalog entries as dispatch admission.

## Verified CI evidence
- PR #358 exact head: `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`.
- Workflow run 39117896120, job 117647309406: the named `Worker run correlation regression tests` step completed successfully; decoded log confirms **7/7 tests passed**.
- The same job reports **429 cloud admission unit tests passed**.
- This is evidence for correlation tests only; it does not validate signed ingress, issuer lifecycle, provider admission, provenance completeness or Contour A qualification.

## Severity and decision
**HIGH / BLOCKING for trusted autonomous ingress qualification.** Do not patch in an invented HMAC envelope or key-management policy: the Wave 149 issuer-governance checkpoint explicitly leaves issuer authority, principal lifecycle, verifier location, trust-anchor/compromise ownership, revocation/freshness, delegation bounds, acceptance evidence and R-06 audit/privacy open. A verifier contract and negative matrix must follow accepted owner/governance decisions.

## Required follow-up
1. Obtain/record the governance decisions listed in the Wave 149 issuer checkpoint.
2. Derive a versioned envelope contract from accepted A0/MH-12/R-06 contracts; include issuer/capability/audience/node, task digest, target/ref/source SHA, expiry/freshness, replay/idempotency and revocation semantics.
3. Add fail-closed negative fixtures and test the worker entry point itself, not only a signing smoke test.
4. Bind GitHub workflow/run/job/attempt/event/ref/source SHA/artifact ID/digest and task-envelope digest to evidence; verify downloaded artifact and authoritative run metadata before accepting PASS.
5. Keep the current self-hosted worker route unqualified until isolation, lifecycle, secret injection, provenance and recovery gates are independently verified. Do not call it GitHub-hosted ephemeral execution.
6. Merge PR #358 only after current-head checks, branch protection/review requirements and exact CI evidence are refreshed.

## Boundaries
No credential values were read, no provider API was called, no worker was dispatched, and no code/secret/runner configuration was modified in this pass. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED; Contour B remains blocked.
