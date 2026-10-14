# MediaHub OS / ASTRA — Unified Architecture, Component Admission and Deployment Contract

- ID: MH-UNIFIED-DEPLOYMENT-CONTRACT-0.1
- Revision: 0.1-draft
- Status: PROPOSED / CROSS-DOMAIN RECONCILIATION DRAFT / NOT ACCEPTED / NOT FROZEN
- Scope: MediaHub OS, MediaHub iOS, ASTRA/Jarvis, local user environment, local developer fabric, cloud development fabric, installation and lifecycle.
- Current functional authority: Functional Baseline 2.0, docs/checkpoints/mediahub-functional-baseline-2.0.md, blob 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f on main.
- Historical provenance: Functional Baseline 1.0 remains preserved at specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md, blob 9df4892ed0734050ac79732603d15bb414717310. This draft does not merge or reinterpret B1.
- Component selection source: docs/checkpoints/mediahub-github-component-final-manifest-2.0.md, blob 45988bf9da202c9597d0ca2de50e92e5c2e6ed55 on main.
- Related domains: MH-12/13 security/privacy; MH-14 persistence; MH-15 OS/appliance; MH-16 installer/update/recovery; MH-20 automation; MH-21 cloud/distributed AI; MH-22 qualification; MH-23 evolution/migration; MH-24 baseline; ASTRA GOLD.
- This is a proposal, not a replacement for domain sources. It grants no implementation, installation, deployment or production authorization.

## 1. Cross-chat architecture status

The repository already contains an accepted functional baseline, project map, domain architecture records, component manifest and ASTRA governance architecture. These are related, but they do not yet form one fully accepted, revision-bound deployment contract. This draft creates a shared crosswalk while each domain's primary documents remain normative.

“Jarvis” is treated as the user-facing name for the ASTRA/MediaHub assistant experience, not as an independent authority, second state store or separate architecture domain.

The map/checkpoint are the durable cross-chat navigation mechanism; they cannot automatically rewrite every separate ChatGPT conversation. Each architecture chat must read the live map and primary sources, work within its domain, and return decisions/evidence to GitHub. The map records navigation and status, not a substitute for primary contracts.



## 1.1 Unified traceability matrix

The companion cross-domain matrix is `docs/checkpoints/mediahub-unified-system-traceability-matrix-v0.1.md`, on the live `docs/mediahub-chat-tree-map-20261012` ref; resolve and record the current blob SHA from GitHub at review time rather than pinning a mutable branch file here (latest verified SHA is recorded in the project map/checkpoint). It provides the MH-01…MH-25 responsibility matrix, Claude/local Ollama decision matrix, component admission crosswalk, hardware-independent deployment phases P00–P20, matrix-local gates MH-UTM-G0…MH-UTM-G9, and required evidence schema. Those matrix-local identifiers are distinct from this contract's MH-UDC-G0…MH-UDC-G9, MH-22 lifecycle gates G1–G9, and ASTRA qualification gates G0–G11; numeric suffixes are not interchangeable. The matrix is a companion inventory/reconciliation draft, not a replacement for primary domain contracts, Baseline 2.0 or the canonical component manifest. Its status is NOT ACCEPTED / NOT FROZEN and it grants no implementation or deployment authority.

## 2. Precedence and evidence labels

Resolve source conflicts explicitly in this order:
1. Explicit owner-approved governance/decision records.
2. Accepted Functional Baseline 2.0 for current functional requirements.
3. Domain contracts, preserving their actual acceptance status.
4. Canonical component manifest for selection/admission status.
5. Reference architectures and implementation blueprints.
6. Implementation, workflow, test and qualification evidence tied to exact revision/artifact.
7. Historical records and unverified claims.

Baseline 1.0 is historical provenance and must not be silently merged with Baseline 2.0.

Label each claim REQUIREMENT, PROPOSED, DECIDED, IMPLEMENTED, EVIDENCED, VERIFIED, QUALIFIED, ACCEPTED, FROZEN, PRODUCTION_AUTHORIZED, HISTORICAL, UNKNOWN or BLOCKED. These labels are not interchangeable. A file or workflow existing in GitHub does not prove installation, runtime operation, verification or qualification.

## 3. Product domains and authority invariants

