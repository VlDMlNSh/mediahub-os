# MEDIAHUB OS / MEDIAHUB iOS
# FUNCTIONAL BASELINE 2.0

**Document status:** RECONCILIATION CANDIDATE — PENDING OWNER ACCEPTANCE  
**Version:** 2.0.0  
**Architecture revision:** MH-24 / 2026-09-30  
**Scope:** MediaHub OS 11.x LTS / MediaHub iOS and associated development infrastructure  
**Supersedes:** Functional Baseline 1.0 as the next functional reference, while preserving Baseline 1.0 as immutable historical provenance.

## 0. Purpose and authority

This document reconciles the user-supplied 68-section functional passport, MH-1…MH-23 decisions, canonical checkpoint documents, and the current GitHub repository state.

It does **not** claim that architecture is implemented merely because a repository artifact exists. The following states remain distinct:

- Requirement
- Decision
- Architecture
- Implementation
- Evidence
- Historical Record
- Open Decision
- Rejected Option

Implementation is never inferred from architecture. Qualification is never inferred from implementation.

## 1. Reconciled system definition

MediaHub is one unified local-first platform architecture deployed over heterogeneous qualified hardware profiles.

Canonical product chain:

**Physical/Platform → MediaHub OS/Core → MediaHub State Authority → Domain Systems → Local AI → Local Cluster AI → controlled Cloud Development AI → Corporate Development Infrastructure**

Product philosophy:

**Local First → Unified State → Unified UI → AI Assisted → Controlled Cloud Escalation**

The system contains two distinct infrastructure domains:

1. **Local MediaHub Cluster** — user-facing local system inside the user's network.
2. **Cloud Development Cluster / Developer Compute Fabric** — corporate engineering environment, including developer servers and explicitly admitted contributed MediaHub compute.

These domains are not a flat global resource pool and are not a shared user cloud.

## 2. Product boundaries

### 2.1 Local user domain

Includes MediaHub OS/Core, State Authority, Smart Home, Media, Documents, Digital Twin, Engineering, local AI, local cluster services, local network, storage, surveillance and qualified automation.

Local data remains local by default.

### 2.2 Developer domain

Includes developer servers, CI/CD, developer compute, distributed development compute, engineering storage/artifacts, model infrastructure, corporate services and qualified contributed MediaHub compute.

Developer domain is not a user-data domain.

### 2.3 Mobile

Exactly two functional application roles:

- MediaHub Core for iOS/iPadOS: local full-minimal MediaHub Core edition, not a remote client.
- MediaHub Remote Access: separate remote access/management application family.

No mobile application is an authority.

## 3. Authority model

| Domain | Canonical authority |
|---|---|
| Platform canonical state | MediaHub State Authority |
| Smart Home operational/device state | Home Assistant Core |
| Identity/trust | MediaHub Identity architecture |
| Policy | MediaHub Policy architecture |
| Security enforcement | Security architecture + distributed enforcement points |
| Media | Media domain within State Authority boundaries |
| Documents | Document domain |
| Knowledge | Knowledge platform; not authority |
| Digital Twin | Twin domain; not authority |
| Engineering | Engineering domain; not authority |
| AI | AI subsystem; not authority |
| Migration | Migration control plane; not authority |
| Qualification | Qualification control plane; not authority |
| Cloud | Supporting external domain; not canonical state authority |
| Developer Fabric | Corporate development domain; not user-data authority |
| Observability | Non-mutating observability control plane |
| Backup | Recovery mechanism; not authority |
| Update | Lifecycle control plane; not authority |
| Scheduler | Resource allocation mechanism; not authority |
| OSS component | Mechanism/adaptor only; never authority |

Hard invariant: there is one logical MediaHub State Authority, including when physically distributed across qualified nodes.

## 4. Functional invariants

