# MediaHub OS — Contour A WB-14M: Broad legacy control and config-loader scan

- Date: 2026-10-16
- Status: **BOUNDED READ-ONLY SOURCE RECONCILIATION / NOT FULL REPOSITORY CLOSURE / NO EXECUTION**
- Parent: WB-14L supplemental non-workflow legacy reference scan.
- Functional source ref: `main`; documentation only on `docs/mediahub-chat-tree-map-20261012`.

## 1. Executive result

This wave cross-checked core execution and security-sensitive sources against the two legacy provider manifests, then expanded the source scan across task data, attestation/evidence producers, orchestration modules, qualification helpers and repository search.

**Confirmed:** the old topology is not confined to workflow YAML. It is embedded in the queue's executor map and dispatch/polling code, worker identity tables, HMAC key maps, attestation/evidence producers, qualification allow-lists, task JSON and a topology-consistency test that asserts the old pool. These are legacy source facts, not accepted greenfield target requirements.

**Not established:** exact code readers of `node-role-map.yaml` and `local-executor-routing-v2.yaml`. The directly inspected `runtime/mediahub_runtime/agent_fabric.py` uses JSON claim-state files and contains no literal reference to either manifest; that file-local result does not establish that the manifests are unused. GitHub code-search queries for both manifest names, `yaml.safe_load`, routing names and workflow dispatch returned zero results, but the repository search index is known to be unavailable and those zero results are non-diagnostic.

## 2. Core control-source pins

Fetched directly from `main`:

| Path | Blob SHA | Evidence |
|---|---|---|
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Lines 25–27 define the fixed legacy executor map; lines 308–328 dispatch and poll `astra-distributed-local-worker.yml`. |
| `runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | Reads/writes JSON claim state; no literal reference to either provider manifest or YAML loader found in this file. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | Contains legacy node/host identity tables and local configuration/evidence file reads. |
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Contains old-node HMAC environment-key mapping, required-node set, and evidence reads. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Security-sensitive signing path repeats old node/HMAC key mappings. |
| `ops/agent-fabric/providers/node-role-map.yaml` | `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Manifest itself encodes old controller and executor-pool identities. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Manifest itself encodes old node/controller identity and executor qualification routing. |
| `tests/test_astra_topology_consistency.py` | `cc5410f631a161b3e3bfb4bae198340f905da6e4` | Test source explicitly asserts the three-node pool and reads task JSON; test was not run. |

## 3. Expanded non-workflow source pins

