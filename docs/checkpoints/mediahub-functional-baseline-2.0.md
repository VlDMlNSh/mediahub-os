# MEDIAHUB OS / MEDIAHUB iOS
# FUNCTIONAL BASELINE 2.0

**Document status:** ACCEPTED — CANONICAL IMMUTABLE REFERENCE POINT  
**Version:** 2.0.0  
**Architecture revision:** MH-24 / 2026-10-01  
**Scope:** MediaHub OS 11.x LTS / MediaHub iOS and associated development infrastructure  
**Supersedes:** Functional Baseline 1.0 as the current functional reference, while preserving Baseline 1.0 as immutable historical provenance.

## 0. Acceptance and authority

This document is the accepted Functional Baseline 2.0 produced by MH-24 reconciliation. It reconciles the user-supplied 68-section functional passport, MH-1…MH-23 decisions, canonical checkpoint documents, and the current GitHub repository state.

Acceptance does **not** claim implementation, verification, qualification or production merely because an architectural artifact exists. The following states remain distinct:

- Requirement
- Decision
- Architecture
- Implementation
- Evidence
- Historical Record
- Open Decision
- Rejected Option
- Verified
- Qualified
- Production Authorized

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

Exactly two functional application roles are retained in the baseline product architecture:

- MediaHub Core for iOS/iPadOS: local full-minimal MediaHub Core edition, not a remote client.
- MediaHub Remote Access: separate remote access/management application family.

Developer Mobile is a separate developer-only application surface and is governed by the Developer Domain boundary; it is not a Remote Access client and does not gain user-data access by virtue of developer status.

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
- Raspberry Pi / specialized profiles;
- iOS Developer Mobile;
- iOS Remote Access.

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

## 23. Traceability and provenance

The 68 passport sections are reconciled in `docs/checkpoints/mediahub-mh24-traceability-matrix.md`.

MH-1…MH-23 remain historical architectural provenance. Functional Baseline 1.0 remains preserved and is superseded as the current functional reference by this accepted Baseline 2.0.

Key MH-24 provenance:

- Baseline candidate creation commit: `26de2e57316155e32e540ce43349b4cd124873c2`.
- Baseline candidate blob SHA: `e01c37e9fe15f91dc5c3ccdab40a47bc281fcfb8`.
- Traceability matrix creation commit: `7bbb0dcdd591a48b0371accfab33c6b933821293`.
- Traceability matrix blob SHA: `8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6`.
- Master reconciliation update commit: `633d734e0a741413bbcdc0d1d00f08bc0a256fe5`.
- Master reconciliation blob SHA: `f3a66e292302984be95ae8085f17e03cd538baae`.

The acceptance update is the controlled successor to the candidate artifact. The accepted file is now the canonical functional reference; future changes require an explicit architectural change process and a new baseline revision.

## 24. MH-24 closure criteria

MH-24 closure is based on the reconciliation evidence recorded in `mediahub-mh24-reconciliation-report.md`:

- full passport received;
- all 68 sections represented and reconciled;
- MH-1…MH-23 reconciled;
- authority, security and privacy boundaries reconciled;
- capability, platform and cluster models reconciled;
- persistence, network, Smart Home, Media, Documents, Knowledge, Digital Twin, Engineering, AI, Compute Fabric and Cloud reconciled;
- update/recovery/migration and qualification models reconciled;
- contradictions registered and resolved or explicitly carried as implementation/open items;
- GitHub drift identified;
- canonical document set established;
- Baseline 2.0 produced and synchronized;
- historical provenance preserved;
- no implementation status falsely inferred.

## 25. Open implementation / qualification work carried forward

The following are intentionally downstream of MH-24 and do not invalidate the accepted functional baseline:

1. State Authority leader election/quorum/replication implementation.
2. Exact consistency-class schema and transaction boundaries.
3. HA takeover policy by safety class.
4. API Gateway/Security-Egress Gateway topology.
5. Final IP/VLAN/VRF/firewall/DNS/DHCP/discovery implementation.
6. Wi-Fi roaming/controller/interoperability qualification.
7. Personal VPN provider/protocol/traffic policy.
8. Thunderbolt/USB4 topology and RDMA applicability.
9. Distributed storage implementation.
10. Primary Development Node election and scheduler algorithm.
11. Compute Contribution workload classes and UX.
12. CPRG cryptographic/bootstrap formats and custody.
13. Data retention/deletion schedules.
14. Mobile capability matrix and packaging.
15. Entitlement/subscription enforcement.
16. Production AI model-router/provider policy.
17. Digital Twin/Engineering entitlement and artifact implementation.
18. Product-edition production qualification evidence.

These are implementation/qualification work items for the next stages and are not unresolved contradictions in the accepted baseline.

## 26. Canonical status

**FUNCTIONAL BASELINE 2.0 — ACCEPTED / CANONICAL / IMMUTABLE REFERENCE POINT**

This document is the functional reference for subsequent Reference Architecture, Reference Implementation Blueprint, implementation, verification and qualification work.

It does not claim that those downstream stages are already complete.

Baseline 1.0 remains retained as historical provenance.
