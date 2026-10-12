# MediaHub OS / MediaHub iOS — System Passport v3

**Document ID:** MH-SYSTEM-PASSPORT-V3-DRAFT-01  
**Revision date:** 2026-10-12  
**Branch:** docs/mediahub-chat-tree-map-20261012  
**Status:** RECONCILED SYSTEM VIEW / DRAFT — NOT A NEW ACCEPTED FUNCTIONAL BASELINE  
**Related integration contract:** docs/architecture/MEDIAHUB-UNIFIED-ARCHITECTURE-CONTRACT-V3-DRAFT-01.md  
**Governing functional reference:** Functional Baseline 2.0, main blob SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f  
**Historical source passport:** Functional Baseline 1.0, main blob SHA 9df4892ed0734050ac79732603d15bb414717310

## 1. Executive system definition

MediaHub is one local-first platform architecture spanning MediaHub OS/Core, MediaHub iOS, Smart Home, media, documents, knowledge and digital-twin capabilities, local AI, local cluster services, network/storage/security functions, and a separate developer/engineering fabric.

Its design principle is:

**Local First → Unified State → Unified UI → AI Assisted → Controlled Cloud Escalation.**

The target product is broader than any one host or runtime. Capability is determined by an explicitly qualified hardware/software profile, not inferred from the brand or model name. The architecture may be deployed as a single node or across qualified nodes, while retaining one logical MediaHub Product State Authority and explicit domain boundaries.

This passport consolidates the accepted target and current evidence. It does not mean all described capabilities are implemented, verified, qualified, released, deployed or production accepted.

## 2. Document and authority status

The accepted Functional Baseline 2.0 is the current functional reference, as declared in its own acceptance section and MH-24 reconciliation report. Functional Baseline 1.0 remains the immutable literal source for the edition-1.0 passport. B1 and B2 are not to be silently merged, and the source SHA must be pinned for every requirement mapping.

This working branch contains a stale branch-local file at the B1 path: SHA 1a2f06f50dd69990be58b12a98376b92f12fd14f, 296 lines. The controlling main version of B1 is SHA 9df4892ed0734050ac79732603d15bb414717310, 1,111 lines. Source line spans in this passport and downstream mapping must use main SHA, not the branch-local copy. The branch copy has been preserved.

This v3 passport is a reconciled system view, not a new accepted baseline. It cannot override the accepted B2, frozen P0 contracts, scoped domain contracts, the governance decision register, or qualification evidence.

## 3. Product purpose and boundaries

MediaHub's purpose is to provide a unified local-first operating and application environment whose capabilities can grow by qualified hardware profile. Product state and policy remain under MediaHub authority. Smart Home state remains under Home Assistant Core in its domain. AI, cloud services, workflow engines, plugins, devices, adapters, persistence systems and transports do not acquire product authority by connection or implementation choice.

The system has at least three explicit boundaries:

1. **User/product domain:** Core runtime, authority, Smart Home, UI/mobile, media, documents, knowledge/digital twin, local AI, network, device integration, recovery and update functions.
2. **Developer/engineering domain:** source repositories, task scheduling, execution workspaces, build/test/verification, component admission, development compute and evidence.
3. **External/cloud domain:** optional providers, controlled API egress, cloud development and external compute, admitted only by trust/privacy/policy and workload-placement gates.

These domains may cooperate through explicit contracts, but their credentials, authority, data classification and lifecycle are not implicitly shared.

## 4. Canonical logical architecture

Product chain:

**Physical/platform profile → MediaHub OS/Core → MediaHub Product State Authority → domain systems/contracts → local AI → local cluster AI/compute → controlled Cloud Development AI → corporate development infrastructure.**

This is a logical chain, not a claim that every layer must run on every node. Platform adaptations and reduced-capability profiles are valid if they preserve the same authority, security and contract semantics.

### 4.1 Authority graph

| Layer | Responsibility | Authority boundary |
|---|---|---|
| Human/product owner | Requirements, product decisions, explicit governance decisions, release and production approvals where applicable | Human approval cannot be replaced by automation or a generated status |
| MediaHub Product State Authority | Canonical platform state, identity/lifecycle/policy and cross-domain canonical references | Sole canonical platform mutation authority |
| Home Assistant Core | Smart Home device and operational state, integrations and Smart Home automation | Sole Smart Home operational authority under its approved scope |
| Core Runtime Services | Lifecycle coordination, runtime sequencing, bounded readiness and diagnostics | Runtime coordinates; it does not mutate canonical state directly |
| Domain contracts/services | Media, documents, knowledge, digital twin, engineering, network and other domain behavior | Domain state/actions are mediated by the applicable domain contract and product authority boundaries |
| Local AI and agents | Local inference, retrieval, proposals and permitted tool use | Advisory/proposal role by default; no implicit platform authority |
| Local cluster services | Qualified distributed workloads, local compute, storage and selected network services | Must not create competing product authority or bypass admission/privacy policy |
| Cloud Development AI / external services | Optional admitted external development/inference capability | External security domain; never canonical product state authority |
| ASTRA GOLD | Distributed autonomous engineering coordination and qualification evidence | A0 is ASTRA engineering coordination/internal queue authority, not MediaHub Product State Authority |

