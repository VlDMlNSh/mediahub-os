# MediaHub OS — Partial PASS Evidence Ledger and Portable Deployment Profiles, Wave 01

- Date: 2026-10-14
- Status: DOCUMENTARY RECONCILIATION / PROPOSED TARGET PROFILES / NOT QUALIFIED / NOT ACCEPTED AS NORMATIVE BASELINE
- Related inventory: MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md
- This document does not replace Baseline 2.0, ASTRA queue/qualification contracts, the system passport or unified matrix.

## 1. Correct top-level status

**ASTRA end-to-end autonomous queue completion has not been achieved on the currently observed system.** This is an owner-reported project status. Some individual services or gates have previously returned PASS, but this instruction did not enumerate the exact service IDs and immutable evidence artifacts.

Therefore:
- Preserve valid, attributable PASS evidence at its original scope.
- Do not upgrade the controller, queue, worker pool, distributed dispatch, A3 verification or end-to-end system to PASS.
- Do not erase individual PASS results merely because the overall queue remains incomplete.
- Where an exact artifact cannot be linked, record the assertion as OWNER_REPORTED_PARTIAL_PASS / EVIDENCE_LINK_PENDING, not independently verified PASS.
- Do not synthesize component names, run IDs, SHAs, dates, logs or qualification results.

## 2. Evidence state ledger

| Evidence item | Current state | Basis | What it proves | What it does not prove |
|---|---|---|---|---|
| Individual service/gate PASS reports | OWNER_REPORTED_PARTIAL_PASS / EVIDENCE_LINK_PENDING | Owner statement on 2026-10-14; service IDs/artifacts not enumerated in this pass | Some subcomponents may have passed their own checks | No particular service's current health, fresh qualification or full-system readiness |
| ASTRA full autonomous queue | NOT ACHIEVED (owner-reported) | Owner statement; current inventory still marks queue/authority/qualification not qualified | Overall queue success must not be claimed | Does not invalidate unrelated, attributable subcomponent PASS artifacts |
| Linux Ollama service | OBSERVED_RUNNING; NOT_QUALIFIED | Read-only service/process inspection; version 0.34.4 | Service/process was active at observation time | Model quality/provenance, inference success, API security or routing correctness |
| macOS Ollama | CLI_PRESENT / SERVER_UNAVAILABLE | Read-only CLI check could not connect to daemon | CLI binary exists; server unavailable to CLI at observation time | That Ollama is absent permanently or model tags are absent elsewhere |
| OmniRoute macOS CLI | CLI_PRESENT / ROUTE_NOT_TESTED | Version 3.8.50 observed | CLI is installed | Auth, endpoint, model discovery, request success or egress authorization |
| Astra GitHub Agent | PROCESS_PRESENT / END_TO_END_NOT_QUALIFIED | Process/service/launchd observations on two online nodes | Process exists | Exclusive queue ownership, mission dispatch, lease integrity or A3 evidence |
| GitHub Actions runners | PROCESS_PRESENT / JOB_PASS_NOT_INFERRED | Runner/listener processes observed | Runner process exists | Any particular workflow passed or used the intended source SHA |
| Linux Docker daemon | ACTIVE / NO_RUNNING_CONTAINERS_OBSERVED | Read-only systemctl and docker ps observations | Daemon active; no running containers returned | Absence of host services or containers on other nodes |
| Existing qualification implementation | SOURCE_DECLARED / RUNTIME_RESULT_NOT_INFERRED | Historical commits discuss G4/A3, queue and qualification behavior | Repository contains implementation/history for those gates | Current live queue success or a fresh qualification result |
| Main checkout combined CI status | NO_STATUS_RECORDS_RETURNED | GitHub combined-status query for main HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8 returned an empty status list; commit workflow query returned no PR-triggered runs | These queries provided no positive CI evidence for that SHA | That no other workflow, local run, artifact or gate result exists |

### Required evidence tuple for each retained PASS

Each PASS must link:
- stable component/gate ID and gate-contract revision;
- exact source commit/target SHA;
- run/execution ID and UTC start/end;
- environment/node ID and tool/provider/model version where relevant;
- expected assertion and observed result;
- immutable evidence/artifact URI plus digest;
- secret-suppression/redaction declaration;
- freshness/expiry rule;
- independent verifier and resulting status.

