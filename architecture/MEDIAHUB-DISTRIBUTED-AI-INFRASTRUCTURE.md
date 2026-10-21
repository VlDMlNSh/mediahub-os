# MediaHub OS — Distributed AI Infrastructure and Model Routing Architecture

- **Date:** 2026-10-12
- **Status:** ACCEPTED TARGET ARCHITECTURE — NOT YET RUNTIME-QUALIFIED
- **Scope:** target pair of a newly purchased Mac Pro and a Linux Mac mini Mid-2011 development host, the separate Mac mini M2 MediaHub prototype, future GPU/video server, FCC/FreeLLMAPI/local model service, optional user-contributed compute, mobile/client surfaces, and registration-only VPS.
- **Authority:** This document records the user's accepted target design. It does not claim that any component is deployed, compatible, or qualified.

## 0.1. Deployment phases and hardware authority

This architecture is being designed and tested before the target computer is purchased. Existing connected Linux hosts and the M2 are a temporary test laboratory; their present topology is not the final deployment map.

**Target deployment near the end of October 2026:**
- **Purchased Mac Pro:** primary target system for MediaHub and developer host #1. After acquisition, record exact generation/model, CPU/GPU, RAM, storage, OS, network interfaces and power/thermal constraints before setting model sizes, service concurrency or production limits.
- **Mac mini Mid-2011 running Linux, planned 16 GB RAM:** developer host #2 and Linux compatibility/executor node. The user plans 16 GB; Apple’s factory specifications list options up to 8 GB, while OWC independently tested 16 GB (2×8 GB) upgrades for Mid-2011 models. Verify the exact machine’s RAM detection, stability, SSD health, Linux firmware and wired network after acquisition. Do not assume it is a GPU inference server.
- **Voktors’ Mac mini M2, 8 GB:** first working MediaHub product prototype / staging and acceptance-test device. It may help with temporary tests during development, but it must not remain a permanent ASTRA developer lane in the final topology.
- **Future GPU/video server:** later optional compute pool for large model inference and media/video processing. It is not a prerequisite for a safe first release and does not become a developer lane or State Authority by default.
- **MacBook and mobile application:** optional client/approval surfaces, not core servers.

The present queue implementation still maps three test lanes, one of which is the M2, and allows three claims. Before deployment to the target hosts, the queue registry, governance/schema, task node IDs, workflow routing and topology tests must be reconciled with the two-host development target. Begin with at most two simultaneous physical development-host claims. A higher count requires a documented decision and capacity/isolated-worker evidence proving that the Mac Pro can safely host multiple disjoint logical workers or another qualified executor exists.

## 1. Architectural decisions

1. **The purchased Mac Pro is the primary target MediaHub server and developer host #1.** It is the intended home of the local model service (working name: Alamo), Jarvis/control APIs, model/API routing, task coordination, monitoring, and node registry, subject to exact hardware/runtime validation after acquisition.
2. **Local inference must remain local when local-only mode is selected.** The Claude Code path must not silently fall back to Anthropic's cloud API. The implementation must prove this through configuration inspection and network/evidence checks.
3. **FCC is a required control/integration layer for the Claude Code path.** Its exact responsibilities and supported configuration must be verified against the pinned FCC release. FCC does not replace Jarvis or become MediaHub's state/authority source.
4. **FreeLLMAPI is a cloud-model provider path, not the MediaHub authority.** It may expose multiple models/providers according to its actual API, availability, terms, and quotas.
5. **Alamo is a local inference endpoint on Mac Pro.** It is reached over the private network through a documented, authenticated API. Its actual runtime, protocol, model, and endpoint remain deployment facts to discover.
6. **Model selection can be manual or policy-driven.** The router may select between approved FreeLLMAPI models, other explicitly configured providers, and Alamo. Routing must respect capability compatibility, privacy mode, availability, quotas, latency, and cost.
7. **Codex remains a separate cloud-authenticated development path.** Its approved cloud API/subscription authentication is not silently replaced by the Claude Code/FCC/FreeLLMAPI path.
8. **The future GPU/video server is an optional compute extension, not a baseline dependency. Where user-contributed compute is later enabled, it is isolated from the operator-owned pool. Separate pools are:**
   - **Pool A — owned GPU server:** trusted, operator-managed hardware providing inference/compute services to Mac Pro.
   - **Pool B — MediaHub user-contributed compute:** untrusted-by-default worker nodes, admitted only through explicit consent, isolation, capability checks, quotas, result verification, and revocation.
9. **The VPS is restricted to the API-key registration/management workflow.** It is not a general egress proxy, model gateway, media relay, or mandatory transit point for ordinary application traffic.
10. **The mobile developer application connects to Jarvis over a private mesh/P2P network.** Mesh membership alone does not grant shell or administrative privileges.