### 4.2 Required state-changing path

Command/request → schema/freshness validation → identity/trust/authorization/policy → consumer/integration contract → Product State Authority → canonical mutation/revision → event/fact → observers.

Events are facts, not commands. UI, AI, workflow engines, plugins, devices, transport, cloud and persistence cannot create a hidden direct mutation path. State Authority failure never creates a second authority; critical ambiguous or conflicting state fails closed.

State must retain distinctions among reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted. These distinctions are required so a proposal or sent command cannot be mistaken for a committed or physically confirmed outcome.

## 5. Runtime baseline versus desired architecture

The current MH-03 runtime foundation remains PROPOSED. It identifies a single-node, in-memory State Authority, no high availability, and no authorized physical persistence in that foundation. Frozen P0-03 through P0-05 semantics remain controlling; the accepted P0-06 contract is scoped to the runtime services it defines.

B2's product target allows a single logical Product State Authority to be physically distributed across qualified nodes. This is not permission to implement distributed writes, failover, replication, quorum or persistence without the corresponding accepted design and qualification. A disconnected secondary node must not become an independent critical-state authority.

The future target therefore has two separately tracked dimensions:
- **Logical product target:** one architecture, one logical Product State Authority, explicit domains and qualified capability profiles.
- **Current executable foundation:** single-node/in-memory runtime under the present MH-03/P0 constraints; persistence and HA remain future-gated.

## 6. Deployment and hardware profiles

A system profile is the tuple: hardware identity + OS/runtime version + enabled capabilities + admitted components/providers + trust/security configuration + source revision + qualification evidence.

| Profile | Intended capabilities | Current status and constraints |
|---|---|---|
| Mac mini / Mini PC | Local full-capability node, developer node, media/local AI and networking capabilities where supported | B2 records Linux as the clean-install direction where supported; qualify exact model, OS and components before claiming feature support |
| Mac Pro / accelerator-capable workstation | Future higher-throughput local AI/media/compute, accelerator workloads and possible cluster contribution | Roadmap target only in this passport; not asserted as accepted B2 support, implemented or qualified |
| Apple platform adaptation | Common MediaHub interfaces/contracts on platforms where the base OS cannot be replaced | Platform-constrained adaptation; capability matrix must document unavailable or changed functions |
| Raspberry Pi / specialized low-power node | Local control and supported integration/edge duties with reduced resource profile | Capability-specific; do not infer high-throughput media, storage or local-recording capacity |
| iPad Core / wall panel | Local or wall-panel capabilities permitted by platform entitlements and accepted edition model | Must be distinguished from the Remote client; validate device/OS capabilities |
| iOS/Android Remote | Authorized remote access to MediaHub APIs and supported subsystems | Not equivalent to a full local MediaHub Core |
| Local cluster node | Qualified CPU/GPU/media/compute/storage/network tasks under admission and isolation | Node-specific admission, capacity, trust, fault-domain and recovery evidence required |
| Cloud/remote compute | Optional remote provider/GPU/workload contribution | Separate trust domain; explicit data-egress and placement policy; not required for local-first core capability |

No product capability follows solely from a hardware label. A future Mac Pro profile must qualify exact GPU/memory capacity, thermals, power, storage, network, identity, isolation and recovery before production admission. A node that contributes compute remains an executor for admitted jobs, not a second Product State Authority.

## 7. User, system and developer capabilities

The feature catalog remains defined by the accepted baselines and domain contracts. The following grouped view is a navigation aid, not a substitute for the 68-section B1/B2 traceability:

