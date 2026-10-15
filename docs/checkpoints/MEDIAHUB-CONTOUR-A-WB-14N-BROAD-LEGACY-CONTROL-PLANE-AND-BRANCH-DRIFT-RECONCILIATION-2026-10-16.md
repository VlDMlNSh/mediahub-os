# MediaHub OS — Contour A WB-14N: Broad legacy control-plane scan and branch-drift reconciliation

- Date: 2026-10-16
- Status: **BOUNDED, SOURCE-PINNED READ-ONLY AUDIT / NOT COMPLETE REPOSITORY CLOSURE / NO EXECUTION**
- Parent: WB-14M Broad Legacy Control and Config-Loader Scan.
- Source ref: main; this report is written only to the documentation ref.
- Project tree: main HEAD/tree SHA ab36db009d034db8dca723691e23b331322287e7, 800 entries / 723 blobs, truncated=false.
- Documentation ref HEAD observed before this pass: 5ee55d125b027959bf6e31c3e113c7b2c1f262e0. Live comparison to main: DIVERGED, 1,466 commits ahead / 4 behind, merge base f0f406feb9f9816b009f4e6e756813541e53b9bc. No integration attempted.

## 1. Executive result

This continuation individually fetched and inspected 98 unique source files from main, spanning runtime modules, workflows, systemd/service configuration, profiles/registries, command and runner contracts, qualification utilities, task manifests, mesh/federation helpers, tools, and tests. Each source is pinned in the inventory below.

The broad pass found three material points:

1. **Old-host assumptions remain across multiple execution and trust boundaries**, not just in the old queue: fixed executor identities appear in backend definitions, agent registries, signed-command configuration, attestation/evidence production, task manifests, runner contracts, workflows and test assertions.
2. **A high-risk legacy storage-migration workflow remains present on main.** Its static source is configured to trigger on pushes to main that change the workflow path, requests contents:write, checks the old mh-dev-01/mediahub-runner identity, manipulates old storage paths, contains an rm -rf of a backup path, removes its own workflow file, commits, and pushes to main. Whether GitHub Actions currently has this workflow enabled or whether it has executed was not checked. This report does not dispatch or run it.
3. **The documentation ref and main disagree about two old operational artifacts.** The workflow .github/workflows/mediahub-one-time-storage-migration.yml and service ops/systemd/mediahub-astra-github-bootstrap.service are present on main but return 404 on the documentation ref. Live branch comparison also classifies them as removed on the documentation ref. This is branch drift, not evidence of an accepted or integrated retirement.

Exact readers of ops/agent-fabric/providers/node-role-map.yaml and ops/agent-fabric/providers/local-executor-routing-v2.yaml remain UNKNOWN. Repository code-search indexing is unavailable; zero-result search queries remain non-diagnostic. No implementation or configuration changes were made.

## 2. High-priority findings

### WB14N-F01 — self-triggering legacy storage migration with destructive side effects

Source: .github/workflows/mediahub-one-time-storage-migration.yml  
Blob SHA on main: b0f71f515419067c6b1508dc073b2dbce4f2ca7b

Static source inspection established:

- Trigger: push on main with a path filter targeting this workflow file itself.
- Permission: contents: write.
- Runner/identity gates: self-hosted Linux x64 runner label mediahub-control; hostname must be mh-dev-01; user must be mediahub-runner.
- Legacy filesystem references: /home/mediahub/local-ai, /srv/mediahub/data/local-ai and /home/mediahub/local-ai.root-backup.
- Destructive operation: as_mediahub rm -rf "$BACKUP" after its own in-workflow verification steps.
- Repository mutation: stages a migration-result marker and the workflow, removes the workflow with git rm, commits and pushes to main.

Risk interpretation: **HIGH-RISK LEGACY OPERATIONAL ARTIFACT / EXECUTION STATUS UNKNOWN**. The YAML source alone does not establish that the workflow is enabled or has run. Do not test, dispatch, edit on main, delete, or merge a change that could activate it without a separately authorized and reviewed disposition plan.

### WB14N-F02 — legacy systemd bootstrap unit

Source: ops/systemd/mediahub-astra-github-bootstrap.service  
Blob SHA on main: bb88eb20bd2127c9c70a223bc07025ee9c150916

