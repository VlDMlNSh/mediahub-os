# MediaHub — Unified Architecture Integration Contract v3

**Artifact ID:** MH-ARCH-CONTRACT-V3-DRAFT-01  
**Revision date:** 2026-10-12  
**Branch:** docs/mediahub-chat-tree-map-20261012  
**Status:** ACTIVE WORKING-BRANCH INTEGRATION CONTRACT / NOT A NEW ACCEPTED BASELINE  
**Scope:** MediaHub OS, MediaHub iOS, development compute fabric, and ASTRA GOLD.  
**Change boundary:** Documentary reconciliation only. This document does not silently replace B1/B2, frozen P0 contracts, domain contracts, qualification schemas, or human approval gates.

## 1. Purpose

This document is the common integration view for this reconciliation branch. It resolves conflicts only where an accepted source already establishes the rule. Unknowns remain explicit gates rather than invented decisions.

It is not a new competing source of product requirements. Requirements remain in canonical baselines/domain contracts; machine-readable schemas remain in designated schema files; live qualification state remains evidence-driven. This document states how those sources compose.

A newer timestamp, a branch-only file, a “canonical” label, or presence in a component manifest is not by itself approval or runtime evidence.

## 2. Source hierarchy and precedence

Precedence is scoped by authority and acceptance status, not date alone.

| Order | Source | Controlling purpose | Limit |
|---|---|---|---|
| 1 | Explicit product-owner decisions and scoped governance approvals | Settles product decisions within the approved scope | Partial approval does not approve an entire proposal or unrelated subsystem |
| 2 | Functional Baseline 2.0, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f on main | Accepted/canonical/immutable current functional reference | Does not prove implementation, testing, qualification, release or production |
| 3 | Functional Baseline 1.0, SHA 9df4892ed0734050ac79732603d15bb414717310 on main | Literal historical passport source and source-atom lineage | No automatic B1→B2 equivalence; immutable source is not edited |
| 4 | Accepted/frozen P0 and other accepted scoped contracts | Normative runtime behavior within exact accepted scope | Must not be expanded beyond the stated authorization |
| 5 | MH domain contracts, reconciliation artifacts and component manifest | Domain boundaries, component classifications and future gates | Component selection is not implementation or production qualification |
| 6 | ASTRA qualification schema, governance contract and generated truth | Gate structure, aligned governance registry and current qualification snapshot | Prose/historical evidence cannot promote a gate |
| 7 | Working drafts and historical checkpoints | Provenance and unresolved questions | Cannot override a later accepted decision without explicit reversal evidence |

### 2.1 B1/B2 identity finding

The accepted B2 file on main is SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. The literal B1 source on main is SHA 9df4892ed0734050ac79732603d15bb414717310. B1 remains separate historical provenance and is not edited.

A branch-drift defect was observed: the B1 path on this working branch has SHA 1a2f06f50dd69990be58b12a98376b92f12fd14f and 296 lines, while main B1 has SHA 9df4892ed0734050ac79732603d15bb414717310 and 1,111 lines. Do not source-map B1 requirements from the branch-local copy. Preserve it and use the explicit main SHA until provenance is reconciled.

### 2.2 MH-24 traceability finding

The working Batch 04 crosswalk has 48 unique historical parent IDs and the owner-approved 12-field schema. Parent-level statuses are 4 MAPPED, 3 NO_DIRECT_COUNTERPART, 41 NOT_REVIEWED, and 0 CONFLICT. Structural review passed; semantic/child-level mapping remains open. These counts do not mean 48 fully mapped atomic requirements.

The historic backlog text says 47 records, while the audited inventory has 48 unique parent IDs. Keep the historic wording intact; report the checked count in new artifacts. UI4-04 remains HOLD / CROSS-LINK-ONLY, and no provisional child ID is promoted by this contract.

## 3. Product authority model