## 2. Target topology

```text
CURRENT TEST LAB (temporary, not the target deployment map)
  ├── mh-dev-01 Linux test runner
  ├── mh-dev-02 Linux test runner
  └── Mac mini M2 — MediaHub prototype; not a permanent dev lane

TARGET DEVELOPER / INITIAL DEPLOYMENT HOSTS (after purchase/commissioning)
  ├── Purchased Mac Pro — primary MediaHub target + developer host #1
  │     ├── Jarvis/control API, A0 queue/state/evidence
  │     ├── model routing + Alamo local inference (after qualification)
  │     └── observability / node registry
  └── Mac mini Mid-2011 + Linux + planned 16 GB RAM — developer host #2
        └── bounded Claude Code/Linux executor and compatibility testing

MacBook / mobile application — optional user/client and approval surfaces

Future GPU/video server — optional inference + media-compute pool, added later

   FCC (required Claude Code integration/control layer)
        │
        ▼
   Model-routing boundary
        ├── FreeLLMAPI ──► specifically admitted cloud models/providers
        ├── other explicitly admitted provider adapters
        └── Alamo API ───► Mac Pro local inference

Mac Pro (primary target server and developer host #1)
  ├── Jarvis / MediaHub control plane
  ├── authenticated API gateway and model routing
  ├── task scheduler, node registry, queue and job state
  ├── Alamo local model service
  ├── observability and evidence collection
  └── direct protected connections to:
        ├── owned GPU server (Pool A)
        ├── MediaHub user-contributed workers (Pool B)
        ├── Mac mini / Linux
        └── mobile client via mesh network

European VPS
  └── isolated API-key registration/management workflow only
      (not in the ordinary model/data traffic path)
```

This topology is a future target plan, not a claim that the equipment has already been purchased or that components are deployed. Existing lab hardware is used for implementation and test only. FCC/FreeLLMAPI compatibility remains unproven; each integration edge requires a compatibility test.

## 3. Responsibility boundaries

| Component | Responsibility | Must not become |
|---|---|---|
| Jarvis | Central orchestration, task state, node coordination and policy enforcement | A provider-specific adapter or an implicit unrestricted shell |
| FCC | Required Claude Code integration/control layer; supported routing and client adaptation | MediaHub state authority or a substitute for Jarvis |
| FreeLLMAPI | One cloud-model/provider path, subject to provider availability and quota | A source of truth or a guarantee of permanently free capacity |
| Alamo | Local inference endpoint on Mac Pro | An assumed compatible endpoint before its API/runtime is verified |
| Model router | Selects only admitted models compatible with the task and policy | A mechanism to bypass provider rules, quotas, or user privacy choices |
| Codex | Separate cloud development workflow using its supported authentication | A component silently redirected to the local model or unrelated gateway |
| Owned GPU worker | Executes admitted jobs on operator-controlled hardware | An implicit shared-memory device for Mac Pro |
| User-contributed worker | Executes explicitly consented, isolated and bounded jobs | A trusted authority, unrestricted host executor, or holder of unrelated secrets |
| Mesh networking | Private node reachability | Application authorization |
| VPS | Narrow registration/management workflow for API keys | General proxy or transit for inference and ordinary application traffic |

## 4. Model-routing policy

The router should support:

- explicit model selection and a visible active-provider/model identity;
- a local-only mode that permits only Alamo and fails closed if Alamo is unavailable;
- a cloud-provider mode that selects only explicitly admitted providers;
- optional policy-driven selection based on capability, availability, quota, latency, and cost;
- fallback only when the task's privacy and capability policy allows it;
- clear reporting when a fallback occurs;
- per-provider timeouts, bounded retries, rate-limit handling, and circuit breaking;
- credential isolation: provider secrets remain on the service that needs them and never enter prompts, logs, or client-visible responses.

Automatic fallback from local inference to a cloud provider is **disabled in local-only mode**. No mode may silently switch providers.

Free-tier availability is best-effort and must not be represented as unlimited or guaranteed. Provider terms, quota, authentication, and model support must be checked for the exact integration.

## 5. GPU pools and resource semantics

### Pool A — owned GPU server

- Mac Pro submits jobs to a worker/runtime on the GPU server over an authenticated private API.
- The future GPU/video server uses its own CPU, RAM, GPU, and VRAM; these resources do not belong to the initial Mac Pro + Linux Mac mini baseline.
- Results and job telemetry return to the coordinator.
- Multi-GPU inference on one host may be used when supported by the selected runtime.
- Splitting one model across separate computers is a later optimization requiring benchmark evidence; it is not assumed to create one transparent VRAM pool.

### Pool B — MediaHub user-contributed compute