The unit defines an auto-start service with Restart=on-failure and WantedBy=multi-user.target. It sets ASTRA_NODE_ID=mh-dev-02, points ASTRA_WORKTREE at /home/mediahub/astra-work, sets state under /var/lib/mediahub-astra, and its ExecStart path may clone the repository's main branch into the old worktree before launching ops/astra-github-bootstrap.sh.

Risk interpretation: **LEGACY-OPERATIONAL**. This is source evidence of an old-host bootstrap definition, not evidence the unit is installed, enabled or running on any machine. The same path is absent from the documentation ref. No host was inspected.

### WB14N-F03 — manually dispatchable legacy runner migration smoke

Source: .github/workflows/mediahub-runner-migration-smoke.yml  
Blob SHA on main: 1f6682584d51b8155e66959734d1f335802dde67

This workflow has workflow_dispatch, binds to the old mediahub-control runner, checks hostname mh-dev-01 and a fixed historical commit SHA, and then invokes a test command. It is not run in this pass. Treat as **LEGACY-OPERATIONAL / NOT TARGET QUALIFICATION**.

### WB14N-F04 — other old runner/workflow bindings

- .github/workflows/mediahub-bridge.yml — 6f482199af32881f42c2c418221aec66530c4b71 — workflow_dispatch and runner label mh-dev-01-canonical.
- .github/workflows/mh25-three-claude-23wave.yml — 3a7327135ea73c7a886c1c8b6dbbf7080aff421c — old Linux and Mac node names, host assertions and old local-model lane definitions.
- .github/workflows/mediahub-agent-fabric-verify.yml — 2cec0ba1f02018f7037417363c707a13bc673117 — no listed literal legacy match in this file-local scan.
- .github/workflows/mediahub-claude-worker.yml — e1260cfef88ac02bcc9d0cce67bb497820f5f63c — no listed literal legacy match in this file-local scan.
- .github/workflows/astra-verify.yml — ae59d954f1ca6569a8d047589a2a54fd03e47f5b — no listed literal legacy match in this file-local scan.
- .github/workflows/astra-cloud.yml — 3cad60423311cead1ce6d1cf8eb224cb7a296844 — no listed literal legacy match in this file-local scan.

A file-local absence of listed strings is not a full caller-closure finding.

## 3. Other material source findings

### Runtime and registry layer

- runtime/mediahub_runtime/execution_backends.py (dd552e9e80623c59d164c77e29620c4256463cd7) hard-codes mh-dev-01 in backend construction.
- profiles/agent-registry.json (993cbbe1b2b2a88da7d8884a897b404f055981a8) contains multiple mh-dev-01 entries.
- profiles/providers/astra-gold-hybrid-agent-fabric.yaml (acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181) had no listed literal host/manifest match in this pass.
- Several other runtime modules did not contain the searched legacy strings or manifest literals. Relevant examples and their source SHAs appear in the inventory. These bounded negative results do not prove they can be removed or that no dynamic consumer exists.

### Command, runner, qualification and task contracts

- control/commands/Voktors-Mini.Dlink.json (df6649e8b419e6e683f8c77ef78961b3f98ac13c), control/commands/mh-dev-01.json (f748520b60d2a7066f1b1331ddede574eef5007d) and control/commands/mh-dev-02.json (d310f5cb1fbeb91b23d2f2639ffa9c61bbf29478) are bound to old node IDs.
- control/qualification/distributed-runner-contract.json (993f51f07c7937165ffb3bfbe59cd0801ea71ec0) and control/qualification/canonical-runner-contract.json (32ec7bbe371b1cfd3f2f46019ee1d2671980aa26) encode old runner identities and hostnames.
- ops/agent-fabric/tasks/MH25-QUEUE-002.json, MH25-QUEUE-003.json, MH25-QUEUE-004.json and MH-25-23-lane-manifest.json contain old executor IDs and/or old topology instructions.
- ops/qualification/produce_distributed_node_attestation.py, produce_distributed_verification_evidence.py, capture_pre_soak_evidence.py and produce_runtime_prereq_evidence.py encode old node checks or identities. The related tests contain the same identities and HMAC-key mapping assumptions.
- tests/test_astra_topology_consistency.py, tests/test_astra_canonical_queue_policy.py, tests/test_autonomous_queue.py, tests/test_distributed_local_worker.py, tests/test_distributed_node_attestation.py, tests/test_distributed_verification.py, tests/test_distributed_workflow_contract.py and tests/test_execution_backends.py assert legacy assumptions or use legacy fixtures.