1. MediaHub State Authority is the sole canonical platform-state authority.
2. Home Assistant Core is the Smart Home operational authority.
3. AI is never authority.
4. Cloud is never State Authority.
5. Developer Fabric is never user-data authority.
6. Remote Mobile is not Local Core.
7. Knowledge is not authority.
8. Migration is not authority.
9. Qualification is not authority.
10. Scheduler is not authority.
11. Unknown/unqualified device → DENY or QUARANTINE.
12. Ambiguous critical state → FAIL CLOSED.
13. Qualified local capability continues without Internet/Cloud within its capability profile.
14. Critical canonical state does not use unconditional Last Write Wins.
15. A disconnected secondary MediaHub node does not become an independent canonical authority.
16. AI and external ecosystems cannot bypass MediaHub policy or HA Core.
17. Compute Contribution ≠ User Data Access ≠ Developer Personnel Access.
18. CPRG is registration-only and is not a general VPN gateway.
19. Development Mesh does not imply access to the Media Data Plane.
20. No implementation artifact changes architecture by existence alone.

## 5. Developer privacy boundary

The following boundary is normative:

**User Data X Developer Cloud / Developer Compute Fabric / Developer AI / Developer Personnel Access**

Developer infrastructure is not:

- a user-data mirror;
- a user-data backup;
- a debugging dump;
- a migration staging area;
- a training corpus for user data.

Qualification uses synthetic data, sanitized fixtures, or explicitly permitted non-user data.

For user-originated cloud execution, local processing is preferred. If bounded data must cross a boundary, it is limited by workload contract, privacy classification, minimization, transformation/redaction/encryption/aggregation where feasible, lease duration, output limits and audit rules.

If raw personal data is intrinsically required and cannot be protected from developer access, execution remains local or is denied until an explicit product-level privacy policy exists.

## 6. Identity, trust and security

Security is layered:

- device/node identity;
- cryptographic proof of possession;
- authentication;
- authorization;
- policy;
- capability admission;
- short-lived credentials;
- leases;
- fencing;
- segmentation;
- egress controls;
- attestation where required;
- audit;
- revocation;
- recovery.

CPRG has its own logical authority identity, separate from MediaHub node identity, Developer Infrastructure identity, Provider identity and GitHub/secret-management identity.

CPRG lifecycle:

REQUESTED → AUTHENTICATED → POLICY_APPROVED → LEASE_ACTIVE → TUNNEL_ACTIVE → REGISTRATION_IN_PROGRESS → REGISTRATION_VERIFIED → CLOSED

Failure after lease creation converges to CLOSED.

CPRG VPN is used exclusively for the bounded API-key registration operation. Other MediaHub nodes remain VPN-free. Ordinary Media/Storage/Compute/Internet traffic does not transit CPRG.

## 7. Data classification baseline

| Data class | Owner | Authority | Default residency | Developer domain |
|---|---|---|---|---|
| Identity | MediaHub/user | Identity architecture | Local/control boundary | No raw user identity |
| Secrets | MediaHub/control plane | Secret-management boundary | GitHub/approved secret store | No payload exposure |
| State Authority state | User/MediaHub | State Authority | Local qualified cluster | No |
| Smart Home state | User | HA Core | Local | No raw user data |
| Media | User | Media domain | Local | No by default |
| Camera recordings | User | Surveillance/media domain | Local | No |
| Documents | User | Document domain | Local | No by default |
| Knowledge | User/MediaHub | Knowledge platform | Local first | Sanitized/approved only |
| Digital Twin | User/project | Twin domain | Local first | Approved engineering artifacts only |
| Engineering | User/company | Engineering domain | Local/project boundary | Approved company workload only |
| AI context | User/workload | Domain contract | Local first | Only policy-approved bounded data |
| AI models | MediaHub/company | Model registry | Qualified registry | Yes for corporate models |
| Telemetry | MediaHub | Observability | Minimized/local first | Sanitized only |
| Audit | MediaHub | Audit/evidence control | Controlled durable store | No personal payloads |
| Backups | User/MediaHub | Recovery policy | Local/approved DR | No unrestricted developer access |
| Configuration | User/MediaHub | State Authority | Local | No |
| Policies | MediaHub | Policy architecture | Controlled local/control plane | No arbitrary modification |

