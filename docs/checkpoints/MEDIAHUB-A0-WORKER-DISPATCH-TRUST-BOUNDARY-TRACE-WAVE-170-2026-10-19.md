# MediaHub OS — worker-dispatch trust-boundary end-to-end trace — Wave 170

- Date: 2026-10-19
- Status: **STATIC SOURCE TRACE COMPLETE / INGRESS AUTHORIZATION AND CREDENTIAL ISOLATION OPEN**
- Repository: `VlDMlNSh/mediahub-os`
- Work branch: `docs/contour-a-wave-163-pypi-publisher-provenance-20261019`
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Canonical project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Scope: follow one dispatch path from the local queue, through GitHub workflow_dispatch inputs, into the self-hosted worker process. No execution, dispatch, secret access, host inspection, or runtime mutation.

## 1. Source pins and path

Current `main` source blob SHAs:
- `runtime/mediahub_runtime/autonomous_queue.py`: `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`
- `.github/workflows/astra-distributed-local-worker.yml`: `f650f2416c19dc75b4a0eeec037661c0c6169910`
- `ops/qualification/run_distributed_local_worker.py`: `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d`
- `astra_github_agent.py`: `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c`

Trace:
1. `process_task_remote()` in the queue copies task fields into JSON and dispatches workflow inputs `command_id`, `target_sha`, `task_id`, `node_id`, `executor`, and `task_json` via `gh workflow run`.
2. `github_auth_env()` starts with `os.environ.copy()`; it may additionally retrieve the authenticated `gh auth token` and place it in `GH_TOKEN` for the dispatch process. This is a publisher/dispatcher credential path, distinct from task authority.
3. The workflow accepts those values as `workflow_dispatch` inputs, grants `contents: write`, runs on self-hosted nodes, and checks out the supplied `target_sha` with `persist-credentials: true`.
4. The worker's `load_task()` parses `ASTRA_MICRO_TASK_JSON` and checks required fields and object shape. The inspected admission path checks node/executor consistency and later checks result fields; this source trace did not find a cryptographic verification of a signed task envelope before model execution.
5. The worker reads the node's FCC environment file and passes its values into the model client's environment, including `ANTHROPIC_AUTH_TOKEN` / `ANTHROPIC_API_KEY`. Model-controlled tools include shell execution and edits in the checked-out workspace. Post-run result and changed-path checks do not provide pre-execution OS isolation.

## 2. Findings — carefully scoped

- **Worker ingress authorization:** a controller command HMAC check in `astra_github_agent.py` does not by itself prove that the independently supplied workflow task JSON is signed and bound to that command, repository, target SHA, workflow audience, node, executor, scope, expiry, and revocation state at the worker's admission boundary.
- **GitHub write authority:** `contents: write` plus persisted checkout credentials makes repository write authority available in the job/workspace context. The trace does not establish that the model actually read or used those credentials.
- **Provider credential boundary:** the FCC token is deliberately placed in the model process environment. This is an exposure path; no token value was read, and its commercial/provider entitlement was not established.
- **Evidence binding:** returned JSON field comparisons occur after execution and cannot replace pre-execution authorization or provenance validation. Matching IDs are correlation, not issuer proof.

These are source-derived security gaps, not evidence of exploitation, exfiltration, a live runner, or a dispatched task.

## 3. Required disposition before any authorized dispatch on this path

1. Keep dispatch gated pending owner-approved WB-05 / GOV-CAP-01…07 and R-06 decisions; do not invent an issuer, token format, revocation policy, or audit-unavailable behavior.
2. Define and accept one canonical command↔task↔target authorization contract, then verify it inside the worker before branch creation or model start. Add positive and negative tests against that exact verifier.
3. Separate the model execution identity from GitHub publication/dispatch credentials; remove persisted checkout credentials from the model workspace; route FCC/provider credentials through an approved broker or otherwise enforce a documented OS-level boundary.
4. Make workflow permissions least-privilege by job and step, and bind execution evidence to workflow run, attempt, event, repository, immutable SHA, job, artifact digest, task ID, and accepted issuer grant.
5. Independently review and test the controls before considering any worker dispatch. Keep publication, PR promotion, merge, deployment, qualification, and acceptance as separate gates.

No source change is proposed as an accepted remediation by this report; these are prerequisites and review criteria, not an authorization to change live infrastructure.

## 4. Live refs, CI and limits

- PR [#373](https://github.com/VlDMlNSh/mediahub-os/pull/373) was OPEN / Draft / unmerged at the start of this pass. Its work branch was 32 commits ahead / 0 behind the intended documentation base `docs/mediahub-chat-tree-map-20261012` at `28816f6b523c8cbc878ebd0575b17bc419669889`.
- Exact-head workflow lookup for pre-wave head `223911050a3c7f01d21e034e527dda33bbf380b7` returned an empty list. The connector covers PR-triggered runs and only the first page; no CI success is claimed.
- Canonical docs ref vs `main` remains diverged: 2,333 ahead / 27 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge, rebase, or cherry-pick wholesale.
- No tests, provider calls, secret reads, live host/process inspection, workflow dispatch, code/runtime/workflow edits, merge, deployment, or qualification occurred.
- Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.

## 5. Next bounded action

Refresh the exact PR head and workflow evidence after this documentation-only update. Then perform a governance/source-bound acceptance review of the proposed worker-ingress verifier and credential isolation requirements; do not dispatch workers until the authorization and isolation gates are satisfied.
