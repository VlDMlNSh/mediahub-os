# MediaHub OS — Contour A WB-14G: Reverse-Reference and Workflow Entry-Point Trace

- Date: 2026-10-15
- Status: **BOUNDED READ-ONLY TRACE / INBOUND CODE SEARCH INCOMPLETE / NO SOURCE OR WORKFLOW EXECUTION**
- Parent: WB-14F Fixed-Topology and Legacy Operational Identifier Census.
- Scope: four host-bound manifests/workflows and their direct, statically visible execution edges.
- Functional source ref: `main`; documentation artifacts written only to `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

The reviewed files contain explicit legacy host/node identities and executable workflow entry points. This pass does **not** establish a complete reverse-reference closure: the GitHub code-search connector returned zero indexed results for all exact-path/name/identifier queries, so zero results are not evidence of no callers. Direct workflow-to-script edges are proven by the workflow text; configuration readers/callers remain unproven unless explicitly identified below.

Do not delete or disable these files based on this pass. Their retirement remains blocked on complete inbound-reference closure and owner-approved greenfield replacement/retirement criteria.

## 2. Source pins and direct findings

| Source | Blob SHA on documentation branch | Directly established facts |
|---|---|---|
| `ops/agent-fabric/providers/node-role-map.yaml` | `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Declares controller `mh-dev-01`, A0-ASTRA, three execution pools, old node IDs, runner labels, model/provider metadata and command/result paths. Exact code readers not established. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Declares ASTRA_GOLD executor routing and qualification-gated selection requirements. Despite filename `v2`, schema declares `mediahub.astra-gold.executor-routing.v3`. Exact code readers not established. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Has `workflow_dispatch`; accepts command/task/node/executor inputs; dispatch conditions bind old node IDs and self-hosted runner labels; calls `python3 ops/qualification/run_distributed_local_worker.py`; checks host/user and local model availability; grants `contents: write`. No workflow was invoked. |
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Has `issue_comment.created` entry point for `/astra `; grants contents/issues/actions write; status and worker branches bind old host/user/node identities; `run-gold` invokes GitHub Actions `createWorkflowDispatch` for `astra-autonomous-supervisor.yml`; worker branch calls the same runner script. No event or dispatch was triggered. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | Defines a hard-coded `NODE_CONFIG` for the old node IDs and per-node users/platform/models/pools/env-file paths. Directly called by both reviewed workflows. Further callers not established. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Defines a hard-coded `PERMANENT_EXECUTOR_POOL` for the same three old executor identities. This is a separate queue code path; no direct call edge to either reviewed workflow is established here. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Security-sensitive command signer; retain pending caller/authority trace. This pass did not establish a direct edge from either reviewed workflow to this signer. |

The source pins above were fetched from `docs/mediahub-chat-tree-map-20261012`; they match the pins recorded in WB-14F for files already inventoried there. They are source-level evidence only and do not prove that runners, hosts, credentials, models, or workflows are live/enabled.

## 3. Workflow-entry graph (proven edges only)

1. GitHub `workflow_dispatch` → `astra-distributed-local-worker.yml` → node-conditioned runner job → `ops/qualification/run_distributed_local_worker.py`.
2. GitHub `issue_comment.created` → `astra-chat-control.yml` when the issue is not a PR and comment starts with `/astra ` → bounded parser and association check.
3. `/astra run-worker` branch → task JSON validation → hard-coded `mh-dev-02` execution assertions → `ops/qualification/run_distributed_local_worker.py`.
4. `/astra run-gold` branch → GitHub Actions dispatch for `astra-autonomous-supervisor.yml`.
5. `node-role-map.yaml` and `local-executor-routing-v2.yaml` → **reader/caller not proven** in this pass.
6. `autonomous_queue.py` → the two reviewed workflow files: **no direct edge proven** in this pass.

## 4. Search limitations and unknowns

- GitHub code-search connector returned no results for exact queries `mh-dev-01`, `node-role-map`, `local-executor-routing-v2`, `astra-distributed-local-worker`, `astra-chat-control`, and `createWorkflowDispatch`. Because the connector search appears unindexed/unavailable for this repository, this is a tooling limitation, not a negative finding.
- No repository-wide local checkout, filesystem search, test, qualification, credential use, host/runtime inspection, workflow dispatch, or infrastructure action was performed.
- Unknown: all inbound references to both YAML manifests; all external/API/UI dispatchers; whether either workflow is enabled, callable or currently used; complete callers of the worker script, signer, and autonomous queue; whether removal would affect security controls or reusable task semantics.
- The inspected workflow contains high-privilege permissions and runner-local assumptions. Retirement or editing without caller closure could create either broken automation or an unsafe residual entry point.

## 5. Safe disposition and next bounded step

- Keep all four target files and related security-sensitive code unchanged.
- Next: obtain a reliable complete repository tree/code-search surface (or a source snapshot explicitly authorized for read-only analysis), then enumerate inbound references for the two manifests and all callers/dispatchers for both workflows and the worker script. Pin every source SHA and distinguish positive references from search coverage gaps.
- Only after closure, prepare an owner-decision packet with options (retain but quarantine; replace with greenfield-neutral contracts; retire after dependency proof). Do not treat any option as accepted absent owner approval.
- No implementation, test, qualification, deployment, workflow invocation, deletion, or normative contract change was performed.

## 6. Navigation

- Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Parent census: [WB-14F](MEDIAHUB-CONTOUR-A-WB-14F-FIXED-TOPOLOGY-LEGACY-IDENTIFIER-CENSUS-2026-10-15.md)