Domains:
- Local user: MediaHub OS/Core, State Authority, Smart Home, Media, Documents, Knowledge, Digital Twin, Engineering, local AI, device/network integrations and UI.
- Local developer: isolated workstations/compute for building and testing; not a user-data export path.
- Cloud Development Fabric: corporate engineering control plane, admitted developer compute, CI/CD, approved source/artifact/model storage and evidence. It is not a user cloud or flat global resource pool.
- Mobile: MediaHub Core for iOS/iPadOS and Remote Access remain distinct roles. Developer Mobile is developer-domain-only and gains no user-data access from developer status.

Invariants:
- Human owner retains final architecture, security, production and launch decisions.
- MediaHub State Authority is the sole canonical authority for platform canonical state.
- ASTRA A0 coordinates bounded work under approved contracts; it does not bypass owner/governance approval. A1 designs, A2 implements bounded slices, A3 independently verifies. Executors, models, providers, gateways, schedulers and transports have no canonical authority.
- Home Assistant Core is authoritative only for Smart Home operational/device state behind the MediaHub Smart Home boundary.
- Cloud, local AI, plugins, automation, telemetry, deployment tools, storage engines and brokers do not become State Authority.
- Persistence, backup, migration, rollback, restore, update and host OS are mechanisms; canonical state changes require approved State Authority semantics.
- Sent != Applied != Verified. Transport acknowledgement is not commit proof.
- Compute contribution is opt-in, scoped, admitted, lease-bound, isolated, audited and revocable; it is not user-data access or developer-personnel access.
- Personal/sensitive user data stays local by default. Cloud egress requires classification, authorization, purpose, minimization, destination and retention controls.
- Local Media Mesh, Developer Mesh, HIGH_SPEED links, CPRG registration path and ordinary Internet are distinct planes. No implicit bridge, route redistribution or default gateway.
- Reliability baseline remains SINGLE NODE / NO HA unless an accepted decision and evidence establish otherwise.

## 4. Component admission summary

The canonical component manifest remains the authority for component status. This summary does not change that status.

| Capability | Component/approach | Status | Boundary/gate |
|---|---|---|---|
| State and policy | MediaHub-owned contracts/State Authority | Current architecture | No authority substitution; P0 gates apply |
| Typed contracts/RPC | Protobuf; gRPC where needed | Selected/conditional | Versioning, authorization, compatibility; generated code is not the domain model |
| Observability | OpenTelemetry, Prometheus | Selected foundation | Observational only; no correctness/mutation authority |
| Secrets/config | SOPS + age | Selected mechanics | Key custody, recovery, least privilege and rotation require operational design |
| Supply chain | Syft, Cosign, Trivy | Selected tools | SBOM, provenance/signature and vulnerability policy; tools do not approve releases |
| Source/evidence | GitHub and workflows | Existing infrastructure | Workflow definition is not a passing run |
| Relational persistence | PostgreSQL | TARGET-GATED | MH-14 authorization, transaction/schema/migration/restore evidence |
| Vector retrieval | pgvector inside PostgreSQL | TARGET-GATED | Workload/benchmark need; no second state authority |
| Smart Home | Home Assistant Core | TARGET-GATED integration | Smart Home authority only; adapter qualification |
| Backup | restic | TARGET-GATED | Restore, integrity, key recovery and retention evidence |
| OTA mechanics | RAUC | TARGET-GATED | MH-16 update authority, atomicity, rollback/recovery evidence |
| Object storage | S3-compatible interface | Interface selected; engine replaceable | SeaweedFS not automatically activated |
| Local AI | ONNX Runtime / llama.cpp behind MediaHub AI Gateway | TARGET-GATED | Exact model/runtime, hardware benchmark, isolation and policy |
| Media | FFmpeg | Selected primitive/conditional use | Isolation, resource limits, timeout and input/output contract |
| Cloud execution | Ray | Candidate | Admission, isolation, lease, network policy, idempotency and evidence |
| Worker isolation | containerd/OCI | Candidate | Threat-based isolation, capabilities, resource/network/mount controls |
| Developer Mesh | Netmaker/WireGuard; Headscale/WireGuard alternative | Reference candidates | Identity/routes/firewall/revocation; no user Media Mesh bridge |
| High-speed links | Thunderbolt/USB4 IP networking | Hardware-specific V1 candidate | Exact hardware/OS and topology/throughput/RTT/loss qualification |
| Artifact registry | Harbor | TARGET-GATED | Need, identity, signing, retention, restore and operational burden |
| Distributed transport/coordination | NATS/JetStream, etcd | FUTURE-GATED | Demonstrated gap; neither becomes canonical domain state |
| Workflow engine | Temporal | Reference/FUTURE-GATED | Demonstrated durability gap; no duplicate workflow authority by default |
| Kubernetes/K3s | Reference only | Not mandatory | Not a prerequisite without explicit accepted decision |
| Edge proxy | Caddy | Reference/TARGET-GATED | Routing/TLS only; no identity or policy authority |