| Capability group | System responsibility | Principal authority/contract |
|---|---|---|
| Core runtime and lifecycle | Boot, configuration validation, readiness, lifecycle, failure/degraded mode and deterministic operation | MH-03/P0-03…P0-06 |
| Smart Home and devices | Integration, normalized devices/entities, commands, automations, device trust, protocol support | Home Assistant Core plus MediaHub integration/device contracts |
| Unified UI and mobile | A coherent UI over authorized APIs; local Core versus Remote client boundaries | UI, API, mobile and platform capability contracts |
| Media and surveillance | Media ingestion, playback/processing, metadata, storage and applicable recording profiles | Media-domain contract, storage and data-plane policies |
| Documents, knowledge and digital twin | Document indexing/retrieval, source provenance, knowledge references, geometry and engineering context | Domain contracts under the platform authority boundary |
| Local AI | On-device/local models, inference and retrieval, tool-scoped agents | Model/provider qualification, privacy/data-classification and tool policies |
| Cluster AI/development compute | Qualified task distribution to local nodes, isolation, scheduling, result provenance and resource control | MediaHub-owned compute/admission/lease/evidence contracts |
| Network and access | Gateway/controller/AP/VPN/network functions where profile-supported | Network/security/equipment qualification; independent control, transport and data planes |
| Identity, security and privacy | Identity, authentication, authorization, secret handling, audit, trust and egress control | Security/trust/authorization contracts and accepted frozen boundaries |
| Persistence, recovery, updates | Verified durable state when authorized, backup/restore, migration, rollback and software-update mechanics | MediaHub retains authority; infrastructure components only supply mechanisms |
| Developer infrastructure | Reproducible source/build/test/verification, component registry, evidence and task execution | Engineering contracts; no developer tool mutates product state by implication |
| Cloud development | Optional remote compute and providers for admitted tasks | Data classification, provider/model identity, cost/egress, trust and workload-placement gates |

## 8. AI and agent execution model

AI is a capability tier, not an authority tier:
- Local AI is preferred when it satisfies the required capability and policy.
- Local cluster AI supplies qualified distributed execution; it does not gain platform authority.
- Cloud Development AI and external providers are controlled escalation paths, not mandatory runtime dependencies for local-first product behavior.
- AI-generated commands and changes are proposals until validated and authorized through the same contract path as other requests.
- Model availability, inference credentials, data-egress permissions, runtime presence and quality are distinct claims. A registered credential, listed provider, installed executable or candidate model is not proof of working/qualified inference.

## 9. Distributed compute, network and storage

The compute architecture is hierarchical/federated rather than one undifferentiated global VPN network. Keep control-plane, development-mesh, media/data, storage, compute-contribution and API-egress boundaries distinct. Each admitted workload receives only its authorized data and network paths for its lease/workspace.

Canonical scheduler/admission/lease/evidence contracts belong to MediaHub. Third-party schedulers, transport, storage, brokers and workflow engines remain subordinate mechanisms. Failed identity, expired lease, uncertain ownership, policy denial, malformed output, evidence mismatch or unresolved network partition must block or revoke work rather than guess.

Storage architecture must not silently become authority. Backups and restored data require identity, integrity/provenance and reconciliation; restoration does not bypass present safety/authorization policy. Target-gated storage/replication components do not become current prerequisites merely because they appear in a blueprint or manifest.

## 10. Security, privacy and operational invariants

1. Default deny; fail closed on uncertainty at security- and state-changing boundaries.
2. No secrets in Git or evidence; use explicit scope, identity and revocation.
3. Cloud egress follows data classification, privacy, residency, cost and workload-placement policy.
4. Logs, metrics, traces and evidence must avoid personal payloads and secrets.
5. Readiness, authentication, transport health and provider availability do not individually establish mutation authority.
6. Unknown devices/executors/providers are not admitted by inference.
7. No fallback Product State Authority is created on service failure.
8. A plugin, adapter, model, executor or storage component can be removed/replaced without silently changing canonical contract semantics.
9. Observability and evidence are not a shadow control plane.
10. Release/production acceptance is separate from architecture, implementation and local qualification.

## 11. Component status interpretation

The Canonical Component Manifest 2.0 is the canonical development input for component selection. The manifest explicitly states that selection is not production qualification. Each component remains at its documented scope: selected foundation, embedded/target-gated, future-gated or reference-only. Where a candidate name appears, do not infer that it is installed, configured, connected, secure, performant or qualified.

The State/HA integration proposal (PostgreSQL persistence, etcd coordination, NATS/JetStream transport) is explicitly a future extension. Current single-node/in-memory runtime semantics remain in force until a specific governance change, compatibility review, acceptance and freeze authorize a transition.

## 12. Current evidence and readiness

This is the documentary status observed in the reviewed refs:
- B2 functional baseline: ACCEPTED / CANONICAL / IMMUTABLE reference.
- MH-24 reconciliation report: CLOSED — Baseline 2.0 accepted/canonical.
- MH-24 traceability matrix: still labelled RECONCILIATION CANDIDATE; this is an unresolved status discrepancy with the report, not permission to silently promote the matrix.
- Batch 04 crosswalk: structural review PASS; semantic atom mapping OPEN. Parent status counts: 4 MAPPED, 3 NO_DIRECT_COUNTERPART, 41 NOT_REVIEWED, 0 CONFLICT.
- UI4-04: HOLD / CROSS-LINK-ONLY.
- MH-03 as a whole: PROPOSED; no blanket architecture or production acceptance inferred.
- ASTRA GOLD generated Current Truth: all G0–G11 BLOCKED; overall NOT_PROVEN / BLOCKED because no gate has fresh PASS evidence.
- ASTRA local qualification record: repository-local only, fail-closed, no live nodes/credentials/24-hour soak; not GOLD qualification.
- Current live distributed transport and multi-node qualification are not claimed as passing from the reviewed documentation.