If any required field is absent, keep the result PARTIAL, STALE, UNATTRIBUTED or UNKNOWN as appropriate. Never convert missing evidence into PASS or FAIL.

## 3. Current local host/worktree observations

### Linux mh-dev-02

- Checkout /home/mediahub/astra-work: branch main, HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8.
- ollama, docker, caddy and fail2ban were reported active by the read-only service query.
- sentinelx-cloud-core, astra_github_agent.py, ollama serve and GitHub Runner.Listener processes were observed.
- git worktree list reports three auxiliary entries at /tmp/astra-gold-mh2-3, /tmp/astra-gold-mh2-4 and /tmp/astra-gold-mh2-b28. All are marked prunable because the gitdir file points to a nonexistent location. Their HEADs were 7286cd32f5baff489e7dfda64f64dad5997246bb, 9048fffb2e9cc5bfa73b14780502221a0cc80f56 and b28c21a1523bb8fcb9255cf4289953ae04b349ea. This is stale worktree metadata; no cleanup was performed.

### macOS Voktors-Mini.Dlink

- Checkout /Users/voktor/astra-work: branch main, HEAD 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8.
- launchd labels observed: com.mediahub.astra.github-agent, com.mediahub.df3-llama and com.mediahub.df3-autonomous.
- git worktree list reports six auxiliary entries at /private/tmp/astra-gold-mac-025, /private/tmp/astra-gold-mac-3, /private/tmp/astra-gold-mac-4, /private/tmp/astra-gold-mac-b28, /private/tmp/astra-gold-recovery-20261011 and /private/tmp/astra-nightly-recovery. All are marked prunable because the gitdir file points to a nonexistent location. HEADs: 9e7d018de966a55ea4f3ede7a2a2a6c138418f16, 7286cd32f5baff489e7dfda64f64dad5997246bb, 9048fffb2e9cc5bfa73b14780502221a0cc80f56, b28c21a1523bb8fcb9255cf4289953ae04b349ea, d823043560be92dd04be21e0149e55451207b865 and aa2ea4281343c084d7f50f49a376be6d8a7d31b9.
- No worktree cleanup, branch changes or process restarts were performed. The prunable state should be handled separately after verifying no active worker depends on those paths.

### Offline node

mh-dev-01 remains offline and NOT OBSERVED. No claims about its installed software or readiness are made.

## 4. Portable deployment profiles (PROPOSAL, not a hardware commitment)

These profiles separate control-plane, engineering-worker and high-VRAM inference duties. They are design targets only; do not install or migrate based on this document.

| Target | Proposed responsibility | Workloads to evaluate | Hard constraints / gates |
|---|---|---|---|
| Mac mini 2011, Intel i7, 16 GB RAM, clean Linux | Low-cost always-on control/edge node; health/evidence collector; bounded runner or light worker | ASTRA/Jarvis control services only after supported-runtime/security review; small local models only if measured RAM/CPU performance is acceptable | Verify exact CPU generation/instruction support, Linux kernel/firmware/network drivers, storage health, RAM, thermals, power-loss recovery, supported Python/Node versions, isolation and security maintenance. Do not assume large-model serving is suitable. |
| Mac Pro 2013 | Secondary engineering worker or orchestration/CI node; optional hardware-specific inference experiment | Parallel bounded workers, build/review jobs, local models only after actual GPU/driver/runtime support is verified | Exact CPU/RAM/GPU/VRAM/storage/OS variant unknown. AMD GPU support and accelerator compatibility must be verified for chosen OS. Do not assume CUDA or modern GPU kernels are available. Measure thermal/power stability and sustained workload performance. |
| Future remote GPU server | Dedicated high-VRAM inference service behind an explicit provider boundary; optionally remote worker if separately admitted | Large model inference and memory-heavy workloads with routing, tenancy and quotas | No connection by default. Require approved network boundary, identity/mTLS or equivalent, egress policy, exact model/digest/license, GPU/VRAM/driver/runtime compatibility, data classification, retention policy, quotas/cost controls, audit, health checks and fail-closed routing. |
| Existing Linux mh-dev-02 | Current observation/reference node, not automatically production authority | Evidence capture and source/architecture reconciliation | Process presence is not proof of queue success or qualification. Preserve current state; no changes in this pass. |
| Existing macOS Voktors-Mini.Dlink | Current observation/reference node | CLI/router/launchd metadata and local worker investigation | Ollama daemon unavailable at observation; OmniRoute route untested; DF3 service identity unresolved. |