Admission sequence: evidenced capability gap → exact source/upstream → license review → provenance and immutable version pin → SBOM/signature/security review → MediaHub adapter/contract → compatibility/resource benchmark → positive and negative tests → degraded/recovery and upgrade/rollback evidence → independent qualification → explicit approval → reversible activation.

No component becomes active merely because it appears here. Do not install/deploy while its gate or authorization is open.

## 4.1 Owner direction — Claude-centered Jarvis with local Ollama inference (2026-10-12)

**Owner-stated target direction:** Jarvis is to use Claude-centered reasoning/engineering workflows while retaining a local Ollama inference capability. Record this as an owner direction for architecture reconciliation, not as evidence that the integration already exists or is qualified.

**Technical distinction:** Claude models are not models served by Ollama. Ollama serves compatible locally hosted models; Claude is a separate model/service family accessed through an approved Anthropic interface or other explicitly supported integration. Therefore, “Claude running locally on Ollama” is not the literal deployment model. The implementable interpretation is a controlled hybrid architecture with distinct Claude and Ollama adapters behind a Jarvis model-routing/orchestration boundary. Whether a specific Claude tool can be configured to call an Ollama endpoint is a separate compatibility question and must not be assumed.

### Proposed model topology

1. **Jarvis orchestration/control plane:** owns task intent, work envelope, routing policy, identity, budgets, deadlines, cancellation and evidence collection. It is not MediaHub Product State Authority.
2. **Claude adapter:** separate external provider path for approved reasoning/coding tasks. External calls are opt-in per task and must pass data classification, purpose, minimization/redaction, destination/provider policy, credentials and retention review. No secrets or personal MediaHub data may be sent by default.
3. **Ollama adapter:** local inference endpoint for an explicitly pinned local model artifact. Model name alone is insufficient: record exact model tag/digest, source/license, quantization, context limits, runtime version, hardware profile, memory/latency benchmarks and safety/permission profile.
4. **Model router:** selects only among admitted model profiles under task policy. It may not silently fall back from Ollama to Claude or from Claude to another provider. Every fallback is a new provider/destination decision and must be authorized and recorded.
5. **Tool gateway:** all filesystem, GitHub, shell, browser, deployment and other tools remain separate, capability-scoped adapters. Neither Claude nor a local model receives arbitrary shell, production credentials or unbounded write access by default.
6. **Result validation:** outputs from both local and external models are untrusted data until validated against the task contract, source provenance, policy and independent verification requirements. Model output cannot authorize its own actions or qualify itself.
7. **MediaHub boundary:** Jarvis engineering memory, task queues and model context are distinct from canonical MediaHub product state. No model, Ollama store, vector index, agent graph or external provider becomes a second State Authority.

### Initial routing policy proposal

- Prefer local Ollama for tasks that can be completed by an admitted local model without external data egress, subject to measured quality and hardware capacity.
- Use Claude only for task classes explicitly approved for external processing and only after the request has been classified and minimized.
- If local inference is unavailable, over budget or below an evidence-based quality threshold, return a bounded failure or request authorized escalation. Do not automatically send the same prompt to a cloud provider.
- Keep deterministic L0 controls and critical local behavior independent of both Claude and Ollama.
- Route coding tasks through bounded task envelopes, isolated worktrees, explicit file allowlists, diff review and independent verification; the model itself is not the merge or release authority.
- Record per invocation: task ID, provider/model/runtime identity, model artifact/version, policy decision, data classification, destination, tool capabilities, budget/deadline, prompt/context provenance where permissible, output digest, validation outcome and cost/latency metrics. Do not log secrets or raw sensitive prompts by default.

### Required decisions/evidence before activation

