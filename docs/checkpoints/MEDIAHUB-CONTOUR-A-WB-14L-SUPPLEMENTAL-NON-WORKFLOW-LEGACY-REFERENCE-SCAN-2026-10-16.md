# MediaHub OS — Contour A WB-14L: Supplemental Non-Workflow Legacy Reference Scan

- Date: 2026-10-16
- Status: **BOUNDED READ-ONLY SOURCE SCAN / NOT COMPLETE REPOSITORY CLOSURE / NO EXECUTION**
- Parent: WB-14K legacy workflow content scan; follows the WB-14I/J tree and caller expansion.
- Functional source ref: `main`; this report and navigation updates are written only to `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

Fetched and scanned 24 non-workflow Python/config/JSON candidates from the complete recursive `main` tree (tree SHA `ab36db009d034db8dca723691e23b331322287e7`, 800 entries, 723 blobs, `truncated=false`). The scan searched literal occurrences of:
- `node-role-map.yaml`
- `local-executor-routing-v2.yaml`
- `astra-distributed-local-worker.yml`
- `astra-chat-control.yml`
- `createWorkflowDispatch`
- `workflow run`
- legacy node/host identifiers
- `run_distributed_local_worker.py`

**No direct literal reference to either provider YAML filename was found in this bounded batch.** This does not establish that the manifests have no readers: indirect path construction, generic YAML loading, dynamic dispatch, unscanned files, and external callers remain possible. The batch did find additional files that encode old node identifiers, including task definitions and qualification contracts.

## 2. Scanned source pins and literal-match results

All listed blob SHAs were fetched from `main` and correspond to entries in the recursive tree. “No listed literal hits” is a file-local result only, not a dependency-absence claim.

| Path | Blob SHA on `main` | Bounded finding |
|---|---|---|
| `ops/qualification/astra_gold_executor.py` | `8d007a95f6cf81173160ad86fad40c77fa3d503d` | No listed literal hits. |
| `ops/qualification/qualification_launch_gate.py` | `5abbbbf3e02d0e4a01aa14b7e6d577912e9f9008` | No listed literal hits. |
| `ops/qualification/qualify_execution_backends.py` | `acf092d5dd9d67ab187f1b67ab691ca730028306` | No listed literal hits. |
| `ops/qualification/build_g4_115_manifest.py` | `17a74f545092c9183d9f4fc4b4b3594cbaf89dee` | No listed literal hits. |
| `ops/qualification/run_g4_round.py` | `22bc31989bc64d4765e9b6f7d0afc87d071f214c` | No listed literal hits. |
| `ops/qualification/run_claude_23wave.py` | `bafb21d53769d74170e9e583c80580f323cd5660` | No listed literal hits. |
| `ops/astra_orchestrator.py` | `7e22a283ddbbdfeceeea9aa1bd01c33fdbf7cfb8` | No listed literal hits in this pass; previously inventoried in WB-14F. |
| `ops/hybrid_orchestrator.py` | `2f6d68856c0ade836c2f1ec41a8a33ed7a6a7e57` | No listed literal hits. |
| `ops/qualification/provider_model_registry.json` | `62328126fd2cd8879a73bb6812adcacd3e2abe84` | No listed literal hits. |
| `ops/agent-fabric/tasks/MH25-QUEUE-001.json` | `123cc2deacd82add2a5a68d21abc2cebbc7f847a` | No listed literal hits. |
| `ops/agent-fabric/tasks/MH25-QUEUE-002.json` | `c3c6d382377782e7cd74a30cc7c5f23c789347a2` | Contains all three old executor identities; legacy task/config data. |
| `.github/agent-system/registry.yaml` | `0317d1e794aa80cd0fa22bd953b95921b26aafd3` | No listed literal hits. |
| `ops/qualification/capture_pre_soak_evidence.py` | `530dc450c81b17ce341db176ba14a17c2a6ad542` | Contains `mh-dev-01` and `mh-dev-02`. |
| `ops/qualification/produce_runtime_gate_evidence.py` | `a6bff26b88a6ecd88bca8f957eb8fb14fbc9e3a2` | No listed literal hits. |
| `ops/qualification/produce_runtime_prereq_evidence.py` | `2e86e6321a81e73636747fbb46efd612254f503c` | Contains `mh-dev-01`. |
| `ops/qualification/render_current_truth.py` | `62a19b62e67c1213e63897531c051ab73db2b967` | No listed literal hits. |
| `ops/qualification/inventory_local_components.py` | `48aab2117c7011a077f1dffd3ad3ab3c761170cd` | No listed literal hits. |
| `ops/qualification/qualify_local_ai_capabilities.py` | `397b9ed8e64321c2ee69441d632b6193247969a4` | No listed literal hits. |
| `ops/qualification/qualify_local_components.py` | `ecb10b8ffd58d5dffcb3e0c712871e3ceb4341d7` | No listed literal hits. |
| `ops/qualification/materialize_g4_evidence.py` | `5e358def026542ed883989a3c5610fa591001457` | No listed literal hits. |
| `ops/qualification/authorized-schemes.yaml` | `5ae1182511486c2961e28c489ce891b74f1252f1` | Contains the three old executor identities. |
| `control/qualification/canonical-runner-contract.json` | `32ec7bbe371b1cfd3f2f46019ee1d2671980aa26` | Contains `mh-dev-01`. |
| `ops/agent-fabric/tasks/MH25-QUEUE-003.json` | `284475465c4142fa4f6830251133135469117706` | Contains repeated `mh-dev-01` references. |
| `ops/agent-fabric/tasks/MH25-QUEUE-004.json` | `68a9f0ddf59eaf7c005387833afcc7e2e3de8a0c` | Contains repeated `mh-dev-02` references. |

## 3. What this proves — and does not prove

**Proven:** legacy identities remain encoded outside workflow YAML, including task JSON, qualification evidence generators, an allow-list/config file, and a runner contract. These are source facts, not proof that any host or workflow is live.

**Not proven:** exact readers of `ops/agent-fabric/providers/node-role-map.yaml` and `local-executor-routing-v2.yaml`; whether generic configuration loaders resolve them dynamically; all callers/dispatchers across the repository; runtime activation; safe retirement.

The GitHub code-search index remains unavailable for this repository. This scan used known-path fetches from a complete tree and local literal inspection of the fetched content; it was not a checkout-wide semantic/data-flow search. Some paths were already inventoried in earlier reports, so this is a supplemental batch rather than a claim of 24 wholly novel dependencies.

## 4. Disposition and next step

- Do not delete, rename, rewrite or disable any legacy source/config based on this scan.
- Keep the new greenfield target topology separate; do not promote old executor IDs to target nodes.
- Continue a SHA-pinned scan of remaining non-documentation code/config/test paths and inspect generic YAML/config-loading abstractions for possible dynamic reads. Record exact coverage and omissions.
- If the manifest-reader closure cannot be established from source-only evidence, report the residual uncertainty explicitly and prepare an owner-decision packet; do not infer “unused” from a negative literal scan.
- No tests, workflows, model/provider calls, credentials, host/runtime inspection, installation, infrastructure change, deployment or branch integration were performed.

## 5. Navigation

- [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [WB-14K legacy workflow scan](MEDIAHUB-CONTOUR-A-WB-14K-LEGACY-WORKFLOW-CONTENT-SCAN-2026-10-16.md)
- [WB-14J targeted caller expansion](MEDIAHUB-CONTOUR-A-WB-14J-TARGETED-LEGACY-CALLER-EXPANSION-2026-10-15.md)
- [WB-14I repository tree and caller expansion](MEDIAHUB-CONTOUR-A-WB-14I-REPOSITORY-TREE-AND-LEGACY-WORKFLOW-CALLER-EXPANSION-2026-10-15.md)