These observations show that a future controlled retirement would need an explicit plan for linked runtime code, security/evidence semantics, contracts, profiles, tasks and tests. They do not authorize deleting shared components or updating normative authority contracts.

### Generic YAML/load paths

Bounded source checks found yaml.safe_load or a generic YAML helper in qualification/governance utilities, including ops/qualification/render_current_truth.py, qualification_launch_gate.py and verify_astra_gold_governance.py. In the inspected contexts, no literal use of either target provider-manifest filename was established. Generic loaders may resolve paths dynamically; exact manifest readers therefore remain UNKNOWN.

### Search surface

Targeted GitHub code-search queries return zero matches while repository code search is unindexed. These results are not evidence of absence. This pass relied on known-path fetches, source blob pins and file-local string inspection. No parser-based data-flow analysis, complete import graph, full file-content scan of all 800 tree entries, external dispatcher inventory, GitHub Actions enabled-state check, or runtime liveness check was performed.

## 4. Main versus documentation-ref reconciliation

Live refs observed before documentation writes:

- main ref / tree HEAD: ab36db009d034db8dca723691e23b331322287e7.
- docs/mediahub-chat-tree-map-20261012 HEAD: 5ee55d125b027959bf6e31c3e113c7b2c1f262e0.
- compare main...docs ref: DIVERGED; ahead_by=1466, behind_by=4; merge base f0f406feb9f9816b009f4e6e756813541e53b9bc.

The two paths highlighted in F01/F02 exist on main and are absent from the docs ref. No merge, rebase, cherry-pick, ref movement or source change was made. A broad, divergent documentation-ref history must not be integrated as a side effect of this audit.

This creates an actionable governance discrepancy: main retains source artifacts that the documentation ref no longer contains, while exact dependency closure and safe disposition are unresolved. The owner’s clean-slate direction determines they are not new-target requirements; it does not, by itself, prove the removal commit is ready to integrate or that all shared semantics are replaceable.

## 5. Disposition recommendation (not an execution)

| Area | Source-grounded class | Recommended next treatment |
|---|---|---|
| One-time storage migration workflow | LEGACY-OPERATIONAL / HIGH-RISK | Hold execution and main edits pending explicit controlled disposition; never invoke as part of greenfield setup. |
| Old systemd bootstrap and runner migration smoke | LEGACY-OPERATIONAL | Exclude from target plan; prepare a path-level retirement proposal with reference and trigger checks. |
| Old bridge and three-node workflows | LEGACY-OPERATIONAL unless source review finds shared semantics | Continue inbound-reference/dispatch review before any removal. |
| Queue, signer, HMAC mappings, attestation/evidence logic, registry and backend code | SHARED-OR-UNKNOWN | Preserve pending per-file dependency closure and security-contract replacement mapping. |
| Old task fixtures, runner contracts and topology tests | LEGACY-OPERATIONAL or SHARED-OR-UNKNOWN by file | Do not treat as target acceptance evidence; revise only under an approved coordinated refactor. |
| Old node/host identifiers | HISTORY or LEGACY-OPERATIONAL depending on artifact role | Never promote to target inventory. Preserve audit provenance where needed. |
| New hardware, new routing, model/backend selection | UNKNOWN until owner/evidence | Keep out of qualified topology claims until supplied/accepted and then separately qualified. |

## 6. Safety and verification record

- Source-only review; no source code or runtime configuration changed.
- No tests, qualification, workflow dispatch, model/provider call, credentials, host/runtime access, installation, infrastructure modification, deployment, migration, branch merge/rebase/cherry-pick, or deletion occurred.
- The workflow and service findings describe checked-in source only. They do not prove those jobs or services are enabled or live.
- Exact manifest readers, dynamic loader references, all external callers and complete repository closure remain unresolved.

## 7. Complete source-pin inventory for this pass

All paths below were fetched from main. SHA values are content blob SHAs. The per-file scan used relevant subsets of literal queries including both provider manifest names, manifest stems, yaml.safe_load/safe_load/yaml.load, dynamic imports, workflow dispatch/call strings, worker/signer paths, old node/host IDs, HMAC environment-key names, providers paths and selected old filesystem/destructive-operation markers. This inventory does not imply every query was semantically exhaustive for every file.