Backup, migration and deletion follow the governing data-class policy. Retention is not globally indefinite by default.

## 8. Capability model

Device names do not define capability.

Canonical chain:

**Hardware Detection → Qualification → Capability Profile → Policy Admission**

Capability profile may include:

CPU, GPU, NPU, RAM, NVMe, HDD, Ethernet, Wi-Fi, network bandwidth, Thunderbolt, USB4, display, camera, media acceleration, AI acceleration, storage throughput, thermal envelope, power envelope and reliability.

Capability drift requires requalification or policy downgrade.

A capability profile is evidence-backed metadata, not authority.

## 9. Platform model

There is one MediaHub architecture plus platform-specific implementation.

Supported/target profiles:

- Linux;
- macOS;
- iPadOS Core;
- Raspberry Pi / specialized profiles.

Clean Mac mini/Mini PC installations use Linux as the baseline implementation direction. Apple platforms remain integrated platform adaptations where the base OS cannot be replaced.

Platform differences must not create independent architecture branches.

## 10. Node and cluster model

A single node is valid.

A qualified multi-node MediaHub cluster may provide:

- distributed State Authority;
- HA;
- distributed storage;
- compute;
- AI;
- media;
- network/mesh;
- Wi-Fi mesh;
- qualified redundancy.

Cluster formation:

**Discovery → Capability Qualification → Trust → Proposal → User Confirmation → Admission → Operation**

No node becomes a cluster member merely because it is discoverable.

Critical failure domains, leadership, quorum, replication, split-brain prevention and recovery remain implementation/qualification concerns of the single logical State Authority.

## 11. Developer Compute Fabric

The developer environment is a heterogeneous distributed compute fabric composed of:

- developer Mac mini nodes;
- Linux developer servers;
- qualified MediaHub compute contributors;
- other explicitly admitted development resources.

A **Primary Development Node** is a dynamic role, not a permanent master. Selection must use measured/qualified compute and operational properties rather than CPU/GPU marketing numbers alone:

CPU, GPU/NPU, RAM, NVMe I/O, network, HIGH_SPEED links, storage bandwidth, reliability/uptime, thermal/power headroom and control-plane capability.

Primary ≠ sole authority and ≠ SPOF.

High-speed developer interconnect may use qualified Thunderbolt/USB4 networking. It is a dedicated developer-plane fabric and must not carry ordinary user MediaHub traffic. RDMA is optional and requires independent qualification.

Compute Contribution is request-scoped, capability-scoped, lease-based, isolated, auditable and revocable.

## 12. Network model

Logical planes:

1. Internet/WAN.
2. Local Media Mesh.
3. Development Mesh.
4. HIGH_SPEED developer fabric.
5. Optional Storage Network.
6. Compute Contribution Plane.
7. Protected Registration Plane / CPRG.
8. API Egress.

Default routing is direct unless a policy explicitly selects another path.

Media data is local/direct by default.

Development Mesh is for authorized management/discovery/control traffic.

HIGH_SPEED is reserved for qualified developer compute/storage transport.

CPRG is not a general gateway, NAT, proxy or transit path.

Seamless wireless coverage is a required functional outcome. AP/radio, controller, gateway/router, switching, backhaul, management, roaming and interoperability are separate capabilities that require qualification.

MediaHub may use wired Ethernet as Internet upstream/backhaul for AP functionality where the deployment profile supports it.

Personal VPN is a user-configurable MediaHub gateway capability; exact provider/protocol/traffic policy remains an open implementation decision.

## 13. Storage and persistence

Canonical baseline:

- transactional State Authority storage;
- relational storage;
- filesystem/domain storage;
- object storage;
- search/index;
- graph;
- vector storage where justified;
- media storage;
- archive;
- backup.

PostgreSQL + pgvector + S3-compatible object storage remain the functional baseline. Qdrant is conditional on benchmark evidence.

Every persisted object must be classified as:

- authoritative;
- derived;
- rebuildable;
- cached;
- historical.

No cache, search index, vector store, graph or object store may silently become State Authority.