- Exact Claude access mode (Claude Code, approved API integration or other named interface), supported authentication and permitted data classes.
- Owner decision D-03 (2026-10-14): use a Jarvis policy-routing/orchestration layer that selects an allowed Claude or Ollama execution path per task. Claude is an external executor; Ollama is a separate local runtime. The detailed adapters and routing enforcement remain to be designed and verified.
- Exact Ollama host hardware/OS/runtime and per-model compatibility, license, provenance, memory/context and latency results.
- Model-routing contract, failure/fallback semantics, local-only mode, egress-denial evidence and provider retention/privacy terms.
- Tool authorization, sandbox/worktree boundaries, approval gates, audit schema and independent verification.
- Explicit MH-10/MH-21 ownership reconciliation and current MH-22 qualification evidence.
- Owner/governance approval before any model runtime, provider credential, API integration or production route is activated.

**Status:** OWNER-ACCEPTED ARCHITECTURE DIRECTION D-03 (2026-10-14) / DESIGN DETAILS PROPOSED / NOT IMPLEMENTED / NOT QUALIFIED. Acceptance is limited to the role and topology direction; this v0.1 contract remains a cross-domain draft and is NOT accepted/frozen as a whole. No installation, provider call, credential use, test, qualification or runtime change was performed.


### 4.1.1 Owner-accepted Jarvis control-plane direction (D-03, 2026-10-14)

The owner explicitly accepts the following architectural direction:

- **Jarvis is the top-level coordination layer** for distributed, hybrid, autonomous engineering. It decomposes and coordinates tasks, chooses the permitted execution method and later coordinates the cloud development system.
- **GitHub is a directly integrated engineering control surface** for Jarvis. All repository actions must pass through a capability-scoped adapter with explicit identity, least privilege, audit, branch/review protections and evidence-bound verification. Direct GitHub management does not authorize bypassing review/branch protection or self-authorizing merge, release, deployment or production changes.
- **Claude** is an external intelligent/engineering executor through an approved interface.
- **Ollama** is a separate local inference runtime for compatible local models. Claude is not hosted inside Ollama.
- **Routing policy** chooses only an eligible executor per task based on task class, data classification, destination policy, local capability, budget and explicit authorization. No silent local-to-cloud fallback.
- **ASTRA** coordinates autonomous engineering only within granted capabilities and existing governance gates.
- **Product State Authority remains the exclusive authority for canonical product-state changes.** Jarvis, ASTRA, model providers and GitHub adapters cannot acquire or infer that authority.

This is an owner-accepted architecture direction, not evidence of implementation, GitHub permissions, provider connectivity, cloud deployment, qualification or operational readiness. Existing non-authorizations remain in force, including provider calls, credential use, tests/qualification, host/runtime inspection, infrastructure changes, deployment and merge absent separate authorization.

## 5. Deployment profiles

### L — Local user MediaHub
Target: qualified local host(s) in the user's network. Future Mac Pro/Mac mini expansion is a design target, not proof that exact models are compatible.

Layers: hardware/firmware and host OS → host security/identity/network/service supervision → MediaHub runtime/contracts → State Authority/policy → persistence only after MH-14 authorization → core domain services/integrations → qualified local AI → UI/mobile → non-authoritative telemetry/backup/update/recovery.

Offline-first critical behavior must not depend on cloud availability. Cloud AI is controlled escalation, not a prerequisite for local core behavior.

### D — Local developer environment
Required: pinned source revision; known worktree; documented toolchain/runtime; reproducible dependencies/artifacts; task-specific branch/worktree and bounded write scope; secrets excluded from source/logs; test fixtures separate from personal data; outputs tied to exact commit; cancellation/timeouts/cleanup. Tests run only when separately authorized. No implicit production credentials, privileged shell or user-data mounts for AI agents. A machine is not a trusted executor merely because registered.

### F — Local developer compute fabric
Multi-node compute is optional later, not a prerequisite for single-node development. Separate control/evidence, compute, developer storage, encrypted Developer Mesh, HIGH_SPEED, per-node Internet, optional shared developer egress and protected CPRG registration.

Initial routing: each node retains its own default Internet route; HIGH_SPEED and Developer Mesh are not default gateways; no user Media Mesh forwarding; shared egress is opt-in and must not alter the ordinary route when disabled.

Sequence: two-node high-speed link → measured evidence → controlled network policy → isolated bounded workload → lease/heartbeat/result/evidence/revocation → failure/recovery tests → 3+ node topology → cost-aware placement → only then consider distributed storage or scheduler expansion.