### Runtime modules

- runtime/mediahub_runtime/__init__.py — 4ff499f8e489e60e344283ee01e4dad5e72a2646
- runtime/mediahub_runtime/astra_gateway.py — 10985e4ad8f682313d08e7492ecc1856a8bce20f
- runtime/mediahub_runtime/astra_lifecycle.py — 703dd1df043a29d187c7ed34c3b519a9f36ed93e
- runtime/mediahub_runtime/astra_context.py — 9a30c0a3299e6b3a47bc03f55f4d26d2d9f14ad9
- runtime/mediahub_runtime/astra_conversation.py — 1182bd774af2d7000061c9ac1cc7c013670b3938
- runtime/mediahub_runtime/astra_developer_context.py — d1806e5e91e16cb27d34d9331b9a25e25d606a46
- runtime/mediahub_runtime/astra_security.py — ff4ba9b581cf30e0f2d6bbed70c5290d93bfa27d
- runtime/mediahub_runtime/authorization.py — 4d8df5d3c1c26f7f133a8093cd270635b085f4d5
- runtime/mediahub_runtime/autonomous_task.py — f2287c962cfc1eac16cf8480dc359def1ce516fa
- runtime/mediahub_runtime/cloud_orchestrator.py — 24c28197df7baca49abd81956752a7a5092506d9
- runtime/mediahub_runtime/execution_adapter.py — f40f8092b63966434f619396b0e8091ceef91a97
- runtime/mediahub_runtime/execution_backends.py — dd552e9e80623c59d164c77e29620c4256463cd7
- runtime/mediahub_runtime/task_ingress.py — 59e1254aa61cc8f55f53bd1e179631e81c441393
- runtime/mediahub_runtime/worker_router.py — 00ce4d3e96d327baa38de9644e7bff20a79040ed
- runtime/mediahub_runtime/lifecycle_service.py — 0b9d3d888e988615f1ad8cd50b1bef22f2be011b
- runtime/mediahub_runtime/coordination_service.py — a4b81f2cfb21980af952aff26fb6e31d33b79bf7
- runtime/mediahub_runtime/mission_journal.py — 518577c35e0bc00aed9be4c8f5b6594de66b5700
- runtime/mediahub_runtime/development_intelligence.py — 1d803ead46e71674dd585bbe3363528493d9d91f
- runtime/mediahub_runtime/local_providers.py — 8361b7d6782adaa9dcd4e47b5d9e9940d41bb1a3
- runtime/mediahub_runtime/lifecycle.py — b20b42a5ad79512575676a97699db2161e459516
- runtime/mediahub_runtime/in_memory_state.py — 0fbc71369d19e09944ba67a60ccb9df802f30a4b
- runtime/mediahub_runtime/diagnostics.py — 8d5da6b778cc2f2bf338dd7577a74724494def9a
- runtime/mediahub_runtime/connectors/tinyfish.py — 0288158c74457b5ed5379dda86d95c6048cec3a2
- runtime/mediahub_runtime/generation.py — 4e4fe0e40d67c18c918881d79dc2cc9933988b2c

### Workflows and bootstrap/service definitions

- .github/workflows/mediahub-agent-fabric-verify.yml — 2cec0ba1f02018f7037417363c707a13bc673117
- .github/workflows/mediahub-bridge.yml — 6f482199af32881f42c2c418221aec66530c4b71
- .github/workflows/mediahub-claude-worker.yml — e1260cfef88ac02bcc9d0cce67bb497820f5f63c
- .github/workflows/mediahub-runner-migration-smoke.yml — 1f6682584d51b8155e66959734d1f335802dde67
- .github/workflows/mediahub-one-time-storage-migration.yml — b0f71f515419067c6b1508dc073b2dbce4f2ca7b
- .github/workflows/astra-verify.yml — ae59d954f1ca6569a8d047589a2a54fd03e47f5b
- .github/workflows/astra-cloud.yml — 3cad60423311cead1ce6d1cf8eb224cb7a296844
- .github/workflows/mh25-three-claude-23wave.yml — 3a7327135ea73c7a886c1c8b6dbbf7080aff421c
- ops/astra-github-bootstrap.sh — 5f36f35ea85f55e5f49af6d3dabb5e876fffa09b
- ops/systemd/mediahub-astra-github-bootstrap.service — bb88eb20bd2127c9c70a223bc07025ee9c150916
- ops/node/mh-dev-02-mesh-check.sh — e588f8d07922ebfe1ad1322d2702c08b2b7eb702