Transactional state publication follows the authoritative-store-first rule and may use an outbox for event delivery.

## 14. Smart Home

HA Core remains the operational authority for Smart Home device state.

MediaHub State Authority owns platform identity/lifecycle/policy/cross-domain references.

Lifecycle:

Discover → Identify → Authenticate → Detect Capability → Trust → Qualify → Admit → Integrate → Operate → Observe → Update → Revoke

AI and external ecosystems do not bypass HA Core.

Duplicate discovery must not create multiple simultaneous owners for one device. Takeover is class/policy controlled.

## 15. Media

Media is local-first and includes:

audio, video, playback, streaming, multiroom, local/network media, HDMI, 4K, phone endpoints, gaming, projection, TV/source integration where qualified, speakers, AVR and codecs/transcoding subject to platform capability and rights.

**TV/source recording is not an obligatory Media capability.**

Camera recording remains a separate hardware-dependent surveillance capability.

DRM, rights and vendor restrictions remain explicit compliance constraints.

## 16. Documents and Knowledge

Documents include OCR, classification, metadata, search, provenance, extraction and workflows.

Knowledge includes semantic/full-text search, graph relations, provenance, evidence, temporal relations, source verification and AI context.

Knowledge is not authority.

AI-generated knowledge is not automatically verified.

## 17. Digital Twin and Engineering

Digital Twin is part of Full editions, not a separate OS.

Capabilities may include:

2D/3D, BIM, CAD, equipment, engineering systems, spatial model, simulation, project state, as-built data, calculations, diagrams, cable journals and engineering project packages.

Professional capabilities are entitlement-controlled.

Engineering and Digital Twin artifacts require provenance, authorization, licensing review and qualification before production use.

## 18. AI architecture

Tiers:

- Local AI;
- Local Cluster AI;
- Cloud Development AI.

Model routing is subordinate to policy and workload classification.

AI may explain, propose, analyze, search verified sources, assist configuration and create artifacts within policy.

AI cannot directly obtain physical authority, canonical state authority or security bypass.

AI provider/model availability is evidence-based. Current provider qualification history is not equivalent to architectural availability; e.g. OpenAI direct is not a qualified current execution dependency, while UnoRouter/ZeroRouter remain retained credentials with current inference limitations documented separately.

## 19. Update / Recovery / Migration

Unified lifecycle:

**Detect → Qualify → Backup → Stage → Checkpoint → Change → Validate → Requalify → Cutover → Observe → Accept → Retire**

Update uses explicit user confirmation where required by product policy.

RAUC remains the target OTA mechanism. Mender is reference/integration material and must not become a second production update authority without a new decision.

Migration must preserve State Authority identity, contracts, provenance, security and data integrity.

Migration is not authority.

## 20. Qualification model

Qualification is an independent control plane.

Distinguish:

Architecturally Defined → Planned → Implemented → Verified → Qualified → Production Authorized.

No self-review is independent qualification.

Operational qualification includes functional, contract, integration, negative-path, security, privacy, recovery, migration, provenance and production-admission gates.

Current Astra/GOLD evidence is historical execution evidence, not blanket proof that the entire MediaHub system is production-qualified.

GOLD #176 is not a 24h GOLD pass: it ended in runner shutdown after approximately 14 hours. GOLD #177 was an old push-triggered run and is not the canonical explicit-admission GOLD run. These facts remain operational provenance, not architecture status.

## 21. OSS and supply chain

Adoption rule:

**Capability Gap → Mature Search → License → Security → Provenance → Adapter → Benchmark → Adoption**

External components are subordinate mechanisms. MediaHub owns authority contracts.

Current architecture candidates include Home Assistant, PostgreSQL, pgvector, Temporal, OpenTelemetry, Prometheus, Cosign/Sigstore, Syft, Trivy, restic, RAUC, OpenBao, OCI tooling, Ray, NATS/JetStream, containerd/OCI, SPIFFE/SPIRE, Netmaker/WireGuard, SeaweedFS, Buf/Protovalidate, gRPC and optional Cilium/eBPF.