- Nodes are untrusted by default and must be explicitly admitted.
- Owners opt in to the exact resource/task policy and can revoke participation.
- Jobs run with least privilege, resource quotas, deadlines, restricted filesystem/network access, and no access to central secrets.
- Sensitive prompts/data are not sent to user-contributed nodes unless a separately approved data policy explicitly allows it.
- Results require validation; workers cannot self-assert qualification or become authorities.
- Node failure, stale heartbeat, policy violation, or inconsistent results trigger quarantine/revocation and an auditable state transition.

Remote RAM, disk, CPU, and GPU are consumed by executing jobs on the remote node or through explicit network services. They do not automatically become ordinary local RAM, disk, or VRAM on Mac Pro.

## 6. Network and security requirements

- Use a private mesh/VPN or equivalent authenticated private connectivity for node-to-node traffic.
- Require service-level authentication and authorization in addition to network membership.
- Encrypt traffic in transit; avoid exposing inference/admin ports directly to the public internet.
- Separate control-plane, model API, worker, storage, and key-management permissions.
- Keep provider credentials in an approved secret store or protected runtime environment; do not commit secrets.
- Record provider/model identity, node, task ID, timestamps, exit state, verification status, and evidence digest without recording secrets or sensitive prompt content by default.
- VPS failure must not interrupt local inference, worker traffic, or normal model requests.
- VPS must not be used to bypass provider account-registration controls, quotas, or authentication requirements.

## 7. Integration and qualification sequence

1. **Inventory current state:** identify exact Mac Pro/macOS/hardware, Alamo model/runtime/API, Mac mini environment, FCC release, FreeLLMAPI release/API, Claude Code version, ports, and existing configuration.
2. **FCC compatibility:** pin a release and verify its supported Claude Code integration, configuration format, lifecycle, and provider-routing capabilities.
3. **FreeLLMAPI adapter:** verify authentication, supported API protocol, model discovery, rate-limit behavior, quota reporting, and provider terms.
4. **Alamo adapter:** verify authenticated private endpoint, request/response format, context limits, tool/function calling, streaming, and health checks.
5. **Local-only acceptance:** prove Claude Code requests reach Alamo and cannot fall back to Anthropic or another cloud provider.
6. **Cloud model acceptance:** verify FreeLLMAPI model selection and report the actual provider/model identity; test quota/error/fallback behavior.
7. **Developer workflow:** run a bounded task against a test repository and validate file changes, tool use, tests, and logs.
8. **Owned GPU pool:** register one worker, run a non-sensitive inference job, measure latency/throughput/VRAM, and test worker loss/recovery.
9. **User-contributed pool:** define the threat model and consent/worker contract before running any user node.
10. **Mobile/mesh:** validate identity, least privilege, reconnect behavior, and access revocation.
11. **VPS isolation:** prove the VPS is not on ordinary inference/data routes and that its failure does not affect them.
12. **Independent verification:** record evidence at the exact source/configuration revision. A written design or successful health check alone does not qualify the runtime.

## 8. Initial acceptance criteria

The architecture is not considered implemented until evidence demonstrates all applicable criteria:

- [ ] Actual FCC version and configuration are pinned and reproducible.
- [ ] Claude Code reaches FCC through the intended local/private route.
- [ ] FCC-to-FreeLLMAPI integration passes a non-mutating probe and a bounded functional test.
- [ ] FCC/router-to-Alamo integration passes a non-mutating probe and a bounded functional test.
- [ ] Local-only mode fails closed and no request is sent to Anthropic/cloud providers.
- [ ] Cloud routing reports the actual provider/model and respects quotas/errors.
- [ ] Codex authentication remains separate from this route.
- [ ] Mac Pro and worker APIs require service-level authentication.
- [ ] Owned GPU worker is measured and recovers from a simulated outage.
- [ ] User-contributed workers have consent, isolation, quota, verification, and revocation tests before admission.
- [ ] Mobile access can be revoked independently of mesh membership.
- [ ] VPS is not an ordinary inference/data proxy.
- [ ] Secrets are absent from repository files, logs, and evidence.
- [ ] A3/independent verification records pass/fail results and supporting evidence.

## 9. Explicit non-claims

This document does not assert that FCC, FreeLLMAPI, Claude Code, Alamo, Codex, or any GPU runtime is already integrated or qualified. It does not assert unlimited free models, seamless tool compatibility, shared physical memory across computers, or successful production operation. Those are implementation questions requiring fresh evidence.

## 10. Related architecture

- `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md`
- `architecture/COMPONENT-ARCHITECTURE-DECISIONS.md`
- `architecture/COMPONENT-INTEGRATION-BOUNDARY.md`
- `components/COMPONENT-REGISTRY.yaml`