### Contracts, manifests, profiles and control files

- control/commands/Voktors-Mini.Dlink.json — df6649e8b419e6e683f8c77ef78961b3f98ac13c
- control/commands/mh-dev-01.json — f748520b60d2a7066f1b1331ddede574eef5007d
- control/commands/mh-dev-02.json — d310f5cb1fbeb91b23d2f2639ffa9c61bbf29478
- control/qualification/distributed-runner-contract.json — 993f51f07c7937165ffb3bfbe59cd0801ea71ec0
- control/qualification/g4-115.json — d4ae8e7cc341706c2a1dd5265726ef1e045f93d1
- ops/agent-fabric/manifest/mediahub-23-lane-execution-manifest.json — b948f0beb510f24399d82aaefcb7f95584e99cab
- ops/agent-fabric/tasks/MH-25-23-lane-manifest.json — f2746a91b8a7577fc4b74c5ae9e4f4c813b7d00b
- ops/qualification/astra-memory-queue.json — 6e1d71f2db594a72c5ec38e9c6bd7aed8c05298f
- profiles/agent-registry.json — 993cbbe1b2b2a88da7d8884a897b404f055981a8
- profiles/providers/astra-gold-hybrid-agent-fabric.yaml — acf3ad43e68bf49ffa5a1d2c89f64bd363c0e181

### Tools, mesh and federation modules

- tools/build_foundation.py — fe3205d2cab9f9edc59d0e0007025c5acc56ce0d
- tools/sign_astra_command.py — a4222ac51a47cbfe8288f9af34f1e542c0a4b6a8
- tools/validate_contracts.py — 61862cfc763e9bf239af8b19242bc11a21f08d70
- ops/mesh/admission.py — 46e92d3c4f9b9865356443403e9ebd34587996cd
- ops/mesh/heartbeat_auth.py — 6cb4adfb616389867c1e6f2490c256e76d0f95a5
- ops/mesh/registry.py — 7d87ae0faf93f55ebbee1c3140b0a1b9cc20a01a
- ops/mesh/verify_mesh.py — f39de55e482ad989fa87abd44de94080be524363
- ops/mesh/inventory.py — b07e84cb6a5144d90e0a01c79e51239d401b8d57
- ops/mesh/state.py — d02780894cfb5d3c0fc7878d57a08fac2e428efc
- ops/federation/cluster_trust_poc.py — bda8b7a6bc131a0f09ef6ec7ac8b36a1713ded56
- ops/federation/compute_contribution_poc.py — 20e9b58f9475032294511b6c1fb7854225f74300
- ops/federation/cprg_security_poc.py — 423e5c6793f41c5fe646d3acc7427c0bbea5e835
- ops/federation/federation_admission_poc.py — aa39036e0613630dc8649db94626ee6753982d19
- ops/federation/privacy_data_boundary_poc.py — d8df71c07c3f81a80ef29ac06966c639e97f6411
- ops/qualification/hybrid_agent_auth_probe.py — 1fb0cb41d219eaf26dc830c8585a790c89a5cb50
- ops/qualification/verify_astra_gold_governance.py — 3de899de0f4712ac206850e2b98ca86f9ab5caae
- ops/qualification/verify_astra_memory_contract.py — 8e1baefc52051ec76e5adc08498f99ed4c4131de
- ops/qualification/verify_astra_memory_gold.py — be29b23ce0ace9c3a759eb1ae1f9fd65a23f17b6
- ops/qualification/verify_astra_memory_soak.py — 7e1cf4738aa00ffadd0507a67fdb1dc631f37a1e
- ops/qualification/verify_dual_local_23wave.py — fcfce9b3d7d1a1d0a1147a9e8f8f61462a92130d
- ops/qualification/verify_g4_115.py — e0e20a9c0685575ce720a004aaa90c56ff27d563

### Tests