Nomad remains a secondary candidate subject to license review. No candidate is production-authoritative merely by appearing in the architecture.

## 22. API and event model

Domains communicate through versioned contracts.

Core compute protocol:

**Capability → Admission → Lease → Dispatch → Heartbeat → Result → Evidence → Revoke/CLOSED**

Transport is subordinate to protocol semantics.

Candidate bindings:

- gRPC/HTTP2 for bounded control;
- NATS/JetStream for asynchronous events;
- local IPC for node execution.

Transport acknowledgement is not proof of authoritative state commit.

Idempotency, deadlines, cancellation, replay resistance, stale epoch/fencing and transactional state/event publication are mandatory.

## 23. Observability

Observability includes metrics, logs, traces, health/readiness, diagnostics, alerts and audit.

OpenTelemetry/Prometheus are target technologies.

Forbidden in developer-facing telemetry:

- API keys;
- private keys;
- personal media;
- user filesystem contents;
- raw sensitive provider/model payloads;
- personal payloads in evidence.

Operational identifiers are allowed when they do not reveal protected payloads.

## 24. Resource management

Resource management covers:

CPU, GPU, NPU, memory, storage, network, Thunderbolt/USB4, reservations, leases, thermal/power envelopes, workload placement and rescheduling.

Resource Manager and scheduler allocate resources; they do not own canonical system authority.

Placement must be capability-aware and performance-aware. Large local datasets should be processed near their data when policy permits.

## 25. User experience

Unified MediaHub UI hides implementation topology.

UI is minimal, mostly gray, intuitive, macOS-like in interaction quality while retaining MediaHub identity.

Technical backend components, databases, schedulers and network planes are not exposed as separate user products unless required for administration.

## 26. Product editions and paid boundaries

Editions:

- MediaHub OS Full for Mac mini;
- MediaHub OS Full for Mini PC;
- Hub OS Raspberry Pi;
- MediaHub Core iOS/iPadOS;
- MediaHub iOS Remote;
- OS Developer;
- iOS Developer.

Paid boundaries include Document, Digital Twin professional, Engineering and relevant commercial capabilities.

Digital Twin is not a separate OS.

## 27. Lifecycle and device management

Device lifecycle follows:

Discover → Identify → Authenticate → Capability → Trust → Qualify → Admit → Integrate → Operate → Observe → Update → Revoke.

Unknown/untrusted devices are denied or quarantined.

Capability drift, identity revocation, ownership change and failed qualification must converge to a safe state.

## 28. Functional 68-section reconciliation