### C — Cloud Development Fabric
Separate engineering environment, never a shared user cloud. Logical components: GitHub/reviewed workflow control; ASTRA control/evidence plane; developer identity/admission/policy; scheduler/lease protocol; qualified execution backend; isolated ephemeral worker workspaces; approved engineering artifact/model storage; SBOM/signature/provenance; non-authoritative telemetry/audit; cost/resource quota, cancellation, revocation and incident handling.

Ray, OCI/containerd, Netmaker/WireGuard, gRPC, NATS, SeaweedFS and Harbor remain subject to their manifest statuses and gates. Cloud control cannot promote its own work, make production decisions or route arbitrary user data to workers.

## 6. Installation and deployment phases

This is a plan, not authorization to install anything.

### Phase 0 — scope and inventory
Confirm profile, owner/operator, exact target identity, purpose, data class, network planes, recovery objectives and authorization. Inventory existing state non-destructively.
Output: deployment manifest and unknowns.
Stop if target, authority, data boundary or recovery plan is unclear.

### Phase 1 — hardware/OS compatibility
Record exact model, CPU/RAM/GPU/NPU, storage health/capacity, NIC, firmware/EFI, thermal/power and supported OS/kernel. Compare with MH-15 and workload envelope. Do not assume the Mac mini Server 2011 candidate or future Mac Pro is qualified.
Output: compatibility evidence and GO/NO-GO.
Stop before firmware, disk, kernel or firewall changes without separate authorization.

### Phase 2 — trust/bootstrap
Verify operator identity, trusted source/revision, artifact identity and verification path. Define secret custody, least-privilege service identities, key recovery/revocation; separate admin, runtime, update, recovery and executor identities where justified.
Output: threat boundary, secret/key lifecycle and bootstrap evidence.
Stop if secrets would enter Git, logs, untrusted workers or chat.

### Phase 3 — host foundation
Choose OS/kernel/service manager only after compatibility review and ADR; systemd is a candidate, not an automatic requirement. Define users/groups, process boundaries, filesystem layout, time, network/firewall, updates, logs, resource limits and shutdown. Root remains exceptional; AI/plugin paths never receive arbitrary privileged shell.
Output: versioned host profile and hardening evidence.
Stop on unsupported hardware, unresolved privilege boundary or unsafe network defaults.

### Phase 4 — build and supply chain
Pin source commit, toolchain, dependencies and build environment. Produce artifact digest, SBOM and provenance; verify signatures and vulnerability policy. Keep outputs separate from user data.
Output: immutable build manifest and verification record.
Stop if artifact/source identity is ambiguous or supply-chain gates fail.

### Phase 5 — runtime/contracts
Install only the minimum approved runtime foundation. Validate schemas/contracts and service identities before enabling integrations. No database, broker, filesystem or AI runtime becomes canonical by default.
Output: runtime inventory, dependency graph and contract verification.
Stop if a component requires unauthorized authority or persistence.

### Phase 6 — persistence/recovery (separate authorization)
Do not activate PostgreSQL or another persistence implementation until MH-14 selects and authorizes the design. Specify transaction/atomicity, schema migration, durability, power-loss behavior, encryption/key recovery, retention/deletion, backup/restore and RPO/RTO. Recovery validates integrity/schema/compatibility then submits a candidate to State Authority; stored data is not promoted directly to canonical state.
Output: approved persistence ADR and verified restore/recovery evidence.
Stop if recovery is unverifiable or canonical-state ownership is ambiguous.

### Phase 7 — core services/integrations
Proposed order: security foundation → runtime → State Authority → policy/configuration → domain core → adapters/integrations → UI/AI/plugins. Process alive, port open or container running does not mean READY. Integrate Home Assistant/media/document/Digital Twin only behind MediaHub contracts and their gates.
Output: service dependency map, health checks, authorization and negative-test evidence.
Stop on policy or canonical-authority bypass.

### Phase 8 — local AI/tools
Qualify exact model variant, weight provenance, runtime, hardware fit, latency/memory, isolation, tool permissions and recovery. Route through MediaHub AI Gateway and bounded tool contracts. Models cannot self-authorize, canonically change architecture or self-qualify.
Output: model/runtime qualification and tool-boundary evidence.
Stop if model identity, data egress or permissions cannot be enforced.