### Proposed deployment tiers

- Tier 0 — source-only/control design: contracts, inventories, schemas, routing policy and audit model; no provider calls or host mutations.
- Tier 1 — clean Linux edge node: deterministic provisioning recipe and offline/static validation artifacts prepared separately; no installation or qualification implied here.
- Tier 2 — engineering worker pool: workers admitted only with immutable target SHA, isolated worktree, lease, scoped permissions, evidence upload and independent A3 review.
- Tier 3 — remote GPU inference: remote model service admitted only as an explicitly authorized provider, never silent fallback from local-only.
- Tier 4 — system qualification: separately authorized qualification proving queue progression, worker dispatch, lease/claim safety, retries, evidence integrity, A3 verification and final status. Partial PASS values do not substitute for this gate.

## 5. Portable architecture invariants

1. Keep ASTRA engineering queue state separate from MediaHub Product State Authority. Product State Authority remains the only canonical product-state writer.
2. Jarvis submits bounded missions through the documented A0-ASTRA interface; it must not mutate ASTRA internal queue/claim/lease/gate state directly.
3. Each worker receives immutable target SHA, isolated workspace, narrow path/branch capabilities, bounded mission and lease. Stale/prunable worktree metadata must not be treated as a live worker workspace.
4. Route decisions bind task class, data classification, allowed egress, executor, provider, model digest, config/policy revision, budget and fallback decision.
5. local-only fails closed. No silent cloud route through OmniRoute, FreeLLMAPI, Anthropic or another provider.
6. Individual service health, unit-level PASS, gate PASS, A3 verification, queue-wave completion, system qualification, release, deployment and owner acceptance are distinct statuses.
7. Never copy credentials or mutable runtime state between nodes as a deployment shortcut. Use declared secret references and approved provisioning.
8. Every deployment profile is versioned and tied to an explicit architecture revision; hardware discovery is a prerequisite, not a guessed inventory.

## 6. Open decisions / blockers

- Component-level prior PASS artifacts have not yet been mapped to exact IDs and immutable evidence links. Current entry is owner-reported only.
- mh-dev-01 is offline.
- Linux and macOS auxiliary worktree entries are stale/prunable; no cleanup performed.
- FreeLLMAPI local_gateway vs cloud/provider wording conflict remains open.
- UnoRouter, OmniRoute and OpenRouter identities remain distinct until source/config mapping is evidenced.
- Linux Ollama tag provenance anomaly and Alamo-to-Ollama identity remain unresolved.
- Exact Mac Pro 2013 and Mac mini 2011 hardware inventory (model identifiers, CPU/GPU/VRAM/storage, firmware, network, thermals) was not collected in this pass.
- Remote GPU provider hardware, location, security boundary, budget and service contract are unspecified.
- Unified deployment contract and traceability matrix remain PROPOSED / NOT ACCEPTED / NOT FROZEN.

## 7. Next bounded steps

1. Reconcile existing qualification/evidence artifacts from GitHub and record every attributable subcomponent PASS with exact SHA/run/artifact; preserve the overall ASTRA queue as NOT ACHIEVED until a full end-to-end evidence bundle exists.
2. Resolve stale worktree records only after owner-authorized verification of active worker leases and path ownership.
3. Draft the Jarvis Control Plane / GitHub Adapter contract and machine-readable component inventory schema.
4. Prepare target-hardware inventory worksheets for Mac Pro and Mac mini; gather exact hardware identifiers only under explicit read-only host-inspection authorization.
5. Keep install, test, qualification, provider invocation, deployment and infrastructure changes separately authorized and gated.