| # | Passport section | Baseline 2.0 status | Implementation status |
|---:|---|---|---|
| 1 | Назначение | RECONCILED | PARTIALLY_IMPLEMENTED |
| 2 | Архитектурная модель | RECONCILED | PARTIALLY_IMPLEMENTED |
| 3 | State Authority | RECONCILED | PARTIALLY_IMPLEMENTED |
| 4 | Home Assistant Core | RECONCILED | PLANNED/PARTIAL |
| 5 | UI | RECONCILED | PLANNED/PARTIAL |
| 6 | Smart Home | RECONCILED | PLANNED/PARTIAL |
| 7 | Manufacturers | RECONCILED | PLANNED / qualification-gated |
| 8 | Kincony/KCS | RECONCILED | PLANNED |
| 9 | Wired protocols | RECONCILED | PLANNED |
| 10 | Wireless | RECONCILED | PLANNED |
| 11 | Virtual Ubiquiti Server | RECONCILED | PLANNED |
| 12 | Smart Home Automation | RECONCILED | PLANNED/PARTIAL |
| 13 | Voice | RECONCILED | PLANNED |
| 14 | AI architecture | RECONCILED | PARTIALLY_IMPLEMENTED |
| 15 | Local AI | RECONCILED | PARTIALLY_IMPLEMENTED |
| 16 | Local Cluster AI | RECONCILED | PLANNED/PARTIAL |
| 17 | Cloud Development AI | RECONCILED | PARTIALLY_IMPLEMENTED |
| 18 | Trusted Sources Intelligence | RECONCILED | PLANNED |
| 19 | AI Human Clone | RECONCILED | PLANNED |
| 20 | Mobile Access Layer | RECONCILED | PLANNED/PARTIAL |
| 21 | Mobile invariants | RECONCILED | ARCHITECTURE_DEFINED |
| 22 | iPhone Media | RECONCILED | PLANNED |
| 23 | Media System | RECONCILED | PLANNED/PARTIAL |
| 24 | Document System | RECONCILED | PLANNED |
| 25 | Digital Twin | RECONCILED | PLANNED |
| 26 | Engineering System | RECONCILED | PLANNED |
| 27 | Network Architecture | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 28 | Equipment discovery | RECONCILED | PARTIALLY_IMPLEMENTED |
| 29 | Smart Home export | RECONCILED | PLANNED |
| 30 | Product Editions | RECONCILED | ARCHITECTURE_DEFINED |
| 31 | Paid functions | RECONCILED | PLANNED |
| 32 | Update System | RECONCILED | PARTIALLY_IMPLEMENTED |
| 33 | Backup/Recovery | RECONCILED | PARTIALLY_IMPLEMENTED |
| 34 | Security | RECONCILED | PARTIALLY_IMPLEMENTED |
| 35 | Cloud security | RECONCILED | PARTIALLY_IMPLEMENTED |
| 36 | Local First | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 37 | Cluster | RECONCILED | PARTIALLY_IMPLEMENTED |
| 38 | New devices | RECONCILED | PARTIALLY_IMPLEMENTED |
| 39 | Observability | RECONCILED | PARTIALLY_IMPLEMENTED |
| 40 | Data/Storage | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 41 | Knowledge/Search | RECONCILED | PARTIALLY_IMPLEMENTED |
| 42 | AI Escalation | RECONCILED | PARTIALLY_IMPLEMENTED |
| 43 | OSS Foundation | RECONCILED | PARTIALLY_IMPLEMENTED |
| 44 | OSS Adoption Rule | CONFIRMED | IMPLEMENTED as governance |
| 45 | Architectural prohibitions | CONFIRMED | IMPLEMENTED as governance |
| 46 | Production/qualification gates | RECONCILED | PARTIALLY_IMPLEMENTED |
| 47 | Git/provenance | RECONCILED | IMPLEMENTED for repository governance |
| 48 | Autonomous development | RECONCILED | IMPLEMENTED as governance |
| 49 | Developer ecosystem | RECONCILED | PARTIALLY_IMPLEMENTED |
| 50 | Overall chain | RECONCILED | ARCHITECTURE_DEFINED |
| 51 | Mobile chain | RECONCILED | ARCHITECTURE_DEFINED |
| 52 | Smart Home chain | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 53 | AI chain | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 54 | Cloud Development structure | RECONCILED | ARCHITECTURE_DEFINED/PARTIAL |
| 55 | UX | RECONCILED | PLANNED |
| 56 | AI principle | CONFIRMED | GOVERNANCE_IMPLEMENTED |
| 57 | Smart Home principle | CONFIRMED | GOVERNANCE_IMPLEMENTED |
| 58 | Mobile principle | CONFIRMED | ARCHITECTURE_DEFINED |
| 59 | Cloud AI principle | CONFIRMED | ARCHITECTURE_DEFINED |
| 60 | Voice order | CONFIRMED | PLANNED |
| 61 | Update principle | CONFIRMED | PARTIALLY_IMPLEMENTED |
| 62 | Local-first | CONFIRMED | ARCHITECTURE_DEFINED/PARTIAL |
| 63 | Functional model | RECONCILED | ARCHITECTURE_DEFINED |
| 64 | Architectural invariant | CONFIRMED | GOVERNANCE_IMPLEMENTED |
| 65 | Qualification | RECONCILED | PARTIALLY_IMPLEMENTED |
| 66 | Release | CONFIRMED | GOVERNANCE_IMPLEMENTED |
| 67 | Final architectural baseline | RECONCILED | ARCHITECTURE_DEFINED |
| 68 | Development chain | CONFIRMED | GOVERNANCE_IMPLEMENTED |