### Phase 9 — network/cloud
Define separate user, management, developer, storage, high-speed, cloud and registration paths. Deny unnecessary ingress; default-deny forwarding; explicit egress/destination policy. Verify data class, region, retention/training policy and failure behavior before cloud egress.
Output: network diagram, route/firewall policy and egress evidence.
Stop if developer workers can access user Media Mesh/storage without explicit scope.

### Phase 10 — developer fabric/cloud execution
Admit nodes/providers individually; verify identity, capability, capacity and network policy. Protocol: Capability → Admission → Lease → Dispatch → Heartbeat → Result → Evidence → Revoke/CLOSED. Use ephemeral isolated workspaces, bounded permissions, quotas, cancellation, idempotent retries and audit.
Output: revision-bound execution and independent verification.
Stop on stale/duplicate claims, untrusted worker, missing lease, policy violation or unverifiable result.

### Phase 11 — backup/update/rollback/recovery
Keep host, application, data migration and security update planes separate. Verify artifact identity, compatibility, authorization, security floor and rollback semantics before activation. Restore must validate recovered state, schema, runtime and health; backup completion alone is not recoverability.
Output: revision-bound update/restore/rollback/recovery record.
Stop on UNKNOWN_STATE, failed Health Gate or migration without validated recovery.

### Phase 12 — qualification/release
Identify exact candidate: product/version/build/commit/digest/dependencies/signature/SBOM/target. Run authorized tests/qualification on that exact candidate and target; preserve logs/results. Independently review security, privacy, hardware, performance/capacity, degraded operation, recovery, observability and operations. Obtain explicit governance decision.
Output: qualification matrix, evidence register and decision.
Stop on critical UNKNOWN, blocker, missing artifact identity or absent owner approval.

### Phase 13 — controlled operation
Monitor non-authoritative telemetry; define incident ownership, escalation, revocation, patching, recovery and evidence retention. Observe SLI/SLO and resource/cost limits. Change only through reviewed, versioned, reversible change control.
Output: operational review and next revision proposal.
Stop/rollback according to approved safety policy when critical invariants fail.

## 7. Deployment manifest required for every target

Record deployment_id/profile; owner/operator; source commit and document revision; hardware/OS/firmware; data classification and allowed egress; exact component versions/digests/licenses/statuses; services/identities/capabilities/network permissions; State Authority and persistence/recovery boundaries; secret/key custody/revocation; health/readiness checks; update/rollback/recovery plan; backup/restore objectives; resource/cost limits; qualification artifacts/gate results; unknowns, deviations and approvals.

## 8. Cross-domain gate matrix

**Draft-local identifier namespace:** `MH-UDC-G0`…`MH-UDC-G9` identify only this contract's proposed cross-domain readiness gates. They do not replace or imply equivalence with MH-22 lifecycle gates G1–G9 or ASTRA launch/qualification gates G0–G11. This mapping is naming disambiguation only; acceptance criteria and statuses remain unchanged.

| Draft-local gate ID | Domains | Minimum exit evidence | Current disposition |
|---|---|---|---|
| MH-UDC-G0 Functional authority | Baseline 2.0, MH-24 | Requirement-to-contract mapping | Baseline accepted; this contract is draft |
| MH-UDC-G1 Hardware/OS | MH-15 | Exact hardware/OS compatibility | Open; not authorized |
| MH-UDC-G2 Identity/security/privacy | MH-12, MH-13, MH-21 | Threat boundary, identity, egress, secret evidence | Open; unknowns remain |
| MH-UDC-G3 Runtime/State Authority | MH-03, P0-03…P0-07 | Current revision-bound enforcement evidence | P0-07 blocker remains; no fresh run verified here |
| MH-UDC-G4 Persistence | MH-14 | Approved ADR, durability and restore evidence | Implementation not authorized |
| MH-UDC-G5 Lifecycle/update/recovery | MH-16 | Install/update/migration/rollback/restore/Health Gate evidence | Governance acceptance pending; implementation blocked |
| MH-UDC-G6 Components | Component manifest | Per-component admission package | Target/Future gates remain |
| MH-UDC-G7 Cloud/developer fabric | MH-21, Cloud Development Fabric | Identity, admission, privacy, network, worker and recovery evidence | MH-21 not accepted/frozen |
| MH-UDC-G8 Qualification | MH-22 | Exact candidate/target qualification matrix PASS | Not qualified / NO-GO |
| MH-UDC-G9 Release/production | MH-22, owner decision | Explicit release/production authorization | Not granted |

