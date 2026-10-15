# MediaHub OS — Contour A WB-14F: Fixed-Topology and Legacy Operational Identifier Census

- Date: 2026-10-15
- Status: **BOUNDED READ-ONLY SOURCE CENSUS / NOT EXHAUSTIVE / NO DELETION OR CODE CHANGE**
- Parent: WB-14E greenfield topology exclusion.
- Goal: identify active-branch source files that still encode the prior executor topology, distinguish legacy operational references from reusable control logic, and define safe next review boundaries.

## 1. Result

The prior executor topology is not merely mentioned in old documents: it remains encoded in operational source/configuration on `main`. These files must not be used as the new target topology by default. This pass confirms the existence of old fixed identities in the files listed below; it does **not** establish whether any old host is online, whether a workflow is currently enabled in GitHub settings, or whether any artifact is safe to delete.

The greenfield target baseline has no accepted node identities yet. “Alamo” is still a proposed logical executor name, not a verified hostname or accepted placement.

## 2. Source-pinned census

| Path on `main` | Blob SHA | Evidence | Classification / disposition |
|---|---|---|---|
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Fixed permanent executor pool with three prior node names; result metadata declares `github_remote_claude_only`. | **LEGACY-OPERATIONAL** as target topology; exclude from greenfield target baseline. Generic queue semantics may be reusable only after independent review. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Header binds schema to ASTRA_GOLD qualification-gated system and node/controller `mh-dev-01`. | **LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN**; not target routing contract. Trace readers/importers before retirement. |
| `ops/agent-fabric/providers/node-role-map.yaml` | `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Declares controller and execution nodes including old node IDs/hostname and old pool/model metadata. | **LEGACY-OPERATIONAL**; not target inventory. Preserve IDs in historical evidence; no blind deletion. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | 715-line worker script contains hard-coded old node identities. | **LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN**; caller and generic signed-task contract review required before removal. |
| `.github/workflows/astra-distributed-local-worker.yml` | `f650f2416c19dc75b4a0eeec037661c0c6169910` | Workflow binds inputs/run name and execution to old node names. | **LEGACY-OPERATIONAL**; review triggers, permissions, dispatchers and dependencies before disable/delete. This pass did not invoke it. |
| `.github/workflows/astra-chat-control.yml` | `51b17ec2410032772f9baa1de4afedb6b000f3c4` | Control workflow includes old executor/node references. | **LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN**; do not assume the entire control path is disposable without caller/contract closure. |
| `control/qualification/distributed-runner-contract.json` | `993f51f07c7937165ffb3bfbe59cd0801ea71ec0` | Versioned contract explicitly lists old node IDs, runner labels and host allowlists. | **LEGACY-OPERATIONAL / SHARED-OR-UNKNOWN**; generic runner admission concepts may be reusable, identities are not. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Signer source contains old node references. | **SHARED-OR-UNKNOWN**; signer/trust semantics may be security-critical and must not be deleted based on node strings alone. |
| `ops/astra_orchestrator.py` | `7e22a283ddbbdfeceeea9aa1bd01c33fdbf7cfb8` | No literal old-node names in the bounded file scan; docstring describes resident Astra coordinator. | **SHARED-OR-UNKNOWN**; absence of literal names does not prove independence from legacy config/imports. |
| `docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md` | `da26185254d9954fcee204f81ecca129bf052e7c` | Canonical ASTRA executor-workflow policy document dated 2026-10-08; no literal old-node strings in the bounded scan. | **NORMATIVE/SHARED REVIEW REQUIRED**; do not rewrite its authority claims implicitly. Needs controlled comparison with greenfield direction and accepted decisions. |

## 3. What is and is not established

### Confirmed
- The old fixed executor topology is still present in `main` source/configuration.
- The legacy ledger correctly warns against treating these paths as new target inventory.
- The documentation branch currently contains the greenfield ledger and WB-14E/WB-14F tracking, while source paths above were read from `main`.

### Not established
- Whether old hosts still exist, are online, or run any service.
- Whether the named workflows are enabled, dispatched or operational in the current GitHub settings.
- Complete reverse-reference closure across all source, workflows, generated files, external callers and repository history.
- Whether generic queue, signature, task, claim or admission semantics can be reused safely.
- Any accepted new node list, target executor pool, provider/backend, or deployment topology.

## 4. Branch-state warning

A fresh GitHub compare reports `docs/mediahub-chat-tree-map-20261012` as **diverged** from `main`: docs branch ahead by 1438 and behind by 4, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`; main-side comparison base commit `ab36db009d034db8dca723691e23b331322287e7`. No merge, rebase, cherry-pick or integration was attempted. Do not treat the docs branch as a clean mirror of main.

## 5. Recommended disposition

1. Keep all identified old operational paths out of the new target deployment plan.
2. Next perform a bounded **reverse-reference and workflow-entry-point trace** for the highest-risk candidates: the local-worker workflow, chat-control workflow, node-role map and local-executor routing YAML. Read only; include exact inbound references and status limits.
3. Separate retirement proposals for host-bound manifests from preservation/review of security-sensitive shared code such as command signing and generic task contracts.
4. Only after dependency closure, historical-ID preservation and explicit authority review should a separate change propose quarantine/removal. This census does not authorize or perform it.
5. Do not add any new target node names until the owner explicitly accepts a target hardware/role map.

## 6. Verification boundary

- Source/document fetches only; no test or qualification execution.
- No workflows invoked; no credentials or provider/model calls.
- No host/runtime inspection, installation, infrastructure change, deployment, migration, merge/rebase/cherry-pick, or deletion.
- Search results alone were insufficient for a complete repository-wide census; this report relies on direct source fetches for the paths listed above.

Project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