These statuses are source-scoped and time/ref dependent; they must be refreshed from GitHub before any future status report or operational action.

## 13. Open decision and qualification register

1. Reconcile the working-branch B1 copy provenance; until then all B1 source-line mapping uses the main SHA.
2. Complete atom-level B1/B2 crosswalk for Batch 04; preserve historical 47 wording and verified 48-ID inventory.
3. Resolve MH-24 matrix status discrepancy through a controlled, evidence-backed update after semantic mapping; do not silently edit the matrix.
4. Complete unresolved GOV-MH24 choices and source-anchored child-level acceptance/evidence fields; keep child IDs provisional and UI4-04 on HOLD.
5. Define the qualified multi-node State Authority topology, split-brain prevention, fencing, replication, recovery and failure semantics.
6. Settle Smart Home multi-instance ownership, loss-of-HA behavior and safe recovery paths without creating competing authority.
7. Gate physical persistence, HA, storage, updates/recovery, gateway/VPN, remote GPU and high-compute hardware through accepted domain contracts.
8. Complete profile-specific security, privacy, performance, resilience and operational qualification before enabling production behavior.
9. Produce fresh ASTRA identity/runtime/scheduler/concurrency/fencing/recovery/current-SHA soak and independent A3 evidence; remain BLOCKED until then.
10. Complete the MH-01…MH-25 acceptance/evidence inventory. Domain-map status is not evidence that all domains are closed.

## 14. Primary evidence index

| Artifact | Ref / blob SHA | Scope |
|---|---|---|
| Context bootstrap instruction | working branch; SHA f86014d81a2db1b5246b4fc2600812340f1c7d22 | Required retrieval/change protocol |
| Functional Baseline 1.0 | main; SHA 9df4892ed0734050ac79732603d15bb414717310 | Literal 68-section historical passport |
| Functional Baseline 2.0 | main; SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f | Accepted current functional reference |
| MH-24 reconciliation report | main; SHA d07d162ebaa57643a7bdd84d6fb13a1102b87bfc | Acceptance and reconciled-status report |
| MH-24 traceability matrix | main; SHA 8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6 | Domain-level traceability; matrix status discrepancy remains |
| MH-03 runtime foundation | main; SHA 325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2 | Current runtime constraints |
| MH-03 master prompt | main; SHA e99035f596e236645bf8f2235fc4d375716ce476 | Runtime boundary summary |
| P0-06 runtime services contract | main; SHA ff21515e589b10fcbe2b167c3aadb3f66b32b4ae | Accepted bounded service contract |
| State/HA integration contract | main; SHA aa68e876d06980ced3e6b6b3995ea6a117446423 | Future-gated persistence/HA extension |
| Component Manifest 2.0 | main; SHA 45988bf9da202c9597dca2de50e92e5c2e6ed55 | Development component selection; not production qualification |
| Security/trust contract | main; SHA 8d831c2a8fa333977dd86524099568bae2a8db0e | Proposed broad security baseline, distinct from accepted scoped rules |
| Unified architecture integration contract v3 | working branch; companion document named above | Cross-domain integration and verification assertions |
| ASTRA launch schema | working branch; SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491 | Gate structure and launch restrictions |
| ASTRA governance contract | working branch; SHA 1d3ac25e7817f365807ad85d0d7c9007bd48bebf | Gate registry, thresholds, invariants and current governance data |
| ASTRA Current Truth | main; SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731 | Generated gate status: BLOCKED / NOT_PROVEN |
| ASTRA local qualification result | main; SHA 3b284dd211414da816af8fc4ac8addbc810a928d | Repository-local-only qualification result |
| Batch 04 crosswalk | working branch; SHA f9e66b7adde7afeaf6a7fb6ef1a867dee07c1b34 | Parent-level traceability draft |
| Batch 04 crosswalk review | working branch; SHA ea64aadc42244fe93a89735e7c0d8bce16b662d2 | Structural pass; semantic mapping open |

## 15. Acceptance boundary

This v3 document is a reconciled passport draft. It does not mark unknown gates as passed, authorize infrastructure/product implementation, replace Baseline 2.0, rewrite Baseline 1.0, declare production readiness, or imply the autonomous controller is executing. Promotion to a new accepted passport/baseline requires explicit owner review, traceable change control, domain contract reconciliation, and the appropriate independent verification and qualification evidence.

**Truth status:** architecture documented and selected conflicts corrected in this working branch; several traceability/governance/qualification gates remain OPEN or BLOCKED.