| Authority or subsystem | Owns | Explicitly does not own |
|---|---|---|
| Human/product owner | Product decisions and governance/release/production approvals where required | Tool execution alone is not approval |
| MediaHub Product State Authority | Sole canonical platform-state authority, including platform identity/lifecycle/policy and cross-domain canonical references | Does not absorb Smart Home operational authority or defer to AI/cloud/infrastructure |
| Home Assistant Core | Smart Home device and operational Smart Home state | Not platform-wide MediaHub State Authority |
| Runtime/Core Runtime Services | Lifecycle coordination, sequencing, bounded readiness/diagnostics | No second canonical mutation path or shadow state store |
| Domain services/adapters | Domain data/actions through governed contracts | No authority by connection, process, database, broker or device selection |
| ASTRA GOLD A0 | Engineering coordination, decomposition, claims, queue progress, integration/reconciliation and ASTRA-internal queue/claim/gate state | Never MediaHub Product State Authority; no product-state mutation privilege |
| ASTRA A1/A2/A3 | A1 architecture; A2 implementation; A3 independent verification | A2 cannot self-verify; no self-qualification or self-promotion |
| Executors/transports/providers/cloud | Only admitted, scoped execution and evidence/capabilities | No product, credential-creation, architecture or qualification authority by implication |
| Persistence/broker/cache/index/object store/graph/telemetry/backup | Explicit storage, transport, indexing, observation or recovery mechanics | Not State Authority merely because they store, transport, observe, restore or coordinate data |

### 3.1 Canonical mutation path

**Command/request → structural/freshness validation → identity/trust and authorization/policy → Consumer/Integration Contract → MediaHub Product State Authority → canonical mutation/revision → fact/event publication → observers.**

Events describe facts; they cannot grant mutation authority. Automation, workflow, provider, mobile client, UI, plugin, device adapter, AI, cloud or transport must re-enter the command path for a new mutation. Runtime coordinates lifecycle; Product State Authority mutates canonical state.

Malformed, stale, unauthenticated, unauthorized, ambiguous or critically conflicting inputs are rejected/denied/quarantined/fail-closed under the relevant contract. Loss of State Authority cannot create a shadow authority. Keep reported, observed, desired, policy-allowed, commanded, committed, applied, confirmed and predicted state distinct.

### 3.2 ASTRA namespace correction

A0 internal state means ASTRA queue, claims/leases, gate progression, executor results, integration and evidence manifests only. It must not be called MediaHub Product State Authority. Three misleading statements were corrected in this branch and read back:

- architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md — SHA c93f69599fd6974847dd86c35af3f7955fccab96, line 28.
- architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md — SHA 4c977539d837292d9a0a65435159e2b81311865a; authority declaration and A0 state column narrowed to ASTRA-internal state.
- architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md — SHA c3453cc1c25709fd11a287e753b6f4435be1065d, diagram line 43.

The qualification schema and execution blueprint already scope the machine-readable state_authority field in a comment to ASTRA-internal state only. The field name is retained for compatibility with existing drift checks; its scope is clarified rather than silently changing an interface.

## 4. Runtime now versus target architecture

MH-03 runtime foundation remains PROPOSED and explicitly describes the current foundation as single-node, in-memory State Authority, no HA, and no authorized physical persistence in that foundation. Frozen P0-03/P0-04/P0-05 semantics are not reopened by component-selection documents. The accepted P0-06 contract authorizes its stated logical runtime-service scope only; it does not accept all MH-03 or activate persistence/HA.

B2's target model allows one logical MediaHub State Authority physically distributed across qualified nodes. That target still requires implementation and qualification of leadership, quorum, replication, conflict handling, failover and recovery. It does not make a multi-node system currently qualified.

PostgreSQL, etcd, NATS/JetStream, Temporal, Ray, storage fabrics, remote GPU and other technologies retain source-specific status: current foundation, selected development input, target-gated, future-gated or reference-only. Do not activate them as current runtime prerequisites without an accepted gate.

## 5. Domain boundary rules

| Domain | Integration rule | Gate/status |
|---|---|---|
| Smart Home | HA Core owns operational device state; MediaHub authority owns platform state and cross-domain references | Clustered ownership, loss-of-HA and failover need separate evidence |
| UI/mobile | UI and clients call governed APIs; Core/wall-panel and Remote clients are not conflated | Entitlement/package/platform matrix remains qualification work |
| AI/agents | Advisory/proposal-producing by default; mutation goes through governed contracts | Model/provider identity, privacy, tool scope and runtime independently qualified |
| Cloud/hybrid development | Separate security/control domain; local-first product capability cannot defer authority to cloud | Egress, classification, provider and workload-placement gates apply |
| Media/storage/knowledge/digital twin | Domain contracts own specialized models/data; shared identity/provenance/policy stays governed | Component selection does not establish feature availability |
| Network/edge/devices | Keep management/control, development mesh, media, storage, compute and API-egress boundaries explicit where relevant | Hardware, roaming, VPN, gateway, protocol and failover behavior need profile-specific evidence |
| Security/privacy/trust | Identity, authorization, privacy, egress and audit precede execution | PROPOSED broad security contract stays proposed except for narrower accepted/frozen rules |
| Persistence/recovery/update | MediaHub retains recovery/update/release authority; components provide mechanics | Physical persistence, HA, backup/restore and update activation follow their specific gates |
| ASTRA engineering fabric | A0 coordinates; A1/A2/A3 are separate capabilities; executors are execution-only | All mandatory gates and Human launch approval remain required |