**Important:** the implementation labels above are conservative architecture-to-repository assessments. They are not production qualification claims.

## 29. Major contradictions and resolutions

### C-01 — Functional Baseline 1.0 vs MH-03 runtime foundation
**Conflict:** Baseline 1.0 defines future persistent/distributed capabilities while MH-03 froze an earlier minimal runtime foundation.

**Resolution:** MH-03 remains historical foundation provenance. Functional Baseline 2.0 is the reconciled target architecture; persistent/distributed capabilities require implementation and qualification gates.

### C-02 — Last Write Wins for critical state
**Conflict:** older distributed-state material could permit generic LWW semantics.

**Resolution:** unconditional LWW is rejected for critical canonical state. Strong consistency / explicit authority epoch / fencing / fail-closed conflict handling apply.

### C-03 — Flat federation / global VPN interpretation
**Conflict:** earlier federation wording could imply one global resource network.

**Resolution:** hierarchical Local MediaHub Cluster + separate Cloud Development Cluster. Compute Contribution is request-scoped; no global full-tunnel.

### C-04 — Developer compute vs user data
**Conflict:** aggregate developer compute could be interpreted as access to local user resources.

**Resolution:** Compute Contribution, User Data Access and Developer Personnel Access are independent authorization domains. Personal user data stays local unless an explicit privacy policy permits bounded processing.

### C-05 — CPRG as general VPN gateway
**Conflict:** protected registration could be interpreted as general transit.

**Resolution:** CPRG VPN is exclusively for bounded API-key registration. CPRG is not NAT/proxy/transit/default gateway.

### C-06 — Primary Development Node as permanent master
**Conflict:** selecting the strongest server could create a master/SPOF.

**Resolution:** Primary Development Node is a dynamic operational role selected from qualified measurements. It is not the authority and not a permanent master.

### C-07 — iPad Core vs Remote Mobile
**Conflict:** older wording could conflate iPad MediaHub OS with remote access.

**Resolution:** iPad/iPadOS Core is a local full-minimal MediaHub OS edition; Remote Mobile is a separate application family.

### C-08 — TV/source recording
**Conflict:** generic media scope could imply mandatory TV/source recording.

**Resolution:** TV/source recording is not mandatory Media capability.

### C-09 — R4 SHA provenance discrepancy
**Conflict:** historical passport text and project declaration contain a SHA formatting discrepancy.

**Resolution:** immutable declared R4 anchor remains unchanged; no silent correction. Machine verification remains a separate technical reconciliation item.

## 30. Open decisions that remain genuinely unresolved

1. Exact State Authority replication/leader-election/quorum implementation.
2. Exact consistency class schema and transaction boundaries beyond the reconciled classes.
3. HA Core owner takeover semantics per Smart Home safety class.
4. API Gateway and Security/Egress Gateway concrete topology.
5. Final IP/VLAN/VRF/firewall/DNS/DHCP/service-discovery network implementation.
6. Final seamless-Wi-Fi/roaming mechanism and vendor qualification.
7. Personal VPN protocol/provider and per-network/per-client policy.
8. Final high-speed Mac mini topology and whether/where RDMA is justified.
9. Distributed storage implementation after benchmark.
10. Developer Fabric primary-node election algorithm and scheduler implementation.
11. Exact compute-contribution workload classes and contributor opt-in UX.
12. Exact bootstrap/trust-root/cryptographic formats for CPRG.
13. Revocation-state distribution and recovery-authority custody.
14. Data retention/deletion schedules by legal/product class.
15. Exact mobile hardware capability matrix and iPad Core runtime packaging.
16. Subscription/entitlement enforcement implementation.
17. Final AI model-router/provider policy and benchmark-based production selection.
18. Exact Digital Twin/Engineering entitlement and artifact model.
19. Production qualification evidence for each product edition.
20. Final Reference Architecture after owner acceptance of this baseline.