- tests/test_agent_fabric.py — ed64595a6e396fc4d58c08b47bf708cd92b1275b
- tests/test_astra_canonical_queue_policy.py — 99e6f556bbd2c566ae3a818b7b1bb780f1c41a30
- tests/test_astra_command_auth.py — 8df49fc55e660c13ad54aca9b9dc78132c335dd1
- tests/test_astra_controller_reconciliation.py — b4553cbc779d2b55c9d8c6576a6f10b8c31b9d06
- tests/test_astra_github_agent_contract.py — 7dc0b70c9b5c3e0ef664749d5527b71740cb1656
- tests/test_astra_gold_architecture_drift.py — d6a0e6a6d81dc6e15e343cd80ee950431b1e3b14
- tests/test_astra_gold_evidence_contracts.py — 2387273506a72ef92483a36d5cf0cd79497b7bba
- tests/test_astra_gold_governance_contract.py — 2b3a530106330ff88a16d296df0272154ecc2052
- tests/test_autonomous_queue.py — 6e33bb83ecd5235284be30a456631856d08938a0
- tests/test_autonomous_queue_contract.py — e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7
- tests/test_canonical_runner_contract.py — 684c2fa2aceda89dc2e0b3d21416595b3c36d2bc
- tests/test_distributed_local_worker.py — 5fd79a665ef49e4e594a8fbccb8d77ec1f0659ae
- tests/test_distributed_node_attestation.py — ac0eaa3a353aa0d8d7c2b9ec000f5b29e69ca74e
- tests/test_distributed_verification.py — 7b212e3ffd3411f6b91de6fb4070ec10f01a7b29
- tests/test_distributed_workflow_contract.py — 267f3d700f5c7728ee18a9363ca5b8f8dfed0ac9
- tests/test_execution_backends.py — f4744496ad6fc4eefe611544d255641e8cbaecbb
- tests/test_gold_unified_workflow_contract.py — ca978a58c65689581c6f53f75ce838e93c9c6182
- tests/test_stale_supervisor_run_reaper.py — 7d146eedaec5a1d3b326161e399518eeda28aa88
- tests/test_verify_execution_backends.py — b7da35a782e2f4c0b9fd1392bb3cc22255a904ba
- tests/test_astra_gold_qualification_launch_schema.py — 090ce2ecb02e58a3c48a7a729279dea9a387f339
- tests/qualification/test_astra_delegate_contracts.py — cb0032d0eb15240c17e6a4c8707886a0f44d4d9c
- tests/qualification/test_astra_gold_security_telemetry_contract.py — c51f8fe2f8fd81f19a61ca0f9f43fd5a16559eaf
- tests/qualification/test_gateway_identity_contract.py — 2ee67bb47b079542483fe9ab1f4c1323983e5571
- tests/test_repo_hygiene.py — b6a63707a4605ab3eaaa10c4094a31266763329b
- tests/test_astra_github_auth_fallback.py — abcc1ae9e861cf6a672dba1da3e6725182176326
- tests/test_autonomous_gold_mission.py — d2707db95efff17bdaacdeaae0eb9f8e489516bc
- tests/test_astra_gold_registry.py — 9a6727c74b675412e60e8e944f4a9f777bfc4192
- tests/test_astra_gold_soak_pin.py — 3436a8fce3eedb34cfc58e5a16a0ef58a9e9ad0d
- tests/test_provider_qualification_classification.py — 6ce80170180a8741f83109c04d1484f289753114
- tests/test_pre_soak_evidence_contract.py — 53e5f621b135ecd713d55683defcae8db23e2395
- tests/test_runtime_prereq_evidence.py — dc4914f9e6031425f4f7db2dbd1d612d1aa93ba3
- tests/test_repo_secret_hygiene.py — 21991478bac150146b73beffea7a10a4375e52d4

## 8. Navigation

- Project map: ../architecture/MEDIAHUB-CHAT-TREE-MAP.md
- WB-14M parent report: MEDIAHUB-CONTOUR-A-WB-14M-BROAD-LEGACY-CONTROL-AND-CONFIG-LOADER-SCAN-2026-10-16.md
- Greenfield/legacy classification baseline: ../architecture/MEDIAHUB-GREENFIELD-LEGACY-ARTIFACT-LEDGER-WAVE-01-2026-10-15.md