## 6. Hardware and deployment profiles

Hardware support is capability-profile driven, not device-name driven. A node gets only the capabilities supported by its hardware/OS, trust posture, components and profile-specific qualification. A single-node installation remains a valid profile; cluster features cannot be inferred.

| Profile | Intent | Current status |
|---|---|---|
| Mac mini / Mini PC clean install | Local full-capability or development node; B2 records Linux as clean-install direction where supported | Profile direction only; qualify the exact model/OS/components |
| Apple platform adaptation | Preserve common product contracts where replacing the base OS is constrained | Capability-limited; no assumption that all Linux-appliance capabilities exist |
| Mac Pro / accelerator-capable node | Future high-throughput local AI/media/compute worker and possible cluster contributor | Roadmap proposal only; not asserted as accepted B2 support or qualified hardware |
| Raspberry Pi / specialized low-power node | Reduced capability with the same authority/security model | Capability-specific; heavy compute/recording not inferred |
| iPad/mobile | Distinguish Core/wall-panel capabilities from Remote client | Entitlements, local/remote model and qualification govern features |
| Cloud/remote compute | Admitted workloads under placement/privacy/egress policy | Optional/future-gated; never required for local-first core operation |

A Mac Pro does not gain product authority by being powerful. Its exact hardware/software profile must qualify compute/GPU/memory, thermals, power, network, storage, identity, isolation and recovery before admission. A model name is not evidence.

## 7. Lifecycle and ASTRA qualification

Keep stages distinct: IDEA → DESIGN → IMPLEMENTED → TESTED → VERIFIED → QUALIFICATION CANDIDATE → QUALIFIED → RELEASED → DEPLOYED → OBSERVED → PRODUCTION ACCEPTED.

Documentation is not implementation; repository-local tests are not live-node qualification; historical soak is not a current soak; a generated status file is a snapshot of machine-readable sources, not promotion authority.

ASTRA rules:
- ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml is the authority for gate structure/required evidence/launch restrictions. Governance registry and numeric values must remain aligned with schema and unified model under the defined drift gate.
- CURRENT-TRUTH.generated.md is generated from ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml and optional gate evidence; do not edit it by hand.
- Current truth SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731 records G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED because no gate has fresh PASS evidence.
- Local qualification result SHA 3b284dd211414da816af8fc4ac8addbc810a928d explicitly excludes live nodes, credentials and the 24-hour soak. It is not GOLD qualification.
- Gap register SHA a0418e29cdbc80006823baec967c4f91737ceaff records blockers for fresh identity/E2E/scheduler/fencing/recovery/current-SHA soak evidence.
- Human authorization is required for launch. Never represent a soak or qualification as running without fresh evidence tied to an exact frozen SHA.

## 8. Verifiable integration assertions

These MHC3 IDs are local to this document; they do not replace MH/P0 IDs.

