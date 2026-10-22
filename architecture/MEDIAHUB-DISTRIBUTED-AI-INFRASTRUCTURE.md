# MediaHub OS — Distributed AI Infrastructure and Model Routing Architecture

- **Date:** 2026-10-12
- **Status:** ACCEPTED TARGET ARCHITECTURE — NOT YET RUNTIME-QUALIFIED
- **Scope:** Mac mini 2018 central node, Mac mini Linux worker, MacBook clients, FCC, FreeLLMAPI, local model service, owned GPU server, MediaHub user-contributed compute, mobile client, and registration-only VPS.
- **Authority:** This document records the user's accepted target design. It does not claim that any component is deployed, compatible, or qualified.
- **Authoritative host identity correction (Wave 364, 2026-10-22): Alamo is the local inference service hosted on `Voktors-Mini.Dlink` (macOS), identified by the owner as the Mac mini 2018 host. Alamo and the central-infrastructure role therefore refer to the same physical Mac mini 2018 unless future inventory evidence distinguishes separate devices. This identity correction does not qualify Alamo's runtime, API, model, route, or production readiness.

## 1. Architectural decisions

1. **Mac mini 2018 is the central infrastructure node.** It hosts Jarvis/control services, model/API routing, task coordination, monitoring, and the node registry, subject to hardware and runtime validation. The local inference service named Alamo runs on `Voktors-Mini.Dlink` (Mac mini 2018).
2. **Local inference must remain local when local-only mode is selected.** The Claude Code path must not silently fall back to Anthropic's cloud API. The implementation must prove this through configuration inspection and network/evidence checks.
3. **FCC is a required control/integration layer for the Claude Code path.** Its exact responsibilities and supported configuration must be verified against the pinned FCC release. FCC does not replace Jarvis or become MediaHub's state/authority source.
4. **FreeLLMAPI is a cloud-model provider path, not the MediaHub authority.** It may expose multiple models/providers according to its actual API, availability, terms, and quotas.
5. **Alamo is a local inference endpoint hosted on `Voktors-Mini.Dlink` (macOS).** It is reached over the private network through a documented, authenticated API. Its actual runtime, protocol, model, API endpoint, and qualification remain deployment facts to discover.
6. **Model selection can be manual or policy-driven.** The router may select between approved FreeLLMAPI models, other explicitly configured providers, and Alamo. Routing must respect capability compatibility, privacy mode, availability, quotas, latency, and cost.
7. **Codex remains a separate cloud-authenticated development path.** Its approved cloud API/subscription authentication is not silently replaced by the Claude Code/FCC/FreeLLMAPI path.
8. **There are two separate GPU execution pools:**
   - **Pool A — owned GPU server:** trusted, operator-managed hardware providing inference/compute services to Mac mini 2018.
   - **Pool B — MediaHub user-contributed compute:** untrusted-by-default worker nodes, admitted only through explicit consent, isolation, capability checks, quotas, result verification, and revocation.
9. **The VPS is restricted to the API-key registration/management workflow.** It is not a general egress proxy, model gateway, media relay, or mandatory transit point for ordinary application traffic.
10. **The mobile developer application connects to Jarvis over a private mesh/P2P network.** Mesh membership alone does not grant shell or administrative privileges.

## 2. Target topology

```text
MacBook
  ├── Claude Desktop / development client
  └── Codex Desktop ───────────────► approved Codex cloud path

Mac mini / Linux
  └── Claude Code
        │
        ▼
       FCC  (required Claude Code integration/control layer)
        │
        ▼
   Model-routing boundary
        ├── FreeLLMAPI ──► available cloud models/providers
        ├── other explicitly admitted provider adapters
        └── Alamo API ───► Voktors-Mini.Dlink (Mac mini 2018) local inference

Mac mini 2018 / Voktors-Mini.Dlink (central infrastructure and Alamo host)
  ├── Jarvis / MediaHub control plane
  ├── authenticated API gateway and model routing
  ├── task scheduler, node registry, queue and job state
  ├── private-network route to Alamo on Voktors-Mini.Dlink
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

This topology is logical, not a claim that all components are already deployed or that FCC/FreeLLMAPI natively support every arrow. Each integration edge requires a compatibility test.

## 3. Responsibility boundaries

| Component | Responsibility | Must not become |
|---|---|---|
| Jarvis | Central orchestration, task state, node coordination and policy enforcement | A provider-specific adapter or an implicit unrestricted shell |
| FCC | Required Claude Code integration/control layer; supported routing and client adaptation | MediaHub state authority or a substitute for Jarvis |
| FreeLLMAPI | One cloud-model/provider path, subject to provider availability and quota | A source of truth or a guarantee of permanently free capacity |
| Alamo | Local inference endpoint hosted on Voktors-Mini.Dlink (macOS) | An assumed compatible endpoint before its API/runtime is verified |
| Model router | Selects only admitted models compatible with the task and policy | A mechanism to bypass provider rules, quotas, or user privacy choices |
| Codex | Separate cloud development workflow using its supported authentication | A component silently redirected to the local model or unrelated gateway |
| Owned GPU worker | Executes admitted jobs on operator-controlled hardware | An implicit shared-memory device for Mac mini 2018 |
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

- Mac mini 2018 submits jobs to a worker/runtime on the GPU server over an authenticated private API.
- The GPU server uses its own CPU, RAM, GPU, and VRAM.
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

Remote RAM, disk, CPU, and GPU are consumed by executing jobs on the remote node or through explicit network services. They do not automatically become ordinary local RAM, disk, or VRAM on Mac mini 2018.

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

1. **Inventory current state:** identify exact Mac mini 2018/macOS/hardware, Alamo model/runtime/API on Voktors-Mini.Dlink, Mac mini environment, FCC release, FreeLLMAPI release/API, Claude Code version, ports, and existing configuration.
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
- [ ] Mac mini 2018 and worker APIs require service-level authentication.
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
