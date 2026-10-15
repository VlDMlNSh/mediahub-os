# MediaHub OS — Contour A WB-14J: Targeted Legacy Caller Expansion

- Date: 2026-10-15
- Status: **READ-ONLY TARGETED SOURCE TRACE / NOT A COMPLETE REPOSITORY SCAN / NO EXECUTION**
- Parent: WB-14I Repository Tree and Legacy Workflow Caller Expansion.
- Functional source ref: `main`; report and navigation updates only on `docs/mediahub-chat-tree-map-20261012`.

## 1. Result

This bounded pass fetched and inspected SHA-pinned source files across the legacy worker workflows, supervisor/reaper/result-publication chain, ASTRA queue, worker script, command signer, node attestation/evidence code, role map and routing manifest, plus the topology consistency test. It adds several explicit workflow lifecycle edges and confirms that the existing queue is a direct dispatcher for the old distributed worker workflow.

This is **not** a complete scan of all 301 non-documentation code/config candidates identified in the recursive tree. No negative claim about unscanned files is made. The exact code readers of `node-role-map.yaml` and `local-executor-routing-v2.yaml` remain unknown.

## 2. Source inventory and evidence pins

All entries below were fetched from `main`; the recorded content blob SHA matched the Git tree entry SHA.

| Path | Blob SHA | Finding |
|---|---|---|
| `ops/agent-fabric/providers/node-role-map.yaml` | `6fab2a8513ad32ed5bb15be819ad74cc2365214b` | Declares old controller `mh-dev-01` and the old node/pool mapping. Reader not proven. |
| `ops/agent-fabric/providers/local-executor-routing-v2.yaml` | `af3d96fe91055af6ba79eded9c800d28d8c0c5c9` | Declares old node/controller `mh-dev-01`; reader not proven. |
| `runtime/mediahub_runtime/agent_fabric.py` | `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd` | No direct reference to either YAML filename or the old node IDs in this file. This is only a file-local negative finding. |
| `runtime/mediahub_runtime/autonomous_queue.py` | `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1` | Defines permanent old executor pool; lines 307–316 dispatch the distributed worker workflow and lines 325–328 poll that workflow. Direct caller/dispatcher confirmed. |
| `ops/qualification/run_distributed_local_worker.py` | `42b2d53361bbd26d7fcaed82dfd710d4f09c4e6d` | Hard-coded per-node users, platforms, models, pools and environment-file paths. |
| `ops/control/sign_command.py` | `fc6943a79cefdf06e59d6e32771d2df551b2f0e9` | Security-sensitive command signing and node-bound command validation. Do not retire with topology files absent authority/dependency review. |
| `astra_github_agent.py` | `dd2f373bf5f3d69dec951c84e3d53b0e9befab0c` | Defines old-node HMAC environment-key mapping and required-node set. Security-sensitive control logic. |
| `ops/agent-fabric/distributed-local-development-plan.json` | `d49d9d9dbab241fe8878fb63aa8adf3db2134a18` | Repeats old controller/node IDs across plan entries. |
| `ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json` | `b948f0beb510f24399d82aaefcb7f95584e99cab` | No searched legacy identifiers or target manifest filenames in this file-local pass. Not evidence of broader independence. |
| `ops/qualification/produce_distributed_node_attestation.py` | `d2d423325558e877845f848314ceaf583a71fd8e` | Hard-coded old hostnames and user identity for node attestation. |
| `ops/qualification/produce_distributed_verification_evidence.py` | `ee3a1fa1d364da5a6d57a47ab0cfdbd3d0897a6f` | Canonical old node IDs and HMAC environment-key names are embedded in evidence generation. |
| `tests/test_astra_topology_consistency.py` | `cc5410f631a161b3e3bfb4bae198340f905da6e4` | Test asserts the three-node permanent executor pool. Test was read only, not run. |
| `.github/workflows/astra-autonomous-supervisor.yml` | `a0209a2d01122354d19e95d2f362a6ecfa3d6186` | Uses `mh-dev-01`, invokes `ops/control/sign_command.py`, writes/validates old command/result paths; workflow dispatch is present. |
| `.github/workflows/astra-stale-supervisor-run-reaper.yml` | `c15df23b85c7b943593383038805d301007db771` | Tracks/cancels both supervisor and distributed-worker workflows; direct lifecycle dependency. |
| `.github/workflows/astra-distributed-verification.yml` | `648f56badd2b919b822b4fe4b61f285cca99ed93` | `workflow_call` entry point and per-old-node attestation jobs. |
| `.github/workflows/astra-queue-recovery.yml` | `5d9e0db244429ba44a433f69cf2ff816df0f9824` | Recovery job binds to runner label `mh-dev-01-canonical`. |
| `.github/workflows/astra-node-result-publication.yml` | `087a373fe113d11a81be4d349e4c3d330a22f33c` | Triggered by `workflow_run`; derives old command/node IDs and publishes `control/results/mh-dev-01.json` to `astra-node/mh-dev-01`. |

## 3. Updated direct dependency graph

1. `runtime/mediahub_runtime/autonomous_queue.py` → `gh workflow run .github/workflows/astra-distributed-local-worker.yml` → old node-bound self-hosted jobs → `ops/qualification/run_distributed_local_worker.py`.
2. Queue polls runs for `astra-distributed-local-worker.yml`; `astra-stale-supervisor-run-reaper.yml` separately handles/cancels old supervisor and worker runs.
3. `astra-chat-control.yml` `/astra run-gold` → `astra-autonomous-supervisor.yml`; supervisor calls `ops/control/sign_command.py` and reads/writes old command/result paths.
4. Supervisor/worker workflow paths feed legacy qualification, attestation and result-publication workflows; `astra-distributed-verification.yml` is reusable via `workflow_call`, and `astra-node-result-publication.yml` is triggered by `workflow_run`.
5. `node-role-map.yaml` and `local-executor-routing-v2.yaml` → **reader still not proven** by the files inspected.

These are static source edges. They do not establish whether any workflow or runner is enabled or currently active.

## 4. Coverage and limitations

- The recursive `main` Git tree previously fetched at SHA `ab36db009d034db8dca723691e23b331322287e7` reports 800 entries, 723 blobs and `truncated=false`.
- Extension/path filtering identifies 301 non-documentation code/config candidates; this pass inspected a bounded subset, not all 301.
- Repository code-search indexing is explicitly unavailable (`is_code_search_indexed=false`), so search endpoint zero-results remain non-diagnostic.
- The manifest-reader closure, all external dispatchers, full history references, and all callers of the signer and worker script remain open.
- No test, qualification, workflow dispatch, model/provider call, credential use, host/runtime inspection, install, deployment or infrastructure change occurred.

## 5. Disposition and next step

Keep all legacy topology files, workflows and security-sensitive components unchanged. Next, continue a deterministic content scan of the remaining tree candidates in small, SHA-pinned batches, prioritizing `.github/workflows`, Python modules, tests and configuration readers. Record each scanned path, source SHA, positive matches and explicit omissions. Do not treat unscanned files as clean and do not propose deletion until reader/caller closure and owner decision are complete.

## 6. Navigation

- [Project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [WB-14I parent trace](MEDIAHUB-CONTOUR-A-WB-14I-REPOSITORY-TREE-AND-LEGACY-WORKFLOW-CALLER-EXPANSION-2026-10-15.md)
- [WB-14G workflow entry-point trace](MEDIAHUB-CONTOUR-A-WB-14G-REVERSE-REFERENCE-WORKFLOW-ENTRY-TRACE-2026-10-15.md)