| ID | Assertion | Evidence anchor | Check method | Current result |
|---|---|---|---|---|
| MHC3-001 | B2 is the accepted current functional reference | B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; reconciliation SHA d07d162ebaa57643a7bdd84d6fb13a1102b87bfc | Read exact refs/status | PASS, documentary |
| MHC3-002 | B1 source-line anchors point to main SHA 9df4892ed0734050ac79732603d15bb414717310 | Main B1 versus branch B1 SHA 1a2f06f50dd69990be58b12a98376b92f12fd14f | Compare blob SHA and line count before mapping | DRIFT FOUND; branch copy preserved |
| MHC3-003 | One MediaHub Product State Authority | B2 §3; P0-06 contract SHA ff21515e589b10fcbe2b167c3aadb3f66b32b4ae | Review actual mutation paths when authorized | PASS, documentary; runtime unqualified |
| MHC3-004 | HA Core is Smart Home authority, not platform authority | Main B1 §4 SHA 9df4892ed0734050ac79732603d15bb414717310; B2 authority table | Review Smart Home write paths/refs | PASS, documentary |
| MHC3-005 | A0 state is ASTRA-internal only | Branch qualification schema SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491; corrected reference architecture SHA c93f69599fd6974847dd86c35af3f7955fccab96 | Search/review A0 authority prose; preserve drift contract | PASS, targeted read-back; no tests run |
| MHC3-006 | Runtime coordinates; Product State Authority mutates | MH-03 master SHA e99035f596e236645bf8f2235fc4d375716ce476; runtime foundation SHA 325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2 | Review callers and contracts | Documentary PASS; MH-03 remains PROPOSED |
| MHC3-007 | Current runtime remains single-node/in-memory; no implicit persistence/HA | Runtime foundation; State/HA future contract SHA aa68e876d06980ced3e6b6b3995ea6a117446423 | Gate any target dependency | PASS, documentary |
| MHC3-008 | AI/cloud/provider/transport/executor have no implicit product authority | B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; branch schema SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491 | Review admission, scope and mutation re-entry | PASS, documentary; runtime pending |
| MHC3-009 | Component selection is not qualification | Manifest SHA 45988bf9da202c9597d0ca2de50e92e5c2e6ed55 | Require exact-profile evidence | PASS, documentary |
| MHC3-010 | Local-first/fail-closed rules survive cloud/AI loss | Main B1 SHA 9df4892ed0734050ac79732603d15bb414717310; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f | Offline/degraded and negative-path checks | Rule clear; runtime test not run |
| MHC3-011 | ASTRA needs fresh same-SHA evidence, independent A3 and Human launch | Launch schema SHA 0b86b07dfa916d4485ce1f8f54d19de136d98491; Current Truth SHA 48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731 | Verify gate/evidence bundle | BLOCKED |
| MHC3-012 | Batch 04 parent statuses do not imply child-atom mapping | Crosswalk SHA f9e66b7adde7afeaf6a7fb6ef1a867dee07c1b34; review SHA ea64aadc42244fe93a89735e7c0d8bce16b662d2 | Source-atom/B2 clause review | OPEN |
| MHC3-013 | UI4-04 stays HOLD without uniqueness evidence | Owner record SHA 9117098e22c26708d48ca8ba5954669faa209d68 | Require cited residual requirement | HOLD |
| MHC3-014 | MH-24 matrix status discrepancy remains explicit | Matrix SHA 8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6; report SHA d07d162ebaa57643a7bdd84d6fb13a1102b87bfc | Reconcile by controlled change | OPEN |
| MHC3-015 | Proposed extensions remain gated | Security/trust SHA 8d831c2a8fa333977dd86524099568bae2a8db0e; State/HA SHA aa68e876d06980ced3e6b6b3995ea6a117446423 | Read each status and gate before activation | PASS, bounded interpretation |

## 9. Explicit open gates

1. Reconcile working-branch B1 provenance or exclude that copy from source-line use; do not rewrite the controlling source.
2. Complete semantic atom-level B1/B2 mapping for Batch 04.
3. Reconcile the MH-24 matrix lifecycle status with the accepted report through an explicit controlled change; do not silently edit the matrix during this pass.
4. Resolve remaining GOV-MH24 dispositions and domain-owner evidence; unapproved proposals/crosswalk fields remain provisional.
5. Qualify clustered Smart Home ownership, loss-of-HA behavior and multi-node State Authority leadership without competing authorities.
6. Define accepted transitions for persistence/HA, storage, recovery/update, gateway/VPN, remote GPU and high-compute hardware profiles.
7. Produce fresh ASTRA live-node E2E, concurrency/fencing, recovery/restore, current-SHA soak and independent A3 evidence; current truth remains BLOCKED.
8. Complete domain-by-domain MH-01…MH-25 acceptance/evidence inventory. This contract is not proof that every domain has passed.

## 10. Change-control rules

- Do not modify B1/B2, frozen P0 contracts, generated qualification outputs, main, canonical matrix/backlog, infrastructure or production without the corresponding scoped authorization.
- Keep these corrections in the working branch; no merge is implied.
- Before every action, reread the current project map, follow it to primary sources and validate path/ref/SHA.
- For every correction, capture source line, make the minimal supported change, read back the changed file, verify blob SHA, and update the map.
- Preserve historical checkpoints and mark supersession instead of overwriting provenance.
- No installation, test/qualification run, queue/soak start, deployment, infrastructure change, credential operation or storage cleanup was authorized or performed in this documentary pass.

**Conclusion:** This is the active integration contract for this reconciliation branch, not a new accepted functional baseline, qualification evidence, production authorization, or permission to merge.