| Path | Blob SHA | Bounded finding |
|---|---|---|
| `ops/astra_orchestrator.py` | `7e22a283ddbbdfeceeea9aa1bd01c33fdbf7cfb8` | No listed legacy identifiers or manifest-name literals found in this file-local pass. |
| `ops/hybrid_orchestrator.py` | `2f6d68856c0ade836c2f1ec41a8a33ed7a6a7e57` | No listed legacy identifiers or manifest-name literals found in this file-local pass. |
| `ops/qualification/verify_execution_backends.py` | `31a8c1887c9506dc2eb1d4e2587f81fa531ff859` | Hard-coded `mh-dev-01` identity checks. |
| `ops/qualification/produce_distributed_node_attestation.py` | `d2d423325558e877845f848314ceaf583a71fd8e` | Old node IDs, hostnames and user identity are part of attestation policy. |
| `ops/qualification/produce_distributed_verification_evidence.py` | `ee3a1fa1d364da5a6d57a47ab0cfdbd3d0897a6f` | Canonical old node set and old HMAC environment-key names are embedded in evidence generation. |
| `ops/qualification/authorized-schemes.yaml` | `5ae1182511486c2961e28c489ce891b74f1252f1` | Old executor identities are present in the authorization/qualification scheme. |
| `ops/agent-fabric/distributed-local-development-plan.json` | `d49d9d9dbab241fe8878fb63aa8adf3db2134a18` | Repeats old controller/executor identities in plan entries. |
| `ops/agent-fabric/tasks/MH25-QUEUE-001.json` | `123cc2deacd82add2a5a68d21abc2cebbc7f847a` | No listed legacy literal hit in this file-local pass. |
| `ops/agent-fabric/tasks/MH25-QUEUE-002.json` | `c3c6d382377782e7cd74a30cc7c5f23c789347a2` | Contains all three old executor identities and task instructions asserting the legacy pool. |
| `ops/agent-fabric/tasks/MH25-QUEUE-003.json` | `284475465c4142fa4f6830251133135469117706` | Task mission and node target reference `mh-dev-01`. |
| `ops/agent-fabric/tasks/MH25-QUEUE-004.json` | `68a9f0ddf59eaf7c005387833afcc7e2e3de8a0c` | Task mission and node target reference `mh-dev-02`. |
| `control/qualification/canonical-runner-contract.json` | `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26` | Canonical runner contract names `mh-dev-01`. |
| `ops/qualification/provider_model_registry.json` | `62328126fd2cd8879a73bb6812adcacd3e2abe84` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/capture_pre_soak_evidence.py` | `530dc450c81b17ce341db176ba14a17c2a6ad542` | Explicit checks for `mh-dev-01` and `mh-dev-02`. |
| `ops/qualification/produce_runtime_prereq_evidence.py` | `2e86e6321a81e73636747fbb46efd612254f503c` | Names `mh-dev-01` as canonical qualification context. |
| `ops/qualification/render_current_truth.py` | `62a19b62e67c1213e63897531c051ab73db2b967` | Uses `yaml.safe_load` for a governance file; no direct provider-manifest filename literal found. |
| `ops/qualification/qualification_launch_gate.py` | `5abbbbf3e02d0e4a01aa14b7e6d577912e9f9008` | Uses `yaml.safe_load` for a schema file; no direct provider-manifest filename literal found. |
| `ops/qualification/inventory_local_components.py` | `48aab2117c7011a077f1dffd3ad3ab3c761170cd` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/qualify_local_ai_capabilities.py` | `397b9ed8e64321c2ee69441d632b6193247969a4` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/qualify_local_components.py` | `ecb10b8ffd58d5dffcb3e0c712871e3ceb4341d7` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/materialize_g4_evidence.py` | `5e358def026542ed883989a3c5610fa591001457` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/produce_runtime_gate_evidence.py` | `a6bff26b88a6ecd88bca8f957eb8fb14fbc9e3a2` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/qualify_execution_backends.py` | `acf092d5dd9d67ab187f1b67ab691ca730028306` | No listed legacy literal hit in this file-local pass. |
| `ops/qualification/build_g4_115_manifest.py` | `17a74f545092c9183d9f4fc4b4b3594cbaf89dee` | No listed legacy literal hit in this file-local pass. |

Several entries above were already inventoried in WB-14L; this report consolidates source pins and adds core runtime/security-path reconciliation. It is not presented as a count of wholly novel files.

## 4. Search and closure assessment

- Targeted GitHub code-search queries for `node-role-map.yaml`, `local-executor-routing-v2.yaml`, `yaml.safe_load`, `local-executor-routing`, and `createWorkflowDispatch` returned zero results. Repository code search is known to be unindexed; therefore these results are **non-diagnostic**.
- Known-path fetches establish source content at the pinned blobs. They do not enumerate dynamic imports, indirect path construction, generated configuration paths, all external dispatchers, or runtime activation.
- The two manifest readers remain UNKNOWN. The old topology also has a wide cross-cutting footprint in source, test assertions, task definitions, qualification evidence and signing policy.
- These files are legacy implementation evidence only. No old node is accepted as a greenfield target node.

## 5. Disposition

1. Preserve legacy files and security/evidence semantics until caller/reader closure and an explicit owner decision.
2. Do not bulk-delete, rename, disable or rewrite manifests, signers, attestation code, workflows or tests based on literal search.
3. Keep greenfield target inventory and accepted execution routes separate from legacy identifiers.
4. Next bounded step: inspect remaining non-documentation candidates for generic config path resolution, imports and dispatch abstractions. If source-only closure remains impossible, prepare an owner decision packet with precise unresolved questions; do not claim “unused”.

No tests, qualification, workflows, provider/model calls, credentials, host/runtime inspection, installation, infrastructure change, deployment, migration or branch integration occurred.

## 6. Navigation

- [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [WB-14L parent scan](MEDIAHUB-CONTOUR-A-WB-14L-SUPPLEMENTAL-NON-WORKFLOW-LEGACY-REFERENCE-SCAN-2026-10-16.md)
- [WB-14K workflow scan](MEDIAHUB-CONTOUR-A-WB-14K-LEGACY-WORKFLOW-CONTENT-SCAN-2026-10-16.md)
- [WB-14J caller expansion](MEDIAHUB-CONTOUR-A-WB-14J-TARGETED-LEGACY-CALLER-EXPANSION-2026-10-15.md)