These are not repeated MH-1…MH-23 questions; they are the remaining implementation/qualification decisions identified by reconciliation.

## 31. Rejected options retained as provenance

- Second independent MediaHub State Authority.
- AI as canonical State Authority.
- Cloud as uncontrolled authority.
- AI direct physical-device authority.
- Bypass of Home Assistant Core.
- Flat global VPN/federated resource pool.
- Permanent full-tunnel Local-to-Cloud architecture.
- CPRG as general VPN/NAT/proxy/transit gateway.
- Developer personnel access to user personal data.
- Compute contribution implying user-data federation.
- Permanent Primary Development Node/master.
- Unconditional Last Write Wins for critical state.
- Multiple competing production OTA authorities without decision.
- Multiple production AI runtimes without benchmark.
- Reference OSS product as core authority.
- Self-review as independent qualification.
- Mandatory TV/source recording capability.
- Provider-specific network workaround for regional restrictions.

## 32. Canonical document map

Current canonical candidates after MH-24 reconciliation:

- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — immutable historical baseline.
- `docs/checkpoints/mediahub-master-architecture-reconciliation.md` — reconciliation history/control record.
- `docs/checkpoints/2026-09-30-mediahub-implementation-blueprint.md` — implementation blueprint.
- `docs/checkpoints/2026-09-30-mediahub-architecture-gaps-and-pushback.md` — gap/pushback register.
- `docs/checkpoints/2026-09-30-mediahub-compute-wire-protocol-v1.md` — compute protocol.
- `docs/checkpoints/2026-09-30-mediahub-hierarchical-cluster-architecture.md` — cluster/federation architecture.
- `docs/checkpoints/2026-09-30-cloud-development-fabric-reference-architecture.md` — developer fabric.
- `docs/checkpoints/2026-09-30-mediahub-network-infrastructure-reference-architecture-v1.md` — network reference architecture.
- CPRG threat/identity/bootstrap documents — security architecture.
- **`docs/checkpoints/mediahub-functional-baseline-2.0.md` — this document.**

A separate final Reference Architecture is intentionally deferred until Functional Baseline 2.0 owner acceptance.

## 33. Traceability and provenance

Primary source classes:

1. User-supplied 68-section passport in MH-24.
2. MH-1…MH-23 historical decisions.
3. Canonical checkpoint documents in GitHub.
4. Current repository implementation/evidence.

Key current GitHub evidence anchors include:

- repository HEAD at reconciliation start: `863e61783272e0107ce74ab1620212285946aca8`;
- Section 2 closure: `38110d7610845874b7287313eee251c289ed5604`;
- Section 3 closure: `f7ab2f4a2a1cab463466a87d344f0261ce7da48a`;
- Section 4 reconciliation: `863e61783272e0107ce74ab1620212285946aca8`;
- compute protocol hardening: `313f257529fbc8b2d732467355c42eb0d1be5a03`;
- implementation blueprint: `dfc2478b663bf88a2aef27b5ef30db17a36f9a9e`;
- cloud development fabric: `038cb7460b32281e419396dd106c0228b834b693`;
- network passport extension: `b2eafbe42e16ae877487572b5006272679fdc93f`;
- CPRG threat model hardening: `286c1457b73c6376a3c7fe18b9a900fe3e2b8216`;
- CPRG trust contract: `c57e0161885695ec0ddffad35dc57fba3271ef70`;
- CPRG bootstrap/recovery: `4b0840b087326af828377d5a2ec03b6b7066f1fd` (historical checkpoint commit).

Qualification evidence is referenced by its own evidence records and must not be inferred from these documentation commits.

## 34. Baseline acceptance rule

This document becomes the immutable Functional Baseline 2.0 reference only after explicit owner acceptance.

After acceptance:

- content is not silently edited;
- changes require a new baseline/revision;
- provenance remains preserved;
- architecture and implementation remain separate;
- every implementation claim requires fresh evidence.

**Current status: RECONCILED CANDIDATE — NOT YET OWNER-ACCEPTED.**