## 9. Proposed cross-chat work allocation

This is a navigation proposal, not a silent charter change:
- MH-15: host/hardware/OS profile and compatibility; no host modifications without authorization.
- MH-14: persistence, durability, restore and data lifecycle; physical implementation remains gated.
- MH-16: installer, bootstrap, update, migration, rollback, recovery and Health Gate.
- MH-12/MH-13: security, identity/trust and privacy/data governance.
- MH-10: AI semantics, model/tool authority and AI Gateway.
- MH-20: automation, energy and bounded self-healing.
- MH-21: cloud boundary, distributed AI, egress, provider/workload admission and cloud failure.
- MH-22: qualification, release identity, operations and production gates.
- MH-23: compatibility, evolution and migration across revisions.
- MH-24: accepted functional baseline and traceability.
- MH-25 / ASTRA GOLD: autonomous development orchestration and execution qualification, subject to resolving the historical MH-25 “Migration” naming/scope discrepancy against primary governance records.
- Component manifest/reference architecture: component admission and cross-domain placement, not permission to activate gated components.

Each domain chat returns decisions/open questions; source path/ref/blob SHA; dependency impacts; status; required evidence; owner decision; map/checkpoint update request. Do not copy proposals into all domains as if accepted.

## 10. Open decisions
1. Exact supported hardware profiles and host OS/kernel/firmware.
2. Approved persistence technology and semantics.
3. Service supervision/isolation technology per host profile.
4. Canonical network addressing/VLAN/VRF/firewall/DNS/DHCP/Wi-Fi roaming implementation.
5. Cloud provider contracts, regions, retention/training use and enforceable egress.
6. Developer node admission, scheduler placement algorithm and high-speed topology evidence.
7. Exact model/runtime/hardware profiles and production routing.
8. Update/atomicity/rollback mechanism and platform compatibility.
9. Current-HEAD P0-07 and full MH-22 qualification evidence.
10. Governance acceptance/freeze of domain architectures that remain proposed.
11. MH-25 historical “Migration” label versus MH-23 migration scope.
12. Owner decisions for changes to accepted Baseline 2.0.

Unknowns remain visible; do not resolve them by popularity or by writing assumptions as facts.

## 11. Explicit non-authorizations
This draft does not authorize software installation, package upgrades, tests/qualification, workflow dispatch/self-hosted runner activity, production/provider credentials or external API calls, host/runtime inspection or changes, firmware/disk/network/firewall/cloud changes, persistence implementation, migration/restore/rollback execution, deployment/release/production promotion, or merge/cherry-pick into main. Such actions require relevant explicit authorization and preflight contract.

## 12. Acceptance path
1. Owner reviews this cross-domain draft and resolves product choices.
2. Domain chats validate their sections against primary sources and return conflicts/evidence.
3. The map links each domain to this draft while domain documents remain normative.
4. Complete a revision-bound crosswalk: requirements → decisions → architecture → implementation → evidence → qualification.
5. Governance explicitly accepts/freezes a new revision; no implicit freeze.
6. Only then create/execute separately authorized implementation slices and deployment runbooks.

**Current conclusion:** Baseline 2.0 is accepted as the functional reference. This deployment contract is a proposed bridge, not an accepted or implementation-verified contract. Architecture remains not fully deployment-qualified.


## Wave 02 local inventory evidence supplement (2026-10-14)

The live, bounded inventory is indexed in [MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md](MEDIAHUB-UNIFIED-LOCAL-INVENTORY-AND-VERIFIABLE-COMPONENT-MATRIX-WAVE-02-2026-10-14.md). It does not change this document's PROPOSED / NOT ACCEPTED / NOT FROZEN status. It distinguishes declarations, installed CLIs, process/service presence, runtime route evidence, qualification and acceptance.

Open documentary conflict C-01: FreeLLMAPI is classified as local_gateway in the agent/provider registries while the distributed AI architecture describes a cloud/provider route in its routing narrative. Resolve service location, upstream provider and egress boundary against pinned source/deployment evidence before route implementation. No authority or admission is granted by this supplement.

